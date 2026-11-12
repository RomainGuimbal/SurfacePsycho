from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Sinh(CustomGeometryGroup):
    _name = "Sinh"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.float("Input", 0.0)
        result = tree.outputs.float("Result")

        mix = g.Mix.float(0.5, g.Math.exponent(input), (0.0 - g.Math.exponent((0.0 - input).props(hide=True))).props(hide=True)).props(hide=True)

        mix >> result

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-387.07, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (554.85, -1.41), None, (("Result", "Mix", "Result"), )),
            "Math": ("ShaderNodeMath", (23.82, 75.03), None, (("Value", "Group Input", "Input"), )),
            "Math.001": ("ShaderNodeMath", (-152.24, -75.03), None, (("Value#1", "Group Input", "Input"), )),
            "Math.002": ("ShaderNodeMath", (19.09, -71.34), None, (("Value", "Math.001", "Value"), )),
            "Math.003": ("ShaderNodeMath", (180.74, -106.24), None, (("Value#1", "Math.002", "Value"), )),
            "Mix": ("ShaderNodeMix", (364.85, -31.51), None, (("A", "Math", "Value"), ("B", "Math.003", "Value"), )),
        }