import bpy

class SP_OT_bevel_macro(bpy.types.Operator):
    #TODO
    pass

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