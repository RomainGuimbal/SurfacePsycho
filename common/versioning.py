import bpy
from ..config import VERSION_STR
import re
from .enums import ASSET_NODE_GROUPS, ADDON_PATH


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


def get_node_version(ng: bpy.types.NodeGroup):
    return ng["version"] if "version" in ng else "0.0.0"


def is_latest_version(ng: bpy.types.NodeGroup):
    return get_node_version(ng) == VERSION_STR


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


def set_nodes_version():
    # get version from toml file
    version = ""
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
