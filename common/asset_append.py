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


def _get_latest_loaded_node_group(asset_name: str):
    ng = bpy.data.node_groups.get(asset_name)
    if ng is None or ng.type != "GEOMETRY":
        return None
    if is_latest_version(ng):
        return ng
    return None


def append_node_group(asset_name, link=False, remove_asset_data=True):
    ng = _get_latest_loaded_node_group(asset_name)
    if ng is not None:
        return ng

    node_groups = append_multiple_node_groups(
        [asset_name], link=link, remove_asset_data=remove_asset_data
    )
    return node_groups[0]


def append_multiple_node_groups(
    ng_names: list, remove_asset_data=True, link=False
) -> list[bpy.types.NodeGroup]:
    to_append = []
    already_present = []

    for asset_name in ng_names:
        ng = _get_latest_loaded_node_group(asset_name)
        if ng is not None:
            already_present.append(ng)
        else:
            to_append.append(asset_name)

    if to_append:
        with bpy.data.libraries.load(ASSETS_FILE, link=link, assets_only=True) as (
            _,
            data_to,
        ):
            data_to.node_groups = list(to_append)

        if remove_asset_data:
            for ng in data_to.node_groups:
                remove_preview_image(ng)
                ng.asset_clear()

        already_present.extend(data_to.node_groups)

    return already_present
