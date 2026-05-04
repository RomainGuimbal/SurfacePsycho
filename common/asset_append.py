import bpy
from .enums import ASSETS_FILE
from .version_utils import is_latest_version


def remove_preview_image(ng: bpy.types.GeometryNodeTree):
    if ng.preview:
        ng.preview.image_size = [0, 0]
        return True
    return False


def append_object_by_name(obj_name, context):  # for importing from the asset file
    with bpy.data.libraries.load(ASSETS_FILE, link=False, assets_only=True) as (
        _,
        data_to,
    ):
        data_to.objects = [obj_name]

    cursor_loc = context.scene.cursor.location

    o = data_to.objects[0]
    if o is not None:
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        context.collection.objects.link(o)
        o.location = cursor_loc
        o.asset_clear()
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        # Iterate through all objects and their geometry node modifiers
        for mod in o.modifiers:
            if mod.type == "NODES" and mod.node_group:
                remove_preview_image(mod.node_group)
                mod.node_group.asset_clear()


def list_geometry_node_groups():
    geometry_node_groups = []

    for node_group in bpy.data.node_groups:
        if node_group.type == "GEOMETRY":
            geometry_node_groups.append(node_group.name)
    return geometry_node_groups


def append_node_group(asset_name, link=False, remove_asset_data=True):
    if asset_name in list_geometry_node_groups():
        ng = bpy.data.node_groups[asset_name]
        if is_latest_version(ng):
            return ng

    # Load the asset file
    with bpy.data.libraries.load(ASSETS_FILE, link=link, assets_only=True) as (
        data_from,
        data_to,
    ):
        data_to.node_groups = [asset_name]

    ng = data_to.node_groups[0]
    if remove_asset_data:
        remove_preview_image(ng)
        ng.asset_clear()

    return ng


def append_multiple_node_groups(
    ng_names: list, remove_asset_data=True
) -> list[bpy.types.NodeGroup]:
    ng_list = list_geometry_node_groups()
    to_append = ng_names.copy()
    already_present = []
    for asset_name in ng_names:
        if asset_name in ng_list:
            ng = bpy.data.node_groups[asset_name]
            if is_latest_version(ng):
                already_present.append(ng)
                to_append.remove(asset_name)

    # Append the new node groups
    with bpy.data.libraries.load(ASSETS_FILE, link=False, assets_only=True) as (
        _,
        data_to,
    ):
        data_to.node_groups = list(to_append)

    if remove_asset_data:
        for ng in data_to.node_groups:
            remove_preview_image(ng)
            ng.asset_clear()

    return list(data_to.node_groups) + already_present
