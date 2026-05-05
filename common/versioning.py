import bpy
from enum import Enum
import re
from ..config import VERSION_STR
from .enums import ASSET_NODE_GROUPS, ADDON_PATH, SP_obj_type, MesherName
from .asset_append import append_node_group
from .enums import ASSETS_FILE
from .modifier_utils import (
    add_sp_modifier,
    remove_modifier,
    change_mod_settings_from_object,
    move_modifier_above_mesher,
)
from .version_utils import is_latest_version, get_node_version
from .utils import sp_type_of_object, has_contour

#####################
## VERSIONING DATA ##
#####################

# Old nodes names
OLD_NODE_MAPPING = {
    "SP - Trim 4 Sides": "SP - Crop or Extend Patch",
    "SP - Any Order Patch Meshing": "SP - Bezier Patch Meshing",
    "SP - Combs": "",
    "SP - Continuities Curve": "SP - Connect Curve",
    "SP - Trim Range Any Order Curve": "SP - Crop or Extend Curve",
    "SP - AOP Continuities": "SP - Connect Bezier Patch",
    "SP - Fillet Flat Patch": "SP - Fillet Curve or FlatPatch",
    "SP - Raise or Lower Curve Order": "SP - Raise or Lower Curve Degree",
    # TODO FILL
}

# Old nodes params
OLD_NODE_PARAMS = {
    "connect": {"side": ((0, 1, 2, 3), (2, 3, 0, 1))}
    # TODO FILL
}

ALL_SP_ASSET_NODE_GROUPS_EVER = ASSET_NODE_GROUPS | set(OLD_NODE_MAPPING.keys())


#####################
## VERSIONING CODE ##
#####################


def replace_all_instances_of_node_group_by_name(
    target_node_group_name, new_node_group_name
):
    # Get the target node group
    prefix, suffix = target_node_group_name[:-2], target_node_group_name[-2:]

    if suffix == ".*":
        pattern = rf"^{re.escape(prefix)}\.(\d{{3}}|\d{{3}}\.\d{{3}})$"
        target_node_groups = [
            ng for ng in bpy.data.node_groups if re.match(pattern, ng.name)
        ]
    else:
        target_node_groups = [bpy.data.node_groups.get(target_node_group_name)]

    # Get the new node group
    new_node_group = bpy.data.node_groups.get(new_node_group_name)
    if not new_node_group:
        return 0  # New node group not found

    if len(target_node_groups) > 0:
        for t in target_node_groups:
            if t and t != new_node_group:
                # Replace the node group data
                t.user_remap(new_node_group)

                # Remove the old node group
                bpy.data.node_groups.remove(t)

        return len(target_node_groups)
    else:
        return -1


def replace_node_group(target_node_group, new_node_group):
    target_node_group.user_remap(new_node_group)


def report_outdated_node_groups():
    # technically, if you are using an old version, this is not "outdated" but "unmatching current"
    outdated_node_groups = [
        ng for ng in bpy.data.node_groups if not is_latest_version(ng)
    ]
    if len(outdated_node_groups) > 0:
        print("Outdated node groups found:")
        for ng in outdated_node_groups:
            print(f"- {ng.name} (version: {get_node_version(ng)})")
    else:
        print("All node groups are up to date.")


def set_nodes_version(version=None):
    # get version from toml file
    if version is None:
        path = ADDON_PATH + "/blender_manifest.toml"
        with open(path, "r") as f:
            for line in f:
                if line.startswith("version"):
                    version = line.split('"')[1]
                    break

    for ng in bpy.data.node_groups:
        ng["version"] = version

    print("version set to " + version)


def replace_duplicates():

    #############################
    #         DANGER            #
    # May remove different node #
    #   groups with same name   #
    #############################

    duplicated_list = []
    for ng in bpy.data.node_groups:
        if ng.name[-4] == ".":
            duplicated_list.append(ng.name[:-4])
            # print(ng.name)
    duplicated_groups = set(duplicated_list)

    for d in duplicated_groups:
        replaced = replace_all_instances_of_node_group_by_name(d + ".*", d)
        if replaced <= 0:
            print(f"No instances of {d}.* found")


def classify_strings_by_prefix(strings):
    import re

    strings.sort()
    object_dict = {}
    for string in strings:
        # Use regex to extract the common prefix
        match = re.match(r"(\D+)(\d*)", string)
        if match:
            prefix = match.group(1)
            if prefix not in object_dict:
                object_dict[prefix] = [string]
            else:
                object_dict[prefix].append(string)
    return object_dict


