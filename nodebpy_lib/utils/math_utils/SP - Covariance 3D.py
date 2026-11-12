from nodebpy import TreeBuilder

with TreeBuilder("SP - Covariance 3D", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
    x2 = tree.outputs.float("x²")
    y2 = tree.outputs.float("y²")
    z2 = tree.outputs.float("z²")
    xy = tree.outputs.float("xy")
    xz = tree.outputs.float("xz")
    yz = tree.outputs.float("yz")

    (vector.x * vector.x).props(width=100.0, hide=True) >> x2
    (vector.x * vector.y).props(width=100.0, hide=True) >> xy
    (vector.y * vector.y).props(width=100.0, hide=True) >> y2
    (vector.x * vector.z).props(width=100.0, hide=True) >> xz
    (vector.y * vector.z).props(width=100.0, hide=True) >> yz
    (vector.z * vector.z).props(width=100.0, hide=True) >> z2

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-299.69, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (306.61, 44.8), None, (("xy", "Math.006", "Value"), ("xz", "Math.009", "Value"), ("x²", "Math.003", "Value"), ("yz", "Math.010", "Value"), ("y²", "Math.007", "Value"), ("z²", "Math.011", "Value"), )),
    "Math.003": ("ShaderNodeMath", (83.9, 70.45), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ.001", "X"), )),
    "Math.006": ("ShaderNodeMath", (83.9, 36.57), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ.001", "Y"), )),
    "Math.007": ("ShaderNodeMath", (83.9, -31.19), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.001", "Y"), )),
    "Math.009": ("ShaderNodeMath", (83.9, 2.69), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ.001", "Z"), )),
    "Math.010": ("ShaderNodeMath", (83.9, -65.07), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.001", "Z"), )),
    "Math.011": ("ShaderNodeMath", (83.9, -98.95), None, (("Value", "Separate XYZ.001", "Z"), ("Value#1", "Separate XYZ.001", "Z"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (-99.69, 36.5), None, (("Vector", "Group Input", "Vector"), )),
}