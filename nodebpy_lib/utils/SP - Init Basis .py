from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPInitBasis(CustomGeometryGroup):
    _name = "SP - Init Basis "
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_init_basis_", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        knot = tree.inputs.float("knot", 0.0)
        t = tree.inputs.float("t", 0.0)
        cp_count = tree.inputs.integer("CP Count", 0)
        cp_i = tree.inputs.integer("CP i", 0)
        max_parameter = tree.inputs.float("Max Parameter", 0.0, min_value=-10_000.0, max_value=10_000.0)
        zero_basis = tree.outputs.float("Zero Basis")

        boolean_math = (t == max_parameter).props(width=145.35) & g.Compare.integer.equal(cp_i, (cp_count - 1).props(hide=True))
        reroute = g.Reroute(input=cp_i).props(width=19.0)
        reroute_1 = g.Reroute(input=knot).props(width=19.0)
        reroute_2 = g.Reroute(input=t).props(width=19.0)
        boolean_math_1 = (reroute_2 >= reroute_1.o.output.point.at(reroute)) & (reroute_2 < reroute_1.o.output.point.at((reroute.o.output + 1).props(hide=True)))
        (boolean_math_1 | boolean_math) >> zero_basis

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (630.13, 109.03), None, (("Boolean", "Boolean Math.001", "Boolean"), ("Boolean#1", "Boolean Math.002", "Boolean"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (369.49, 107.17), None, (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Compare.002", "Result"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (317.64, -180.62), None, (("Boolean", "Compare", "Result"), ("Boolean#1", "Compare.003", "Result"), )),
            "Compare": ("FunctionNodeCompare", (16.32, -203.96), None, (("A", "Group Input", "t"), ("B", "Group Input", "Max Parameter"), )),
            "Compare.001": ("FunctionNodeCompare", (58.49, 175.94), None, (("A", "Reroute.042", "Output"), ("B", "Evaluate at Index.005", "Value"), )),
            "Compare.002": ("FunctionNodeCompare", (52.62, 14.14), None, (("A", "Reroute.042", "Output"), ("B", "Evaluate at Index.006", "Value"), )),
            "Compare.003": ("FunctionNodeCompare", (6.94, -395.06), None, (("A", "Group Input", "CP i"), ("B", "Integer Math", "Value"), )),
            "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (-245.72, 191.05), None, (("Index", "Reroute.002", "Output"), ("Value", "Reroute.041", "Output"), )),
            "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (-247.67, 58.56), None, (("Index", "Integer Math.003", "Value"), ("Value", "Reroute.041", "Output"), )),
            "Group Input": ("NodeGroupInput", (-805.46, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (939.1, 82.44), None, (("Zero Basis", "Boolean Math", "Boolean"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-189.41, -498.55), None, (("Value", "Group Input", "CP Count"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-456.8, -37.66), None, (("Value", "Reroute.002", "Output"), )),
            "Reroute.002": ("NodeReroute", (-478.98, -27.09), None, (("Input", "Group Input", "CP i"), )),
            "Reroute.041": ("NodeReroute", (-357.75, 69.31), None, (("Input", "Group Input", "knot"), )),
            "Reroute.042": ("NodeReroute", (-36.77, -105.44), None, (("Input", "Group Input", "t"), )),
        }