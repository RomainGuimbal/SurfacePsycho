import bpy

class SP_OT_toogle_control_geom(bpy.types.Operator):
    bl_idname = "sp.toogle_control_geom"
    bl_label = "SP - Toogle Control Geom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.selected_objects]
        first_obj_found = False
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group.name[:5]=='SP - ':
                    for it in m.node_group.interface.items_tree :
                        if it.name in ['Control Polygon', 'Control Geometry', 'Control Grid', 'Control Edges'] and it.socket_type =='NodeSocketBool':
                            input_id = it.identifier
                            if not first_obj_found:
                                first_obj_found=True
                                toogle_side = not m[input_id]
                            m[input_id] = toogle_side
                    m.node_group.interface_update(context)
        return {'FINISHED'}


class SP_OT_select_visible_curves(bpy.types.Operator):
    bl_idname = "sp.select_visible_curves"
    bl_label = "SP - Select Visible Curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group is not None and m.node_group.name in ['SP -  Mesh Bezier Chain', 'SP -  Bezier Curve Any Order']:
                    o.select_set(True)
        return {'FINISHED'}


class SP_OT_select_visible_surfaces(bpy.types.Operator):
    bl_idname = "sp.select_visible_surfaces"
    bl_label = "SP - Select Visible Surfaces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group is not None and m.node_group.name[:-4] in ['SP - Any Order Patch Meshing', 'SP - Bicubic Patch Meshing','SP - Mesh Flat patch',
                                                                                                  'SP - Any Order Patch Mes', 'SP - Bicubic Patch Mes','SP - Mesh Flat p']:
                    o.select_set(True)
        return {'FINISHED'}

class SP_OT_show_only_curves(bpy.types.Operator):
    #TODO
    pass

class SP_OT_bevel_macro(bpy.types.Operator):
    #TODO
    pass

class SP_OT_solidify(bpy.types.Operator):
    #TODO
    # Thickness Driver ?
    # Linked data
    pass






def classify_strings_by_prefix(strings):
    import re
    strings.sort()
    object_dict = {}
    for string in strings:
        # Use regex to extract the common prefix
        match = re.match(r'(\D+)(\d*.*)', string)
        if match:
            prefix = match.group(1)
            if prefix not in object_dict:
                object_dict[prefix] = [string]
            else:
                object_dict[prefix].append(string)
    return object_dict

def highest_suffix_of_each_object_name(names):
    classified_objects=classify_strings_by_prefix(names)
    last_string = []
    for key, value in classified_objects.items():
        if value:
            last_string+= [value[-1]]
    return last_string



class SP_OT_unify_versions(bpy.types.Operator):
    bl_idname = "sp.unify_versions"
    bl_label = "SP - Unify versions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        effect_counter=0
        #Store modifier names
        objects = [ob for ob in context.visible_objects]
        mod_names = []
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group.name[:5]=='SP - ' and m.node_group.name not in mod_names:
                    mod_names.append(m.node_group.name)
        
        latest_mod_names = highest_suffix_of_each_object_name(mod_names)
        latest_mod_names_no_suffix = [l[:-4] for l in latest_mod_names]

        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group.name[:5]=='SP - ' and m.node_group.name not in latest_mod_names:
                    name=m.node_group.name
                    name_no_suffix = name[:-4]

                    if name in latest_mod_names_no_suffix: #if only latest_v_name has a suffix
                        found_name = latest_mod_names[latest_mod_names_no_suffix.index(name)]
                        m.node_group = bpy.data.node_groups[found_name]
                        effect_counter+=1
                        
                    elif name_no_suffix in latest_mod_names_no_suffix: #if latest_v_name AND name have a suffix
                        found_name = latest_mod_names[latest_mod_names_no_suffix.index(name_no_suffix)]
                        m.node_group = bpy.data.node_groups[found_name]
                        effect_counter+=1
        if effect_counter>0:
            self.report({'INFO'}, effect_counter+" modifiers replaced")
        else :
            self.report({'INFO'}, "No SP modifiers replaced")

        return {'FINISHED'}