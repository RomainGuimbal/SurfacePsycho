import bpy
from .enums import SP_obj_type, MESHER_NAMES, geom_to_sp_type, ASSETS_FILE
from .utils import change_GN_modifier_settings

def remove_preview_image(ng: bpy.types.GeometryNodeTree):
    if ng.preview:
        ng.preview.image_size = [0, 0]
        return True
    return False


def append_object_by_name(obj_name, context):  # for importing from the asset file
    with bpy.data.libraries.load(ASSETS_FILE, link=False, assets_only=True) as (
        data_from,
        data_to,
    ):
        data_to.objects = [name for name in data_from.objects if name == obj_name]

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
    # Load the asset file
    with bpy.data.libraries.load(ASSETS_FILE, link=link, assets_only=True) as (
        data_from,
        data_to,
    ):
        # Find the node group in the file
        if asset_name not in data_from.node_groups:
            raise ValueError(f"Asset '{asset_name}' not found")
        else:
            data_to.node_groups = [asset_name]

    ng = data_to.node_groups[0]
    if remove_asset_data:
        remove_preview_image(ng)
        ng.asset_clear()

    return ng


def append_multiple_node_groups(ng_names: set, remove_asset_data=True):
    # TODO : variant where it append only if there isn't already the current version

    # Append the new node groups
    with bpy.data.libraries.load(ASSETS_FILE, link=False, assets_only=True) as (
        data_from,
        data_to,
    ):
        # Filter the node groups that exist in the asset file
        valid_node_groups = [name for name in ng_names if name in data_from.node_groups]

        # Append the valid node groups
        data_to.node_groups = valid_node_groups

    if remove_asset_data:
        for ng in data_to.node_groups:
            remove_preview_image(ng)
            ng.asset_clear()

    return data_to.node_groups


def add_sp_modifier(
    obj,
    asset_name: str,
    settings_dict={},
    pin=False,
    append=False,
    render=True,
    force_last=False,
):
    if append:
        append_node_group(asset_name)

    if force_last:
        # Unpin modifiers
        pinned_mods = []
        for m in obj.modifiers:
            if m.use_pin_to_last:
                m.use_pin_to_last = False
                pinned_mods.append(m)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=asset_name, type="NODES")
    modifier.node_group = bpy.data.node_groups.get(asset_name)
    modifier.use_pin_to_last = pin
    modifier.show_render = render

    if force_last:
        # Re-pin modifiers
        for m in pinned_mods:
            m.use_pin_to_last = True

    if modifier.node_group == None:
        raise ValueError(f"Node group '{asset_name}' not found")

    # Change settings
    change_GN_modifier_settings(modifier, settings_dict)

    return modifier


def add_sp_modifier_from_node_group(
    obj,
    node_group,
    settings_dict={},
    pin=False,
    render=True,
    force_last=False,
):
    if force_last:
        # Unpin modifiers
        pinned_mods = []
        for m in obj.modifiers:
            if m.use_pin_to_last:
                m.use_pin_to_last = False
                pinned_mods.append(m)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=node_group.name, type="NODES")
    modifier.node_group = node_group
    modifier.use_pin_to_last = pin
    modifier.show_render = render

    if force_last:
        # Re-pin modifiers
        for m in pinned_mods:
            m.use_pin_to_last = True

    # Change settings
    change_GN_modifier_settings(modifier, settings_dict)

    return modifier
