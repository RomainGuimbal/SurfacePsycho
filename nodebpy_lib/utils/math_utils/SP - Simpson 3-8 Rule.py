from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSimpson38Rule(CustomGeometryGroup):
    _name = "SP - Simpson 3-8 Rule"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 180, "node_tool_idname": "geometry.sp_simpson_s_3_8_rule", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        function = tree.inputs.float("Function", 0.0)
        interval_count = tree.inputs.integer("Interval Count", 0)
        sample_spacing = tree.inputs.float("Sample spacing", 0.5, min_value=-10_000.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        integral = tree.outputs.float("Integral")

        integer_math = g.Index().o.index * 3
        math_1 = function.point.at(integer_math).props(label="y0") + 3.0 * function.point.at(integer_math + 1).props(label="y1")
        math_2 = 3.0 * function.point.at(integer_math + 2).props(label="y2") + function.point.at(integer_math + 3).props(label="y3")
        (
            (g.Index() >= interval_count).switch.float((math_1 + math_2) * (sample_spacing / 8.0)).point.total()
            >> integral
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (1188.12, 72.4), None, (("Value", "Switch", "Output"), )),
            "Compare": ("FunctionNodeCompare", (715.91, 191.76), None, (("A", "Index.001", "Index"), ("B", "Group Input", "Interval Count"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (-180.32, 6.28), None, (("Index", "Integer Math", "Value"), ("Value", "Group Input", "Function"), )),
            "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (-180.32, -121.91), None, (("Index", "Integer Math.001", "Value"), ("Value", "Group Input", "Function"), )),
            "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (-180.32, -249.58), None, (("Index", "Integer Math.002", "Value"), ("Value", "Group Input", "Function"), )),
            "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (-180.32, -377.25), None, (("Index", "Integer Math.003", "Value"), ("Value", "Group Input", "Function"), )),
            "Group Input": ("NodeGroupInput", (-577.15, 30.05), None, ()),
            "Group Output": ("NodeGroupOutput", (1381.07, 7.26), None, (("Integral", "Accumulate Field", "Total"), )),
            "Index": ("GeometryNodeInputIndex", (-760.17, -167.02), None, ()),
            "Index.001": ("GeometryNodeInputIndex", (383.62, 133.24), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (-599.83, -127.02), None, (("Value", "Index", "Index"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-392.83, -167.72), None, (("Value", "Integer Math", "Value"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-397.16, -305.18), None, (("Value", "Integer Math", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-401.49, -440.48), None, (("Value", "Integer Math", "Value"), )),
            "Math": ("ShaderNodeMath", (713.56, -190.37), None, (("Value", "Math.006", "Value"), ("Value#1", "Math.007", "Value"), )),
            "Math.002": ("ShaderNodeMath", (198.3, -6.81), None, (("Value", "Evaluate at Index", "Value"), ("Value#1", "Math.003", "Value"), )),
            "Math.003": ("ShaderNodeMath", (-7.31, -103.33), None, (("Value#1", "Evaluate at Index.001", "Value"), )),
            "Math.004": ("ShaderNodeMath", (-7.31, -264.52), None, (("Value#1", "Evaluate at Index.002", "Value"), )),
            "Math.005": ("ShaderNodeMath", (174.27, -306.18), None, (("Value", "Math.004", "Value"), ("Value#1", "Evaluate at Index.003", "Value"), )),
            "Math.006": ("ShaderNodeMath", (514.59, -137.87), None, (("Value", "Math.002", "Value"), ("Value#1", "Math.005", "Value"), )),
            "Math.007": ("ShaderNodeMath", (521.24, -331.79), None, (("Value", "Group Input", "Sample spacing"), )),
            "Switch": ("GeometryNodeSwitch", (988.6, 139.39), None, (("False", "Math", "Value"), ("Switch", "Compare", "Result"), )),
        }