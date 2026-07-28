import bpy
import re
from .enums import VERSION_STR
from packaging.version import Version


def get_node_version(ng: bpy.types.NodeGroup):
    return Version(ng["version"] if "version" in ng else "0.0.0")


def is_latest_version(ng: bpy.types.NodeGroup):
    return get_node_version(ng) >= Version(VERSION_STR)


def set_nodes_version(version=None):
    # get version from toml file
    if version is None:
        version = VERSION_STR

    for ng in bpy.data.node_groups:
        ng["version"] = version

    print("Version set to " + version)


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


def replace_node_group(target_ng, new_ng):
    assert (target_ng != new_ng) or (
        target_ng == new_ng and target_ng.library != new_ng.library
    )
    target_ng.user_remap(new_ng)
