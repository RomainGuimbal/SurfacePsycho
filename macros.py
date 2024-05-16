import bpy
from utils import *
from mathutils import Vector

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
                if m.type == "NODES" and m.node_group is not None and m.node_group.name[:-4] in ['SP - Mesh Bezier Chain', 'SP - Bezier Curve Any Order', 'SP -  Mesh Bezier Chain', 'SP -  Bezier Curve Any Order', 
                                                                                                 'SP - Mesh Bezier C', 'SP - Bezier Curve Any O', 'SP -  Mesh Bezier C', 'SP -  Bezier Curve Any O']:
                    o.select_set(True)
                    break
        return {'FINISHED'}

class SP_OT_select_visible_surfaces(bpy.types.Operator):
    bl_idname = "sp.select_visible_surfaces"
    bl_label = "SP - Select Visible Surfaces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group is not None and m.node_group.name[:-4] in ['SP - Any Order Patch Meshing', 'SP - Bicubic Patch Meshing','SP - Mesh Flat patch', 'SP - Patch meshing',
                                                                                                 'SP - Any Order Patch Mes', 'SP - Bicubic Patch Mes','SP - Mesh Flat p', 'SP - Patch mes']:
                    o.select_set(True)
                    break
        return {'FINISHED'}







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
            self.report({'INFO'}, str(effect_counter)+" modifiers replaced")
        else :
            self.report({'INFO'}, "No SP modifiers replaced")

        return {'FINISHED'}
    




class SP_OT_psychopatch_to_bl_nurbs(bpy.types.Operator):
    bl_idname = "sp.psychopatch_to_bl_nurbs"
    bl_label = "Convert Psychopatches to internal NURBS"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        i=-1
        for o in context.selected_objects :
            type = geom_type_of_object(o, context)
            ob = o.evaluated_get(context.evaluated_depsgraph_get())
            match type :
                case "bezier_surf":
                    cp=get_attribute_by_name(ob, 'CP_bezier_surf', 'vec3', 16)
                    bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                    i+=1
                    spline=context.active_object.data.splines[i]
                    spline.use_endpoint_u = True
                    spline.use_endpoint_v = True
                    spline.order_u = 4
                    spline.order_v = 4
                    
                    # set CP of spline
                    for j,p in enumerate(spline.points): 
                        p.co = (cp[j][0], cp[j][1], cp[j][2], 1)
                    
                case "surf_any":
                    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
                    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
                    cp=get_attribute_by_name(ob, 'CP_any_order_surf', 'vec3', u_count*v_count)
                    if i == -1 :
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.ops.curve.delete(type='VERT')
                    i+=1
                    splines = context.active_object.data.splines
                    for v in range(v_count):
                        spline = splines.new('NURBS')
                        spline.points.add(u_count-1)
                        spline.use_endpoint_u = True
                        spline.use_endpoint_v = True
                        spline.use_bezier_u = True
                        spline.use_bezier_v = True
                        # set CP of spline
                        for j,p in enumerate(spline.points): 
                            p.co = (cp[j+v*u_count][0], cp[j+v*u_count][1], cp[j+v*u_count][2], 1)

                    for s in splines[i:i+v_count]:
                        for p in s.points:
                            p.select = True
                    bpy.ops.object.mode_set(mode = 'EDIT') 
                    bpy.ops.curve.make_segment()
                    splines[i].order_u =min(v_count,6)
                    splines[i].order_v =min(u_count,6)
                
                case "curve_any":
                    cp_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
                    cp=get_attribute_by_name(ob, 'CP_any_order_curve', 'vec3', cp_count)
                    if i == -1 :
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.ops.curve.delete(type='VERT')
                    i+=1
                    spline = context.active_object.data.splines.new('NURBS')
                    spline.points.add(cp_count-1)
                    spline.use_endpoint_u = True
                    spline.use_endpoint_v = True
                    spline.use_bezier_u = True
                    spline.use_bezier_v = True
                    spline.order_u =min(cp_count,6)
                    spline.order_v =min(cp_count,6)

                    # set CP of spline
                    for j,p in enumerate(spline.points): 
                        p.co = (cp[j][0], cp[j][1], cp[j][2], 1)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class SP_OT_bl_nurbs_to_psychopatch(bpy.types.Operator):
    bl_idname = "sp.bl_nurbs_to_psychopatch"
    bl_label = "Convert internal NURBS to Psychopatches"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj_to_convert = context.selected_objects
        first_patch_flag=True

        for o in obj_to_convert:
            if o.type == 'SURFACE':
                for s in o.data.splines:
                    if first_patch_flag :
                        append_object_by_name("PsychoPatch Any Order", context)
                        first_sp_patch = context.selected_objects[0]
                        first_sp_patch.location = o.location
                        sp_patch = first_sp_patch
                        first_patch_flag = False
                    else :
                        sp_patch = first_sp_patch.copy()
                        sp_patch.animation_data_clear()
                        sp_patch.matrix_world = o.matrix_world
                        bpy.context.collection.objects.link(sp_patch)

                    spline_cp = [Vector(p.co[0:3]) for p in s.points]
                    
                    #create mesh grid
                    u_count = s.order_u
                    v_count = s.order_v
                    
                    faces = [(v*u_count + u, (v + 1)*u_count + u, (v + 1)*u_count + 1 + u, v*u_count + 1 + u) for v in range(v_count-1) for u in range(u_count-1)]
                    mesh = bpy.data.meshes.new("Grid") 
                    mesh.from_pydata(spline_cp, [], faces)
                    sp_patch.data=mesh
                    bpy.ops.object.shade_smooth()
        return {'FINISHED'}











class SP_OT_assign_as_endpoint(bpy.types.Operator):
    bl_idname = "sp.assign_as_endpoint"
    bl_label = "Assign as Endpoint"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objs = context.objects_in_mode

        for o in objs :
            bpy.ops.object.mode_set(mode='OBJECT')  # Switch to object mode to modify vertex groups
            # Ensure "Endpoints" vertex group exists
            if "Endpoints" not in o.vertex_groups:
                o.vertex_groups.new(name="Endpoints")
            
            vg = o.vertex_groups["Endpoints"]
            
            # Add selected vertices to the vertex group
            for v in o.data.vertices:
                if v.select:
                    vg.add([v.index], 1.0, 'ADD')
            bpy.ops.object.mode_set(mode='EDIT') 
        return {'FINISHED'}
    

class SP_OT_remove_from_endpoints(bpy.types.Operator):
    bl_idname = "sp.remove_from_endpoints"
    bl_label = "Remove from Endpoints"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objs = context.objects_in_mode
        for o in objs :
            bpy.ops.object.mode_set(mode='OBJECT')
            # Ensure "Endpoints" vertex group exists
            if "Endpoints" in o.vertex_groups:
                vg = o.vertex_groups["Endpoints"]
                
                # Remove selected vertices to the vertex group
                for v in o.data.vertices:
                    if v.select:
                        vg.remove([v.index])
                bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}





class SP_OT_show_only_curves(bpy.types.Operator):
    #TODO
    #Store the state before ?
    pass

class SP_OT_bevel_macro(bpy.types.Operator):
    #TODO
    # Select two CONNECTED patches
    # Trim them 
    # Add a blend surface between (origin at mean of patches origins)
    pass

class SP_OT_solidify(bpy.types.Operator):
    #TODO
    # Thickness Driver ?
    # Linked data
    pass