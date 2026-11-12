from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPMultiplyMatrix2x21x2(CustomGeometryGroup):
    _name = "SP - Multiply Matrix 2x2 @ 1x2"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_multiply_matrix_2x2_1x2", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        a = tree.inputs.float("a", 0.0)
        b = tree.inputs.float("b", 0.0)
        c_ = tree.inputs.float("c", 0.0)
        d = tree.inputs.float("d", 0.0)
        x = tree.inputs.float("x", 0.5, min_value=-10_000.0, max_value=10_000.0)
        y = tree.inputs.float("y", 0.5, min_value=-10_000.0, max_value=10_000.0)
        a_1 = tree.outputs.float("a")
        b_1 = tree.outputs.float("b")

        a * x + b * y >> a_1
        c_ * x + d * y >> b_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-462.46, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (536.53, -8.6), None, (("a", "Math.001", "Value"), ("b", "Math.004", "Value"), )),
            "Math": ("ShaderNodeMath", (2.76, 241.1), None, (("Value", "Group Input", "a"), ("Value#1", "Group Input", "x"), )),
            "Math.001": ("ShaderNodeMath", (305.84, 151.9), None, (("Value", "Math", "Value"), ("Value#1", "Math.002", "Value"), )),
            "Math.002": ("ShaderNodeMath", (-3.26, 79.58), None, (("Value", "Group Input", "b"), ("Value#1", "Group Input", "y"), )),
            "Math.003": ("ShaderNodeMath", (-5.07, -72.91), None, (("Value", "Group Input", "c"), ("Value#1", "Group Input", "x"), )),
            "Math.004": ("ShaderNodeMath", (298.01, -162.11), None, (("Value", "Math.003", "Value"), ("Value#1", "Math.005", "Value"), )),
            "Math.005": ("ShaderNodeMath", (-11.09, -234.43), None, (("Value", "Group Input", "d"), ("Value#1", "Group Input", "y"), )),
        }