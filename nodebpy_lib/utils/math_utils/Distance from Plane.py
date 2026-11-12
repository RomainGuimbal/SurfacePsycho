from nodebpy import TreeBuilder

with TreeBuilder("Distance from Plane", arrange=None, clear=True) as tree:
    point = tree.inputs.vector("Point", (0.0, 0.0, 0.0))
    plane_normal = tree.inputs.vector("Plane Normal", (0.0, 0.0, 0.0), hide_value=True)
    plane_point = tree.inputs.vector("Plane Point", (0.0, 0.0, 0.0), hide_value=True)
    signed_distance = tree.outputs.float("Signed Distance")
    distance = tree.outputs.float("Distance")

    vector_math = plane_normal.dot(point - plane_point)
    abs(vector_math) >> distance

    vector_math >> signed_distance

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-361.59, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (416.45, -7.76), None, (("Distance", "Math", "Value"), ("Signed Distance", "Vector Math", "Value"), )),
    "Math": ("ShaderNodeMath", (222.5, -72.86), None, (("Value", "Vector Math", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (51.22, 29.4), None, (("Vector", "Group Input", "Plane Normal"), ("Vector#1", "Vector Math.001", "Vector"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (-156.86, -81.54), None, (("Vector", "Group Input", "Point"), ("Vector#1", "Group Input", "Plane Point"), )),
}