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
from utils import *
import macros
from macros import *
import gui
from gui import *


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





##############################
##         REGISTER         ##
##############################

classes = (
    SP_AddonPreferences,
    SP_OT_add_curve,
    SP_OT_add_aop,
    SP_OT_add_bicubic_patch,
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
    SP_OT_ImportCAD,
    SP_OT_assign_as_endpoint,
    SP_OT_remove_from_endpoints,
    SP_OT_add_trim_contour,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_class(SP_OT_add_library)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.append(menu_convert)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    # bpy.types.WindowManager.progress = bpy.props.FloatProperty()
    # bpy.types.TEXT_HT_header.append(progress_bar)

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.remove(menu_convert)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    # bpy.types.TEXT_HT_header.remove(progress_bar)

if __name__ == "__main__":
    register()
    bpy.ops.sp.cad_import()









