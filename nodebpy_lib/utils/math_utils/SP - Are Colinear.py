from nodebpy import TreeBuilder

with TreeBuilder("SP - Are Colinear", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
    vector_1 = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
    tolerence = tree.inputs.float("Tolerence", 0.00001, min_value=-10_000.0, max_value=10_000.0)
    result = tree.outputs.boolean("Result")

    vector_math = vector.cross(vector_1).props(hide=True)
    math_1 = (vector.dot(vector).props(hide=True) * vector_1.dot(vector_1).props(hide=True)).props(hide=True)
    (
        (vector_math.dot(vector_math).props(hide=True) <= (tolerence * math_1).props(hide=True))
        >> result
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare": ("FunctionNodeCompare", (361.07, 144.54), None, (("A", "Vector Math.002", "Value"), ("B", "Math.001", "Value"), )),
    "Group Input": ("NodeGroupInput", (-592.1, 59.69), None, ()),
    "Group Output": ("NodeGroupOutput", (544.65, 135.52), None, (("Result", "Compare", "Result"), )),
    "Math": ("ShaderNodeMath", (-107.37, -98.16), None, (("Value", "Vector Math.004", "Value"), ("Value#1", "Vector Math.005", "Value"), )),
    "Math.001": ("ShaderNodeMath", (101.78, -44.94), None, (("Value", "Group Input", "Tolerence"), ("Value#1", "Math", "Value"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (-67.57, 69.74), None, (("Vector", "Vector Math.003", "Vector"), ("Vector#1", "Vector Math.003", "Vector"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (-239.73, 64.94), None, (("Vector", "Group Input", "Vector"), ("Vector#1", "Group Input", "Vector#1"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (-275.46, -74.62), None, (("Vector", "Group Input", "Vector"), ("Vector#1", "Group Input", "Vector"), )),
    "Vector Math.005": ("ShaderNodeVectorMath", (-275.2, -116.95), None, (("Vector", "Group Input", "Vector#1"), ("Vector#1", "Group Input", "Vector#1"), )),
}