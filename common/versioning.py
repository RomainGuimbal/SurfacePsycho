import bpy
import re
import numpy as np
from packaging.version import Version
from .asset_list import ASSET_NODE_GROUPS
from .enums import ADDON_PATH, SP_obj_type, MesherName
from .asset_append import append_node_group
from .enums import ASSETS_FILE
from .modifier_utils import (
    add_modifier_asset,
    remove_modifier,
    move_modifier_above_mesher,
    get_modifier_by_name,
    get_modifier_by_names,
    set_modifier_values,
    get_modifier_value,
)
from .version_utils import is_latest_version, get_node_version
from .utils import sp_type_of_object, has_contour, remove_suffix

#####################
## VERSIONING DATA ##
#####################

# Old nodes names
OLD_TO_NEW_NODE_MAPPING = {
    "SP - Trim 4 Sides": "SP - Crop or Extend Patch",
    "SP - AOP Trim 4 sides": "SP - Crop or Extend Patch",
    "SP - Any Order Patch Meshing": "SP - Bezier Patch Meshing",
    "SP - Continuities Curve": "SP - Connect Curve",
    "SP - Trim Range Any Order Curve": "SP - Crop or Extend Curve",
    "SP - AOP Continuities": "SP - Connect Bezier Patch",
    "SP - Fillet Flat Patch": "SP - Fillet Curve or FlatPatch",
    "SP - Raise or Lower Curve Order": "SP - Raise or Lower Curve Degree",
    "SP - Extrude FlatPatch": "SP - Extrude Compound",
    "SP - Plot Distance Between Curves": "SP - Distance Between Curves",
    "SP - Bezier Curve Any Order": "SP - Curve Meshing",
    "SP - AOP Continuities with Flat Patch": "SP - Connect Bezier Patch",
    # TODO FILL
}

# Reversed mapping
NEW_TO_OLD_NODE_MAPPING = {}
for k, v in OLD_TO_NEW_NODE_MAPPING.items():
    NEW_TO_OLD_NODE_MAPPING[v] = NEW_TO_OLD_NODE_MAPPING.get(v, []) + [k]

# Old nodes params
OLD_NODE_PARAMS = {
    "connect": {"side": ((0, 1, 2, 3), (2, 3, 0, 1))}
    # TODO FILL
}

ALL_SP_ASSET_NODE_GROUPS_EVER = ASSET_NODE_GROUPS | set(OLD_TO_NEW_NODE_MAPPING.keys())


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


def update_node_group(name):
    """
    At bpy.data level. Replaces all instances
    """
    # check if name is outdated
    new_name = name
    if remove_suffix(name) in OLD_TO_NEW_NODE_MAPPING:
        new_name = OLD_TO_NEW_NODE_MAPPING[name]

    # Get latest version if it exists
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
            and (ng_name in ASSET_NODE_GROUPS or ng_name in OLD_TO_NEW_NODE_MAPPING)
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


def update_modifier(modifier):
    name = remove_suffix(modifier.node_group.name)
    if name in ASSET_NODE_GROUPS:
        curr_node_group = bpy.data.node_groups.get(name)
        if is_latest_version(curr_node_group):
            return

        new_node_group = append_node_group(name)
        modifier.node_group = new_node_group
        modifier.node_group.interface_update(bpy.context)

    if name in OLD_TO_NEW_NODE_MAPPING.keys():
        curr_node_group = bpy.data.node_groups.get(name)

        new_name = OLD_TO_NEW_NODE_MAPPING[name]
        new_node_group = append_node_group(new_name)
        modifier.node_group = new_node_group
        modifier.node_group.interface_update(bpy.context)


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
        elif name in OLD_TO_NEW_NODE_MAPPING.keys():
            new_name = OLD_TO_NEW_NODE_MAPPING[name]
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


def get_node_names_all_versions(curr_name):
    list = [curr_name]
    list.extend(NEW_TO_OLD_NODE_MAPPING.get(curr_name, []))
    return list


def sp_type_of_outdated_objects(o):
    type = sp_type_of_object(o)
    if not type:
        for m in reversed(o.modifiers):
            if m.type == "NODES" and m.node_group and m.show_viewport:
                name = remove_suffix(m.node_group.name)
                # endswith is not very clean but ok
                if name.endswith("Meshing") and name in OLD_TO_NEW_NODE_MAPPING.keys():
                    type = SP_obj_type[MesherName(OLD_TO_NEW_NODE_MAPPING[name]).name]
                    break
    return type


#####################
#     SCENARIOS     #
#####################
def update_scenario_deprecate_contour_fit(m, object):
    set_modifier_values(m, {"Scaling Method": 1})
    if has_contour(object):
        conv_mod = add_modifier_asset(
            object, "SP - Convert Contour", {}, pin=False, append=True
        )
        move_modifier_above_mesher(object, conv_mod)


