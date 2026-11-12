from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPTranspose(CustomGeometryGroup):
    _name = "SP - Transpose"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        u_count = tree.inputs.integer("U Count", 0)
        v_count = tree.inputs.integer("V Count", 0)
        index = tree.inputs.integer("Index", 0, min_value=0, hide_value=True, default_input="INDEX")
        index_1 = tree.outputs.integer("Index")

        reroute = g.Reroute(input=u_count).props(width=19.0)
        (
            ((v_count * (index % reroute)).props(width=100.0) + index // reroute).props(width=100.0)
            >> index_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-328.91, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (323.04, -15.93), None, (("Index", "Integer Math.024", "Value"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-71.64, -74.07), None, (("Value", "Group Input", "Index"), ("Value#1", "Reroute", "Output"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-71.64, -113.08), None, (("Value", "Group Input", "Index"), ("Value#1", "Reroute", "Output"), )),
            "Integer Math.019": ("FunctionNodeIntegerMath", (120.31, -51.29), None, (("Value", "Group Input", "V Count"), ("Value#1", "Integer Math", "Value"), )),
            "Integer Math.024": ("FunctionNodeIntegerMath", (118.62, -88.02), None, (("Value", "Integer Math.019", "Value"), ("Value#1", "Integer Math.001", "Value"), )),
            "Reroute": ("NodeReroute", (-107.41, -34.56), None, (("Input", "Group Input", "U Count"), )),
        }