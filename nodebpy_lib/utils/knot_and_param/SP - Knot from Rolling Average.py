from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPKnotFromRollingAverage(CustomGeometryGroup):
    _name = "SP - Knot from Rolling Average"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 247, "node_tool_idname": "geometry.sp_knot_from_rolling_average", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        t_k = tree.inputs.float("t_k", 0.0, hide_value=True)
        p_count = tree.inputs.integer("P Count", 0)
        degree = tree.inputs.integer("Degree", 0)
        unique_knot = tree.outputs.float("Unique Knot")

        reroute = g.Reroute(input=degree).props(width=19.0)
        reroute_1 = g.Reroute(input=reroute.o.output).props(width=19.0)
        reroute_2 = g.Reroute(input=p_count).props(width=19.0)
        with g.Frame("Internal knots (rolling average)"):
            index = g.Index()
            reroute_3 = g.Reroute(input=reroute.o.output).props(width=19.0)
            reroute_4 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
            integer_math = ((index.o.index // reroute_4).props(hide=True) + 1).props(hide=True)
            reroute_5 = g.Reroute(input=reroute_4.o.output).props(width=19.0)
            reroute_6 = g.Reroute(input=reroute_4.o.output).props(width=19.0)
            integer_math_1 = ((integer_math * (reroute_6.o.output - 1).props(hide=True)).props(hide=True) - reroute_6).props(hide=True)
            evaluate_at_index = t_k.point.at((index.o.index - integer_math_1).props(hide=True))
            reroute_7 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
            integer_math_2 = (g.Reroute(input=reroute_7.o.output).props(width=19.0).o.output * ((reroute_2.o.output - reroute_7).props(hide=True) - 1).props(hide=True)).props(hide=True)
            points = g.Points(count=integer_math_2, radius=0.0).props(hide=True)
            sample_index = g.SampleIndex.point.float(points, evaluate_at_index.point.total(integer_math), (reroute_5.o.output * g.Index()).props(hide=True))
            math_1 = sample_index.o.value / reroute_5
        reroute_8 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
        with g.Frame():
            index_1 = g.Index()
            (
                (index_1 >= reroute_8.o.output - reroute_1).switch.float(math_1.point.at(index_1.o.index - 1), 1.0)
                >> unique_knot
            )
        viewer = g.Viewer()
        viewer.items.geometry(points, "Points")
        viewer.items.float(evaluate_at_index, "Value")

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (1390.2, -162.94), "Frame.001", (("Group ID", "Integer Math.005", "Value"), ("Value", "Evaluate at Index", "Value"), )),
            "Compare.003": ("FunctionNodeCompare", (453.3, -185.32), "Frame", (("A", "Index.002", "Index"), ("B", "Integer Math.011", "Value"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (1221.28, -171.75), "Frame.001", (("Index", "Integer Math.007", "Value"), ("Value", "Group Input", "t_k"), )),
            "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (390.01, -30.33), "Frame", (("Index", "Integer Math.003", "Value"), ("Value", "Math.001", "Value"), )),
            "Frame": ("NodeFrame", (608.82, 92.12), None, ()),
            "Frame.001": ("NodeFrame", (-1463.29, 56.15), None, ()),
            "Group Input": ("NodeGroupInput", (-1654.92, 171.82), None, ()),
            "Group Output": ("NodeGroupOutput", (1681.26, -11.49), None, (("Unique Knot", "Switch.005", "Output"), )),
            "Index": ("GeometryNodeInputIndex", (30.39, -351.0), "Frame.001", ()),
            "Index.001": ("GeometryNodeInputIndex", (1203.55, -406.87), "Frame.001", ()),
            "Index.002": ("GeometryNodeInputIndex", (30.31, -144.41), "Frame", ()),
            "Integer Math.001": ("FunctionNodeIntegerMath", (309.41, -323.37), "Frame.001", (("Value", "Index", "Index"), ("Value#1", "Reroute.015", "Output"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (210.14, -58.29), "Frame", (("Value", "Index.002", "Index"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (507.42, -414.48), "Frame.001", (("Value", "Reroute.018", "Output"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (476.21, -325.95), "Frame.001", (("Value", "Integer Math.001", "Value"), )),
            "Integer Math.006": ("FunctionNodeIntegerMath", (1222.19, -122.74), "Frame.001", (("Value", "Reroute.020", "Output"), ("Value#1", "Integer Math.014", "Value"), )),
            "Integer Math.007": ("FunctionNodeIntegerMath", (1036.31, -387.25), "Frame.001", (("Value", "Index", "Index"), ("Value#1", "Integer Math.009", "Value"), )),
            "Integer Math.008": ("FunctionNodeIntegerMath", (693.39, -410.62), "Frame.001", (("Value", "Integer Math.005", "Value"), ("Value#1", "Integer Math.004", "Value"), )),
            "Integer Math.009": ("FunctionNodeIntegerMath", (875.41, -432.59), "Frame.001", (("Value", "Integer Math.008", "Value"), ("Value#1", "Reroute.018", "Output"), )),
            "Integer Math.010": ("FunctionNodeIntegerMath", (1376.87, -400.0), "Frame.001", (("Value", "Reroute.013", "Output"), ("Value#1", "Index.001", "Index"), )),
            "Integer Math.011": ("FunctionNodeIntegerMath", (252.05, -251.02), "Frame", (("Value", "Reroute.033", "Output"), ("Value#1", "Reroute.028", "Output"), )),
            "Integer Math.013": ("FunctionNodeIntegerMath", (883.03, -145.41), "Frame.001", (("Value", "Reroute.032", "Output"), ("Value#1", "Reroute.029", "Output"), )),
            "Integer Math.014": ("FunctionNodeIntegerMath", (1055.07, -152.95), "Frame.001", (("Value", "Integer Math.013", "Value"), )),
            "Math.001": ("ShaderNodeMath", (1787.14, -233.06), "Frame.001", (("Value", "Sample Index", "Value"), ("Value#1", "Reroute.013", "Output"), )),
            "Points": ("GeometryNodePoints", (1385.4, -121.05), "Frame.001", (("Count", "Integer Math.006", "Value"), )),
            "Reroute.009": ("NodeReroute", (234.74, -156.91), "Frame.001", (("Input", "Reroute.014", "Output"), )),
            "Reroute.013": ("NodeReroute", (1345.78, -367.01), "Frame.001", (("Input", "Reroute.015", "Output"), )),
            "Reroute.014": ("NodeReroute", (-1290.7, 89.2), None, (("Input", "Group Input", "Degree"), )),
            "Reroute.015": ("NodeReroute", (229.65, -372.67), "Frame.001", (("Input", "Reroute.009", "Output"), )),
            "Reroute.018": ("NodeReroute", (373.2, -453.25), "Frame.001", (("Input", "Reroute.015", "Output"), )),
            "Reroute.020": ("NodeReroute", (896.24, -120.79), "Frame.001", (("Input", "Reroute.029", "Output"), )),
            "Reroute.028": ("NodeReroute", (498.36, 102.17), None, (("Input", "Reroute.014", "Output"), )),
            "Reroute.029": ("NodeReroute", (831.23, -162.54), "Frame.001", (("Input", "Reroute.009", "Output"), )),
            "Reroute.032": ("NodeReroute", (-709.66, 114.79), None, (("Input", "Group Input", "P Count"), )),
            "Reroute.033": ("NodeReroute", (499.48, 131.62), None, (("Input", "Reroute.032", "Output"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (1589.43, -35.81), "Frame.001", (("Geometry", "Points", "Points"), ("Index", "Integer Math.010", "Value"), ("Value", "Accumulate Field", "Total"), )),
            "Switch.005": ("GeometryNodeSwitch", (770.66, -80.61), "Frame", (("False", "Evaluate at Index.002", "Value"), ("Switch", "Compare.003", "Result"), )),
            "Viewer": ("GeometryNodeViewer", (287.18, 145.06), None, (("Points", "Points", "Points"), ("Value", "Evaluate at Index", "Value"), )),
        }