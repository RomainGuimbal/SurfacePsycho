from nodebpy import TreeBuilder

with TreeBuilder("SP - Angle between 2D vectors", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
    vector_1 = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
    angle = tree.outputs.float("Angle")

    (vector.x * vector_1.y - vector.y * vector_1.x).atan2(vector.dot(vector_1)) >> angle

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-495.0, 48.08), None, ()),
    "Group Output": ("NodeGroupOutput", (735.55, 50.53), None, (("Angle", "Math.017", "Value"), )),
    "Math": ("ShaderNodeMath", (13.16, 282.22), None, (("Value", "Separate XYZ", "X"), ("Value#1", "Separate XYZ.001", "Y"), )),
    "Math.001": ("ShaderNodeMath", (218.0, 202.12), None, (("Value", "Math", "Value"), ("Value#1", "Math.002", "Value"), )),
    "Math.002": ("ShaderNodeMath", (11.73, 124.73), None, (("Value", "Separate XYZ", "Y"), ("Value#1", "Separate XYZ.001", "X"), )),
    "Math.017": ("ShaderNodeMath", (434.72, 44.6), None, (("Value", "Math.001", "Value"), ("Value#1", "Vector Math", "Value"), )),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (-212.13, 215.37), None, (("Vector", "Group Input", "Vector"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (-211.24, 76.27), None, (("Vector", "Group Input", "Vector#1"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-194.06, -76.77), None, (("Vector", "Group Input", "Vector"), ("Vector#1", "Group Input", "Vector#1"), )),
}