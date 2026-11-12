from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Ellipse Parameter of Point", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), subtype="XYZ")
    scaled_basis = tree.inputs.matrix("Scaled Basis")
    parameter_angle = tree.outputs.float("Parameter Angle", subtype="ANGLE")

    _reroute = g.Reroute().props(label="Pseudo angle, between -pi and pi", width=19.0)
    vector_1 = vector.transform(scaled_basis.invert())
    vector_1.y.atan2(vector_1.x) >> parameter_angle

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-578.76, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (463.92, 0.0), None, (("Parameter Angle", "Math.004", "Value"), )),
    "Invert Matrix.002": ("FunctionNodeInvertMatrix", (-332.99, -42.73), None, (("Matrix", "Group Input", "Scaled Basis"), )),
    "Math.004": ("ShaderNodeMath", (197.5, 57.91), None, (("Value", "Separate XYZ", "Y"), ("Value#1", "Separate XYZ", "X"), )),
    "Reroute.007": ("NodeReroute", (467.12, -126.9), None, ()),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (25.83, 31.86), None, (("Vector", "Transform Point.003", "Vector"), )),
    "Transform Point.003": ("FunctionNodeTransformPoint", (-150.81, -0.3), None, (("Transform", "Invert Matrix.002", "Matrix"), ("Vector", "Group Input", "Vector"), )),
}