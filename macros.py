import bpy
import bmesh
from utils import *
from mathutils import Vector
from datetime import datetime
from os.path import dirname, abspath, join
import platform
os = platform.system()

if os!="Darwin":
    from importer import *
    from exporter import *

    class SP_OT_quick_export(bpy.types.Operator):
        bl_idname = "sp.quick_export"
        bl_label = "SP - Quick export"
        bl_options = {'REGISTER', 'UNDO'}
        bl_description =  "Exports selection as .STEP at current .blend location."

        def execute(self, context):

            blenddir = bpy.path.abspath("//")
            if blenddir !="":#avoids exporting to root
                dir =  blenddir
            else :
                dir = context.preferences.filepaths.temporary_directory
            pathstr = dir + str(datetime.today())[:-7].replace('-','').replace(' ','-').replace(':','')

            export_isdone = export_step(context, f"{pathstr}.step", True)
            if export_isdone:
                self.report({'INFO'}, f"Step file exported as {pathstr}.step")
            else :
                self.report({'INFO'}, 'No SurfacePsycho Objects selected')
            return {'FINISHED'}


class SP_OT_add_bicubic_patch(bpy.types.Operator):
    bl_idname = "sp.add_bicubic_patch"
    bl_label = "Add Bicubic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("Bicubic Bezier Patch", context)
        return {'FINISHED'}
    

class SP_OT_add_bezier_patch(bpy.types.Operator):
    bl_idname = "sp.add_bezier_patch"
    bl_label = "Add Bezier Patch"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        append_asset("SP - Bezier Patch Meshing")
        return self.execute(context)

    order_u : bpy.props.IntProperty(
        name="Order U",
        description="Number of control points in U direction -1",
        default=3,
        min=1,
    )

    order_v : bpy.props.IntProperty(
        name="Order V",
        description="Number of control points in V direction -1",
        default=3,
        min=1
    )

    def execute(self, context):
        # Create a new mesh and a new object
        mesh = bpy.data.meshes.new(name="Grid")
        obj = bpy.data.objects.new("Bezier Patch", mesh)

        # Link the object to the scene
        bpy.context.collection.objects.link(obj)
        
        # Create a new bmesh
        bm = bmesh.new()

        step_x = 2 / self.order_v
        step_y = 2 / self.order_u

        # Create vertices
        for i in range(self.order_u + 1):
            for j in range(self.order_v + 1):
                x = j * step_x - 1  # Subtract 1 to center
                y = i * step_y - 1  # Subtract 1 to center
                bm.verts.new((x, y, 0))

        bm.verts.ensure_lookup_table()

        # Create faces
        for i in range(self.order_u):
            for j in range(self.order_v):
                v1 = bm.verts[i * (self.order_v + 1) + j]
                v2 = bm.verts[i * (self.order_v + 1) + j + 1]
                v3 = bm.verts[(i + 1) * (self.order_v + 1) + j + 1]
                v4 = bm.verts[(i + 1) * (self.order_v + 1) + j]
                bm.faces.new((v1, v2, v3, v4))

        # Update bmesh
        bm.to_mesh(mesh)
        bm.free()

        # set smooth
        mesh = obj.data
        values = [True] * len(mesh.polygons)
        mesh.polygons.foreach_set("use_smooth", values)

        # Update mesh
        mesh.update()

        add_sp_modifier(obj, "SP - Bezier Patch Meshing", {}, False)
        

        # Set object location to 3D cursor
        obj.location = bpy.context.scene.cursor.location

        # Select the new object and make it active
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        return {'FINISHED'}
        
        

    
class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "sp.add_flat_patch"
    bl_label = "Add flat PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("FlatPatch", context)
        return {'FINISHED'}
    
class SP_OT_add_curve(bpy.types.Operator):
    bl_idname = "sp.add_curve"
    bl_label = "Add PsychoCurve"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoCurve", context)
        return {'FINISHED'}

class SP_OT_add_curvatures_probe(bpy.types.Operator):
    bl_idname = "sp.add_curvatures_probe"
    bl_label = "Add Curvatures Probe"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Object inspect curvature. Bind to surface in modifier's properties"

    def execute(self, context):
        append_object_by_name("SP - Curvatures Probe", context)
        return {'FINISHED'}


class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "sp.add_library"
    bl_label = "Add Library"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):

        #create lib
        asset_lib_path = join(dirname(abspath(__file__)),"assets")
        paths = [a.path for a in bpy.context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths :
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)
        
        #Rename lib
        asset_library = bpy.context.preferences.filepaths.asset_libraries.get("assets")
        if asset_library:
            asset_library.name = "SurfacePsycho"

        return {'FINISHED'}





class SP_OT_toogle_control_geom(bpy.types.Operator):
    bl_idname = "sp.toogle_control_geom"
    bl_label = "SP - Toogle Control Geom"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Toogle the control geometry of selected object. The active object determines whether to show or hide"

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
    bl_description = "Select Visible Curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group is not None and m.node_group.name[:-4] in ['SP - Mesh Bezier Chain', 'SP - Bezier Curve Any Order', 'SP -  Mesh Bezier Chain', 'SP -  Bezier Curve Any Order', 'SP - Curve Meshing', 
                                                                                                 'SP - Mesh Bezier C', 'SP - Bezier Curve Any O', 'SP -  Mesh Bezier C', 'SP -  Bezier Curve Any O', 'SP - Curve Mes']:
                    o.select_set(True)
                    break
        return {'FINISHED'}

