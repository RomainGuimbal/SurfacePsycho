from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Cyclic-Clamped Uniform Knot", arrange=None, clear=True) as tree:
    p_count = tree.inputs.integer("P Count", 0, structure_type="SINGLE", force_non_field=True)
    degree = tree.inputs.integer("Degree", 0, structure_type="SINGLE", force_non_field=True)
    knot = tree.outputs.integer("Knot")

    index = g.Index()
    integer_math = g.IntegerMath(value=(index.o.index - degree).max(0).min(p_count - degree), value_001=index > 0)
    integer_math_1 = p_count + degree
    switch = g.Compare.integer.equal(index, integer_math_1).o.result.switch.integer(integer_math, integer_math.o.value + 1)
    (index > integer_math_1).switch.integer(switch) >> knot

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare": ("FunctionNodeCompare", (615.91, -332.57), None, (("A", "Index.011", "Index"), )),
    "Compare.001": ("FunctionNodeCompare", (622.1, -514.47), None, (("A", "Index.011", "Index"), ("B", "Integer Math.008", "Value"), )),
    "Compare.002": ("FunctionNodeCompare", (617.66, -672.02), None, (("A", "Index.011", "Index"), ("B", "Integer Math.008", "Value"), )),
    "Group Input": ("NodeGroupInput", (-333.66, -61.94), None, ()),
    "Group Output": ("NodeGroupOutput", (1741.43, -386.28), None, (("Knot", "Switch", "Output"), )),
    "Index.011": ("GeometryNodeInputIndex", (-50.01, 88.96), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (826.18, -244.68), None, (("Value", "Integer Math.006", "Value"), ("Value#1", "Compare", "Result"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (316.66, 112.07), None, (("Value", "Integer Math.005", "Value"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (1093.8, -252.22), None, (("Value", "Integer Math", "Value"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (141.26, 115.84), None, (("Value", "Index.011", "Index"), ("Value#1", "Group Input", "Degree"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (532.29, 73.65), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Integer Math.007", "Value"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (314.7, -22.62), None, (("Value", "Group Input", "P Count"), ("Value#1", "Group Input", "Degree"), )),
    "Integer Math.008": ("FunctionNodeIntegerMath", (377.52, -647.1), None, (("Value", "Group Input", "P Count"), ("Value#1", "Group Input", "Degree"), )),
    "Switch": ("GeometryNodeSwitch", (1501.79, -360.97), None, (("False", "Switch.001", "Output"), ("Switch", "Compare.001", "Result"), )),
    "Switch.001": ("GeometryNodeSwitch", (1306.09, -494.33), None, (("False", "Integer Math", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Integer Math.003", "Value"), )),
}