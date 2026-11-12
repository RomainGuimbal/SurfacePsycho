from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPColwiseReverse(CustomGeometryGroup):
    _name = "SP - Colwise Reverse"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        u_count = tree.inputs.integer("U Count", 0)
        index = tree.inputs.integer("Index", 0, default_input="INDEX")
        index_1 = tree.outputs.integer("Index")

        (
            ((u_count * (u_count - 1 - index // u_count)).props(width=100.0) + index % u_count).props(width=100.0)
            >> index_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-233.9, -22.91), None, ()),
            "Group Output": ("NodeGroupOutput", (622.1, 52.44), None, (("Index", "Integer Math.024", "Value"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (46.39, -178.38), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (49.92, -122.9), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.019": ("FunctionNodeIntegerMath", (403.49, -69.05), None, (("Value", "Group Input", "U Count"), ("Value#1", "Integer Math.028", "Value"), )),
            "Integer Math.024": ("FunctionNodeIntegerMath", (401.63, -113.22), None, (("Value", "Integer Math.019", "Value"), ("Value#1", "Integer Math", "Value"), )),
            "Integer Math.028": ("FunctionNodeIntegerMath", (218.49, -94.71), None, (("Value", "Integer Math.031", "Value"), ("Value#1", "Integer Math.001", "Value"), )),
            "Integer Math.031": ("FunctionNodeIntegerMath", (48.1, -79.35), None, (("Value", "Group Input", "U Count"), )),
        }