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

class SP_OT_unify_versions(bpy.types.Operator):
    #TODO
    #select the one with the highest index (.00i)
    pass