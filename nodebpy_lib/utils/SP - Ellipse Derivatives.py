from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Ellipse Derivatives", arrange=None, clear=True) as tree:
    parameter = tree.inputs.float("Parameter", 0.0, description="Pseudo angle")
    scaled_basis = tree.inputs.matrix("Scaled Basis")
    position = tree.outputs.vector("Position", subtype="XYZ")
    tangent = tree.outputs.vector("Tangent", subtype="XYZ")
    acceleration = tree.outputs.vector("Acceleration", subtype="XYZ")
    jerk = tree.outputs.vector("Jerk", subtype="XYZ")
    snap = tree.outputs.vector("Snap", subtype="XYZ")

    math_1 = parameter.sin()
    math_2 = (0.0 - math_1).props(hide=True)
    math_3 = parameter.cos()
    math_4 = (0.0 - math_3).props(hide=True)
    combine_transform = g.CombineTransform(rotation=scaled_basis.rotation, scale=scaled_basis.scale)
    g.CombineXYZ(x=math_2, y=math_3).o.vector.transform(combine_transform) >> tangent
    (
        g.CombineXYZ(x=math_4, y=math_2).o.vector.transform(combine_transform)
        >> acceleration
    )
    g.CombineXYZ(x=math_1, y=math_4).o.vector.transform(combine_transform) >> jerk
    g.CombineXYZ(x=math_3, y=math_1).o.vector.transform(combine_transform) >> snap
    g.CombineXYZ(x=math_3, y=math_1).o.vector.transform(scaled_basis) >> position

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Combine Transform": ("FunctionNodeCombineTransform", (83.2, -617.76), None, (("Rotation", "Separate Transform", "Rotation"), ("Scale", "Separate Transform", "Scale"), )),
    "Combine XYZ": ("ShaderNodeCombineXYZ", (78.8, -112.03), None, (("X", "Math.001", "Value"), ("Y", "Math.003", "Value"), )),
    "Combine XYZ.001": ("ShaderNodeCombineXYZ", (78.8, -235.26), None, (("X", "Math.002", "Value"), ("Y", "Math.001", "Value"), )),
    "Combine XYZ.002": ("ShaderNodeCombineXYZ", (78.8, -358.49), None, (("X", "Math", "Value"), ("Y", "Math.002", "Value"), )),
    "Combine XYZ.003": ("ShaderNodeCombineXYZ", (78.8, -481.72), None, (("X", "Math.003", "Value"), ("Y", "Math", "Value"), )),
    "Combine XYZ.004": ("ShaderNodeCombineXYZ", (78.8, 11.2), None, (("X", "Math.003", "Value"), ("Y", "Math", "Value"), )),
    "Group Input": ("NodeGroupInput", (-1171.71, -111.31), None, ()),
    "Group Output": ("NodeGroupOutput", (697.33, -194.94), None, (("Acceleration", "Transform Point.001", "Vector"), ("Jerk", "Transform Point.002", "Vector"), ("Position", "Transform Point.004", "Vector"), ("Snap", "Transform Point.003", "Vector"), ("Tangent", "Transform Point", "Vector"), )),
    "Math": ("ShaderNodeMath", (-555.76, 218.08), None, (("Value", "Group Input", "Parameter"), )),
    "Math.001": ("ShaderNodeMath", (-340.65, -310.41), None, (("Value#1", "Math", "Value"), )),
    "Math.002": ("ShaderNodeMath", (-341.57, -364.05), None, (("Value#1", "Math.003", "Value"), )),
    "Math.003": ("ShaderNodeMath", (-556.62, 79.25), None, (("Value", "Group Input", "Parameter"), )),
    "Separate Transform": ("FunctionNodeSeparateTransform", (-107.82, -670.59), None, (("Transform", "Group Input", "Scaled Basis"), )),
    "Transform Point": ("FunctionNodeTransformPoint", (328.75, -158.04), None, (("Transform", "Combine Transform", "Transform"), ("Vector", "Combine XYZ", "Vector"), )),
    "Transform Point.001": ("FunctionNodeTransformPoint", (328.75, -237.28), None, (("Transform", "Combine Transform", "Transform"), ("Vector", "Combine XYZ.001", "Vector"), )),
    "Transform Point.002": ("FunctionNodeTransformPoint", (328.75, -316.53), None, (("Transform", "Combine Transform", "Transform"), ("Vector", "Combine XYZ.002", "Vector"), )),
    "Transform Point.003": ("FunctionNodeTransformPoint", (328.75, -395.78), None, (("Transform", "Combine Transform", "Transform"), ("Vector", "Combine XYZ.003", "Vector"), )),
    "Transform Point.004": ("FunctionNodeTransformPoint", (328.75, -77.16), None, (("Transform", "Group Input", "Scaled Basis"), ("Vector", "Combine XYZ.004", "Vector"), )),
}