##############################
##            GUI           ##
##############################
import bpy
import platform
os = platform.system()
from . import macros
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty
import threading
import functools
# from .macros import SP_Props_Group


from .importer import prepare_import, ShapeHierarchy, import_face_nodegroups, process_topods_face, create_blender_object, build_SP_curve
from .utils import append_node_group
from .exporter_cad import export_step, export_iges
from .exporter_svg import export_svg

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper, orientation_helper, axis_conversion

addon_keymaps = []

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
    sew_tolerance_exponent : IntProperty(name= "Sewing Tolerance Exponent", description="In millimeter, after scale have been applied (-1 = 0.1mm)", default = -1, soft_min = -10, soft_max=0)

    def execute(self, context):
        export_isdone = export_step(context, self.filepath, self.use_selection, self.scale, 10**self.sew_tolerance_exponent, 'Z', 'Y', )
        
        if export_isdone:
            pass
            # self.report({'INFO'}, f"Step file exported as {self.filepath}.step")
        else :
            self.report({'INFO'}, 'No SurfacePsycho Objects selected')
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
    sew_tolerance_exponent : IntProperty(name= "Sewing Tolerance Exponent", description="In millimeter, after scale have been applied (-1 = 0.1mm)", default = -1, soft_min = -10, soft_max=0)


    def execute(self, context):
        export_iges(context, self.filepath, self.use_selection, self.scale, 10**self.sew_tolerance_exponent, 'Z', 'Y')
        return {'FINISHED'}

@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
    bl_idname = "sp.cad_import"
    bl_label = "Import CAD"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".step;.stp;.iges;.igs"
    filter_glob: StringProperty(default="*.step;*.stp;*.iges;*.igs", options={'HIDDEN'}, maxlen=255)
    faces_on: BoolProperty(name="Faces", description="Import Faces", default=True)
    trims_on: BoolProperty(name="Trim Contours", description="Import faces with their trim contours", default=True)
    curves_on: BoolProperty(name="Curves", description="Import Curves", default=True)
    scale: FloatProperty(name="Scale", default=.001, precision=3)
    resolution : IntProperty(name="Resolution", default=16, soft_min = 6, soft_max=256)

    io_pool = None  # I/O workers
    result_queue = None  # Thread-safe object creation queue
    stop_event = None
    faces_processed = 0
    active_timers = None
    curve_start_at = 0

    def execute(self, context):
        self.context = context
        
        # Show wait cursor
        context.window.cursor_set("WAIT")  

        # Initialize member variables
        self.result_queue = Queue()
        self.stop_event = threading.Event()
        self.faces_processed = 0
        self.active_timers = set()
        self.io_pool = ThreadPoolExecutor(max_workers=30)

        # Initialize your CAD import generator
        shape, self.doc, container_name = prepare_import(self.filepath)
        
        # Create hierarchy and collections
        self.shape_count = 0
        shape_hierarchy = ShapeHierarchy(shape, container_name)

        shapes = []
        if self.faces_on :
            self.shape_count += len(shape_hierarchy.faces)
            self.curve_start_at = len(shape_hierarchy.faces)
            import_face_nodegroups(shape_hierarchy)
            shapes.extend(shape_hierarchy.faces)
        if self.curves_on :
            self.shape_count += len(shape_hierarchy.edges)
            append_node_group("SP - Curve Meshing")
            shapes.extend(shape_hierarchy.edges)

        # Setup progress bar
        context.window.cursor_set("DEFAULT")
        wm = context.window_manager
        wm.progress_begin(0, self.shape_count)
            
        # Start I/O workers
        for index, (shape, col) in enumerate(shapes):
            self.io_pool.submit(
                self.process_object_io,
                shape, col, self.trims_on, 
                self.scale, self.resolution,
                index
            )

            # Start object creation thread
            threading.Thread(target=self._object_creator).start()    

        # Use modal timer instead of modal() for better control
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if self.faces_processed >= self.shape_count :
            self.stop_event.set()
            context.window_manager.progress_end()

        if event.type == 'TIMER' and self._timer:
            # Check for completion
            if self.stop_event.is_set() and self.result_queue.empty():
                self._cleanup(context)
                return {'FINISHED'}
            
        if event.type == 'ESC':
            self.stop_event.set()
            self.io_pool.shutdown(wait=False)
            context.window_manager.progress_end()
            return {'CANCELLED'}
                
        return {'PASS_THROUGH'}
    

    def process_object_io(self, shape, col, trims_on, scale, resolution, index):
        """Pure I/O - runs in worker threads"""
        
        # Data gathering
        if index < self.curve_start_at :
            processed_data = process_topods_face(shape, self.doc, col, trims_on, scale, resolution)
        else :
            processed_data = build_SP_curve(shape, self.doc, col, scale, resolution)
        # Pass to main thread via queue
        self.result_queue.put((processed_data))

    def _object_creator(self):
        """Dedicated thread for Blender object creation"""
        while not self.stop_event.is_set():
            try:
                data = self.result_queue.get(timeout=0.1)
                
                # Create timer with unique ID
                timer_id = str(hash(str(data)))
                callback = functools.partial(
                    self._safe_create_object,
                    object_data=data,
                    timer_id=timer_id
                )
                
                bpy.app.timers.register(
                    callback,
                    first_interval=0.0001,
                    persistent=True
                )
                self.active_timers.add(timer_id)
                
            except Empty:
                continue

    def _safe_create_object(self, object_data, timer_id):
        """Main-thread object creation"""
        try:
            create_blender_object(object_data)
            self.faces_processed += 1
            # Update progress
            self.context.window_manager.progress_update(self.faces_processed)
            
            # Force UI update
            for window in bpy.context.window_manager.windows:
                window.screen.areas[0].tag_redraw()
            
        finally:
            self.active_timers.discard(timer_id)
        return None  # Single-shot timer

    def _cleanup(self, context):
            """Proper resource cleanup"""
            if self._timer:
                context.window_manager.event_timer_remove(self._timer)
            self.io_pool.shutdown(wait=False)
            
            # Clear any remaining timers
            for timer_id in list(self.active_timers):
                # Timers will self-clean when they run
                pass





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
    bl_category = "Item"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            row = self.layout.row()
            row.scale_y = 2.0
            row.operator("sp.quick_export", text="Quick .STEP Export", icon="EXPORT")
        
            # Toggle control geom            
            row = self.layout.row()
            row.operator("sp.toggle_control_geom", text="Toggle Control Geometry", icon="OUTLINER_DATA_LATTICE")

        # Combs
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        heading = self.layout.column(align=True, heading="Combs")
        row = heading.row(align=True)
        row.prop(context.scene.sp_properties, "combs_on", text="")
        sub = row.row()
        sub.active = context.scene.sp_properties.combs_on
        sub.prop(context.scene.sp_properties, "combs_scale", text="")
        
        if context.mode == 'OBJECT':
            # Select all
            row = self.layout.row()
            row.label(text="Select Visible")
            sub = row.row(align=True)
            sub.operator("sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE")
            sub.operator("sp.select_visible_surfaces", text="Surfaces", icon="OUTLINER_OB_SURFACE")
        
            # Add Probe
            row = self.layout.row()
            row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR")

            # Replace node group
            row = self.layout.row()
            row.operator("sp.replace_node_group", text="Replace Node Group", icon="UV_SYNC_SELECT")




