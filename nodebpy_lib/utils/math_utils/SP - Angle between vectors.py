from nodebpy import TreeBuilder

with TreeBuilder("SP - Angle between vectors", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
    vector_1 = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
    angle = tree.outputs.float("Angle", subtype="ANGLE")

    (vector.dot(vector_1) / (vector.length() * vector_1.length())).acos() >> angle

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-465.35, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (444.9, -4.38), None, (("Angle", "Math.016", "Value"), )),
    "Math": ("ShaderNodeMath", (-94.95, -88.15), None, (("Value", "Vector Math", "Value"), ("Value#1", "Vector Math.011", "Value"), )),
    "Math.001": ("ShaderNodeMath", (114.47, 20.88), None, (("Value", "Vector Math.016", "Value"), ("Value#1", "Math", "Value"), )),
    "Math.016": ("ShaderNodeMath", (272.72, 15.82), None, (("Value", "Math.001", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-257.83, -81.87), None, (("Vector", "Group Input", "Vector"), )),
    "Vector Math.011": ("ShaderNodeVectorMath", (-261.88, -193.32), None, (("Vector", "Group Input", "Vector#1"), )),
    "Vector Math.016": ("ShaderNodeVectorMath", (-93.61, 51.92), None, (("Vector", "Group Input", "Vector"), ("Vector#1", "Group Input", "Vector#1"), )),
}