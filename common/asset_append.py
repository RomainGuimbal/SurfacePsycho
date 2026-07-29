import bpy
from .enums import ASSETS_FILE
from .version_utils import is_current_version


def append_object_by_name(obj_name, context):  # for importing from the asset file
    with bpy.data.libraries.load(
        str(ASSETS_FILE), link=True, assets_only=True, pack=True
    ) as (
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
                mod.node_group.asset_clear()


def _get_latest_loaded_node_group(asset_name: str):
    ng = bpy.data.node_groups.get(asset_name)
    if ng is None or ng.type != "GEOMETRY":
        return None
    if is_current_version(ng):
        return ng
    return None


def append_node_group(asset_name, force=False):
    if not force:
        ng = _get_latest_loaded_node_group(asset_name)
        if ng is not None:
            return ng

    node_groups = append_multiple_node_groups([asset_name], force)
    return node_groups[0]


def append_multiple_node_groups(
    ng_names: list, force=False
) -> list[bpy.types.NodeGroup]:
    to_append = []
    ids = []
    already_present = [None] * len(ng_names)

    if force:
        to_append = ng_names
        ids = list(range(len(to_append)))
        # bpy.data.node_groups[].make_local
    else:
        for i, asset_name in enumerate(ng_names):
            ng = _get_latest_loaded_node_group(asset_name)
            if ng is not None:
                already_present[i] = ng
            else:
                to_append.append(asset_name)
                ids.append(i)

    if to_append:
        with bpy.data.libraries.load(
            str(ASSETS_FILE), link=True, assets_only=True, pack=True
        ) as (
            _,
            data_to,
        ):
            data_to.node_groups = list(to_append)

        for i, dt in enumerate(data_to.node_groups):
            already_present[ids[i]] = dt

    return already_present
