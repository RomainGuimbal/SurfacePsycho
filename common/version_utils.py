import bpy
from .enums import VERSION_STR
from packaging.version import Version

def get_node_version(ng: bpy.types.NodeGroup):
    return  Version(ng["version"] if "version" in ng else "0.0.0")


def is_latest_version(ng: bpy.types.NodeGroup):
    return get_node_version(ng) == Version(VERSION_STR)