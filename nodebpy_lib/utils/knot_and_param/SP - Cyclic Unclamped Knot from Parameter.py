from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Cyclic Unclamped Knot from Parameter", arrange=None, clear=True) as tree:
    parameter = tree.inputs.float("Parameter", 0.0)
    virtual_point_count = tree.inputs.integer("Virtual Point Count", 1)
    degree = tree.inputs.integer("Degree", 0)
    knot = tree.outputs.float("Knot")

    index = g.Index()
    integer_math = index.o.index % virtual_point_count
    math_1 = (parameter.point.at((integer_math + 1).props(hide=True)) - parameter.point.at(integer_math)).props(hide=True)
    evaluate_at_index = math_1.point.at((index.o.index + (degree + 4)) % virtual_point_count).props(width=134.48, hide=True)
    evaluate_at_index.point.leading() >> knot
    viewer = g.Viewer()
    viewer.items.geometry(g.MeshLine(), "Mesh")
    viewer.items.float(evaluate_at_index, "Value")

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field": ("GeometryNodeAccumulateField", (1377.07, 37.69), None, (("Value", "Evaluate at Index.008", "Value"), )),
    "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (769.83, 72.38), None, (("Index", "Integer Math.001", "Value"), ("Value", "Group Input", "Parameter"), )),
    "Evaluate at Index.007": ("GeometryNodeFieldAtIndex", (765.64, -57.5), None, (("Index", "Integer Math.005", "Value"), ("Value", "Group Input", "Parameter"), )),
    "Evaluate at Index.008": ("GeometryNodeFieldAtIndex", (1152.27, -95.07), None, (("Index", "Integer Math.006", "Value"), ("Value", "Math.001", "Value"), )),
    "Group Input": ("NodeGroupInput", (-103.71, 3.05), None, ()),
    "Group Output": ("NodeGroupOutput", (1660.16, -8.45), None, (("Knot", "Accumulate Field", "Leading"), )),
    "Index": ("GeometryNodeInputIndex", (149.27, -230.75), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (442.64, -261.06), None, (("Value", "Index", "Index"), ("Value#1", "Integer Math.002", "Value"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (591.46, -55.14), None, (("Value", "Integer Math.005", "Value"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (152.09, -293.24), None, (("Value", "Group Input", "Degree"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (421.98, -103.02), None, (("Value", "Index", "Index"), ("Value#1", "Group Input", "Virtual Point Count"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (833.96, -229.64), None, (("Value", "Integer Math", "Value"), ("Value#1", "Group Input", "Virtual Point Count"), )),
    "Math.001": ("ShaderNodeMath", (961.22, -89.12), None, (("Value", "Evaluate at Index.006", "Value"), ("Value#1", "Evaluate at Index.007", "Value"), )),
    "Mesh Line": ("GeometryNodeMeshLine", (1171.15, 282.95), None, ()),
    "Viewer": ("GeometryNodeViewer", (1381.0, 226.71), None, (("Mesh", "Mesh Line", "Mesh"), ("Value", "Evaluate at Index.008", "Value"), )),
}