from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPUVTranslateGizmo(CustomGeometryGroup):
    _name = "SP - UV Translate Gizmo"
    _color_tag = "OUTPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_uv_translate_gizmo", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        position = tree.inputs.vector("Position", (0.0, 0.0, 0.0), hide_value=True)

        _linear_gizmo = g.LinearGizmo(value=(position.x,), position=position, direction=(1.0, 0.0, 0.0), color_id="X")
        _linear_gizmo_1 = g.LinearGizmo(value=(position.y,), position=position, direction=(0.0, 1.0, 0.0), color_id="Y")

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-302.35, -4.1), None, ()),
            "Linear Gizmo": ("GeometryNodeGizmoLinear", (167.48, 111.47), None, (("Position", "Group Input", "Position"), ("Value", "Separate XYZ", "X"), )),
            "Linear Gizmo.001": ("GeometryNodeGizmoLinear", (159.78, -141.79), None, (("Position", "Group Input", "Position"), ("Value", "Separate XYZ", "Y"), )),
            "Separate XYZ": ("ShaderNodeSeparateXYZ", (-58.39, -116.04), None, (("Vector", "Group Input", "Position"), )),
        }