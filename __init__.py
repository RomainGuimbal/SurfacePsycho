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
    "version": (0, 5),
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

import sys
from os.path import dirname, abspath
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

from utils import *
import macros
from macros import *
import gui
from gui import *

import platform
os = platform.system()


class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("sp.add_library", text="Add Assets Path")



##############################
##         REGISTER         ##
##############################

classes = [
    SP_AddonPreferences,
    SP_OT_add_curve,
    SP_OT_add_aop,
    SP_OT_add_bicubic_patch,
    SP_OT_add_curvatures_probe,
    SP_OT_add_flat_patch,
    SP_OT_add_library,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_toogle_control_geom,
    SP_PT_MainPanel,
    SP_OT_unify_versions,
    SP_OT_assign_as_endpoint,
    SP_OT_remove_from_endpoints,
    SP_OT_add_trim_contour,
    
]

if os=="Windows":
    classes+= [
        SP_OT_quick_export,
        SP_OT_ExportStep,
        SP_OT_ExportIges,
        SP_OT_ImportCAD,
    ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.append(menu_convert)
    if os=="Windows":
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
    if os=="Windows":
        bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
        bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    # bpy.types.TEXT_HT_header.remove(progress_bar)

if __name__ == "__main__":
    register()
    bpy.ops.sp.cad_import()









