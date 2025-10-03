import bpy
from ..utils import *
from ..exporter.export_process_svg import *
from ..importer.import_shape_to_blender_object import *
from ..exporter.export_process_cad import *


class SP_OT_add_NURBS_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_nurbs_patch"
    bl_label = "SP - Add NURBS PsychoPatch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("NURBS Patch", context)
        return {"FINISHED"}
    

class SP_OT_add_bezier_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_bezier_patch"
    bl_label = "SP - Add Bezier Patch"
    bl_options = {"REGISTER", "UNDO"}

    degree_u: bpy.props.IntProperty(
        name="Degree U",
        description="Number of control points in U direction -1",
        default=1,
        min=1,
        max=16,
    )

    degree_v: bpy.props.IntProperty(
        name="Degree V",
        description="Number of control points in V direction -1",
        default=1,
        min=1,
        max=16,
    )

    show_control_geom: bpy.props.BoolProperty(
        name="Show Control Geometry", default=False
    )

    def execute(self, context):
        mesh = create_grid_mesh(self.degree_u + 1, self.degree_v + 1)

        # Create and link the object
        self.obj = bpy.data.objects.new("Bezier Patch", mesh)
        context.collection.objects.link(self.obj)

        add_sp_modifier(self.obj, "SP - Reorder Grid Index", append=True)
        add_sp_modifier(
            self.obj,
            "SP - Connect Bezier Patch",
            {"Continuity Level": 3},
            append=True,
        )
        add_sp_modifier(
            self.obj,
            "SP - Bezier Patch Meshing",
            {"Control Polygon": self.show_control_geom},
            pin=True,
            append=True,
        )

        # Set object location to 3D cursor
        self.obj.location = context.scene.cursor.location

        # Select the new object and make it active
        bpy.ops.object.select_all(action="DESELECT")
        self.obj.select_set(True)
        context.view_layer.objects.active = self.obj

        return {"FINISHED"}


class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_flat_patch"
    bl_label = "SP - Add flat PsychoPatch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("FlatPatch", context)
        return {"FINISHED"}


class SP_OT_add_curve(bpy.types.Operator):
    bl_idname = "object.sp_add_curve"
    bl_label = "SP - Add PsychoCurve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("PsychoCurve", context)
        return {"FINISHED"}


classes = [
    SP_OT_add_bezier_patch,
    SP_OT_add_curve,
    SP_OT_add_flat_patch,
    SP_OT_add_NURBS_patch,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
