##############################
##            GUI           ##
##############################
import bpy
import platform

os = platform.system()
from .operators import macros

# from .macros import SP_Props_Group
from .exporter.exporter_cad import export_step, export_iges
from .exporter.exporter_svg import export_svg
from .importer.multiStagePipeline import *
from .importer.shape_to_blender_object import *
from .importer.reader import read_cad
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)
from bpy_extras.io_utils import (
    ExportHelper,
    ImportHelper,
    orientation_helper,
    axis_conversion,
)



class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.step_export"
    bl_label = "Export STEP"
    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    scale: FloatProperty(name="Scale", default=1000, min=0)
    sew_tolerance_exponent: IntProperty(
        name="Sewing Tolerance Exponent",
        description="In millimeter, after scale have been applied (-1 = 0.1mm)",
        default=-1,
        soft_min=-10,
        soft_max=0,
    )

    def execute(self, context):
        export_isdone = export_step(
            context,
            self.filepath,
            self.use_selection,
            self.scale,
            10**self.sew_tolerance_exponent,
        )

        if export_isdone:
            pass
            # self.report({'INFO'}, f"Step file exported as {self.filepath}.step")
        else:
            self.report({"INFO"}, "No SurfacePsycho Objects selected")
        return {"FINISHED"}


class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.iges_export"
    bl_label = "Export IGES"
    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    scale: FloatProperty(name="Scale", default=1000, min=0)
    sew_tolerance_exponent: IntProperty(
        name="Sewing Tolerance Exponent",
        description="In millimeter, after scale have been applied (-1 = 0.1mm)",
        default=-1,
        soft_min=-10,
        soft_max=0,
    )

    def execute(self, context):
        export_iges(
            context,
            self.filepath,
            self.use_selection,
            self.scale,
            10**self.sew_tolerance_exponent,
        )
        return {"FINISHED"}


@orientation_helper(axis_forward="Y", axis_up="Z")
class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
    bl_idname = "sp.cad_import"
    bl_label = "Import CAD"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".step;.stp;.iges;.igs"
    filter_glob: StringProperty(
        default="*.step;*.stp;*.iges;*.igs", options={"HIDDEN"}, maxlen=255
    )
    faces_on: BoolProperty(name="Faces", description="Import Faces", default=True)
    trims_on: BoolProperty(
        name="Trim Contours",
        description="Import faces with their trim contours",
        default=True,
    )
    curves_on: BoolProperty(name="Curves", description="Import Curves", default=True)
    scale: FloatProperty(name="Scale", default=0.001, precision=3)
    resolution: IntProperty(name="Resolution", default=16, soft_min=6, soft_max=256)

    pipeline = None
    _timer = None

    def execute(self, context):
        self.context = context

        # Show wait cursor
        context.window.cursor_set("WAIT")

        # Initialize your CAD import data
        shape, self.doc, container_name = read_cad(self.filepath)
        shape_hierarchy = ShapeHierarchy(shape, container_name)

        # Collect shapes to process
        shapes = []

        if self.faces_on:
            import_face_nodegroups(shape_hierarchy)
            shapes.extend([(shape, col, False) for shape, col in shape_hierarchy.faces])

        if self.curves_on:
            append_node_group("SP - Curve Meshing")
            shapes.extend([(shape, col, True) for shape, col in shape_hierarchy.edges])

        if not shapes:
            self.report({"WARNING"}, "No shapes to import")
            return {"CANCELLED"}

        # Setup pipeline
        config = PipelineConfig(
            io_workers=min(len(shapes), (os.cpu_count()) * 5),
            compute_workers=os.cpu_count(),
            batch_size=100,
        )

        self.pipeline = MultiStagePipeline(config)

        # Set processors
        self.pipeline.set_processors(
            io_processor=self._process_cad_io,
            compute_processor=self._process_cad_compute,
            result_handler=self._create_blender_object,
        )

        # Set callbacks
        self.pipeline.set_callbacks(
            progress_callback=self._on_progress, completion_callback=self._on_completion
        )

        # Setup progress bar
        context.window.cursor_set("DEFAULT")
        wm = context.window_manager
        wm.progress_begin(0, len(shapes))

        # Start processing
        if not self.pipeline.start(shapes):
            self.report({"ERROR"}, "Failed to start pipeline")
            return {"CANCELLED"}

        # Start modal timer
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "TIMER" and self._timer and self.pipeline:
            status = self.pipeline.poll()

            if status != PipelineStatus.RUNNING:
                return self._finish_modal(context, status)

        elif event.type == "ESC":
            if self.pipeline:
                self.pipeline.cancel()
            return self._finish_modal(context, PipelineStatus.CANCELLED)

        return {"PASS_THROUGH"}

    def _process_cad_io(self, shape_data):
        """I/O stage: Parse CAD data"""
        shape, col, iscurve = shape_data

        return process_object_data_of_shape(
            shape, self.doc, col, self.trims_on, self.scale, self.resolution, iscurve
        )

    def _process_cad_compute(self, io_data):
        """Compute stage: Heavy mesh processing"""
        # Add any CPU-intensive mesh operations here
        return io_data

    def _create_blender_object(self, object_data):
        """Result handler: Create Blender objects (main thread)"""
        create_blender_object(object_data)

        # Force UI update
        for area in self.context.screen.areas:
            if area.type in {"VIEW_3D", "OUTLINER"}:
                area.tag_redraw()

    def _on_progress(self, processed, total):
        """Progress callback"""
        if self.context:
            self.context.window_manager.progress_update(processed)

    def _on_completion(self, status, processed, error_msg):
        """Completion callback"""
        if status == PipelineStatus.COMPLETED:
            self.report({"INFO"}, f"{processed} Objects Imported")
        elif status == PipelineStatus.CANCELLED:
            self.report({"INFO"}, "Import Cancelled")
        elif status == PipelineStatus.ERROR:
            self.report({"ERROR"}, f"Import Error: {error_msg}")

    def _finish_modal(self, context, status):
        """Clean up and finish modal operation"""
        # Cleanup
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None

        context.window_manager.progress_end()

        if status == PipelineStatus.COMPLETED:
            return {"FINISHED"}
        else:
            return {"CANCELLED"}


