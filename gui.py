##############################
##            GUI           ##
##############################
import bpy
import platform
os = platform.system()
from . import macros
# from .macros import SP_Props_Group


from .importer import prepare_import, topods_to_sp_patch_generator, topods_to_sp_curve_generator, ShapeHierarchy, import_face_nodegroups
from .utils import append_node_group
from .exporter_cad import export_step, export_iges
from .exporter_svg import export_svg

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper, orientation_helper, axis_conversion


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.step_export"
    bl_label = "Export STEP"

    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    # axis_up: EnumProperty(default='Z')
    # axis_forward: EnumProperty(default='Y')
    scale: FloatProperty(name="Scale", default=1000, min=0)

    def execute(self, context):
        export_step(context, self.filepath, self.use_selection, 'Z', 'Y', self.scale)
        return {'FINISHED'}


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.iges_export"
    bl_label = "Export IGES"

    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    # axis_up: EnumProperty(default='Z')
    # axis_forward: EnumProperty(default='Y')
    scale: FloatProperty(name="Scale", default=1000, min=0)

    def execute(self, context):
        export_iges(context, self.filepath, self.use_selection, 'Z', 'Y', self.scale)
        return {'FINISHED'}

@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
    bl_idname = "sp.cad_import"
    bl_label = "Import CAD"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".step;.stp;.iges;.igs"
    filter_glob: StringProperty(default="*.step;*.stp;*.iges;*.igs", options={'HIDDEN'}, maxlen=255)
    faces: BoolProperty(name="Faces", description="Import Faces", default=True)
    trim_contours: BoolProperty(name="Trim Contours", description="Import faces with their trim contours", default=True)
    curves: BoolProperty(name="Curves", description="Import Curves", default=True)
    scale: FloatProperty(name="Scale", default=.001, precision=3)
    resolution : IntProperty(name="Resolution", default=10, soft_min = 6, soft_max=256)

    def execute(self, context):
        # Initialize your CAD import generator
        shape, doc, container_name = prepare_import(self.filepath)
        
        # Create hierarchy and collections
        shape_hierarchy = ShapeHierarchy(shape, container_name)
        shape_count= len(shape_hierarchy.faces) + len(shape_hierarchy.edges)

        # Face generator
        if self.faces:
            import_face_nodegroups(shape_hierarchy)
            self.generator1 = topods_to_sp_patch_generator(shape_hierarchy.faces, doc, self.trim_contours, self.scale, self.resolution)
        self.generator1_active = self.faces

         # Curve generator
        if self.curves:
            append_node_group("SP - Curve Meshing")
            self.generator2 = topods_to_sp_curve_generator(shape_hierarchy.edges, doc, self.scale, self.resolution)
        self.generator2_active = self.curves

        self.objects_processed = 0
        self.batch_size = 500  # Adjust based on performance
        
        # Setup progress bar
        wm = context.window_manager
        wm.progress_begin(0, shape_count)
        
        # Add timer to trigger modal updates
        self.timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        
        # import cProfile
        # profiler = cProfile.Profile()
        # profiler.enable()

        # profiler.disable()
        # profiler.print_stats()
        
        #self.report({'INFO'}, 'Shapes of unsupported types are ignored')
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            for _ in range(self.batch_size):
                if self.generator1_active:
                    try:
                        # Run a step of generator 1 if it's still active
                        next(self.generator1)
                        self.objects_processed += 1
                    except StopIteration:
                        # Mark generator 1 as finished
                        self.generator1_active = False
                
                if self.generator2_active:
                    try:
                        # Run a step of generator 2 if it's still active
                        next(self.generator2)
                        self.objects_processed += 1
                    except StopIteration:
                        # Mark generator 2 as finished
                        self.generator2_active = False
                # Update progress
                context.window_manager.progress_update(self.objects_processed)

            if not self.generator1_active and not self.generator2_active:
                context.window_manager.progress_end()
                context.window_manager.event_timer_remove(self.timer)
                return {'FINISHED'}

            # Redraw the UI
            context.area.tag_redraw()
            
            return {'PASS_THROUGH'}
        
        return {'PASS_THROUGH'}





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
    bl_category = "Tool"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
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
            # Endpoints
            self.layout.label(text="Endpoints")
            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.assign_as_endpoint", text="Assign")
            sub.operator("sp.remove_from_endpoints", text="Remove")
            sub = row.row(align=True)
            sub.operator("sp.select_endpoints", text="Select")

            # Segment Degree
            self.layout.label(text="NURBS")
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_segment_degree", text="Degree")

            # Circles
            self.layout.label(text="Circle")
            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.assign_as_circle", text="Assign")
            sub.operator("sp.remove_from_circles", text="Remove")

        

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

    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_svg)
    
def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_svg)
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
    bpy.ops.sp.cad_import()