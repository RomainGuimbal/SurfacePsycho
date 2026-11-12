from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Side Index of Grid Contour", arrange=None, clear=True) as tree:
    vertices_u = tree.inputs.integer("Vertices U", 0)
    vertices_v = tree.inputs.integer("Vertices V", 0)
    index_edge_attribute = tree.outputs.integer("Index (Edge Attribute)", attribute_domain="EDGE")

    index = g.Index()
    index_1 = g.Index()
    integer_math = vertices_u - 1
    integer_math_1 = (integer_math * 2).props(hide=True)
    integer_math_2 = (integer_math_1 + (vertices_v - 1)).props(hide=True)
    compare = g.Index() >= integer_math_2
    integer_math_3 = (g.IntegerMath.multiply((index >= integer_math) & (index < integer_math_1), 2).o.value + g.IntegerMath.multiply((index_1 >= integer_math_1) & (index_1 < integer_math_2), 3)).props(hide=True)
    integer_math_4 = g.IntegerMath(value=compare, value_001=integer_math_3).props(hide=True)
    viewer = g.Viewer()
    viewer.items.boolean(compare, "Result")

    integer_math_4 >> index_edge_attribute

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math.002": ("FunctionNodeBooleanMath", (-14.23, 112.06), None, (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
    "Boolean Math.003": ("FunctionNodeBooleanMath", (-8.05, -229.79), None, (("Boolean", "Compare.006", "Result"), ("Boolean#1", "Compare.007", "Result"), )),
    "Compare.002": ("FunctionNodeCompare", (-193.13, 334.35), None, (("A", "Index.003", "Index"), ("B", "Integer Math.008", "Value"), )),
    "Compare.004": ("FunctionNodeCompare", (-192.05, 169.01), None, (("A", "Index.004", "Index"), ("B", "Integer Math", "Value"), )),
    "Compare.005": ("FunctionNodeCompare", (-198.83, 7.5), None, (("A", "Index.004", "Index"), ("B", "Integer Math.007", "Value"), )),
    "Compare.006": ("FunctionNodeCompare", (-196.47, -169.87), None, (("A", "Index.005", "Index"), ("B", "Integer Math.007", "Value"), )),
    "Compare.007": ("FunctionNodeCompare", (-192.64, -334.35), None, (("A", "Index.005", "Index"), ("B", "Integer Math.008", "Value"), )),
    "Group Input": ("NodeGroupInput", (-982.67, -10.03), None, ()),
    "Group Output": ("NodeGroupOutput", (789.99, 104.86), None, (("Index (Edge Attribute)", "Integer Math.003", "Value"), )),
    "Index.003": ("GeometryNodeInputIndex", (-375.24, 240.28), None, ()),
    "Index.004": ("GeometryNodeInputIndex", (-382.67, 36.6), None, ()),
    "Index.005": ("GeometryNodeInputIndex", (-428.25, -407.86), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (-801.34, 47.03), None, (("Value", "Group Input", "Vertices U"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (-796.7, -99.67), None, (("Value", "Group Input", "Vertices V"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (600.79, 74.46), None, (("Value", "Compare.002", "Result"), ("Value#1", "Integer Math.005", "Value"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (147.53, 112.16), None, (("Value", "Boolean Math.002", "Boolean"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (349.93, -50.9), None, (("Value", "Integer Math.004", "Value"), ("Value#1", "Integer Math.012", "Value"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (-486.74, -143.53), None, (("Value", "Integer Math", "Value"), )),
    "Integer Math.008": ("FunctionNodeIntegerMath", (-427.56, -332.95), None, (("Value", "Integer Math.007", "Value"), ("Value#1", "Integer Math.002", "Value"), )),
    "Integer Math.012": ("FunctionNodeIntegerMath", (204.41, -147.4), None, (("Value", "Boolean Math.003", "Boolean"), )),
    "Viewer": ("GeometryNodeViewer", (-32.06, 364.88), None, (("Result", "Compare.002", "Result"), )),
}