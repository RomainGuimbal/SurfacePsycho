from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Arcsinh(CustomGeometryGroup):
    _name = "Arcsinh"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        value = tree.inputs.float("Value", 0.5, min_value=-10_000.0, max_value=10_000.0)
        value_1 = tree.outputs.float("Value")

        (((value * value).props(hide=True) + 1.0).sqrt() + value).log() >> value_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-200.0, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (892.13, 19.2), None, (("Value", "Math", "Value"), )),
            "Math": ("ShaderNodeMath", (713.94, 26.24), None, (("Value", "Math.021", "Value"), )),
            "Math.001": ("ShaderNodeMath", (14.74, 40.4), None, (("Value", "Group Input", "Value"), ("Value#1", "Group Input", "Value"), )),
            "Math.019": ("ShaderNodeMath", (186.34, 140.08), None, (("Value", "Math.001", "Value"), )),
            "Math.020": ("ShaderNodeMath", (367.17, 69.88), None, (("Value", "Math.019", "Value"), )),
            "Math.021": ("ShaderNodeMath", (540.46, 13.66), None, (("Value", "Math.020", "Value"), ("Value#1", "Group Input", "Value"), )),
        }