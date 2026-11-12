from nodebpy import TreeBuilder

with TreeBuilder("SP - Line-Line Intersection Parameter", arrange=None, clear=True) as tree:
    with tree.inputs.panel("Line 1"):
        origin = tree.inputs.vector("Origin", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        direction = tree.inputs.vector("Direction", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
    with tree.inputs.panel("Line 2"):
        origin_1 = tree.inputs.vector("Origin", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        direction_1 = tree.inputs.vector("Direction", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
    t1 = tree.outputs.float("t1")
    t2 = tree.outputs.float("t2")

    math_1 = (direction.y * direction_1.x).props(hide=True)
    math_2 = (direction.x * direction_1.y).props(hide=True)
    math_3 = (math_1 - math_2).props(hide=True)
    math_4 = (((origin_1.y - origin.y).props(hide=True) * direction.x).props(hide=True) / math_3).props(hide=True)
    math_5 = (math_2 - math_1).props(hide=True)
    math_6 = (((origin_1.x - origin.x).props(hide=True) * direction.y).props(hide=True) / math_5).props(hide=True)
    (math_4 + math_6).props(hide=True) >> t2
    math_7 = (((origin.y - origin_1.y).props(hide=True) * direction_1.x).props(hide=True) / math_5).props(hide=True)
    math_8 = (((origin.x - origin_1.x).props(hide=True) * direction_1.y).props(hide=True) / math_3).props(hide=True)
    (math_7 + math_8).props(hide=True) >> t1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-1101.91, -3.37), None, ()),
    "Group Output": ("NodeGroupOutput", (574.88, 22.24), None, (("t1", "Math.015", "Value"), ("t2", "Math.007", "Value"), )),
    "Math": ("ShaderNodeMath", (-328.11, 162.34), None, (("Value", "Separate XYZ.002", "Y"), ("Value#1", "Separate XYZ.001", "Y"), )),
    "Math.001": ("ShaderNodeMath", (-325.39, 123.28), None, (("Value", "Separate XYZ.002", "X"), ("Value#1", "Separate XYZ.001", "X"), )),
    "Math.002": ("ShaderNodeMath", (-162.74, 153.51), None, (("Value", "Math", "Value"), ("Value#1", "Separate XYZ", "X"), )),
    "Math.003": ("ShaderNodeMath", (-332.59, -48.67), None, (("Value", "Separate XYZ", "Y"), ("Value#1", "Separate XYZ.003", "X"), )),
    "Math.004": ("ShaderNodeMath", (-174.12, -68.4), None, (("Value", "Math.003", "Value"), ("Value#1", "Math.008", "Value"), )),
    "Math.005": ("ShaderNodeMath", (87.54, 76.5), None, (("Value", "Math.009", "Value"), ("Value#1", "Math.011", "Value"), )),
    "Math.006": ("ShaderNodeMath", (85.07, 116.95), None, (("Value", "Math.002", "Value"), ("Value#1", "Math.004", "Value"), )),
    "Math.007": ("ShaderNodeMath", (273.28, 102.92), None, (("Value", "Math.006", "Value"), ("Value#1", "Math.005", "Value"), )),
    "Math.008": ("ShaderNodeMath", (-334.71, -85.41), None, (("Value", "Separate XYZ", "X"), ("Value#1", "Separate XYZ.003", "Y"), )),
    "Math.009": ("ShaderNodeMath", (-168.39, 109.0), None, (("Value", "Math.001", "Value"), ("Value#1", "Separate XYZ", "Y"), )),
    "Math.011": ("ShaderNodeMath", (-178.18, -107.07), None, (("Value", "Math.008", "Value"), ("Value#1", "Math.003", "Value"), )),
    "Math.012": ("ShaderNodeMath", (-313.14, -330.22), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.002", "Y"), )),
    "Math.013": ("ShaderNodeMath", (119.02, -203.42), None, (("Value", "Math.018", "Value"), ("Value#1", "Math.004", "Value"), )),
    "Math.014": ("ShaderNodeMath", (116.54, -162.96), None, (("Value", "Math.017", "Value"), ("Value#1", "Math.011", "Value"), )),
    "Math.015": ("ShaderNodeMath", (304.75, -176.99), None, (("Value", "Math.014", "Value"), ("Value#1", "Math.013", "Value"), )),
    "Math.016": ("ShaderNodeMath", (-310.43, -369.27), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ.002", "X"), )),
    "Math.017": ("ShaderNodeMath", (-147.77, -339.05), None, (("Value", "Math.012", "Value"), ("Value#1", "Separate XYZ.003", "X"), )),
    "Math.018": ("ShaderNodeMath", (-153.42, -383.56), None, (("Value", "Math.016", "Value"), ("Value#1", "Separate XYZ.003", "Y"), )),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (-660.73, 88.66), None, (("Vector", "Group Input", "Direction"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (-661.0, 237.91), None, (("Vector", "Group Input", "Origin"), )),
    "Separate XYZ.002": ("ShaderNodeSeparateXYZ", (-655.66, -132.18), None, (("Vector", "Group Input", "Origin#1"), )),
    "Separate XYZ.003": ("ShaderNodeSeparateXYZ", (-653.71, -283.1), None, (("Vector", "Group Input", "Direction#1"), )),
}