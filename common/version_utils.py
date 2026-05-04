import bpy
from ..config import VERSION_STR

def get_node_version(ng: bpy.types.NodeGroup):
    return ng["version"] if "version" in ng else "0.0.0"


def is_latest_version(ng: bpy.types.NodeGroup):
    return get_node_version(ng) == VERSION_STR