def highest_suffix_of_each_object_name(names):
    classified_objects = classify_strings_by_prefix(names)
    last_string = []
    for key, value in classified_objects.items():
        if value:
            last_string += [value[-1]]
    return last_string


def remove_suffix(data_block_name):
    if re.match(r"[.]\d*$", data_block_name):
        return data_block_name[:-4]
    else:
        return data_block_name


def update_node_group(name):
    # check if name is outdated
    new_name = name
    if remove_suffix(name) in OLD_NODE_MAPPING.keys():
        new_name = OLD_NODE_MAPPING[name]

    # get latest version if it exists
    latest_node = None
    for ng in bpy.data.node_groups:
        # assumes latest version never has suffix
        if (
            ng.type == "GEOMETRY"
            and ng.name == new_name
            and ng.name in ASSET_NODE_GROUPS
            and is_latest_version(ng)
            and ng.library.filepath == ASSETS_FILE
        ):
            latest_node = ng
            break

    # Make a unique id for each current node group
    snapshot = [
        (ng.name, ng.library)
        for ng in bpy.data.node_groups
        if ng.type == "GEOMETRY" and ng.name in ALL_SP_ASSET_NODE_GROUPS_EVER
    ]

    # update all non-latest versions
    replaced = 0
    for n, lib in snapshot:
        ng = bpy.data.node_groups.get(n, lib)
        ng_name = remove_suffix(ng.name)
        if (
            ng.type == "GEOMETRY"
            and ng_name == name
            and ng != latest_node
            and (ng_name in ASSET_NODE_GROUPS or ng_name in OLD_NODE_MAPPING.keys())
        ):
            if latest_node is None:
                latest_node = append_node_group(new_name)
            replace_node_group(ng, latest_node)
            bpy.data.node_groups.remove(ng)
            replaced += 1

    for ob in bpy.data.objects:
        for mod in ob.modifiers:
            if mod.type == "NODES" and mod.node_group == latest_node:
                mod.node_group.interface_update(bpy.context)

    return replaced


def update_all_node_groups():
    # get latest version nodes if they exist
    latest_nodes = {}
    for ng in bpy.data.node_groups:
        # assumes latest version never has suffix
        if (
            ng.type == "GEOMETRY"
            and ng.name in ASSET_NODE_GROUPS
            and is_latest_version(ng)
            and ng.library.filepath == ASSETS_FILE
        ):
            latest_nodes[ng.name] = ng

    # Make a unique id for each current node group
    snapshot = [
        (ng.name, ng.library)
        for ng in bpy.data.node_groups
        if ng.type == "GEOMETRY" and ng.name in ALL_SP_ASSET_NODE_GROUPS_EVER
    ]

    # update all non-latest versions
    replaced = 0
    for n, lib in snapshot:
        ng = bpy.data.node_groups.get(n, lib)
        name = remove_suffix(ng.name)

        if name in ASSET_NODE_GROUPS and ng not in latest_nodes.values():
            if name not in latest_nodes.keys():
                latest_nodes[name] = append_node_group(name)
            replace_node_group(ng, latest_nodes[name])
            bpy.data.node_groups.remove(ng)
            replaced += 1
        elif name in OLD_NODE_MAPPING.keys():
            new_name = OLD_NODE_MAPPING[name]
            if new_name not in latest_nodes.keys():
                latest_nodes[new_name] = append_node_group(new_name)
            replace_node_group(ng, latest_nodes[new_name])
            bpy.data.node_groups.remove(ng)
            replaced += 1

    for ob in bpy.data.objects:
        for mod in ob.modifiers:
            if mod.type == "NODES" and mod.node_group in latest_nodes.values():
                mod.node_group.interface_update(bpy.context)

    return replaced


#####################
#     SCENARIOS     #
#####################


def scenario_branching(obj, condition, scenario1, scenario2=None):
    if condition(obj):
        scenario1.run(obj)
    elif scenario2 != None:
        scenario2.run(obj)

class ReplaceActionFunc(Enum):
    UPDATE_MOD = None
    ADD_MOD = add_sp_modifier
    REMOVE_MOD = remove_modifier
    CHANGE_MOD_VAL = change_mod_settings_from_object
    MOD_EXISTS = None
    MOVE_MOD = None
    MOVE_ABOVE_MESHER = move_modifier_above_mesher
    CONDITION = scenario_branching


