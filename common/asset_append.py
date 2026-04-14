import bpy
from .enums import ASSETS_FILE
from .utils import change_GN_modifier_settings
from .versioning import (
    is_latest_version,
    remove_suffix,
    replace_node_group,
    OLD_NODE_MAPPING,
    ASSET_NODE_GROUPS,
    ALL_SP_ASSET_NODE_GROUPS_EVER,
)


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


def update_node_group(name):
    # check if name is outdated
    new_name = name
    if remove_suffix(name) in OLD_NODE_MAPPING.keys():
        new_name = OLD_NODE_MAPPING[name]

    # get latest version if it exists
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
            and (ng_name in ASSET_NODE_GROUPS or ng_name in OLD_NODE_MAPPING.keys())
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
        elif name in OLD_NODE_MAPPING.keys():
            new_name = OLD_NODE_MAPPING[name]
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
