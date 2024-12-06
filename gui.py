##############################
##            GUI           ##
##############################
import bpy
import platform
os = platform.system()
from . import macros
# from .macros import SP_Props_Group

if os!="Darwin":
    from .importer import import_cad
    from .exporter_cad import export_step, export_iges

    from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
    from bpy_extras.io_utils import ExportHelper, ImportHelper, orientation_helper, axis_conversion


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


    class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
        bl_idname = "sp.cad_import"
        bl_label = "Import CAD"
        bl_options = {'REGISTER', 'UNDO'}

        filename_ext = ".step;.stp;.iges;.igs"
        filter_glob: StringProperty(default="*.step;*.stp;*.iges;*.igs", options={'HIDDEN'}, maxlen=255)
        faces: BoolProperty(name="Faces", description="Import Faces", default=True)
        trim_contours: BoolProperty(name="Trim Contours", description="Import faces with their trim contours", default=True)
        curves: BoolProperty(name="Curves", description="Import Curves", default=False)

        def modal(self, context, event):
            return {'PASS_THROUGH'}

        def execute(self, context):
            import_cad(self.filepath, context, {"faces":self.faces, "curves":self.curves, "trim_contours":self.trim_contours,})
            self.report({'INFO'}, 'Some surface types may have been ignored')
            return {'RUNNING_MODAL'}



from .exporter_svg import export_svg

class SP_OT_ExportSvg(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.svg_export"
    bl_label = "Export SVG"

    filename_ext = ".svg"
    filter_glob: StringProperty(default="*.svg", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    plane: EnumProperty(name="Projection Plane", default='XY', items=[('XY', "XY", "XY Plane"), ('YZ', "YZ", "YZ Plane"), ('XZ', "XZ", "XZ Plane")])
    origin_mode: EnumProperty(name="Origin Mode", default='auto', items=[('auto', "Auto", "Fits exported entities"), 
                                                                         ('world', "World", "Place entities relative to Scene origin. Thay may be out of canvas")])
    scale: FloatProperty(name="Scale", default=100, min=0, description="In pixel per Blender unit")
    color_mode: EnumProperty(name="Color", default='material', items=[('material', "From Material", "Color svg paths according to material in object first slot", 'MATERIAL', 1),
                                                                      ('object', "From Object", "Color svg paths according to object color property", 'OBJECT_DATAMODE', 2)])
    def execute(self, context):
        export_svg(context, self.filepath, self.use_selection, self.plane, self.origin_mode, self.scale, self.color_mode)
        return {'FINISHED'}










class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            if os != "Darwin" :
                row = self.layout.row()
                row.scale_y = 2.0
                row.operator("sp.quick_export", text="Quick export as .STEP", icon="EXPORT")
            
            row = self.layout.row()
            row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR")
            row = self.layout.row()
            row.operator("sp.replace_node_group", text="Replace Node Group", icon="UV_SYNC_SELECT")
            

        if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH' :
            row = self.layout.row()
            row.operator("sp.add_trim_contour", text="Add Trim Contour", icon="MOD_MESHDEFORM")

        if context.mode == 'EDIT_MESH':
            self.layout.label(text="Bezier Segments Endpoints")
            row = self.layout.row()

            sub = row.row(align=True)
            sub.operator("sp.assign_as_endpoint", text="Assign")
            sub.operator("sp.remove_from_endpoints", text="Remove")

            sub = row.row(align=True)
            sub.operator("sp.select_endpoints", text="Select")
            
        

class SP_PT_ViewPanel(bpy.types.Panel):
    bl_idname = "SP_PT_ViewPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "View"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    

    def draw(self, context):
        row = self.layout.row()
        row.operator("sp.toggle_control_geom", text="Toggle Control Geometry", icon="OUTLINER_DATA_LATTICE")
        row = self.layout.row()
        row.operator("sp.toggle_combs", text="Toggle Combs", icon="PARTICLEMODE")

        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        col = self.layout.column()
        col.prop(context.scene.sp_properties, "combs_scale", text="Combs Scale")


class SP_PT_SelectPanel(bpy.types.Panel):
    bl_idname = "SP_PT_SelectPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Select"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    

    def draw(self, context):
        # self.layout.label(text="Select Entities")
        layout = self.layout
        split = layout.split(factor=0.5, align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        col1.operator("sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE")
        col2.operator("sp.select_visible_surfaces", text="Surfaces", icon="OUTLINER_OB_SURFACE")





def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_bezier_patch", text="Bezier PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_nurbs_patch", text="NURBS PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_curve", text="PsychoCurve", icon="CURVE_NCURVE")


def menu_convert(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        if context.active_object.type == 'SURFACE':
            self.layout.operator("sp.bl_nurbs_to_psychopatch", text="Internal NURBS to PsychoPatch", icon="SURFACE_NSURFACE")
        if context.active_object.type == 'MESH':
            self.layout.operator("sp.psychopatch_to_bl_nurbs", text="PsychoPatch to internal NURBS", icon="SURFACE_NSURFACE")


if os!="Darwin":
    def menu_export_step(self, context):
        self.layout.operator("sp.step_export", text="SurfacePsycho CAD (.step)")

    def menu_export_iges(self, context):
        self.layout.operator("sp.iges_export", text="SurfacePsycho CAD (.iges)")

    def menu_func_import(self, context):
        self.layout.operator(SP_OT_ImportCAD.bl_idname, text="SurfacePsycho CAD (.step, .iges)")

def menu_export_svg(self, context):
    self.layout.operator("sp.svg_export", text="SurfacePsycho SVG (.svg)")


classes = [
    SP_PT_MainPanel,
    SP_PT_ViewPanel,
    SP_PT_SelectPanel,
    SP_OT_ExportSvg,
]

if os!="Darwin":
    classes+= [
        SP_OT_ExportStep,
        SP_OT_ExportIges,
        SP_OT_ImportCAD,
    ]


def register():
    macros.register()
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.append(menu_convert)
    if os!="Darwin":
        bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
        bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_svg)
    
def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_svg)
    if os!="Darwin":
        bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
        bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.remove(menu_convert)
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    macros.unregister()

if __name__ == "__main__":
    if os!="Darwin":
        bpy.ops.sp.cad_import()