class SP_OT_ExportSvg(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.svg_export"
    bl_label = "Export SVG"

    filename_ext = ".svg"
    filter_glob: StringProperty(default="*.svg", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    plane: EnumProperty(
        name="Projection Plane",
        default="XY",
        items=[
            ("XY", "XY", "XY Plane"),
            ("YZ", "YZ", "YZ Plane"),
            ("XZ", "XZ", "XZ Plane"),
        ],
    )
    origin_mode: EnumProperty(
        name="Origin Mode",
        default="auto",
        items=[
            ("auto", "Auto", "Fits exported entities"),
            (
                "world",
                "World",
                "Place entities relative to Scene origin. Thay may be out of canvas",
            ),
        ],
    )
    scale: FloatProperty(
        name="Scale", default=100, min=0, description="In pixel per Blender unit"
    )
    color_mode: EnumProperty(
        name="Color",
        default="material",
        items=[
            (
                "material",
                "From Material",
                "Color svg paths according to material in object first slot",
                "MATERIAL",
                1,
            ),
            (
                "object",
                "From Object",
                "Color svg paths according to object color property",
                "OBJECT_DATAMODE",
                2,
            ),
        ],
    )

    def execute(self, context):
        export_svg(
            context,
            self.filepath,
            self.use_selection,
            self.plane,
            self.origin_mode,
            self.scale,
            self.color_mode,
        )
        return {"FINISHED"}


class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        if context.mode == "OBJECT":
            row = self.layout.row()
            row.scale_y = 2.0
            row.operator("sp.quick_export", text="Quick .STEP Export", icon="EXPORT")

            # Toggle control geom
            row = self.layout.row()
            row.operator(
                "sp.toggle_control_geom",
                text="Toggle Control Geometry",
                icon="OUTLINER_DATA_LATTICE",
            )

        # Combs
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        heading = self.layout.column(align=True, heading="Combs")
        row = heading.row(align=True)
        row.prop(context.scene.sp_properties, "combs_on", text="")
        sub = row.row()
        sub.active = context.scene.sp_properties.combs_on
        sub.prop(context.scene.sp_properties, "combs_scale", text="")

        if context.mode == "OBJECT":
            # Select all
            row = self.layout.row()
            row.label(text="Select Visible")
            sub = row.row(align=True)
            sub.operator(
                "sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE"
            )
            sub.operator(
                "sp.select_visible_surfaces",
                text="Surfaces",
                icon="OUTLINER_OB_SURFACE",
            )

            # Add Probe
            row = self.layout.row()
            row.operator(
                "sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR"
            )

            # Replace node group
            row = self.layout.row()
            row.operator(
                "sp.replace_node_group",
                text="Replace Node Group",
                icon="UV_SYNC_SELECT",
            )


class SP_PT_EditPanel(bpy.types.Panel):
    bl_idname = "SP_PT_EditPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"

    def draw(self, context):
        if context.mode == "OBJECT" or context.mode == "EDIT_MESH":
            row = self.layout.row()
            row.operator(
                "sp.add_trim_contour", text="Add Trim Contour", icon="MOD_MESHDEFORM"
            )

        if context.mode == "EDIT_MESH":
            # Endpoints
            row = self.layout.row()
            row.label(text="Endpoints")
            sub = row.row(align=True)
            sub.operator("sp.toggle_endpoints", text="Toggle")
            sub.operator("sp.select_endpoints", text="Select")

            # Type
            row = self.layout.row()
            row.operator(
                "sp.set_segment_type", text="Spline", icon="MOD_CURVE"
            ).type = "spline"

            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator(
                "sp.set_segment_type", text="Circle", icon="MESH_CIRCLE"
            ).type = "circle"
            sub.operator("sp.set_segment_type", text="Arc", icon="SPHERECURVE").type = "circle_arc"

            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator(
                "sp.set_segment_type", text="Ellipse", icon="MESH_CAPSULE"
            ).type = "ellipse"
            sub.operator(
                "sp.set_segment_type", text="Arc", icon="INVERSESQUARECURVE"
            ).type = "ellipse_arc"

            # Segment Degree
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(
                context.scene.sp_properties,
                "active_segment_degree",
                text="NURBS Degree",
            )

            # Weight
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_vert_weight", text="Weight")


class SP_MT_PIE_SegmentEdit(bpy.types.Menu):
    bl_label = "SP Segment Type"

    def draw(self, context):
        if context.mode == "EDIT_MESH":
            layout = self.layout
            pie = layout.menu_pie()
            # Pie order: west, east, south, north, north-west, north-east, south-west, south-east
            pie.operator("sp.set_segment_type", text="Circle", icon="MESH_CIRCLE").type = "circle"#West
            pie.operator(
                "sp.set_segment_type", text="Ellipse", icon="MESH_CAPSULE"
            ).type = "ellipse" #East
            pie.operator("sp.toggle_endpoints", text="Toggle Endpoints") #South
            pie.operator("sp.set_spline", text="Spline", icon="RNDCURVE") #North
            pie.operator("sp.set_segment_type", text="Circle Arc", icon="SPHERECURVE"
            ).type = "circle_arc" #North-west
            pie.operator(
                "sp.set_segment_type", text="Ellipse Arc", icon="INVERSESQUARECURVE"
            ).type = "ellipse_arc" #North-east
            # pie.separator() #South-west
            # pie.separator() #South-east


def menu_surface(self, context):
    self.layout.separator()
    if context.mode == "OBJECT":
        self.layout.operator(
            "sp.add_bezier_patch", text="Bezier PsychoPatch", icon="SURFACE_NSURFACE"
        )
        self.layout.operator(
            "sp.add_nurbs_patch", text="NURBS PsychoPatch", icon="SURFACE_NSURFACE"
        )
        self.layout.operator(
            "sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE"
        )
        # self.layout.operator("sp.add_cylinder", text="Cylinder", icon="SURFACE_NCYLINDER")


def menu_curve(self, context):
    self.layout.separator()
    if context.mode == "OBJECT":
        self.layout.operator("sp.add_curve", text="PsychoCurve", icon="CURVE_NCURVE")


def menu_convert(self, context):
    self.layout.separator()
    self.layout.label(text="SurfacePsycho")
    # if context.mode == "OBJECT":
    # if context.active_object.type == "SURFACE":
    self.layout.operator(
        "sp.bl_nurbs_to_psychopatch",
        text="Internal NURBS to PsychoPatch",
        icon="SURFACE_NSURFACE",
    )
    # if context.active_object.type == "MESH":
    self.layout.operator(
        "sp.psychopatch_to_bl_nurbs",
        text="PsychoPatch to internal NURBS",
        icon="SURFACE_NSURFACE",
    )


def menu_export_step(self, context):
    self.layout.operator("sp.step_export", text="SurfacePsycho CAD (.step)")


def menu_export_iges(self, context):
    self.layout.operator("sp.iges_export", text="SurfacePsycho CAD (.iges)")


def menu_func_import(self, context):
    self.layout.operator(
        SP_OT_ImportCAD.bl_idname, text="SurfacePsycho CAD (.step, .iges)"
    )


def menu_export_svg(self, context):
    self.layout.operator("sp.svg_export", text="SurfacePsycho SVG (.svg)")


# topbar menu (fails)
def menu_segment_edit(self, context):
    self.layout.menu("SP_MT_SegmentEdit")


addon_keymaps = []


def hotkeys_add(addon_keymaps):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")

        kmi = km.keymap_items.new("sp.toggle_endpoints","F", "PRESS", shift=True, alt= True)
        addon_keymaps.append((km, kmi))
        
        kmi = km.keymap_items.new("wm.call_menu_pie","F", "PRESS", shift=True)
        kmi.properties.name = "SP_MT_PIE_SegmentEdit"
        addon_keymaps.append((km, kmi))


def hotkeys_remove(addon_keymaps):
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = [
    SP_PT_MainPanel,
    SP_PT_EditPanel,
    SP_MT_PIE_SegmentEdit,
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
    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_svg)
    # bpy.types.TOPBAR_MT_editor_menus.append(menu_segment_edit)

    hotkeys_add(addon_keymaps)


def unregister():
    hotkeys_remove(addon_keymaps)

    # bpy.types.TOPBAR_MT_editor_menus.remove(menu_segment_edit)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_svg)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)

    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    macros.unregister()


if __name__ == "__main__":
    bpy.ops.sp.cad_import()
