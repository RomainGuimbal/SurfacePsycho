from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Is Mesh Grid", arrange=None, clear=True) as tree:
    input = tree.inputs.geometry("Input")
    output = tree.outputs.boolean("Output")

    vertex_neighbors = g.VertexNeighbors()
    boolean_math = (g.Compare.integer.equal(vertex_neighbors.o.vertex_count, 2).o.result & (vertex_neighbors.o.face_count >= 1)).props(hide=True)
    float_to_integer = g.FloatToInteger(float=g.AttributeStatistic.point.float(input, boolean_math, g.Value(1.0)).o.sum, rounding_mode="FLOOR")
    g.Compare.integer.equal(float_to_integer, 4) >> output

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Attribute Statistic": ("GeometryNodeAttributeStatistic", (354.1, -36.33), None, (("Attribute", "Value", "Value"), ("Geometry", "Group Input", "Input"), ("Selection", "Boolean Math", "Boolean"), )),
    "Boolean Math": ("FunctionNodeBooleanMath", (157.51, -334.01), None, (("Boolean", "Compare", "Result"), ("Boolean#1", "Compare.001", "Result"), )),
    "Compare": ("FunctionNodeCompare", (-59.95, -295.19), None, (("A", "Vertex Neighbors", "Vertex Count"), )),
    "Compare.001": ("FunctionNodeCompare", (-67.17, -454.59), None, (("A", "Vertex Neighbors", "Face Count"), )),
    "Compare.002": ("FunctionNodeCompare", (715.26, -118.84), None, (("A", "Float to Integer", "Integer"), )),
    "Float to Integer": ("FunctionNodeFloatToInt", (544.31, -135.52), None, (("Float", "Attribute Statistic", "Sum"), )),
    "Group Input": ("NodeGroupInput", (-396.03, -210.07), None, ()),
    "Group Output": ("NodeGroupOutput", (927.63, -98.13), None, (("Output", "Compare.002", "Result"), )),
    "Value": ("ShaderNodeValue", (158.5, -378.55), None, ()),
    "Vertex Neighbors": ("GeometryNodeInputMeshVertexNeighbors", (-294.45, -409.03), None, ()),
}