class ReplaceAction:
    def __init__(self, func, *args):
        self.function = func
        self.args = args

    def __add__(self, action):
        return ReplaceScenario().add(self).add(action)

    def run(self, object):
        self.function(object, *self.args)


class ReplaceScenario:
    def __init__(self):
        self.actions = []

    def add(self, *args):
        if type(args[0]) == ReplaceAction:
            self.actions.append(args[0])
        else:
            self.actions.append(ReplaceAction(*args))
        return self

    def insert(self, action, index):
        self.actions.insert(index, action)

    def __add__(self, scenario):
        self.actions.extend(scenario.actions)
        return self

    def run(self, object):
        for a in self.actions:
            a.run(object)


# Deprecate contour fit
deprecate_contour_fit_option = ReplaceScenario()
deprecate_contour_fit_option.add(
    ReplaceActionFunc.CHANGE_MOD_VAL, MesherName.BEZIER_SURFACE, {"Scaling Method": 1}
)
deprecate_contour_fit_option.add(  # only add converter if trim exists
    ReplaceActionFunc.CONDITION,
    has_contour,
    ReplaceScenario()
    .add(
        ReplaceActionFunc.ADD_MOD,
        "SP - Convert Contour",
        {},
        False,
        True,  # append if not already
    )
    .add(ReplaceActionFunc.MOVE_ABOVE_MESHER, "SP - Convert Contour")
)
# deprecate_contour_fit_option.add(ReplaceActionFunc.UPDATE_MOD, MesherName.BEZIER_SURFACE, {}, True)


def update_object(obj):
    type = sp_type_of_object(obj)
    match type:
        case SP_obj_type.BEZIER_SURFACE:
            deprecate_contour_fit_option.run(obj)
        case _:
            pass


#####################
#     OPERATORS     #
#####################


class SP_OT_report_outdated_nodes(bpy.types.Operator):
    bl_idname = "object.sp_report_outdated_nodes"
    bl_label = "SP - Report Outdated Nodes"
    bl_description = "Report outdated nodes in the console"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        report_outdated_node_groups()
        return {"FINISHED"}


class SP_OT_set_all_nodes_version(bpy.types.Operator):
    bl_idname = "object.sp_set_all_nodes_version"
    bl_label = "SP - Set All Nodes Version"
    bl_description = "Report outdated nodes in the console"
    bl_options = {"REGISTER", "UNDO"}

    major: bpy.props.IntProperty(default=0)
    minor: bpy.props.IntProperty(default=0)
    patch: bpy.props.IntProperty(default=0)

    def execute(self, context):
        set_nodes_version(f"{self.major}.{self.minor}.{self.patch}")
        return {"FINISHED"}


class SP_OT_update_node_group(bpy.types.Operator):
    bl_idname = "object.sp_update_node_group"
    bl_label = "SP - Update Node Group"
    bl_description = (
        "Make sure specified node group is the same as in current addon version"
    )
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Node Group", description="", default="")

    def invoke(self, context, event):
        # Populate the filtered node groups before opening the dialog
        self.nodegroup_items.clear()
        for ng in bpy.data.node_groups:
            if (
                ng.type == "GEOMETRY"
                and remove_suffix(ng.name) in ALL_SP_ASSET_NODE_GROUPS_EVER
            ):
                self.nodegroup_items.add().name = ng.name

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop_search(
            self,
            "name",
            bpy.data,
            "node_groups",
            text="Node Group",
            icon="NODETREE",
        )

    def execute(self, context):
        replaced = update_node_group(self.name)
        self.report({"INFO"}, f"Replaced " + str(replaced) + " node groups")
        return {"FINISHED"}

    def invoke(self, context, event):
        # call itself and run
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class SP_OT_update_all_node_groups(bpy.types.Operator):
    bl_idname = "object.sp_update_all_node_groups"
    bl_label = "SP - Update All Node Groups"
    bl_description = (
        "Make sure each SP node group is the same as assets in current addon version"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        replaced = update_all_node_groups()
        self.report({"INFO"}, f"Replaced " + str(replaced) + " node groups")
        return {"FINISHED"}


class SP_OT_update_objects(bpy.types.Operator):
    bl_idname = "object.sp_update_objects"
    bl_label = "SP - Update Objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            update_object(o)

        return {"FINISHED"}


classes = [
    SP_OT_report_outdated_nodes,
    SP_OT_update_all_node_groups,
    SP_OT_update_node_group,
    SP_OT_update_objects,
    SP_OT_set_all_nodes_version,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
