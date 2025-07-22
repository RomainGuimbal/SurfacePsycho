import bpy
import platform

os = platform.system()

from .import_process_pipeline import *
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

    def execute(self, context):
        self.context = context

        # Show wait cursor
        context.window.cursor_set("WAIT")

        # Initialize your CAD import data
        shape, self.doc, container_name = read_cad(self.filepath)
        shape_hierarchy = ShapeHierarchy(shape, container_name)

        # Collect shapes to process
        shapes_args = []

        if self.faces_on:
            import_face_nodegroups(shape_hierarchy)
            shapes_args.extend(
                [(shape, col, False) for shape, col in shape_hierarchy.faces]
            )

        if self.curves_on:
            append_node_group("SP - Curve Meshing")
            shapes_args.extend(
                [(shape, col, True) for shape, col in shape_hierarchy.edges]
            )

        if not shapes_args:
            self.report({"WARNING"}, "No shapes to import")
            return {"CANCELLED"}

        # Create and run pipeline
        pipeline = IOCPUPipeline(
            io_function=_process_cad_io,
            cpu_function=_process_cad_compute,
            io_workers=3,
            cpu_workers=mp.cpu_count(),
        )

        tasks = [f"task_{i}" for i in range(len(shapes_args))]
        task_args = list(zip(shapes_args, (self.doc, self.trims_on, self.scale, self.resolution)*len(shapes_args)))

        start_time = time.time()
        # Pass both tasks and arguments
        results = pipeline.process_tasks(tasks, task_args)
        end_time = time.time()

        print(f"\nProcessed {len(tasks)} tasks in {end_time - start_time:.2f} seconds")
        print(f"First few results:")
        for i, result in enumerate(results[:3]):
            if isinstance(result, Exception):
                print(f"  Task {i}: ERROR - {result}")
            else:
                print(f"  Task {i}: {result[:50]}...")

        # Setup progress bar
        context.window.cursor_set("DEFAULT")
        wm = context.window_manager
        wm.progress_begin(0, len(tasks))

        # Start modal timer
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "TIMER" and self._timer and self.pipeline:

            for area in self.context.screen.areas:
                if area.type in {"VIEW_3D", "OUTLINER"}:
                    area.tag_redraw()

            # status = self.pipeline.poll()
            # if status != PipelineStatus.RUNNING:
            #     return self._finish_modal(context, status)

        # elif event.type == "ESC":
        #     if self.pipeline:
        #         self.pipeline.cancel()
        #     return self._finish_modal(context, PipelineStatus.CANCELLED)

        return {"PASS_THROUGH"}



def _process_cad_io(shape_args, global_args):
    """I/O stage: Parse CAD data"""
    shape, col, iscurve = shape_args
    doc, trims_on, scale, resolution = global_args

    return process_object_data_of_shape(
        shape, doc, col, trims_on, scale, resolution, iscurve
    )

def _process_cad_compute(object_data):
    create_blender_object(object_data)
    return f"CPU_processed_{object_data['name']}"




classes = [
    SP_OT_ImportCAD,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)