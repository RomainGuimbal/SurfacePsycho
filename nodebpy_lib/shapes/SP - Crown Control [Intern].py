from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Crown Control [Intern]", arrange=None, clear=True) as tree:
    end_1 = tree.inputs.vector("End 1", (0.0, 0.0, 0.0), hide_value=True)
    end_2 = tree.inputs.vector("End 2", (0.0, 0.0, 0.0), hide_value=True)
    normal = tree.inputs.vector("Normal", (0.0, 0.0, 0.0), hide_value=True)
    ratio = tree.inputs.float("Ratio", 0.1, min_value=0.0, max_value=1.0, subtype="FACTOR")
    bias = tree.inputs.float("Bias", 0.0, min_value=-1.0, max_value=1.0, subtype="FACTOR")
    spread = tree.inputs.float("Spread", 0.0, min_value=0.0, max_value=1.0)
    point_count = tree.outputs.integer("Point Count")
    position = tree.outputs.vector("Position")

    with g.Frame("No spread : Degree 2"):
        compare = g.Compare.float.equal(spread, 0.0, 0.0).props(hide=True)
    with g.Frame("Factor between ends"):
        with g.Frame("Bias"):
            math_1 = bias / 2.0 + 0.5
        with g.Frame("Bias and spread"):
            reroute = g.Reroute(input=spread).props(width=19.0)
            reroute_1 = g.Reroute(input=bias).props(width=19.0)
            math_2 = (1.0 + reroute_1 - reroute) / 3.0
            math_3 = (2.0 + reroute_1 + reroute) / 3.0
        switch = compare.o.result.switch.float(math_2, math_1)
    reroute_2 = g.Reroute(input=spread).props(width=19.0)
    reroute_3 = g.Reroute(input=bias).props(width=19.0)
    reroute_4 = g.Reroute(input=ratio).props(width=19.0)
    with g.Frame("Points info"):
        reroute_5 = g.Reroute(input=g.Reroute(input=end_2).props(width=19.0).o.output).props(width=19.0)
        reroute_6 = g.Reroute(input=g.Reroute(input=end_1).props(width=19.0).o.output).props(width=19.0)
        reroute_7 = g.Reroute(input=reroute_6.o.output.distance(reroute_5).props(hide=True)).props(label="Length", width=19.0)
    with g.Frame():
        reroute_8 = g.Reroute(input=reroute_5.o.output).props(width=19.0)
        reroute_9 = g.Reroute(input=reroute_6.o.output).props(width=19.0)
        mix = g.Mix.vector(math_3, reroute_9, reroute_8, clamp_factor=False).props(hide=True)
        mix_1 = g.Mix.vector(switch, reroute_9, reroute_8, clamp_factor=False).props(hide=True)
    with g.Frame("Tangent"):
        vector_math = (reroute_5.o.output - reroute_6).props(hide=True)
        vector_math_1 = vector_math.normalize()
    with g.Frame("Normal"):
        reroute_10 = g.Reroute(input=normal).props(width=19.0)
        compare_1 = g.Compare(a=reroute_10, b=(0.0, 0.0, 0.0), operation="EQUAL", data_type="VECTOR", mode="ELEMENT").props(hide=True)
        vector_math_2 = vector_math_1.cross(reroute_10).props(hide=True)
        _warning = g.Warning.warning(compare_1, "Input segment doesn't define a plane").props(width=265.67)
    with g.Frame("No orientation or ratio 0"):
        boolean_math = (g.Compare.float.equal(ratio, 0.0, 0.0).props(hide=True).o.result | compare_1).props(hide=True)
    boolean_math_1 = (~boolean_math).props(hide=True)
    integer_math = g.IntegerMath(value=boolean_math_1, value_001=(boolean_math_1 & (~compare.o.result).props(hide=True)).props(hide=True)).props(hide=True)
    integer_math.o.value + 2 >> point_count
    reroute_11 = g.Reroute(input=reroute_7.o.output).props(width=19.0)
    with g.Frame("Max height point"):
        with g.Frame():
            mix_2 = g.Mix.vector((math_1 + 0.5) / 2.0, reroute_9, reroute_8, clamp_factor=False)
        math_4 = (reroute_4.o.output * reroute_11).props(hide=True)
        switch_1 = compare.o.result.switch.float((math_4 * 1.3333334).props(hide=True), (math_4 * 2.0).props(hide=True))
        vector_math_3 = (mix_2.o.result_vector + (vector_math_2 * math_4).props(hide=True)).props(hide=True)
    vector_math_4 = (vector_math_2 * switch_1).props(hide=True)
    with g.Frame("Gizmos"):
        reroute_12 = g.Reroute(input=vector_math).props(width=19.0, mute=True)
        reroute_13 = g.Reroute(input=vector_math_3).props(width=19.0)
        _linear_gizmo = g.LinearGizmo(value=((reroute_3.o.output * (reroute_11.o.output / 4.0).props(hide=True)).props(hide=True),), position=reroute_13, direction=reroute_12, color_id="X")
        _linear_gizmo_1 = g.LinearGizmo(value=(math_4,), position=reroute_13, direction=vector_math_4, color_id="Z")
        _linear_gizmo_2 = g.LinearGizmo(value=(reroute_2,), position=reroute_13, direction=((0.0, 0.0, 0.0) - reroute_12).props(width=100.0, hide=True), draw_style="BOX")
    reroute_14 = g.Reroute(input=vector_math_4).props(width=19.0)
    vector_math_5 = (mix_1.o.result_vector + reroute_14).props(hide=True)
    vector_math_6 = (mix.o.result_vector + reroute_14).props(hide=True)
    with g.Frame():
        index = g.Index()
        reroute_15 = g.Reroute(input=reroute_5.o.output).props(width=19.0)
        reroute_16 = g.Reroute(input=reroute_6.o.output).props(width=19.0)
        index_switch = g.IndexSwitch.vector(index, (reroute_16, reroute_15))
        index_switch_1 = g.IndexSwitch.vector(index, (reroute_16, vector_math_5, reroute_15))
        index_switch_2 = g.IndexSwitch.vector(index, (reroute_16, vector_math_5, vector_math_6, reroute_15))
    (
        g.IndexSwitch.vector(integer_math, (index_switch, index_switch_1, index_switch_2))
        >> position
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (202.07, -69.04), "Frame.012", (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Compare", "Result"), )),
    "Boolean Math.001": ("FunctionNodeBooleanMath", (1779.26, 277.09), None, (("Boolean", "Compare.002", "Result"), )),
    "Boolean Math.002": ("FunctionNodeBooleanMath", (1779.85, 316.65), None, (("Boolean", "Boolean Math", "Boolean"), )),
    "Boolean Math.003": ("FunctionNodeBooleanMath", (1955.86, 278.71), None, (("Boolean", "Boolean Math.002", "Boolean"), ("Boolean#1", "Boolean Math.001", "Boolean"), )),
    "Compare": ("FunctionNodeCompare", (52.73, -157.8), "Frame.001", (("A", "Reroute.020", "Output"), )),
    "Compare.001": ("FunctionNodeCompare", (30.16, -45.02), "Frame.012", (("A", "Group Input", "Ratio"), )),
    "Compare.002": ("FunctionNodeCompare", (30.24, -44.86), "Frame.003", (("A", "Group Input", "Spread"), )),
    "Frame": ("NodeFrame", (172.13, -36.04), "Frame.011", ()),
    "Frame.001": ("NodeFrame", (177.73, -216.71), None, ()),
    "Frame.002": ("NodeFrame", (1216.59, -781.38), None, ()),
    "Frame.003": ("NodeFrame", (-1050.88, 349.5), None, ()),
    "Frame.004": ("NodeFrame", (1569.01, 1017.0), None, ()),
    "Frame.005": ("NodeFrame", (-360.0, -325.02), None, ()),
    "Frame.006": ("NodeFrame", (-72.72, 498.23), None, ()),
    "Frame.007": ("NodeFrame", (30.18, -36.04), "Frame.008", ()),
    "Frame.008": ("NodeFrame", (-86.29, -545.79), None, ()),
    "Frame.009": ("NodeFrame", (30.18, -270.56), "Frame.011", ()),
    "Frame.010": ("NodeFrame", (-1288.84, 783.05), None, ()),
    "Frame.011": ("NodeFrame", (-1468.66, 130.31), None, ()),
    "Frame.012": ("NodeFrame", (1165.76, -30.09), None, ()),
    "Group Input": ("NodeGroupInput", (-2312.45, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (2593.2, 778.16), None, (("Point Count", "Integer Math.001", "Value"), ("Position", "Index Switch.003", "Output"), )),
    "Index Switch": ("GeometryNodeIndexSwitch", (317.63, -205.83), "Frame.004", (("0", "Reroute.024", "Output"), ("1", "Vector Math.002", "Vector"), ("2", "Reroute.019", "Output"), ("Index", "Index.002", "Index"), )),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (314.84, -408.24), "Frame.004", (("0", "Reroute.024", "Output"), ("1", "Vector Math.002", "Vector"), ("2", "Vector Math.008", "Vector"), ("3", "Reroute.019", "Output"), ("Index", "Index.002", "Index"), )),
    "Index Switch.002": ("GeometryNodeIndexSwitch", (318.46, -30.27), "Frame.004", (("0", "Reroute.024", "Output"), ("1", "Reroute.019", "Output"), ("Index", "Index.002", "Index"), )),
    "Index Switch.003": ("GeometryNodeIndexSwitch", (2227.16, 662.06), None, (("0", "Index Switch.002", "Output"), ("1", "Index Switch", "Output"), ("2", "Index Switch.001", "Output"), ("Index", "Integer Math", "Value"), )),
    "Index.002": ("GeometryNodeInputIndex", (85.85, -63.62), "Frame.004", ()),
    "Integer Math": ("FunctionNodeIntegerMath", (1954.69, 318.37), None, (("Value", "Boolean Math.002", "Boolean"), ("Value#1", "Boolean Math.003", "Boolean"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (2230.86, 807.69), None, (("Value", "Integer Math", "Value"), )),
    "Linear Gizmo": ("GeometryNodeGizmoLinear", (226.37, -215.49), "Frame.002", (("Direction", "Reroute.003", "Output"), ("Position", "Reroute.001", "Output"), ("Value", "Math", "Value"), )),
    "Linear Gizmo.001": ("GeometryNodeGizmoLinear", (226.37, -36.23), "Frame.002", (("Direction", "Vector Math.010", "Vector"), ("Position", "Reroute.001", "Output"), ("Value", "Math.001", "Value"), )),
    "Linear Gizmo.002": ("GeometryNodeGizmoLinear", (226.65, -394.05), "Frame.002", (("Direction", "Vector Math.004", "Vector"), ("Position", "Reroute.001", "Output"), ("Value", "Reroute.004", "Output"), )),
    "Math": ("ShaderNodeMath", (34.71, -295.69), "Frame.002", (("Value", "Reroute.009", "Output"), ("Value#1", "Math.010", "Value"), )),
    "Math.001": ("ShaderNodeMath", (44.44, -374.41), "Frame.008", (("Value", "Reroute.010", "Output"), ("Value#1", "Reroute.008", "Output"), )),
    "Math.002": ("ShaderNodeMath", (195.58, -38.96), "Frame", (("Value", "Math.012", "Value"), )),
    "Math.003": ("ShaderNodeMath", (428.61, -209.82), "Frame.009", (("Value", "Math.011", "Value"), )),
    "Math.004": ("ShaderNodeMath", (424.8, -46.33), "Frame.009", (("Value", "Math.009", "Value"), )),
    "Math.005": ("ShaderNodeMath", (205.41, -63.69), "Frame.007", (("Value", "Math.008", "Value"), )),
    "Math.006": ("ShaderNodeMath", (271.37, -428.4), "Frame.008", (("Value", "Math.001", "Value"), )),
    "Math.007": ("ShaderNodeMath", (272.85, -393.75), "Frame.008", (("Value", "Math.001", "Value"), )),
    "Math.008": ("ShaderNodeMath", (29.99, -61.38), "Frame.007", (("Value", "Math.002", "Value"), )),
    "Math.009": ("ShaderNodeMath", (257.99, -44.93), "Frame.009", (("Value", "Math.016", "Value"), ("Value#1", "Reroute.015", "Output"), )),
    "Math.010": ("ShaderNodeMath", (30.42, -254.74), "Frame.002", (("Value", "Reroute.008", "Output"), )),
    "Math.011": ("ShaderNodeMath", (259.28, -209.98), "Frame.009", (("Value", "Math.017", "Value"), ("Value#1", "Reroute.015", "Output"), )),
    "Math.012": ("ShaderNodeMath", (30.13, -35.98), "Frame", (("Value", "Group Input", "Bias"), )),
    "Math.016": ("ShaderNodeMath", (87.63, -35.82), "Frame.009", (("Value#1", "Reroute.017", "Output"), )),
    "Math.017": ("ShaderNodeMath", (88.92, -200.86), "Frame.009", (("Value#1", "Reroute.017", "Output"), )),
    "Mix": ("ShaderNodeMix", (116.51, -39.14), "Frame.006", (("A#1", "Reroute", "Output"), ("B#1", "Reroute.006", "Output"), ("Factor", "Switch.002", "Output"), )),
    "Mix.001": ("ShaderNodeMix", (115.44, -96.44), "Frame.006", (("A#1", "Reroute", "Output"), ("B#1", "Reroute.006", "Output"), ("Factor", "Math.003", "Value"), )),
    "Mix.002": ("ShaderNodeMix", (380.19, -30.21), "Frame.007", (("A#1", "Reroute", "Output"), ("B#1", "Reroute.006", "Output"), ("Factor", "Math.005", "Value"), )),
    "Reroute": ("NodeReroute", (35.71, -63.5), "Frame.006", (("Input", "Reroute.014", "Output"), )),
    "Reroute.001": ("NodeReroute", (65.4, -159.57), "Frame.002", (("Input", "Vector Math.009", "Vector"), )),
    "Reroute.003": ("NodeReroute", (57.35, -201.6), "Frame.002", (("Input", "Vector Math", "Vector"), )),
    "Reroute.004": ("NodeReroute", (-737.01, -1277.92), None, (("Input", "Group Input", "Spread"), )),
    "Reroute.006": ("NodeReroute", (35.21, -99.28), "Frame.006", (("Input", "Reroute.012", "Output"), )),
    "Reroute.008": ("NodeReroute", (-200.89, -1044.33), None, (("Input", "Reroute.016", "Output"), )),
    "Reroute.009": ("NodeReroute", (-872.89, -1092.67), None, (("Input", "Group Input", "Bias"), )),
    "Reroute.010": ("NodeReroute", (-991.38, -926.66), None, (("Input", "Group Input", "Ratio"), )),
    "Reroute.011": ("NodeReroute", (1078.15, 371.87), None, (("Input", "Vector Math.010", "Vector"), )),
    "Reroute.012": ("NodeReroute", (300.67, -92.18), "Frame.010", (("Input", "Reroute.021", "Output"), )),
    "Reroute.014": ("NodeReroute", (302.95, -41.06), "Frame.010", (("Input", "Reroute.022", "Output"), )),
    "Reroute.015": ("NodeReroute", (35.21, -230.79), "Frame.009", (("Input", "Group Input", "Spread"), )),
    "Reroute.016": ("NodeReroute", (505.62, -61.73), "Frame.010", (("Input", "Vector Math.001", "Value"), )),
    "Reroute.017": ("NodeReroute", (38.95, -187.25), "Frame.009", (("Input", "Group Input", "Bias"), )),
    "Reroute.019": ("NodeReroute", (35.21, -328.47), "Frame.004", (("Input", "Reroute.012", "Output"), )),
    "Reroute.020": ("NodeReroute", (35.21, -41.46), "Frame.001", (("Input", "Group Input", "Normal"), )),
    "Reroute.021": ("NodeReroute", (35.21, -100.42), "Frame.010", (("Input", "Group Input", "End 2"), )),
    "Reroute.022": ("NodeReroute", (39.61, -46.15), "Frame.010", (("Input", "Group Input", "End 1"), )),
    "Reroute.024": ("NodeReroute", (36.39, -291.63), "Frame.004", (("Input", "Reroute.014", "Output"), )),
    "Switch.002": ("GeometryNodeSwitch", (811.49, -138.36), "Frame.011", (("False", "Math.004", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Math.002", "Value"), )),
    "Switch.003": ("GeometryNodeSwitch", (476.16, -294.45), "Frame.008", (("False", "Math.007", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Math.006", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (30.34, -100.22), "Frame.005", (("Vector", "Reroute.012", "Output"), ("Vector#1", "Reroute.014", "Output"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (315.59, -51.7), "Frame.010", (("Vector", "Reroute.014", "Output"), ("Vector#1", "Reroute.012", "Output"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (1125.3, 408.0), None, (("Vector", "Mix", "Result#1"), ("Vector#1", "Reroute.011", "Output"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (337.5, -39.8), "Frame.001", (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Reroute.020", "Output"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (89.27, -448.31), "Frame.002", (("Vector#1", "Reroute.003", "Output"), )),
    "Vector Math.007": ("ShaderNodeVectorMath", (190.03, -35.9), "Frame.005", (("Vector", "Vector Math", "Vector"), )),
    "Vector Math.008": ("ShaderNodeVectorMath", (1127.41, 354.76), None, (("Vector", "Mix.001", "Result#1"), ("Vector#1", "Reroute.011", "Output"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (908.54, -218.09), "Frame.008", (("Vector", "Mix.002", "Result#1"), ("Vector#1", "Vector Math.011", "Vector"), )),
    "Vector Math.010": ("ShaderNodeVectorMath", (886.41, -267.64), None, (("Scale", "Switch.003", "Output"), ("Vector", "Vector Math.003", "Vector"), )),
    "Vector Math.011": ("ShaderNodeVectorMath", (723.58, -299.93), "Frame.008", (("Scale", "Math.001", "Value"), ("Vector", "Vector Math.003", "Vector"), )),
    "Warning": ("GeometryNodeWarning", (226.66, -111.94), "Frame.001", (("Show", "Compare", "Result"), )),
}