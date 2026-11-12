from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Transpose Matrix", arrange=None, clear=True) as tree:
    m = tree.inputs.integer("m", 0)
    n = tree.inputs.integer("n", 0)
    matrix = tree.inputs.float("Matrix", 0.0, hide_value=True)
    n_1 = tree.outputs.integer("n")
    m_1 = tree.outputs.integer("m")
    matrix_1 = tree.outputs.float("Matrix")

    index = g.Index()
    integer_math = (((index.o.index % m).props(label="U", hide=True) * n).props(hide=True) + (index.o.index // m).props(hide=True)).props(hide=True)
    matrix.point.at(integer_math).props(label="M Transposed") >> matrix_1

    n >> n_1
    m >> m_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (758.83, -164.12), None, (("Index", "Integer Math.001", "Value"), ("Value", "Group Input", "Matrix"), )),
    "Group Input": ("NodeGroupInput", (-268.72, -54.23), None, ()),
    "Group Output": ("NodeGroupOutput", (996.14, -100.15), None, (("Matrix", "Evaluate at Index", "Value"), ("m", "Group Input", "m"), ("n", "Group Input", "n"), )),
    "Index.004": ("GeometryNodeInputIndex", (-1.49, 100.77), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (467.79, 64.91), None, (("Value", "Integer Math.002", "Value"), ("Value#1", "Group Input", "n"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (469.74, 12.9), None, (("Value", "Integer Math", "Value"), ("Value#1", "Integer Math.004", "Value"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (195.83, 59.78), None, (("Value", "Index.004", "Index"), ("Value#1", "Group Input", "m"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (192.68, 21.58), None, (("Value", "Index.004", "Index"), ("Value#1", "Group Input", "m"), )),
}