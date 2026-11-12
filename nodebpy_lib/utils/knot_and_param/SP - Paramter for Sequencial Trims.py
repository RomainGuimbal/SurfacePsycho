from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPParamterForSequencialTrims(CustomGeometryGroup):
    _name = "SP - Paramter for Sequencial Trims"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 260, "node_tool_idname": "geometry.sp_paramter_for_sequencial_chain_trims", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        end_1 = tree.inputs.float("End 1", 0.0, subtype="FACTOR")
        end_2 = tree.inputs.float("End 2", 0.0, subtype="FACTOR")
        factor_1 = tree.outputs.float("Factor 1")
        factor_2 = tree.outputs.float("Factor 2")
        boolean = tree.outputs.boolean("Boolean")
        null_curve = tree.outputs.boolean("Null Curve")

        with g.Frame():
            reroute = g.Reroute(input=end_2).props(width=19.0)
            math_1 = (1.0 - reroute).props(label="invert")
            reroute_1 = g.Reroute(input=end_1).props(width=19.0)
            with g.Frame("Avoid 0 division"):
                reroute_2 = g.Reroute(input=math_1).props(width=19.0)
                reroute_3 = g.Reroute(input=reroute_1.o.output).props(width=19.0)
                compare = (abs(reroute_3.o.output - 1.0).props(hide=True) < abs(reroute_2.o.output - 1.0).props(hide=True)).props(width=100.0, hide=True)
                reroute_4 = g.Reroute(input=((reroute_1 <= reroute.o.output + 1.0) & compare).props(width=100.0, hide=True)).props(width=19.0)
                reroute_5 = g.Reroute(input=reroute_4.o.output).props(width=19.0)
                switch = reroute_5.o.output.switch.float(reroute_2, reroute_3)
                switch_1 = reroute_5.o.output.switch.float(reroute_3, reroute_2)
            with g.Frame("b-a / 1-a"):
                reroute_6 = g.Reroute(input=switch_1).props(label="a", width=19.0)
                (
                    (g.Reroute(input=switch).props(label="b", width=19.0).o.output - reroute_6) / (1.0 - reroute_6)
                    >> factor_2
                )
        g.Compare.float.equal(math_1, reroute_1, 0.0) >> null_curve
        viewer = g.Viewer()
        viewer.items.float(reroute_2, "Value")

        switch_1 >> factor_1
        reroute_5 >> boolean

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (614.86, -264.88), "Frame.001", (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.001", "Result"), )),
            "Compare.001": ("FunctionNodeCompare", (492.38, -284.56), "Frame.001", (("A", "Math.005", "Value"), ("B", "Math.006", "Value"), )),
            "Compare.002": ("FunctionNodeCompare", (265.35, -613.36), None, (("A", "Math.001", "Value"), ("B", "Reroute.007", "Output"), )),
            "Compare.004": ("FunctionNodeCompare", (296.05, -44.43), "Frame.001", (("A", "Reroute.007", "Output"), ("B", "Math.007", "Value"), )),
            "Frame": ("NodeFrame", (1033.9, -387.0), "Frame.004", ()),
            "Frame.001": ("NodeFrame", (249.21, -30.18), "Frame.004", ()),
            "Frame.004": ("NodeFrame", (-686.8, 310.27), None, ()),
            "Group Input": ("NodeGroupInput", (-886.76, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (1304.91, -5.25), None, (("Boolean", "Reroute.002", "Output"), ("Factor 1", "Switch.002", "Output"), ("Factor 2", "Math.008", "Value"), ("Null Curve", "Compare.002", "Result"), )),
            "Math.001": ("ShaderNodeMath", (68.02, -597.94), "Frame.004", (("Value#1", "Reroute.005", "Output"), )),
            "Math.003": ("ShaderNodeMath", (136.88, -202.17), "Frame.001", (("Value", "Reroute", "Output"), )),
            "Math.004": ("ShaderNodeMath", (136.88, -368.3), "Frame.001", (("Value", "Reroute.001", "Output"), )),
            "Math.005": ("ShaderNodeMath", (302.58, -259.85), "Frame.001", (("Value", "Math.003", "Value"), )),
            "Math.006": ("ShaderNodeMath", (306.46, -311.55), "Frame.001", (("Value", "Math.004", "Value"), )),
            "Math.007": ("ShaderNodeMath", (136.88, -36.05), "Frame.001", (("Value", "Reroute.005", "Output"), )),
            "Math.008": ("ShaderNodeMath", (339.65, -117.8), "Frame", (("Value", "Math.010", "Value"), ("Value#1", "Math.009", "Value"), )),
            "Math.009": ("ShaderNodeMath", (139.98, -211.61), "Frame", (("Value#1", "Reroute.003", "Output"), )),
            "Math.010": ("ShaderNodeMath", (137.93, -36.16), "Frame", (("Value", "Reroute.004", "Output"), ("Value#1", "Reroute.003", "Output"), )),
            "Reroute": ("NodeReroute", (35.21, -535.76), "Frame.001", (("Input", "Reroute.007", "Output"), )),
            "Reroute.001": ("NodeReroute", (38.64, -564.5), "Frame.001", (("Input", "Math.001", "Value"), )),
            "Reroute.002": ("NodeReroute", (529.61, -590.18), "Frame.001", (("Input", "Reroute.006", "Output"), )),
            "Reroute.003": ("NodeReroute", (35.21, -143.21), "Frame", (("Input", "Switch.002", "Output"), )),
            "Reroute.004": ("NodeReroute", (38.66, -202.43), "Frame", (("Input", "Switch.001", "Output"), )),
            "Reroute.005": ("NodeReroute", (35.21, -522.06), "Frame.004", (("Input", "Group Input", "End 2"), )),
            "Reroute.006": ("NodeReroute", (546.22, -387.08), "Frame.001", (("Input", "Boolean Math", "Boolean"), )),
            "Reroute.007": ("NodeReroute", (39.41, -477.96), "Frame.004", (("Input", "Group Input", "End 1"), )),
            "Switch.001": ("GeometryNodeSwitch", (577.35, -575.9), "Frame.001", (("False", "Reroute.001", "Output"), ("Switch", "Reroute.002", "Output"), ("True", "Reroute", "Output"), )),
            "Switch.002": ("GeometryNodeSwitch", (584.65, -416.19), "Frame.001", (("False", "Reroute", "Output"), ("Switch", "Reroute.002", "Output"), ("True", "Reroute.001", "Output"), )),
            "Viewer": ("GeometryNodeViewer", (648.24, -83.24), None, (("Value", "Reroute.001", "Output"), )),
        }