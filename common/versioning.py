import bpy
from ..config import VERSION
import re


def get_node_version(ng: bpy.types.NodeGroup):
    return ng["version"] if "version" in ng else "0.0.0"


def is_latest_version(ng: bpy.types.NodeGroup):
    return get_node_version(ng) == VERSION


def replace_all_instances_of_node_group(target_node_group_name, new_node_group_name):
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

# def make_names_unique