from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Align CVs of Bezier Patch", arrange=None, clear=True) as tree:
    row_0 = tree.inputs.vector("Row 0", (0.0, 0.0, 0.0), hide_value=True)
    row_1 = tree.inputs.vector("Row 1", (0.0, 0.0, 0.0), hide_value=True)
    row_2 = tree.inputs.vector("Row 2", (0.0, 0.0, 0.0), hide_value=True)
    row_3 = tree.inputs.vector("Row 3", (0.0, 0.0, 0.0), hide_value=True)
    row_4 = tree.inputs.vector("Row 4", (0.0, 0.0, 0.0), hide_value=True)
    k = tree.inputs.integer("k", 0)
    n = tree.inputs.integer("n", 0)
    row_0_1 = tree.outputs.vector("Row 0")
    row_1_1 = tree.outputs.vector("Row 1")
    row_2_1 = tree.outputs.vector("Row 2")
    row_3_1 = tree.outputs.vector("Row 3")
    row_4_1 = tree.outputs.vector("Row 4")

    integer_math = (n - 1).props(label="n")
    integer_math_1 = (k - 1).props(label="k")
    with g.Frame():
        with g.Frame():
            with g.Frame("k(k-1)"):
                reroute = g.Reroute(input=integer_math_1).props(width=19.0)
                integer_math_2 = (reroute.o.output - 1) * reroute
            integer_math_3 = (reroute.o.output - 2) * integer_math_2
        integer_math_4 = (reroute.o.output - 3) * integer_math_3
    with g.Frame():
        with g.Frame():
            with g.Frame("n(n-1)"):
                reroute_1 = g.Reroute(input=integer_math).props(width=19.0)
                integer_math_5 = (reroute_1.o.output - 1) * reroute_1
            integer_math_6 = (reroute_1.o.output - 2) * integer_math_5
        integer_math_7 = (reroute_1.o.output - 3) * integer_math_6
    reroute_2 = g.Reroute(input=g.Reroute(input=g.Reroute(input=row_3).props(width=19.0).o.output).props(width=19.0).o.output).props(width=19.0)
    reroute_3 = g.Reroute(input=g.Reroute(input=g.Reroute(input=row_4).props(width=19.0).o.output).props(width=19.0).o.output).props(width=19.0)
    reroute_4 = g.Reroute(input=row_0).props(width=19.0)
    g.Reroute(input=reroute_4.o.output).props(width=19.0) >> row_0_1
    reroute_5 = g.Reroute(input=reroute_4.o.output).props(width=19.0)
    reroute_6 = g.Reroute(input=reroute_5.o.output).props(width=19.0)
    reroute_7 = g.Reroute(input=row_1).props(width=19.0)
    with g.Frame("P1"):
        reroute_8 = g.Reroute(input=integer_math).props(label="n", width=19.0)
        reroute_9 = g.Reroute(input=integer_math_1).props(label="k", width=19.0)
        math_1 = (g.Math.subtract(reroute_9, reroute_8).props(label="k-n").o.value / reroute_9).props(label="k_n/k")
        vector_math = g.Reroute(input=reroute_7.o.output).props(label="P11", width=19.0).o.output * (reroute_8.o.output / reroute_9).props(label="n/k")
        vector_math_1 = vector_math + g.Reroute(input=reroute_4.o.output).props(label="P0", width=19.0).o.output * math_1
    reroute_10 = g.Reroute(input=reroute_7.o.output).props(width=19.0)
    reroute_11 = g.Reroute(input=reroute_10.o.output).props(width=19.0)
    reroute_12 = g.Reroute(input=g.Reroute(input=row_2).props(width=19.0).o.output).props(width=19.0)
    with g.Frame("P2"):
        reroute_13 = g.Reroute(input=reroute_5.o.output).props(width=19.0)
        vector_math_2 = g.Reroute(input=reroute_12.o.output).props(width=19.0).o.output + g.Reroute(input=reroute_10.o.output).props(width=19.0).o.output * -2.0
        vector_math_3 = (vector_math_2 + reroute_13) * (integer_math_5 / integer_math_2) + vector_math_1 * 2.0 - reroute_13
    reroute_14 = g.Reroute(input=reroute_12.o.output).props(width=19.0)
    with g.Frame("P3"):
        reroute_15 = g.Reroute(input=reroute_6.o.output).props(width=19.0)
        vector_math_4 = g.Reroute(input=reroute_2.o.output).props(width=19.0).o.output - g.Reroute(input=reroute_14.o.output).props(width=19.0).o.output * 3.0
        vector_math_5 = g.Reroute(input=reroute_11.o.output).props(width=19.0).o.output * 3.0 - reroute_15 + vector_math_4
        vector_math_6 = vector_math_5 * (integer_math_6 / integer_math_3) - vector_math_1 * 3.0 + vector_math_3 * 3.0
        vector_math_7 = vector_math_6 + reroute_15
    with g.Frame("P4"):
        reroute_16 = g.Reroute(input=reroute_6.o.output).props(width=19.0)
        vector_math_8 = g.Reroute(input=reroute_3.o.output).props(width=19.0).o.output - g.Reroute(input=reroute_2.o.output).props(width=19.0).o.output * 4.0
        vector_math_9 = reroute_16.o.output - g.Reroute(input=reroute_11.o.output).props(width=19.0).o.output * 4.0
        vector_math_10 = vector_math_9 + vector_math_8 + g.Reroute(input=reroute_14.o.output).props(width=19.0).o.output * 6.0
        vector_math_11 = vector_math_10 * (integer_math_7 / integer_math_4) + vector_math_1 * 4.0 - vector_math_3 * 6.0
        vector_math_12 = vector_math_11 + vector_math_7 * 4.0 - reroute_16
    g.Reroute(input=vector_math_1).props(width=19.0) >> row_1_1
    g.Reroute(input=vector_math_3).props(width=19.0) >> row_2_1
    g.Reroute(input=vector_math_7).props(width=19.0) >> row_3_1
    g.Reroute(input=vector_math_12).props(width=19.0) >> row_4_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Frame.003": ("NodeFrame", (30.18, -168.6), "Frame.006", ()),
    "Frame.004": ("NodeFrame", (30.18, -168.45), "Frame.007", ()),
    "Frame.006": ("NodeFrame", (30.18, -169.94), "Frame.009", ()),
    "Frame.007": ("NodeFrame", (30.18, -169.94), "Frame.017", ()),
    "Frame.009": ("NodeFrame", (-1245.47, 370.06), None, ()),
    "Frame.013": ("NodeFrame", (-55.24, -106.38), None, ()),
    "Frame.014": ("NodeFrame", (-12.2, 412.45), None, ()),
    "Frame.015": ("NodeFrame", (201.43, 966.74), None, ()),
    "Frame.016": ("NodeFrame", (-267.54, -707.26), None, ()),
    "Frame.017": ("NodeFrame", (-1241.68, 1005.35), None, ()),
    "Group Input": ("NodeGroupInput", (-1990.69, -465.52), None, ()),
    "Group Output": ("NodeGroupOutput", (2218.21, 254.86), None, (("Row 0", "Reroute.008", "Output"), ("Row 1", "Reroute.011", "Output"), ("Row 2", "Reroute.002", "Output"), ("Row 3", "Reroute.007", "Output"), ("Row 4", "Reroute.003", "Output"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (-1635.37, -238.21), None, (("Value", "Group Input", "n"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-1638.05, -97.56), None, (("Value", "Group Input", "k"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (118.22, -60.15), "Frame.003", (("Value", "Reroute.004", "Output"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (281.48, -57.99), "Frame.003", (("Value", "Integer Math.002", "Value"), ("Value#1", "Reroute.004", "Output"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (336.29, -30.33), "Frame.006", (("Value", "Reroute.004", "Output"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (523.48, -37.65), "Frame.006", (("Value", "Integer Math.004", "Value"), ("Value#1", "Integer Math.003", "Value"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (561.48, -30.11), "Frame.009", (("Value", "Reroute.004", "Output"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (748.67, -37.42), "Frame.009", (("Value", "Integer Math.006", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
    "Integer Math.008": ("FunctionNodeIntegerMath", (118.22, -60.15), "Frame.004", (("Value", "Reroute.010", "Output"), )),
    "Integer Math.009": ("FunctionNodeIntegerMath", (281.48, -57.99), "Frame.004", (("Value", "Integer Math.008", "Value"), ("Value#1", "Reroute.010", "Output"), )),
    "Integer Math.010": ("FunctionNodeIntegerMath", (336.29, -30.18), "Frame.007", (("Value", "Reroute.010", "Output"), )),
    "Integer Math.011": ("FunctionNodeIntegerMath", (523.48, -37.5), "Frame.007", (("Value", "Integer Math.010", "Value"), ("Value#1", "Integer Math.009", "Value"), )),
    "Integer Math.012": ("FunctionNodeIntegerMath", (561.48, -29.96), "Frame.017", (("Value", "Reroute.010", "Output"), )),
    "Integer Math.013": ("FunctionNodeIntegerMath", (748.67, -37.28), "Frame.017", (("Value", "Integer Math.012", "Value"), ("Value#1", "Integer Math.011", "Value"), )),
    "Math.027": ("ShaderNodeMath", (301.73, -36.05), "Frame.013", (("Value", "Integer Math.009", "Value"), ("Value#1", "Integer Math.003", "Value"), )),
    "Math.028": ("ShaderNodeMath", (485.48, -35.93), "Frame.014", (("Value", "Integer Math.011", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
    "Math.029": ("ShaderNodeMath", (451.02, -39.21), "Frame.015", (("Value", "Integer Math.013", "Value"), ("Value#1", "Integer Math.007", "Value"), )),
    "Math.030": ("ShaderNodeMath", (296.11, -204.09), "Frame.016", (("Value", "Math.031", "Value"), ("Value#1", "Reroute.047", "Output"), )),
    "Math.031": ("ShaderNodeMath", (125.55, -212.29), "Frame.016", (("Value", "Reroute.047", "Output"), ("Value#1", "Reroute.046", "Output"), )),
    "Math.032": ("ShaderNodeMath", (301.36, -36.29), "Frame.016", (("Value", "Reroute.046", "Output"), ("Value#1", "Reroute.047", "Output"), )),
    "Reroute.002": ("NodeReroute", (2139.74, 177.89), None, (("Input", "Vector Math.009", "Vector"), )),
    "Reroute.003": ("NodeReroute", (2139.74, 132.47), None, (("Input", "Vector Math.033", "Vector"), )),
    "Reroute.004": ("NodeReroute", (35.21, -41.06), "Frame.003", (("Input", "Integer Math.001", "Value"), )),
    "Reroute.006": ("NodeReroute", (35.21, -325.44), "Frame.014", (("Input", "Reroute.036", "Output"), )),
    "Reroute.007": ("NodeReroute", (2139.74, 155.18), None, (("Input", "Vector Math.020", "Vector"), )),
    "Reroute.008": ("NodeReroute", (2139.74, 223.31), None, (("Input", "Reroute.089", "Output"), )),
    "Reroute.009": ("NodeReroute", (35.21, -519.43), "Frame.013", (("Input", "Reroute.020", "Output"), )),
    "Reroute.010": ("NodeReroute", (35.21, -41.06), "Frame.004", (("Input", "Integer Math", "Value"), )),
    "Reroute.011": ("NodeReroute", (2139.74, 200.6), None, (("Input", "Vector Math.005", "Vector"), )),
    "Reroute.016": ("NodeReroute", (-716.73, -516.24), None, (("Input", "Reroute.089", "Output"), )),
    "Reroute.017": ("NodeReroute", (-716.73, -543.04), None, (("Input", "Reroute.090", "Output"), )),
    "Reroute.020": ("NodeReroute", (-716.73, -569.84), None, (("Input", "Reroute.091", "Output"), )),
    "Reroute.021": ("NodeReroute", (-716.73, -596.63), None, (("Input", "Reroute.067", "Output"), )),
    "Reroute.023": ("NodeReroute", (-716.73, -617.54), None, (("Input", "Reroute.088", "Output"), )),
    "Reroute.024": ("NodeReroute", (35.21, -457.43), "Frame.013", (("Input", "Reroute.016", "Output"), )),
    "Reroute.025": ("NodeReroute", (35.21, -488.43), "Frame.013", (("Input", "Reroute.017", "Output"), )),
    "Reroute.027": ("NodeReroute", (35.21, -294.44), "Frame.014", (("Input", "Reroute.037", "Output"), )),
    "Reroute.028": ("NodeReroute", (35.21, -263.44), "Frame.014", (("Input", "Reroute.035", "Output"), )),
    "Reroute.034": ("NodeReroute", (38.18, -358.17), "Frame.014", (("Input", "Reroute.038", "Output"), )),
    "Reroute.035": ("NodeReroute", (-158.25, 141.95), None, (("Input", "Reroute.016", "Output"), )),
    "Reroute.036": ("NodeReroute", (-158.25, 79.95), None, (("Input", "Reroute.020", "Output"), )),
    "Reroute.037": ("NodeReroute", (-158.25, 110.95), None, (("Input", "Reroute.017", "Output"), )),
    "Reroute.038": ("NodeReroute", (-158.25, 48.95), None, (("Input", "Reroute.021", "Output"), )),
    "Reroute.039": ("NodeReroute", (-158.25, 17.95), None, (("Input", "Reroute.023", "Output"), )),
    "Reroute.040": ("NodeReroute", (35.21, -457.94), "Frame.015", (("Input", "Reroute.039", "Output"), )),
    "Reroute.041": ("NodeReroute", (35.21, -426.94), "Frame.015", (("Input", "Reroute.038", "Output"), )),
    "Reroute.042": ("NodeReroute", (35.21, -395.94), "Frame.015", (("Input", "Reroute.036", "Output"), )),
    "Reroute.043": ("NodeReroute", (35.21, -364.94), "Frame.015", (("Input", "Reroute.037", "Output"), )),
    "Reroute.044": ("NodeReroute", (35.21, -333.94), "Frame.015", (("Input", "Reroute.035", "Output"), )),
    "Reroute.046": ("NodeReroute", (35.21, -236.8), "Frame.016", (("Input", "Integer Math", "Value"), )),
    "Reroute.047": ("NodeReroute", (35.21, -205.8), "Frame.016", (("Input", "Integer Math.001", "Value"), )),
    "Reroute.048": ("NodeReroute", (35.21, -174.8), "Frame.016", (("Input", "Reroute.090", "Output"), )),
    "Reroute.049": ("NodeReroute", (35.21, -143.8), "Frame.016", (("Input", "Reroute.089", "Output"), )),
    "Reroute.067": ("NodeReroute", (-1326.91, -609.64), None, (("Input", "Group Input", "Row 3"), )),
    "Reroute.088": ("NodeReroute", (-1326.91, -632.84), None, (("Input", "Group Input", "Row 4"), )),
    "Reroute.089": ("NodeReroute", (-1326.91, -540.05), None, (("Input", "Group Input", "Row 0"), )),
    "Reroute.090": ("NodeReroute", (-1326.91, -563.24), None, (("Input", "Group Input", "Row 1"), )),
    "Reroute.091": ("NodeReroute", (-1326.91, -586.44), None, (("Input", "Group Input", "Row 2"), )),
    "Vector Math": ("ShaderNodeVectorMath", (479.41, -204.82), "Frame.013", (("Scale", "Math.027", "Value"), ("Vector", "Vector Math.003", "Vector"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (148.71, -216.91), "Frame.013", (("Vector", "Reroute.009", "Output"), ("Vector#1", "Vector Math.002", "Vector"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (137.33, -355.25), "Frame.013", (("Vector", "Reroute.025", "Output"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (310.2, -214.14), "Frame.013", (("Vector", "Vector Math.001", "Vector"), ("Vector#1", "Reroute.024", "Output"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (490.98, -66.24), "Frame.016", (("Scale", "Math.032", "Value"), ("Vector", "Reroute.048", "Output"), )),
    "Vector Math.005": ("ShaderNodeVectorMath", (665.94, -89.14), "Frame.016", (("Vector", "Vector Math.004", "Vector"), ("Vector#1", "Vector Math.006", "Vector"), )),
    "Vector Math.006": ("ShaderNodeVectorMath", (487.18, -202.14), "Frame.016", (("Scale", "Math.030", "Value"), ("Vector", "Reroute.049", "Output"), )),
    "Vector Math.007": ("ShaderNodeVectorMath", (649.3, -214.0), "Frame.013", (("Vector", "Vector Math", "Vector"), ("Vector#1", "Vector Math.008", "Vector"), )),
    "Vector Math.008": ("ShaderNodeVectorMath", (639.3, -348.36), "Frame.013", (("Vector", "Vector Math.005", "Vector"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (863.66, -238.87), "Frame.013", (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Reroute.024", "Output"), )),
    "Vector Math.010": ("ShaderNodeVectorMath", (721.1, -47.59), "Frame.014", (("Scale", "Math.028", "Value"), ("Vector", "Vector Math.016", "Vector"), )),
    "Vector Math.011": ("ShaderNodeVectorMath", (898.23, -47.61), "Frame.014", (("Vector", "Vector Math.010", "Vector"), ("Vector#1", "Vector Math.018", "Vector"), )),
    "Vector Math.012": ("ShaderNodeVectorMath", (300.46, -306.17), "Frame.014", (("Vector", "Reroute.034", "Output"), ("Vector#1", "Vector Math.013", "Vector"), )),
    "Vector Math.013": ("ShaderNodeVectorMath", (123.3, -304.65), "Frame.014", (("Vector", "Reroute.006", "Output"), )),
    "Vector Math.014": ("ShaderNodeVectorMath", (124.11, -175.87), "Frame.014", (("Vector", "Reroute.027", "Output"), )),
    "Vector Math.015": ("ShaderNodeVectorMath", (302.47, -173.51), "Frame.014", (("Vector", "Vector Math.014", "Vector"), ("Vector#1", "Reroute.028", "Output"), )),
    "Vector Math.016": ("ShaderNodeVectorMath", (482.78, -205.91), "Frame.014", (("Vector", "Vector Math.015", "Vector"), ("Vector#1", "Vector Math.012", "Vector"), )),
    "Vector Math.017": ("ShaderNodeVectorMath", (1103.39, -183.15), "Frame.014", (("Vector", "Vector Math.009", "Vector"), )),
    "Vector Math.018": ("ShaderNodeVectorMath", (888.62, -184.07), "Frame.014", (("Vector", "Vector Math.005", "Vector"), )),
    "Vector Math.019": ("ShaderNodeVectorMath", (1114.5, -53.97), "Frame.014", (("Vector", "Vector Math.011", "Vector"), ("Vector#1", "Vector Math.017", "Vector"), )),
    "Vector Math.020": ("ShaderNodeVectorMath", (1283.34, -60.72), "Frame.014", (("Vector", "Vector Math.019", "Vector"), ("Vector#1", "Reroute.028", "Output"), )),
    "Vector Math.021": ("ShaderNodeVectorMath", (639.38, -49.39), "Frame.015", (("Scale", "Math.029", "Value"), ("Vector", "Vector Math.026", "Vector"), )),
    "Vector Math.022": ("ShaderNodeVectorMath", (259.99, -331.22), "Frame.015", (("Vector", "Reroute.040", "Output"), ("Vector#1", "Vector Math.023", "Vector"), )),
    "Vector Math.023": ("ShaderNodeVectorMath", (91.17, -343.9), "Frame.015", (("Vector", "Reroute.041", "Output"), )),
    "Vector Math.024": ("ShaderNodeVectorMath", (442.93, -363.69), "Frame.015", (("Vector", "Reroute.042", "Output"), )),
    "Vector Math.025": ("ShaderNodeVectorMath", (453.78, -210.85), "Frame.015", (("Vector", "Vector Math.027", "Vector"), ("Vector#1", "Vector Math.022", "Vector"), )),
    "Vector Math.026": ("ShaderNodeVectorMath", (646.78, -226.16), "Frame.015", (("Vector", "Vector Math.025", "Vector"), ("Vector#1", "Vector Math.024", "Vector"), )),
    "Vector Math.027": ("ShaderNodeVectorMath", (251.75, -181.68), "Frame.015", (("Vector", "Reroute.044", "Output"), ("Vector#1", "Vector Math.028", "Vector"), )),
    "Vector Math.028": ("ShaderNodeVectorMath", (82.94, -194.36), "Frame.015", (("Vector", "Reroute.043", "Output"), )),
    "Vector Math.029": ("ShaderNodeVectorMath", (1191.58, -176.35), "Frame.015", (("Vector", "Vector Math.020", "Vector"), )),
    "Vector Math.030": ("ShaderNodeVectorMath", (1193.87, -41.77), "Frame.015", (("Vector", "Vector Math.032", "Vector"), ("Vector#1", "Vector Math.029", "Vector"), )),
    "Vector Math.031": ("ShaderNodeVectorMath", (1025.47, -179.75), "Frame.015", (("Vector", "Vector Math.009", "Vector"), )),
    "Vector Math.032": ("ShaderNodeVectorMath", (1027.67, -41.72), "Frame.015", (("Vector", "Vector Math.035", "Vector"), ("Vector#1", "Vector Math.031", "Vector"), )),
    "Vector Math.033": ("ShaderNodeVectorMath", (1382.13, -53.55), "Frame.015", (("Vector", "Vector Math.030", "Vector"), ("Vector#1", "Reroute.044", "Output"), )),
    "Vector Math.034": ("ShaderNodeVectorMath", (855.0, -170.46), "Frame.015", (("Vector", "Vector Math.005", "Vector"), )),
    "Vector Math.035": ("ShaderNodeVectorMath", (857.29, -35.89), "Frame.015", (("Vector", "Vector Math.021", "Vector"), ("Vector#1", "Vector Math.034", "Vector"), )),
}