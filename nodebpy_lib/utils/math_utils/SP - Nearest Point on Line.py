from nodebpy import TreeBuilder

with TreeBuilder("SP - Nearest Point on Line", arrange=None, clear=True) as tree:
    position_to_project = tree.inputs.vector("Position to Project", (0.0, 0.0, 0.0))
    with tree.inputs.panel("Line"):
        point = tree.inputs.vector("Point", (0.0, 0.0, 0.0), hide_value=True)
        direction = tree.inputs.vector("Direction", (0.0, 0.0, 0.0), hide_value=True)
    projected_position = tree.outputs.vector("Projected Position")
    distance = tree.outputs.float("Distance")

    vector_math = direction.dot((position_to_project - point).props(width=100.0, hide=True)).props(hide=True)
    vector_math_1 = (direction * (vector_math / direction.dot(direction).props(hide=True)).props(label="Normalize")).props(hide=True)
    vector_math_2 = (vector_math_1 + point).props(hide=True)
    position_to_project.distance(vector_math_2) >> distance

    vector_math_2 >> projected_position

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-621.18, 174.87), None, ()),
    "Group Output": ("NodeGroupOutput", (753.74, 89.01), None, (("Distance", "Vector Math", "Value"), ("Projected Position", "Vector Math.008", "Vector"), )),
    "Math.001": ("ShaderNodeMath", (-20.07, -9.76), None, (("Value", "Vector Math.009", "Value"), ("Value#1", "Vector Math.002", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (551.88, 240.63), None, (("Vector", "Group Input", "Position to Project"), ("Vector#1", "Vector Math.008", "Vector"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (-379.44, -123.08), None, (("Vector", "Group Input", "Direction"), ("Vector#1", "Group Input", "Direction"), )),
    "Vector Math.007": ("ShaderNodeVectorMath", (166.27, 97.65), None, (("Scale", "Math.001", "Value"), ("Vector", "Group Input", "Direction"), )),
    "Vector Math.008": ("ShaderNodeVectorMath", (356.67, 137.12), None, (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Group Input", "Point"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (-216.26, -18.06), None, (("Vector", "Group Input", "Direction"), ("Vector#1", "Vector Math.012", "Vector"), )),
    "Vector Math.012": ("ShaderNodeVectorMath", (-405.32, -8.3), None, (("Vector", "Group Input", "Position to Project"), ("Vector#1", "Group Input", "Point"), )),
}