class SP_OT_select_visible_surfaces(bpy.types.Operator):
    bl_idname = "sp.select_visible_surfaces"
    bl_label = "SP - Select Visible Surfaces"
    bl_description = "Select Visible Surfaces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects=[ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers :
                if m.type == "NODES" and m.node_group is not None and m.node_group.name[:-4] in ['SP - Any Order Patch Meshing', 'SP - Bicubic Patch Meshing','SP - Mesh Flat patch', 'SP - Patch meshing', 'SP - FlatPatch Meshing'
                                                                                                 'SP - Any Order Patch Mes', 'SP - Bicubic Patch Mes','SP - Mesh Flat p', 'SP - Patch mes', 'SP - FlatPatch Mes']:
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
            # Switch to object mode to modify vertex groups
            bpy.ops.object.mode_set(mode='OBJECT')  
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
    


class SP_OT_select_endpoints(bpy.types.Operator):
    bl_idname = "sp.select_endpoints"
    bl_label = "Select Endpoints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
        
        # Ensure we're in edit mode, Switch to object mode to access mesh data
        bpy.ops.object.mode_set(mode='EDIT') 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        vertex_group = obj.vertex_groups.get("Endpoints")
        if not vertex_group:
            self.report({'INFO'}, "No Endpoints")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}
        
        for v in obj.data.vertices:
            try:
                weight = vertex_group.weight(v.index)
                if weight > 0.6:
                    v.select = True
            except RuntimeError:
                # Vertex is not in the group, skip it
                pass
        
        # Switch back to edit mode to show the selection
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}




class SP_OT_add_trim_contour(bpy.types.Operator):
    bl_idname = "sp.add_trim_contour"
    bl_label = "Add Trim Contour"
    bl_description = "Add Trim Contour to selected patch"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        # set mode
        original_mode = bpy.context.mode
        if original_mode == 'EDIT_MESH':
            selected_objects = context.objects_in_mode
        else:
            selected_objects = context.selected_objects
        
        # loop through selection
        for obj in selected_objects:

            #check if supported object
            is_patch=False
            try :
                if original_mode=='EDIT_MESH':
                    bpy.ops.object.mode_set(mode='OBJECT')
                ob = obj.evaluated_get(context.evaluated_depsgraph_get())
                points = get_attribute_by_name(ob, 'CP_any_order_surf', 'vec3', 1)
                is_patch = True
            except :
                try :
                    if original_mode=='EDIT_MESH':
                        bpy.ops.object.mode_set(mode='OBJECT')
                    ob = obj.evaluated_get(context.evaluated_depsgraph_get())
                    points = get_attribute_by_name(ob, 'CP_NURBS_patch', 'vec3', 1)
                    is_patch = True
                except :
                    pass
            
            #add contour
            if obj.type == 'MESH' and is_patch:
                self.add_square_inside_mesh(context, obj)

        # Restore the original mode
        if original_mode=='EDIT_MESH':
            original_mode='EDIT'
        bpy.ops.object.mode_set(mode=original_mode)




        return {'FINISHED'}
    
    def add_square_inside_mesh(self, context, obj):
        
        # Ensure the object is active and enter Edit mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Create bmesh from the object
        bm = bmesh.from_edit_mesh(obj.data)
        
        # Create vertices of the square
        verts = [
            bm.verts.new(Vector((0, 0, 0))),
            bm.verts.new(Vector((1, 0, 0))),
            bm.verts.new(Vector((1, 1, 0))),
            bm.verts.new(Vector((0, 1, 0))),
        ]
        
        # Create edges
        bm.edges.new(verts[0:2])
        bm.edges.new(verts[1:3])
        bm.edges.new(verts[2:])
        bm.edges.new([verts[3],verts[0]])
        
        # Update the mesh
        bmesh.update_edit_mesh(obj.data)
        
        # Ensure the new vertices are selected
        for vert in verts:
            vert.select = True
        
        # Assign to Trim contour groups


        # Switch to object mode to modify vertex groups
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add vertex groups
        if "Endpoints" not in obj.vertex_groups:
            obj.vertex_groups.new(name="Endpoints")
        if "Trim Contour" not in obj.vertex_groups:
            obj.vertex_groups.new(name="Trim Contour")

        vg_endpoint = obj.vertex_groups["Endpoints"]
        vg_contour = obj.vertex_groups["Trim Contour"]
        
        # Add selected vertices to the vertex group
        for v in obj.data.vertices[-4:]:
            if v.select:
                vg_endpoint.add([v.index], 1.0, 'ADD')
                vg_contour.add([v.index], 1.0, 'ADD')

    



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

#TODO
# Bridge patches


classes = [
    SP_OT_add_bezier_patch,
    SP_OT_add_bicubic_patch,
    SP_OT_add_curvatures_probe,
    SP_OT_add_curve,
    SP_OT_add_flat_patch,
    SP_OT_add_library,
    SP_OT_add_trim_contour,
    SP_OT_assign_as_endpoint,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_remove_from_endpoints,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_toogle_control_geom,
    SP_OT_unify_versions,
    SP_OT_select_endpoints,
]
if os!="Darwin":
    classes+= [
        SP_OT_quick_export,
    ]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)