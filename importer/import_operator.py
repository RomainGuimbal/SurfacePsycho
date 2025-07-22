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
            # io_workers=min(len(shapes), (os.cpu_count()) * 5),
            batch_size=100,
        )

        self.pipeline = MultiStagePipeline(config)

        # Set processors
        self.pipeline.set_processors(
            io_processor=self._process_cad_io,
            compute_processor_name=self._process_cad_compute,
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

    def _process_cad_compute(self, object_data):
        """Compute stage: Heavy mesh processing"""
        create_blender_object(object_data)
        return True

    def _create_blender_object(self, object_data):
        """Result handler: Create Blender objects (main thread)"""
        

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
        


classes = [
    SP_OT_ImportCAD,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)




# Example usage and test functions
def example_io_function(task):
    """Example I/O function - simulates network request or file I/O"""
    # Simulate I/O delay
    time.sleep(0.1)  # 100ms I/O operation
    return f"IO_result_for_{task}"

def example_cpu_function(io_result):
    """Example CPU function - simulates heavy computation"""
    # Simulate CPU work
    result = 0
    for i in range(1000000):  # CPU intensive loop
        result += i * 0.001
    return f"CPU_processed_{io_result}_result_{result}"

def main():
    """Example usage of the pipeline"""
    # Create sample tasks
    tasks = [f"task_{i}" for i in range(50)]
    
    # Create and run pipeline
    pipeline = IOCPUPipeline(
        io_function=example_io_function,
        cpu_function=example_cpu_function,
        io_workers=3,
        cpu_workers=mp.cpu_count()
    )
    
    start_time = time.time()
    results = pipeline.process_tasks(tasks)
    end_time = time.time()
    
    print(f"\nProcessed {len(tasks)} tasks in {end_time - start_time:.2f} seconds")
    print(f"First few results:")
    for i, result in enumerate(results[:3]):
        if isinstance(result, Exception):
            print(f"  Task {i}: ERROR - {result}")
        else:
            print(f"  Task {i}: {result[:50]}...")