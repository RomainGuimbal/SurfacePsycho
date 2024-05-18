##############################
##            GUI           ##
##############################
import sys
from os.path import dirname
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

import bpy
import platform
os = platform.system()

from importer import *
from exporter import export_step, export_iges

from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import (
    ExportHelper,
    orientation_helper,
    axis_conversion,
)




@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.step_export"
    bl_label = "Export STEP"

    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    axis_up: EnumProperty(default='Z')
    axis_forward: EnumProperty(default='Y')

    def execute(self, context):
        export_step(context, self.filepath, self.use_selection, self.axis_up, self.axis_forward)
        return {'FINISHED'}


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.iges_export"
    bl_label = "Export IGES"

    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    axis_up: EnumProperty(default='Z')
    axis_forward: EnumProperty(default='Y')

    def execute(self, context):
        export_iges(context, self.filepath, self.use_selection,self.axis_up, self.axis_forward)
        return {'FINISHED'}








class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            if os == "Windows" :
                row = self.layout.row()
                row.scale_y = 2.0
                row.operator("sp.quick_export", text="Quick export as .STEP", icon="EXPORT")
            row = self.layout.row()
            row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR")
            row = self.layout.row()
            row.operator("sp.toogle_control_geom", text="Toogle Control Geometry", icon="OUTLINER_DATA_LATTICE")
            
            self.layout.label(text="Select Entities")
            layout = self.layout
            split = layout.split(factor=0.5, align=True)
            col1 = split.column(align=True)
            col2 = split.column(align=True)

            col1.operator("sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE")
            col2.operator("sp.select_visible_surfaces", text="Surfaces", icon="OUTLINER_OB_SURFACE")

        if context.mode == 'EDIT_MESH':
            self.layout.label(text="Bezier Segments Endpoints")
            layout = self.layout
            split = layout.split(factor=0.5, align=True)
            col1 = split.column(align=True)
            col2 = split.column(align=True)
            
            col1.operator("sp.assign_as_endpoint", text="Assign")
            col2.operator("sp.remove_from_endpoints", text="Remove")
            
        if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH' :
            row = self.layout.row()
            row.operator("sp.add_trim_contour", text="Add Trim Contour", icon="MOD_MESHDEFORM")


            


class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("sp.add_library", text="Add Assets Path")

def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_aop", text="Any Order PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_bicubic_patch", text="Bicubic PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_cubic_bezier_chain", text="Cubic Bezier Chain", icon="CURVE_BEZCURVE")
        self.layout.operator("sp.add_any_order_curve", text="Any Order PsychoCurve", icon="CURVE_NCURVE")


def menu_convert(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        if context.active_object.type == 'SURFACE':
            self.layout.operator("sp.bl_nurbs_to_psychopatch", text="Internal NURBS to PsychoPatch", icon="SURFACE_NSURFACE")
        if context.active_object.type == 'MESH':
            self.layout.operator("sp.psychopatch_to_bl_nurbs", text="PsychoPatch to internal NURBS", icon="SURFACE_NSURFACE")


def menu_export_step(self, context):
    self.layout.operator("sp.step_export", text="SurfacePsycho CAD (.step)")

def menu_export_iges(self, context):
    self.layout.operator("sp.iges_export", text="SurfacePsycho CAD (.iges)")


