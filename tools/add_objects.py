import bpy
from ..common.enums import SP_obj_type, MESHER_NAMES
from ..common.utils import (
    create_grid_mesh,
    add_sp_modifier,
    append_object_by_name,
    append_multiple_node_groups,
)


class SP_OT_add_NURBS_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_nurbs_patch"
    bl_label = "SP - Add NURBS PsychoPatch"
    bl_options = {"REGISTER", "UNDO"}

    degree_u: bpy.props.IntProperty(
        name="Degree U",
        description="Number of control points in U direction -1",
        default=3,
        min=1,
        max=16,
    )

    degree_v: bpy.props.IntProperty(
        name="Degree V",
        description="Number of control points in V direction -1",
        default=3,
        min=1,
        max=16,
    )

    u_count: bpy.props.IntProperty(
        name="U Count",
        description="Number of control points in U direction",
        default=2,
        min=2,
        soft_max=16,
    )

    v_count: bpy.props.IntProperty(
        name="V Count",
        description="Number of control points in V direction",
        default=2,
        min=2,
        soft_max=16,
    )

    show_control_geom: bpy.props.BoolProperty(
        name="Show Control Geometry", default=False
    )

    def execute(self, context):
        append_multiple_node_groups(
            {"SP - Reorder Grid Index", MESHER_NAMES[SP_obj_type.BSPLINE_SURFACE]}
        )
        # Create and link the object
        mesh = create_grid_mesh(self.u_count, self.v_count)
        obj = bpy.data.objects.new("Nurbs Patch", mesh)
        context.collection.objects.link(obj)

        add_sp_modifier(obj, "SP - Reorder Grid Index")
        add_sp_modifier(
            obj,
            MESHER_NAMES[SP_obj_type.BSPLINE_SURFACE],
            {
                "Control Polygon": self.show_control_geom,
                "Degree U": self.degree_u,
                "Degree V": self.degree_v,
            },
            pin=True,
        )

        # Set object location to 3D cursor
        obj.location = context.scene.cursor.location

        # Select the new object and make it active
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj

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
        soft_max=16,
    )

    degree_v: bpy.props.IntProperty(
        name="Degree V",
        description="Number of control points in V direction -1",
        default=1,
        min=1,
        soft_max=16,
    )

    show_control_geom: bpy.props.BoolProperty(
        name="Show Control Geometry", default=False
    )

    def execute(self, context):
        append_multiple_node_groups(
            {
                "SP - Reorder Grid Index",
                "SP - Connect Bezier Patch",
                MESHER_NAMES[SP_obj_type.BEZIER_SURFACE],
            }
        )

        # Create and link the object
        mesh = create_grid_mesh(self.degree_u + 1, self.degree_v + 1)
        obj = bpy.data.objects.new("Bezier Patch", mesh)
        context.collection.objects.link(obj)

        add_sp_modifier(obj, "SP - Reorder Grid Index")
        add_sp_modifier(
            obj,
            "SP - Connect Bezier Patch",
            {"Continuity": 3},
        )
        add_sp_modifier(
            obj,
            MESHER_NAMES[SP_obj_type.BEZIER_SURFACE],
            {"Control Polygon": self.show_control_geom},
            pin=True,
        )

        # Set object location to 3D cursor
        obj.location = context.scene.cursor.location

        # Select the new object and make it active
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj

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


class SP_OT_add_compound(bpy.types.Operator):
    bl_idname = "object.sp_add_compound"
    bl_label = "SP - Add PsychoCompound"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("Compound", context)
        return {"FINISHED"}


classes = [
    SP_OT_add_bezier_patch,
    SP_OT_add_curve,
    SP_OT_add_flat_patch,
    SP_OT_add_NURBS_patch,
    SP_OT_add_compound,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
