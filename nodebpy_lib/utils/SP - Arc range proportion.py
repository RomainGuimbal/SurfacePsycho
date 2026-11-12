from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPArcRangeProportion(CustomGeometryGroup):
    _name = "SP - Arc range proportion"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_arc_range_proportion", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        end_1 = tree.inputs.float("End 1", 0.5, min_value=-10_000.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        end_2 = tree.inputs.float("End 2", 0.5, min_value=-10_000.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        start_angle = tree.inputs.float("Start Angle", 0.5, min_value=-10_000.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        range = tree.inputs.float("Range", 0.5, min_value=-10_000.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        parameter_pseudo_angle = tree.outputs.float("Parameter (pseudo angle)")

        reroute = g.Reroute(input=range).props(width=19.0)
        reroute_1 = g.Reroute(input=start_angle).props(width=19.0)
        math_1 = end_2.mul_add(reroute, reroute_1)
        math_2 = (1.0 - end_1).props(hide=True).mul_add(reroute, reroute_1)
        (
            g.IndexSwitch.float(g.Index(), (math_2, g.Mix.float(0.5, math_2, math_1, clamp_factor=False).props(hide=True).o.result_float, math_1))
            >> parameter_pseudo_angle
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-536.5, -52.35), None, ()),
            "Group Output": ("NodeGroupOutput", (707.79, 0.0), None, (("Parameter (pseudo angle)", "Index Switch.002", "Output"), )),
            "Index Switch.002": ("GeometryNodeIndexSwitch", (517.79, -7.74), None, (("0", "Math.006", "Value"), ("1", "Mix.002", "Result"), ("2", "Math.005", "Value"), ("Index", "Index.002", "Index"), )),
            "Index.002": ("GeometryNodeInputIndex", (260.76, 83.35), None, ()),
            "Math.003": ("ShaderNodeMath", (-219.16, -12.44), None, (("Value#1", "Group Input", "End 1"), )),
            "Math.005": ("ShaderNodeMath", (-54.45, -118.22), None, (("Value", "Group Input", "End 2"), ("Value#1", "Reroute.004", "Output"), ("Value#2", "Reroute.005", "Output"), )),
            "Math.006": ("ShaderNodeMath", (-49.0, 68.15), None, (("Value", "Math.003", "Value"), ("Value#1", "Reroute.004", "Output"), ("Value#2", "Reroute.005", "Output"), )),
            "Mix.002": ("ShaderNodeMix", (188.25, -99.83), None, (("A", "Math.006", "Value"), ("B", "Math.005", "Value"), )),
            "Reroute.004": ("NodeReroute", (-229.49, -220.96), None, (("Input", "Group Input", "Range"), )),
            "Reroute.005": ("NodeReroute", (-189.02, -210.13), None, (("Input", "Group Input", "Start Angle"), )),
        }