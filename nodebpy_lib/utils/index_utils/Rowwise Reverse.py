from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class RowwiseReverse(CustomGeometryGroup):
    _name = "Rowwise Reverse"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        v_count = tree.inputs.integer("V Count", 0)
        u = tree.inputs.integer("U", 0, description="Column of vertex (0,1,2,0,1,2...)")
        v = tree.inputs.integer("V", 0, description="Row of vertex (0,0,0,1,1,1...)")
        index = tree.outputs.integer("Index")

        ((v_count * v).props(width=100.0) + (v_count - 1 - u)).props(width=100.0) >> index

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-391.03, -45.42), None, ()),
            "Group Output": ("NodeGroupOutput", (364.98, -52.87), None, (("Index", "Integer Math.024", "Value"), )),
            "Integer Math.019": ("FunctionNodeIntegerMath", (234.05, -108.51), None, (("Value", "Group Input", "V Count"), ("Value#1", "Group Input", "V"), )),
            "Integer Math.024": ("FunctionNodeIntegerMath", (232.72, -68.89), None, (("Value", "Integer Math.019", "Value"), ("Value#1", "Integer Math.029", "Value"), )),
            "Integer Math.029": ("FunctionNodeIntegerMath", (47.22, -35.34), None, (("Value", "Integer Math.031", "Value"), ("Value#1", "Group Input", "U"), )),
            "Integer Math.031": ("FunctionNodeIntegerMath", (-159.08, -15.16), None, (("Value", "Group Input", "V Count"), )),
        }