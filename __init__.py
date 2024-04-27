# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Surface Psycho",
    "author": "Romain Guimbal",
    "version": (0, 4),
    "blender": (4, 1, 0),
    "description": "Surface design for the mechanical industry",
    "warning": "Alpha",
    "doc_url": "https://github.com/RomainGuimbal/SurfacePsycho/wiki",
    "category": "3D View",
    "location": "View3D > Add > Surface/Curve  |  View3D > N Panel > Edit"
}

#Packages From Blender
import bpy
import numpy as np
from mathutils import Vector

from datetime import datetime

import sys
from os.path import dirname, abspath
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

#Local Packages
import platform
os = platform.system()
if os=="Windows":
    from importer import *
    from exporter import *
import macros
from macros import *
import gui
from gui import *

##############################
##         FUNCTIONS        ##
##############################

def append_object_by_name(obj_name, context):# for importing from the asset file
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name==obj_name]

    cursor_loc = context.scene.cursor.location

    for o in data_to.objects:
        if o is not None:
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            context.collection.objects.link(o)
            o.location = cursor_loc
            o.asset_clear()
            o.select_set(True)
            bpy.context.view_layer.objects.active = o






##############################
##       OPERTATORS         ##
##############################
    
class SP_OT_quick_export(bpy.types.Operator):
    bl_idname = "sp.quick_export"
    bl_label = "SP - Quick export"
    bl_options = {'REGISTER', 'UNDO'}

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
        append_object_by_name("PsychoPatch", context)
        return {'FINISHED'}
    
class SP_OT_add_biquadratic_patch(bpy.types.Operator):
    bl_idname = "sp.add_biquadratic_patch"
    bl_label = "Add Biquadratic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoPatch Quadratic", context)
        return {'FINISHED'}
    
class SP_OT_add_aop(bpy.types.Operator):
    bl_idname = "sp.add_aop"
    bl_label = "Add Any Order PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoPatch Any Order", context)
        return {'FINISHED'}
    
class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "sp.add_flat_patch"
    bl_label = "Add flat PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("FlatPatch", context)
        return {'FINISHED'}

class SP_OT_add_cubic_bezier_chain(bpy.types.Operator):
    bl_idname = "sp.add_cubic_bezier_chain"
    bl_label = "Add Cubic Bezier Chain"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("Psycho Cubic Chain", context)
        return {'FINISHED'}
    
class SP_OT_add_any_order_curve(bpy.types.Operator):
    bl_idname = "sp.add_any_order_curve"
    bl_label = "Add Any Order PsychoCurve"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoCurve Any Order", context)
        return {'FINISHED'}

class SP_OT_add_curvatures_probe(bpy.types.Operator):
    bl_idname = "sp.add_curvatures_probe"
    bl_label = "Add Curvatures Probe"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("SP - Curvatures Probe", context)
        return {'FINISHED'}

class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "sp.add_library"
    bl_label = "Add Library"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        asset_lib_path = dirname(abspath(__file__))
        paths = [a.path for a in bpy.context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths :
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)
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



##############################
##         REGISTER         ##
##############################

classes = (
    SP_AddonPreferences,
    SP_OT_add_any_order_curve,
    SP_OT_add_aop,
    SP_OT_add_bicubic_patch,
    SP_OT_add_biquadratic_patch,
    SP_OT_add_cubic_bezier_chain,
    SP_OT_add_curvatures_probe,
    SP_OT_add_flat_patch,
    SP_OT_add_library,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_quick_export,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_toogle_control_geom,
    SP_PT_MainPanel,
    SP_OT_ExportStep,
    SP_OT_ExportIges,
    SP_OT_unify_versions,
    SP_OT_import_step_file,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_class(SP_OT_add_library)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)

if __name__ == "__main__":
    register()