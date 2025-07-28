import bpy
import platform

os = platform.system()

from .import_shape_to_blender_object import *
from .import_reader import read_cad
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    IntProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
)


def process_batch(self, context):
    """Function called regularly to update Blender scene from main process"""

    # Create the object
    if self.created_object_count < self.total_count:
        for i in range(self.batch_size):
            create_blender_object(self.object_data[self.created_object_count])
            self.created_object_count += 1
            if self.created_object_count >= self.total_count:
                return {"FINISHED"}
    else:
        return {"FINISHED"}

    # Report progress
    wm = context.window_manager
    wm.progress_update(self.created_object_count)

    # # Force UI update
    for area in self.context.screen.areas:
        if area.type in {"VIEW_3D", "OUTLINER"}:
            area.tag_redraw()

    # Update status text
    self.status = f"{self.created_object_count}/{self.total_count} shapes imported"

    return {"PASS_THROUGH"}


class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
    bl_idname = "object.sp_cad_import"
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

    batch_size = 300
    created_object_count = 0
    total_count = 0
    object_data = []

    def execute(self, context):
        self.context = context
        self.status = "Gathering shape data..."

        # Show wait cursor
        context.window.cursor_set("WAIT")

        # import cProfile
        # profiler = cProfile.Profile()
        # profiler.enable()

        # Initialize your CAD import data
        shape, doc, container_name = read_cad(self.filepath)
        shape_hierarchy = ShapeHierarchy(shape, container_name, doc)

        # Collect shapes to process
        shapes_args = []

        if self.faces_on:
            import_face_nodegroups(shape_hierarchy)
            shapes_args.extend(
                [
                    (shape, name, color, collection, False)
                    for shape, name, color, collection in shape_hierarchy.faces
                ]
            )

        if self.curves_on:
            append_node_group("SP - Curve Meshing")
            shapes_args.extend(
                [
                    (shape, name, color, collection, True)
                    for shape, name, color, collection in shape_hierarchy.edges
                ]
            )

        self.total_count = len(shapes_args)
        if self.total_count == 0:
            self.report({"WARNING"}, "No shapes to import")
            return {"CANCELLED"}

        # Create object data
        for s in shapes_args:
            shape, name, color, collection, iscurve = s
            self.object_data.append(
                process_object_data_of_shape(
                    shape,
                    name,
                    color,
                    collection,
                    self.trims_on,
                    self.scale,
                    self.resolution,
                    iscurve,
                )
            )

        # profiler.disable()
        # profiler.print_stats()

        # Setup modal operation
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)

        # Initialize tracking
        self.objects_created = 0
        self.status = "Starting object creation..."

        # Setup progress bar
        context.window_manager.progress_begin(0, self.total_count)
        context.window.cursor_set("DEFAULT")

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "TIMER":
            return process_batch(self, context)
        elif event.type == "ESC":
            context.window_manager.progress_end()
            return {"CANCELLED"}
        return {"PASS_THROUGH"}


classes = [
    SP_OT_ImportCAD,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