class SP_PT_EditPanel(bpy.types.Panel):
    bl_idname = "SP_PT_EditPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    
    def draw(self, context):
        if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH' :
            row = self.layout.row()
            row.operator("sp.add_trim_contour", text="Add Trim Contour", icon="MOD_MESHDEFORM")

        if context.mode == 'EDIT_MESH':
            # Endpoints
            row = self.layout.row()
            row.label(text="Endpoints")
            sub = row.row(align=True)
            sub.operator("sp.assign_as_endpoint", text="Assign")
            sub.operator("sp.remove_from_endpoints", text="Remove")
            sub = row.row()
            sub.operator("sp.select_endpoints", text="Select")

            # Type
            row = self.layout.row()
            row.operator("sp.set_segment_type", text="Spline", icon = "MOD_CURVE").type = 0

            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.set_segment_type", text="Circle", icon = "MESH_CIRCLE").type = 3
            sub.operator("sp.set_segment_type", text="Arc", icon = "SPHERECURVE").type = 2
            
            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.set_segment_type", text="Ellipse", icon = "MESH_CAPSULE").type = 5
            sub.operator("sp.set_segment_type", text="Arc", icon = "INVERSESQUARECURVE").type = 4

            # Segment Degree
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_segment_degree", text="NURBS Degree")
            
            # Weight
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_vert_weight", text="Weight")


def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_bezier_patch", text="Bezier PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_nurbs_patch", text="NURBS PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")
        # self.layout.operator("sp.add_cylinder", text="Cylinder", icon="SURFACE_NCYLINDER")
        

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



def hotkeys_add(addon_keymaps):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("sp.toggle_endpoints", type='F', value='PRESS', shift=True)
        addon_keymaps.append((km, kmi))


def hotkeys_remove(addon_keymaps):
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()





classes = [
    SP_PT_MainPanel,
    SP_PT_EditPanel,
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

    hotkeys_add(addon_keymaps)
    
def unregister():  
    hotkeys_remove(addon_keymaps)

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