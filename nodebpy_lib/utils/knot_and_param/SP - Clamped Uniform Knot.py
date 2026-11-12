from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Clamped Uniform Knot", arrange=None, clear=True) as tree:
    p_count = tree.inputs.integer("P Count", 0, structure_type="SINGLE", force_non_field=True)
    degree = tree.inputs.integer("Degree", 0, structure_type="SINGLE", force_non_field=True)
    knot = tree.outputs.integer("Knot")

    index = g.Index()
    (
        (index > p_count + degree).switch.integer((index.o.index - degree).max(0).min(p_count - degree))
        >> knot
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare.001": ("FunctionNodeCompare", (396.6, -193.43), None, (("A", "Index.011", "Index"), ("B", "Integer Math.008", "Value"), )),
    "Group Input": ("NodeGroupInput", (-333.66, -61.94), None, ()),
    "Group Output": ("NodeGroupOutput", (867.05, 29.08), None, (("Knot", "Switch", "Output"), )),
    "Index.011": ("GeometryNodeInputIndex", (-50.01, 88.96), None, ()),
    "Integer Math.001": ("FunctionNodeIntegerMath", (316.66, 112.07), None, (("Value", "Integer Math.005", "Value"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (141.26, 115.84), None, (("Value", "Index.011", "Index"), ("Value#1", "Group Input", "Degree"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (487.85, 69.41), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Integer Math.007", "Value"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (314.7, -22.62), None, (("Value", "Group Input", "P Count"), ("Value#1", "Group Input", "Degree"), )),
    "Integer Math.008": ("FunctionNodeIntegerMath", (172.65, -232.8), None, (("Value", "Group Input", "P Count"), ("Value#1", "Group Input", "Degree"), )),
    "Switch": ("GeometryNodeSwitch", (680.32, 54.57), None, (("False", "Integer Math.006", "Value"), ("Switch", "Compare.001", "Result"), )),
}