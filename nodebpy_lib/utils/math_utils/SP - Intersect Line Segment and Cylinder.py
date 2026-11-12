from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPIntersectLineSegmentAndCylinder(CustomGeometryGroup):
    _name = "SP - Intersect Line Segment and Cylinder"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_intersect_line_segment_and_cylinder", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        edge_vertex_1 = tree.inputs.vector("Edge vertex 1", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        edge_vertex_2 = tree.inputs.vector("Edge vertex 2", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        with tree.inputs.panel("Cylinder"):
            radius = tree.inputs.float("Radius", 0.0)
            height = tree.inputs.float("Height", 0.0)
            axis = tree.inputs.vector("Axis", (0.0, 0.0, 0.0), hide_value=True)
            origin = tree.inputs.vector("Origin", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        intersect_sol1 = tree.outputs.vector("Intersect Sol1")
        intersect_sol2 = tree.outputs.vector("Intersect Sol2")
        intersects_sol1 = tree.outputs.boolean("Intersects Sol1")
        intersects_sol2 = tree.outputs.boolean("Intersects Sol2")
        z_sol_1 = tree.outputs.float("Z Sol 1")
        z_sol_2 = tree.outputs.float("Z Sol 2")

        reroute = g.Reroute(input=axis).props(width=19.0)
        reroute_1 = g.Reroute(input=origin).props(width=19.0)
        reroute_2 = g.Reroute(input=g.Reroute(input=reroute.o.output).props(width=19.0).o.output).props(width=19.0)
        reroute_3 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
        reroute_4 = g.Reroute(input=g.Reroute(input=reroute_1.o.output).props(width=19.0).o.output).props(width=19.0)
        with g.Frame("Line info"):
            reroute_5 = g.Reroute(input=edge_vertex_2).props(label="o", width=19.0)
            vector_math = edge_vertex_1 - edge_vertex_2
            reroute_6 = g.Reroute(input=vector_math.normalize()).props(label="n", width=19.0)
        with g.Frame("Cylinder Info"):
            reroute_7 = g.Reroute(input=radius).props(label="Radius", width=19.0)
            reroute_8 = g.Reroute(input=height).props(label="Height", width=19.0)
            reroute_9 = g.Reroute(input=reroute.o.output).props(label="a", width=19.0)
            reroute_10 = g.Reroute(input=reroute_1.o.output - reroute_5).props(label="b", width=19.0)
        reroute_11 = g.Reroute(input=reroute_7.o.output).props(width=19.0)
        reroute_12 = g.Reroute(input=reroute_5.o.output).props(width=19.0)
        reroute_13 = g.Reroute(input=reroute_6.o.output).props(width=19.0)
        vector_math_1 = reroute_6.o.output.cross(reroute_9).props(label="n ^ a")
        vector_math_2 = vector_math_1.dot(reroute_10.o.output.cross(reroute_9).props(label="b^a"))
        vector_math_3 = vector_math_1.dot(vector_math_1)
        reroute_14 = g.Reroute(input=vector_math_3).props(width=19.0)
        vector_math_4 = reroute_10.o.output.dot(vector_math_1).props(label="b . (n^a)")
        math_1 = vector_math_3 * (reroute_11.o.output * reroute_11).props(label="r**2") - vector_math_4 * vector_math_4
        math_2 = math_1.sqrt()
        reroute_15 = g.Reroute(input=math_1).props(width=19.0)
        reroute_16 = g.Reroute(input=(vector_math_2 + math_2) / reroute_14).props(label="t Sol 2", width=19.0)
        reroute_17 = g.Reroute(input=(vector_math_2 - math_2) / reroute_14).props(label="t Sol 1", width=19.0)
        reroute_18 = g.Reroute(input=reroute_17.o.output).props(width=19.0)
        reroute_19 = g.Reroute(input=reroute_13.o.output * reroute_17 + reroute_12).props(label="Sol 1", width=19.0)
        vector_math_5 = (reroute_19.o.output - reroute_4).dot(reroute_3)
        reroute_20 = g.Reroute(input=reroute_13.o.output * reroute_16 + reroute_12).props(label="Sol 2", width=19.0)
        vector_math_6 = (reroute_20.o.output - reroute_4).dot(reroute_3)
        with g.Frame("Intersect cond"):
            reroute_21 = g.Reroute(input=reroute_8.o.output).props(width=19.0)
            vector_math_7 = vector_math.length()
            reroute_22 = g.Reroute(input=reroute_15 >= 0.0).props(width=19.0)
            reroute_23 = g.Reroute(input=reroute_16.o.output).props(width=19.0)
            reroute_24 = g.Reroute(input=vector_math_5).props(width=19.0)
            (
                (reroute_22.o.output & ((reroute_18 <= vector_math_7) & (reroute_18 >= 0.0)) & ((reroute_24 <= reroute_21) & (reroute_24 >= 0.0)))
                >> intersects_sol1
            )
            reroute_25 = g.Reroute(input=vector_math_6).props(width=19.0)
            (
                (reroute_22.o.output & ((reroute_23 <= vector_math_7) & (reroute_23 >= 0.0)) & ((reroute_25 <= reroute_21) & (reroute_25 >= 0.0)))
                >> intersects_sol2
            )

        reroute_19 >> intersect_sol1
        reroute_20 >> intersect_sol2
        vector_math_5 >> z_sol_1
        vector_math_6 >> z_sol_2

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (505.89, -81.46), "Frame", (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Compare.008", "Result"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (529.82, -423.41), "Frame", (("Boolean", "Compare.006", "Result"), ("Boolean#1", "Compare.009", "Result"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (1262.4, -472.2), "Frame", (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Compare.004", "Result"), )),
            "Boolean Math.003": ("FunctionNodeBooleanMath", (1258.08, -810.01), "Frame", (("Boolean", "Compare.003", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (1564.63, -350.8), "Frame", (("Boolean", "Reroute.003", "Output"), ("Boolean#1", "Boolean Math", "Boolean"), )),
            "Boolean Math.005": ("FunctionNodeBooleanMath", (1746.45, -390.39), "Frame", (("Boolean", "Boolean Math.004", "Boolean"), ("Boolean#1", "Boolean Math.002", "Boolean"), )),
            "Boolean Math.006": ("FunctionNodeBooleanMath", (1728.46, -712.47), "Frame", (("Boolean", "Boolean Math.007", "Boolean"), ("Boolean#1", "Boolean Math.003", "Boolean"), )),
            "Boolean Math.007": ("FunctionNodeBooleanMath", (1555.42, -640.41), "Frame", (("Boolean", "Reroute.003", "Output"), ("Boolean#1", "Boolean Math.001", "Boolean"), )),
            "Compare": ("FunctionNodeCompare", (580.89, -769.59), "Frame", (("A", "Reroute.010", "Output"), )),
            "Compare.001": ("FunctionNodeCompare", (311.77, -36.21), "Frame", (("A", "Reroute.002", "Output"), ("B", "Vector Math.015", "Value"), )),
            "Compare.002": ("FunctionNodeCompare", (1078.02, -403.9), "Frame", (("A", "Reroute.034", "Output"), ("B", "Reroute.031", "Output"), )),
            "Compare.003": ("FunctionNodeCompare", (1073.7, -741.72), "Frame", (("A", "Reroute.035", "Output"), ("B", "Reroute.031", "Output"), )),
            "Compare.004": ("FunctionNodeCompare", (1071.06, -571.61), "Frame", (("A", "Reroute.034", "Output"), )),
            "Compare.005": ("FunctionNodeCompare", (1066.74, -909.43), "Frame", (("A", "Reroute.035", "Output"), )),
            "Compare.006": ("FunctionNodeCompare", (335.7, -378.15), "Frame", (("A", "Reroute.001", "Output"), ("B", "Vector Math.015", "Value"), )),
            "Compare.008": ("FunctionNodeCompare", (316.26, -197.39), "Frame", (("A", "Reroute.002", "Output"), )),
            "Compare.009": ("FunctionNodeCompare", (340.19, -539.33), "Frame", (("A", "Reroute.001", "Output"), )),
            "Frame": ("NodeFrame", (562.76, 1823.86), None, ()),
            "Frame.001": ("NodeFrame", (-2175.35, 653.86), None, ()),
            "Frame.002": ("NodeFrame", (-1937.12, 96.77), None, ()),
            "Group Input": ("NodeGroupInput", (-2416.53, 116.06), None, ()),
            "Group Output": ("NodeGroupOutput", (2698.31, 613.69), None, (("Intersect Sol1", "Reroute.033", "Output"), ("Intersect Sol2", "Reroute.032", "Output"), ("Intersects Sol1", "Boolean Math.005", "Boolean"), ("Intersects Sol2", "Boolean Math.006", "Boolean"), ("Z Sol 1", "Vector Math", "Value"), ("Z Sol 2", "Vector Math.001", "Value"), )),
            "Math.007": ("ShaderNodeMath", (-220.44, 207.64), None, (("Value", "Vector Math.013", "Value"), ("Value#1", "Math.013", "Value"), )),
            "Math.008": ("ShaderNodeMath", (-65.79, 400.72), None, (("Value", "Math.009", "Value"), ("Value#1", "Reroute.011", "Output"), )),
            "Math.009": ("ShaderNodeMath", (-232.68, 403.76), None, (("Value", "Vector Math.013", "Value"), ("Value#1", "Math.013", "Value"), )),
            "Math.010": ("ShaderNodeMath", (-754.39, -12.86), None, (("Value", "Vector Math.016", "Value"), ("Value#1", "Math.011", "Value"), )),
            "Math.011": ("ShaderNodeMath", (-946.19, -51.6), None, (("Value", "Reroute.023", "Output"), ("Value#1", "Reroute.023", "Output"), )),
            "Math.012": ("ShaderNodeMath", (-569.07, -63.92), None, (("Value", "Math.010", "Value"), ("Value#1", "Math.016", "Value"), )),
            "Math.013": ("ShaderNodeMath", (-450.0, 237.12), None, (("Value", "Math.012", "Value"), )),
            "Math.014": ("ShaderNodeMath", (-44.67, 209.8), None, (("Value", "Math.007", "Value"), ("Value#1", "Reroute.011", "Output"), )),
            "Math.016": ("ShaderNodeMath", (-763.19, -197.7), None, (("Value", "Vector Math.017", "Value"), ("Value#1", "Vector Math.017", "Value"), )),
            "Reroute": ("NodeReroute", (1173.84, 129.59), None, (("Input", "Reroute.008", "Output"), )),
            "Reroute.001": ("NodeReroute", (302.92, -637.06), "Frame", (("Input", "Reroute.024", "Output"), )),
            "Reroute.002": ("NodeReroute", (846.17, 1565.48), None, (("Input", "Reroute.028", "Output"), )),
            "Reroute.003": ("NodeReroute", (1468.58, -661.68), "Frame", (("Input", "Compare", "Result"), )),
            "Reroute.004": ("NodeReroute", (636.37, -396.28), None, (("Input", "Reroute.006", "Output"), )),
            "Reroute.005": ("NodeReroute", (639.98, -427.93), None, (("Input", "Reroute.007", "Output"), )),
            "Reroute.006": ("NodeReroute", (-2107.61, -345.57), None, (("Input", "Group Input", "Axis"), )),
            "Reroute.007": ("NodeReroute", (-2115.76, -374.68), None, (("Input", "Group Input", "Origin"), )),
            "Reroute.008": ("NodeReroute", (908.1, 116.23), None, (("Input", "Reroute.004", "Output"), )),
            "Reroute.009": ("NodeReroute", (951.58, 167.61), None, (("Input", "Reroute.005", "Output"), )),
            "Reroute.010": ("NodeReroute", (581.93, -132.12), None, (("Input", "Math.012", "Value"), )),
            "Reroute.011": ("NodeReroute", (-64.73, 38.96), None, (("Input", "Vector Math.016", "Value"), )),
            "Reroute.013": ("NodeReroute", (396.59, -84.7), "Frame.001", (("Input", "Vector Math.006", "Vector"), )),
            "Reroute.015": ("NodeReroute", (53.75, -187.62), "Frame.001", (("Input", "Group Input", "Edge vertex 2"), )),
            "Reroute.017": ("NodeReroute", (217.99, -41.06), "Frame.002", (("Input", "Group Input", "Radius"), )),
            "Reroute.018": ("NodeReroute", (214.2, -74.59), "Frame.002", (("Input", "Group Input", "Height"), )),
            "Reroute.019": ("NodeReroute", (220.68, -123.06), "Frame.002", (("Input", "Reroute.006", "Output"), )),
            "Reroute.022": ("NodeReroute", (216.89, -251.1), "Frame.002", (("Input", "Vector Math.007", "Vector"), )),
            "Reroute.023": ("NodeReroute", (-1005.24, -156.81), None, (("Input", "Reroute.017", "Output"), )),
            "Reroute.024": ("NodeReroute", (228.33, 172.73), None, (("Input", "Math.014", "Value"), )),
            "Reroute.025": ("NodeReroute", (92.16, 605.64), None, (("Input", "Reroute.013", "Output"), )),
            "Reroute.026": ("NodeReroute", (61.14, 508.17), None, (("Input", "Reroute.015", "Output"), )),
            "Reroute.028": ("NodeReroute", (227.96, 365.76), None, (("Input", "Math.008", "Value"), )),
            "Reroute.031": ("NodeReroute", (874.84, -624.65), "Frame", (("Input", "Reroute.018", "Output"), )),
            "Reroute.032": ("NodeReroute", (832.26, 406.84), None, (("Input", "Vector Math.021", "Vector"), )),
            "Reroute.033": ("NodeReroute", (836.42, 543.38), None, (("Input", "Vector Math.019", "Vector"), )),
            "Reroute.034": ("NodeReroute", (1044.12, -588.53), "Frame", (("Input", "Vector Math", "Value"), )),
            "Reroute.035": ("NodeReroute", (1039.81, -926.35), "Frame", (("Input", "Vector Math.001", "Value"), )),
            "Vector Math": ("ShaderNodeVectorMath", (1194.35, 431.71), None, (("Vector", "Vector Math.002", "Vector"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (1206.04, 286.55), None, (("Vector", "Vector Math.003", "Vector"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (1022.41, 436.16), None, (("Vector", "Reroute.033", "Output"), ("Vector#1", "Reroute.009", "Output"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (1018.77, 281.48), None, (("Vector", "Reroute.032", "Output"), ("Vector#1", "Reroute.009", "Output"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (30.01, -36.07), "Frame.001", (("Vector", "Group Input", "Edge vertex 1"), ("Vector#1", "Group Input", "Edge vertex 2"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (190.34, -49.99), "Frame.001", (("Vector", "Vector Math.004", "Vector"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (30.11, -219.48), "Frame.002", (("Vector", "Reroute.007", "Output"), ("Vector#1", "Reroute.015", "Output"), )),
            "Vector Math.008": ("ShaderNodeVectorMath", (-1156.4, 283.51), None, (("Vector", "Reroute.013", "Output"), ("Vector#1", "Reroute.019", "Output"), )),
            "Vector Math.013": ("ShaderNodeVectorMath", (-938.3, 291.8), None, (("Vector", "Vector Math.008", "Vector"), ("Vector#1", "Vector Math.014", "Vector"), )),
            "Vector Math.014": ("ShaderNodeVectorMath", (-1151.94, 140.61), None, (("Vector", "Reroute.022", "Output"), ("Vector#1", "Reroute.019", "Output"), )),
            "Vector Math.015": ("ShaderNodeVectorMath", (30.34, -221.33), "Frame", (("Vector", "Vector Math.004", "Vector"), )),
            "Vector Math.016": ("ShaderNodeVectorMath", (-941.99, 84.81), None, (("Vector", "Vector Math.008", "Vector"), ("Vector#1", "Vector Math.008", "Vector"), )),
            "Vector Math.017": ("ShaderNodeVectorMath", (-943.45, -230.08), None, (("Vector", "Reroute.022", "Output"), ("Vector#1", "Vector Math.008", "Vector"), )),
            "Vector Math.018": ("ShaderNodeVectorMath", (476.04, 582.97), None, (("Scale", "Reroute.028", "Output"), ("Vector", "Reroute.025", "Output"), )),
            "Vector Math.019": ("ShaderNodeVectorMath", (649.78, 584.27), None, (("Vector", "Vector Math.018", "Vector"), ("Vector#1", "Reroute.026", "Output"), )),
            "Vector Math.020": ("ShaderNodeVectorMath", (472.95, 446.61), None, (("Scale", "Reroute.024", "Output"), ("Vector", "Reroute.025", "Output"), )),
            "Vector Math.021": ("ShaderNodeVectorMath", (648.03, 448.58), None, (("Vector", "Vector Math.020", "Vector"), ("Vector#1", "Reroute.026", "Output"), )),
        }