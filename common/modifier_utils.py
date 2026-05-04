import bpy
from .asset_append import append_node_group
from .enums import MESHER_NAMES


def get_modifier_by_name(obj: bpy.types.Object, name):
    for m in obj.modifiers:
        if m.type == name or (m.type == "NODES" and m.node_group.name == name):
            return m
    return None


def change_node_socket_value(
    ob: bpy.types.Object, value, socket_potential_names, socket_type, context
):
    for m in ob.modifiers:
        if m.type == "NODES" and m.node_group and m.node_group.name.startswith("SP - "):
            # Collect items first to avoid modifying during iteration
            items_to_process = []

            for it in list(m.node_group.interface.items_tree):  # Create a copy
                if (
                    it.item_type == "SOCKET"
                    and it.socket_type == socket_type
                    and it.name in socket_potential_names
                ):
                    items_to_process.append(it)

            # Process collected items
            modifier_updated = False
            for it in items_to_process:
                input_id = it.identifier
                # if input_id in m:  # Check existence before access
                m[input_id] = value
                modifier_updated = True

            # Single interface update after all changes
            if modifier_updated:
                m.node_group.interface_update(context)


def change_GN_modifier_settings(modifier, settings_dict):
    tree = modifier.node_group.interface.items_tree
    remaining = set(settings_dict.keys())
    for item in tree:
        if item.name in remaining and isinstance(
            item, bpy.types.NodeTreeInterfaceSocket
        ):
            modifier[item.identifier] = settings_dict[item.name]
            remaining.discard(item.name)
            if not remaining:
                break


def change_mod_settings_from_object(
    object: bpy.types.Object, modifier_name, settings_dict
):
    m = get_modifier_by_name(object, modifier_name)
    change_GN_modifier_settings(m, settings_dict)


def add_sp_modifier(
    obj,
    asset_name: str,
    settings_dict={},
    pin=False,
    append=False,
    render=True,
    force_last=False,
) -> bpy.types.Modifier:
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
) -> bpy.types.Modifier:
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


def remove_modifier(object, name: str):
    for m in object.modifiers:
        if m.type == "NODES" and m.node_group.name == name:
            object.modifiers.remove(m)
            return True
        elif m.type == name:
            object.modifiers.remove(m)
            return True
    return False


def modifier_exists(object, name: str):
    for m in object.modifiers:
        if m.type == "NODES" and m.node_group.name == name:
            return True
    return False


def move_modifier_above_mesher(obj, name):
    mod_index = -1
    mesh_mod_index = -1
    mod_count = len(obj.modifiers)

    for i, m in enumerate(reversed(obj.modifiers)):
        if m.type == "NODES":
            if m.node_group.name == name:
                mod_index = mod_count - 1 - i
            elif m.node_group.name in MESHER_NAMES.values():
                mesh_mod_index = mod_count - 1 - i
        if mod_index>-1 and mesh_mod_index>-1:
            break
        
    if mod_index==-1 or mesh_mod_index==-1:
        raise Exception(f"Modifier \"{name}\" couldn't be moved")
    elif mod_index <= mesh_mod_index:
        return 
    
    obj.modifiers.move(mod_index, index=mesh_mod_index)