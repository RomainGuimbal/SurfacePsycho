from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPUnclampedKnotFromParameter(CustomGeometryGroup):
    _name = "SP - Unclamped Knot from Parameter"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_unclamped_knot_from_parameter", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.float("Input", 0.0)
        virtual_point_count = tree.inputs.integer("Virtual Point Count", 1)
        output = tree.outputs.float("Output")

        with g.Frame():
            math_1 = (input.point.at() - input.point.at(1)).props(hide=True)
        evaluate_at_index = input.point.at(g.Index().o.index - 1)
        reroute = g.Reroute(input=virtual_point_count).props(width=19.0)
        with g.Frame():
            integer_math = reroute.o.output - 1
            evaluate_at_index_1 = input.point.at(integer_math)
            integer_math_1 = g.Index().o.index - (reroute.o.output + 1)
        accumulate_field = (input - evaluate_at_index).props(hide=True).point.at(integer_math - g.Index()).point.leading()
        switch = g.Compare.integer.equal(g.Index(), 0).o.result.switch.float(evaluate_at_index, math_1).props(hide=True)
        (
            (g.Index() > reroute).props(hide=True).switch.float(switch, accumulate_field.point.at(integer_math_1) + evaluate_at_index_1)
            >> output
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (877.79, 166.9), None, (("Value", "Evaluate at Index.005", "Value"), )),
            "Compare.001": ("FunctionNodeCompare", (238.18, -152.92), None, (("A", "Index.001", "Index"), ("B", "Reroute.001", "Output"), )),
            "Compare.002": ("FunctionNodeCompare", (-312.42, -312.08), None, (("A", "Index.003", "Index"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (-237.13, 13.77), None, (("Index", "Integer Math", "Value"), ("Value", "Group Input", "Input"), )),
            "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (30.01, -160.99), "Frame.001", (("Value", "Group Input", "Input"), )),
            "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (35.08, -30.31), "Frame.001", (("Value", "Group Input", "Input"), )),
            "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (290.14, -171.09), "Frame", (("Index", "Integer Math.001", "Value"), ("Value", "Group Input", "Input"), )),
            "Evaluate at Index.004": ("GeometryNodeFieldAtIndex", (1055.17, 59.47), None, (("Index", "Integer Math.002", "Value"), ("Value", "Accumulate Field", "Leading"), )),
            "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (711.66, 103.09), None, (("Index", "Integer Math.003", "Value"), ("Value", "Math.001", "Value"), )),
            "Frame": ("NodeFrame", (182.65, -331.41), None, ()),
            "Frame.001": ("NodeFrame", (-474.35, -522.0), None, ()),
            "Group Input": ("NodeGroupInput", (-779.9, 55.03), None, ()),
            "Group Output": ("NodeGroupOutput", (1735.34, -70.39), None, (("Output", "Switch.001", "Output"), )),
            "Index": ("GeometryNodeInputIndex", (-586.2, -145.12), None, ()),
            "Index.001": ("GeometryNodeInputIndex", (39.28, -60.93), None, ()),
            "Index.002": ("GeometryNodeInputIndex", (293.57, 39.66), None, ()),
            "Index.003": ("GeometryNodeInputIndex", (-468.31, -370.18), None, ()),
            "Index.004": ("GeometryNodeInputIndex", (30.24, -35.37), "Frame", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (-433.84, -89.86), None, (("Value", "Index", "Index"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (35.93, -238.75), "Frame", (("Value", "Reroute.001", "Output"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (291.88, -30.37), "Frame", (("Value", "Index.004", "Index"), ("Value#1", "Integer Math.004", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (531.34, 96.17), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Index.002", "Index"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (33.32, -97.04), "Frame", (("Value", "Reroute.001", "Output"), )),
            "Math": ("ShaderNodeMath", (207.58, -143.01), "Frame.001", (("Value", "Evaluate at Index.002", "Value"), ("Value#1", "Evaluate at Index.001", "Value"), )),
            "Math.001": ("ShaderNodeMath", (21.81, 157.42), None, (("Value", "Group Input", "Input"), ("Value#1", "Evaluate at Index", "Value"), )),
            "Math.002": ("ShaderNodeMath", (1264.41, 6.47), None, (("Value", "Evaluate at Index.004", "Value"), ("Value#1", "Evaluate at Index.003", "Value"), )),
            "Reroute.001": ("NodeReroute", (-110.64, -290.03), None, (("Input", "Group Input", "Virtual Point Count"), )),
            "Switch": ("GeometryNodeSwitch", (239.32, -189.81), None, (("False", "Evaluate at Index", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Math", "Value"), )),
            "Switch.001": ("GeometryNodeSwitch", (1522.94, -96.26), None, (("False", "Switch", "Output"), ("Switch", "Compare.001", "Result"), ("True", "Math.002", "Value"), )),
        }