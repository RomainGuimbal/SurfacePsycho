from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSignedDistanceFrom2dLine(CustomGeometryGroup):
    _name = "SP - Signed distance from 2d line"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_signed_distance_from_2d_line", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        line_point_1 = tree.inputs.vector("Line Point 1", (0.0, 0.0, 0.0), hide_value=True)
        line_point_2 = tree.inputs.vector("Line point 2", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        point = tree.inputs.vector("Point", (0.0, 0.0, 0.0))
        signed_distance = tree.outputs.float("Signed distance")

        vector = (line_point_2 - line_point_1).normalize()
        (
            g.CombineXYZ(x=vector.y, y=(0.0 - vector.x).props(hide=True)).o.vector.dot(point - line_point_1)
            >> signed_distance
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Combine XYZ.002": ("ShaderNodeCombineXYZ", (363.94, 63.35), None, (("X", "Separate XYZ", "Y"), ("Y", "Math", "Value"), )),
            "Group Input": ("NodeGroupInput", (-696.87, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (732.69, 34.96), None, (("Signed distance", "Vector Math.008", "Value"), )),
            "Math": ("ShaderNodeMath", (180.2, 46.5), None, (("Value#1", "Separate XYZ", "X"), )),
            "Separate XYZ": ("ShaderNodeSeparateXYZ", (-24.99, 55.72), None, (("Vector", "Vector Math.009", "Vector"), )),
            "Vector Math": ("ShaderNodeVectorMath", (-384.66, 75.91), None, (("Vector", "Group Input", "Line point 2"), ("Vector#1", "Group Input", "Line Point 1"), )),
            "Vector Math.008": ("ShaderNodeVectorMath", (542.25, 61.36), None, (("Vector", "Combine XYZ.002", "Vector"), ("Vector#1", "Vector Math.010", "Vector"), )),
            "Vector Math.009": ("ShaderNodeVectorMath", (-210.23, 48.54), None, (("Vector", "Vector Math", "Vector"), )),
            "Vector Math.010": ("ShaderNodeVectorMath", (360.96, -83.26), None, (("Vector", "Group Input", "Point"), ("Vector#1", "Group Input", "Line Point 1"), )),
        }