def update_scenario_replace_fillet_factor_2(mod):
    """
    Old fillets with fast method where 2 times 2 short with straight edges.
    """
    fillet_method = get_modifier_value(mod, "Method")
    item = 1
    if fillet_method == item:
        current_fillet = get_modifier_value(mod, "Fillet")
        set_modifier_values(mod, {"Fillet": current_fillet / 2})


def update_scenario_curve_preserve_combs_display(mod):
    if get_modifier_value(mod, "Enable"):
        update_modifier(mod)
        set_modifier_values(mod, {"Combs": True})


def upgrade_vertex_group_endpoints(obj):
    vg = obj.vertex_groups["Endpoints"]
    indices = [
        v.index
        for v in obj.data.vertices
        if (vg.index in [vg.group for vg in v.groups])
        and v.groups[vg.index].weight > 0.6
    ]
    obj.vertex_groups.remove(vg)
    att = obj.data.attributes.new(name="Endpoints", type="BOOLEAN", domain="POINT")
    values = np.full(len(obj.data.vertices), False, dtype=bool)
    for i in indices:
        values[i] = True
    att.data.foreach_set("value", values)


def update_scenario_switch_resolutions(mod):
    u = get_modifier_value(mod, "Resolution U")
    v = get_modifier_value(mod, "Resolution V")
    set_modifier_values(mod, {"Resolution U": v, "Resolution V": u})


def update_scenario_loft_segment(mod):
    tree = mod.node_group.interface.items_tree

    # Because of a mistake, "Segment" is also the name of 2 sockets in 0.9 loft
    seg_sockets_count = sum([item.name.startswith("Segment") for item in tree])
    if seg_sockets_count > 1:
        update_modifier(mod)
        return

    try:
        segment = get_modifier_value(mod, "Segment")
    except ValueError:
        update_modifier(mod)
        return

    update_modifier(mod)
    new_tree = mod.node_group.interface.items_tree
    for item in new_tree:
        if item.name.startswith("Segment") and isinstance(
            item, bpy.types.NodeTreeInterfaceSocketInt
        ):
            mod[item.identifier] = segment



def common_to_all_non_plane_surfaces(m, name, mesher_names, obj, version):
    if name in mesher_names:
        update_scenario_deprecate_contour_fit(m, obj)
        if version < Version("0.9.0"):
            # issue here because versions were not set in 0.9
            update_scenario_switch_resolutions(m)


# TODO ?
# - def update_scenario_patch_combs_to_isoparams(mod)(also do the operator for fast isoparam)
# - def update_scenario_remove_standalone_modifier_combs(["SP - Combs Any Order Curve", "SP - Combs"])


def update_object(obj):
    """
    Apply every update scenario to the object
    """
    type = sp_type_of_outdated_objects(obj)
    if not type:
        print(f"{obj.name} is not a SurfacePsycho object")
        return None

    if "Endpoints" in obj.vertex_groups.keys():
        upgrade_vertex_group_endpoints(obj)

    mesher_names = get_node_names_all_versions(str(type.mesher_name))

    # Declare before loop for performances
    fillet_names = get_node_names_all_versions("SP - Fillet Curve or FlatPatch")
    loft_names = get_node_names_all_versions("SP - Loft")

    # To ckeck : what happen on non SP modifiers (but sp object)
    for m in obj.modifiers:
        if m.type == "NODES" and m.node_group:
            name = remove_suffix(m.node_group.name)
            version = get_node_version(m.node_group)
            match type:
                case SP_obj_type.PLANE:
                    if name in fillet_names:
                        update_scenario_replace_fillet_factor_2(m)
                    update_modifier(m)
                case SP_obj_type.CYLINDER:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.CONE:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.SPHERE:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.TORUS:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.BEZIER_SURFACE:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    if name in loft_names:
                        update_scenario_loft_segment(m)
                    else:
                        update_modifier(m)
                case SP_obj_type.BSPLINE_SURFACE:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.SURFACE_OF_REVOLUTION:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.SURFACE_OF_EXTRUSION:
                    common_to_all_non_plane_surfaces(
                        m, name, mesher_names, obj, version
                    )
                    update_modifier(m)
                case SP_obj_type.CURVE:
                    if name in mesher_names:
                        update_scenario_curve_preserve_combs_display(m)
                    else:  # To skip update modifier which has to be inside the scenario
                        if name in fillet_names:
                            update_scenario_replace_fillet_factor_2(m)
                        update_modifier(m)
                case SP_obj_type.COMPOUND:
                    update_modifier(m)


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
