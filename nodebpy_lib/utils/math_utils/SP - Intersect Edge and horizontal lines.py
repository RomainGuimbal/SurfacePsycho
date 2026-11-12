from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Intersect Edge and horizontal lines", arrange=None, clear=True) as tree:
    y_line_height = tree.inputs.float("Y (Line height)", 0.0)
    x_max = tree.inputs.float("X max", 0.0)
    edge_point = tree.inputs.vector("Edge Point", (0.0, 0.0, 0.0), hide_value=True)
    edge_point_1 = tree.inputs.vector("Edge Point", (0.0, 0.0, 0.0), hide_value=True)
    p_sol = tree.outputs.vector("P sol")
    intersects = tree.outputs.boolean("Intersects")
    x_sol = tree.outputs.float("X sol")

    _clamp = g.Clamp()
    reroute = g.Reroute(input=y_line_height).props(width=19.0)
    reroute_1 = g.Reroute(input=edge_point).props(width=19.0)
    reroute_2 = g.Reroute(input=edge_point_1).props(width=19.0)
    separate_xyz = g.SeparateXYZ(reroute_1)
    vector_math = reroute_2.o.output - reroute_1
    vector = vector_math.normalize()
    vector_1 = g.CombineXYZ(x=vector.y, y=(vector.x * -1.0).props(hide=True)).o.vector
    math_1 = (vector_1.x * separate_xyz.o.x - vector_1.y * (reroute.o.output - separate_xyz.o.y)) / vector_1.x
    combine_xyz = g.CombineXYZ(x=math_1, y=reroute)
    reroute_3 = g.Reroute(input=math_1).props(width=19.0)
    with g.Frame("Intersect cond"):
        separate_xyz_1 = g.SeparateXYZ(reroute_1).props(label="xA", hide_outputs=["Y", "Z"])
        boolean_math = g.BooleanMath.equal((math_1 - separate_xyz_1.o.x).props(label="xP-xA") >= 0.0, (reroute_2.o.output.x - separate_xyz_1.o.x).props(label="xB-xA") >= 0.0)
        reroute_4 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
        (
            ((reroute_1.o.output.distance(combine_xyz) <= vector_math.length()) & boolean_math & ((reroute_4 <= g.Reroute(input=x_max).props(width=19.0)) & (reroute_4 >= 0.0)))
            >> intersects
        )

    combine_xyz >> p_sol
    reroute_3 >> x_sol

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (862.56, -260.94), "Frame.001", (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Boolean Math.009", "Boolean"), )),
    "Boolean Math.002": ("FunctionNodeBooleanMath", (927.79, -768.74), "Frame.001", (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Compare.004", "Result"), )),
    "Boolean Math.005": ("FunctionNodeBooleanMath", (1198.14, -554.42), "Frame.001", (("Boolean", "Boolean Math", "Boolean"), ("Boolean#1", "Boolean Math.002", "Boolean"), )),
    "Boolean Math.009": ("FunctionNodeBooleanMath", (620.13, -445.28), "Frame.001", (("Boolean", "Compare.011", "Result"), ("Boolean#1", "Compare.012", "Result"), )),
    "Clamp": ("ShaderNodeClamp", (1884.88, -566.76), None, ()),
    "Combine XYZ.002": ("ShaderNodeCombineXYZ", (715.68, -788.52), None, (("X", "Math.009", "Value"), ("Y", "Reroute.003", "Output"), )),
    "Combine XYZ.004": ("ShaderNodeCombineXYZ", (-520.69, -430.72), None, (("X", "Separate XYZ", "Y"), ("Y", "Math.006", "Value"), )),
    "Compare.001": ("FunctionNodeCompare", (620.83, -52.4), "Frame.001", (("A", "Vector Math.003", "Value"), ("B", "Vector Math.015", "Value"), )),
    "Compare.002": ("FunctionNodeCompare", (743.42, -700.45), "Frame.001", (("A", "Reroute.034", "Output"), ("B", "Reroute.010", "Output"), )),
    "Compare.004": ("FunctionNodeCompare", (736.46, -868.15), "Frame.001", (("A", "Reroute.034", "Output"), )),
    "Compare.011": ("FunctionNodeCompare", (436.84, -383.01), "Frame.001", (("A", "Math.014", "Value"), )),
    "Compare.012": ("FunctionNodeCompare", (439.46, -546.31), "Frame.001", (("A", "Math.016", "Value"), )),
    "Frame.001": ("NodeFrame", (631.59, 615.21), None, ()),
    "Group Input": ("NodeGroupInput", (-1859.52, -743.88), None, ()),
    "Group Output": ("NodeGroupOutput", (2157.73, -398.24), None, (("Intersects", "Boolean Math.005", "Boolean"), ("P sol", "Combine XYZ.002", "Vector"), ("X sol", "Reroute", "Output"), )),
    "Math.004": ("ShaderNodeMath", (258.11, -624.97), None, (("Value", "Math.005", "Value"), ("Value#1", "Math.007", "Value"), )),
    "Math.005": ("ShaderNodeMath", (-140.15, -397.75), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ.002", "X"), )),
    "Math.006": ("ShaderNodeMath", (-687.63, -515.47), None, (("Value", "Separate XYZ", "X"), )),
    "Math.007": ("ShaderNodeMath", (84.94, -628.08), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Math.008", "Value"), )),
    "Math.008": ("ShaderNodeMath", (-86.15, -628.08), None, (("Value", "Reroute.003", "Output"), ("Value#1", "Separate XYZ.002", "Y"), )),
    "Math.009": ("ShaderNodeMath", (427.14, -628.08), None, (("Value", "Math.004", "Value"), ("Value#1", "Separate XYZ.001", "X"), )),
    "Math.014": ("ShaderNodeMath", (249.02, -387.08), "Frame.001", (("Value", "Math.009", "Value"), ("Value#1", "Separate XYZ.003", "X"), )),
    "Math.016": ("ShaderNodeMath", (253.3, -551.71), "Frame.001", (("Value", "Separate XYZ.004", "X"), ("Value#1", "Separate XYZ.003", "X"), )),
    "Reroute": ("NodeReroute", (1126.79, -584.63), None, (("Input", "Math.009", "Value"), )),
    "Reroute.003": ("NodeReroute", (-289.9, -866.99), None, (("Input", "Group Input", "Y (Line height)"), )),
    "Reroute.007": ("NodeReroute", (-1322.06, -588.17), None, (("Input", "Group Input", "Edge Point"), )),
    "Reroute.010": ("NodeReroute", (674.53, -973.02), "Frame.001", (("Input", "Group Input", "X max"), )),
    "Reroute.016": ("NodeReroute", (-1316.15, -611.45), None, (("Input", "Group Input", "Edge Point#1"), )),
    "Reroute.034": ("NodeReroute", (667.12, -947.8), "Frame.001", (("Input", "Reroute", "Output"), )),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (-864.25, -438.34), None, (("Vector", "Vector Math.009", "Vector"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (-346.26, -446.0), None, (("Vector", "Combine XYZ.004", "Vector"), )),
    "Separate XYZ.002": ("ShaderNodeSeparateXYZ", (-348.11, -590.88), None, (("Vector", "Reroute.007", "Output"), )),
    "Separate XYZ.003": ("ShaderNodeSeparateXYZ", (31.19, -508.33), "Frame.001", (("Vector", "Reroute.007", "Output"), )),
    "Separate XYZ.004": ("ShaderNodeSeparateXYZ", (30.27, -596.5), "Frame.001", (("Vector", "Reroute.016", "Output"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-1217.36, -427.18), None, (("Vector", "Reroute.016", "Output"), ("Vector#1", "Reroute.007", "Output"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (444.31, -156.49), "Frame.001", (("Vector", "Reroute.007", "Output"), ("Vector#1", "Combine XYZ.002", "Vector"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (-1049.49, -445.53), None, (("Vector", "Vector Math", "Vector"), )),
    "Vector Math.015": ("ShaderNodeVectorMath", (451.19, -35.87), "Frame.001", (("Vector", "Vector Math", "Vector"), )),
}