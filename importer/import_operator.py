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
import multiprocessing
from multiprocessing import Manager
import time
import random


def object_data_creator(shapes_of_worker, queue, shared_dict, objects_to_create):
    """Worker process that creates object data and puts it in the queue"""

    for i in range(objects_to_create):
        shape, col, iscurve = shapes_of_worker[i]
        obj_data = process_object_data_of_shape(
                shape,
                shared_dict["doc"],
                col,
                shared_dict["trims_on"],
                shared_dict["scale"],
                shared_dict["resolution"],
                iscurve,
            )

        # Put in queue and update shared progress
        queue.put(obj_data)
        with shared_dict["lock"]:
            shared_dict["progress"] += 1
            shared_dict["last_update"] = time.time()


def modal_update(self, context):
    """Function called regularly to update Blender scene from main process"""
    # Process available objects from queue
    processed_count = 0
    while not self.queue.empty() and processed_count < self.batch_size:
        obj_data = self.queue.get()

        # Create the object in Blender
        create_blender_object(obj_data)

        processed_count += 1
        self.objects_created += 1

    # Update progress
    with self.shared_dict["lock"]:
        progress = self.shared_dict["progress"]
        total = self.shared_dict["total"]

    # Report progress
    wm = context.window_manager
    wm.progress_update(progress)
    
    # # Force UI update
    # for area in self.context.screen.areas:
    #     if area.type in {"VIEW_3D", "OUTLINER"}:
    #         area.tag_redraw()

    # Update status text
    self.status = f"Created {self.objects_created}/{total} objects"

    # Check if we're done
    if progress >= total:
        wm.progress_end()
        self.report({"INFO"}, f"Finished creating {total} objects")
        return {"FINISHED"}

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

    # for test
    total_objects=100
    batch_size=5
    num_workers=4

    def execute(self, context):
        self.context = context

        # Show wait cursor
        context.window.cursor_set("WAIT")

        # Initialize your CAD import data
        shape, doc, container_name = read_cad(self.filepath)
        shape_hierarchy = ShapeHierarchy(shape, container_name)

        # Collect shapes to process
        shapes_args = []

        if self.faces_on:
            import_face_nodegroups(shape_hierarchy)
            shapes_args.extend(
                [(shape, name, color, collection, False) for shape, collection in shape_hierarchy.faces]
            )

        if self.curves_on:
            append_node_group("SP - Curve Meshing")
            shapes_args.extend(
                [(shape, col, True) for shape, col in shape_hierarchy.edges]
            )

        if (not self.faces_on) and (not self.curves_on):
            self.report({"WARNING"}, "No shapes to import")
            return {"CANCELLED"}
        

        # Setup modal operation
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)

        # Create shared objects
        self.manager = Manager()
        self.shared_dict = self.manager.dict()
        self.queue = self.manager.Queue()

        # Initialize shared state
        self.shared_dict["progress"] = 0
        self.shared_dict["total"] = self.total_objects
        self.shared_dict["lock"] = self.manager.Lock()
        self.shared_dict["doc"] = doc
        self.shared_dict["trims_on"] = self.trims_on
        self.shared_dict["scale"] = self.scale
        self.shared_dict["resolution"] = self.resolution

        # Start worker processes
        self.workers = []
        objects_per_worker = self.total_objects // self.num_workers
        remaining = self.total_objects % self.num_workers

        for i in range(self.num_workers):
            count = objects_per_worker + (1 if i < remaining else 0)
            shapes_of_worker = shapes_args[i * objects_per_worker : (i + 1) * objects_per_worker]
            if count > 0:
                p = multiprocessing.Process(
                    target=object_data_creator, args=(shapes_of_worker, self.queue, self.shared_dict, count)
                )
                p.start()
                self.workers.append(p)

        # Initialize tracking
        self.objects_created = 0
        self.status = "Starting creation..."

        # Setup progress bar
        context.window_manager.progress_begin(0, self.total_objects)
        context.window.cursor_set("DEFAULT")

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == 'TIMER':
            return modal_update(self, context)
        elif event.type == 'ESC':
            return self.cancel(context)
        return {'PASS_THROUGH'}

    def cancel(self, context):
        """Cleanup if operator is cancelled"""
        # Terminate worker processes
        for p in self.workers:
            p.terminate()

        # Cleanup manager
        self.manager.shutdown()

        # End progress bar
        context.window_manager.progress_end()

        self.report({"WARNING"}, "Operation cancelled")


classes = [
    SP_OT_ImportCAD,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
