from nodebpy import TreeBuilder

with TreeBuilder("Colwise reverse", arrange=None, clear=True, collapse=True) as tree:
    index_u = tree.inputs.integer("Index U", 0, description="Column of vertex (0,1,2,0,1,2...)")
    index_v = tree.inputs.integer("Index V", 0, description="Row of vertex (0,0,0,1,1,1...)")
    u_count = tree.inputs.integer("U Count", 0)
    index = tree.outputs.integer("Index")

    (
        ((u_count * (u_count - 1 - index_v)).props(width=100.0) + index_u).props(width=100.0)
        >> index
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-391.03, -45.42), None, ()),
    "Group Output": ("NodeGroupOutput", (364.98, -52.87), None, (("Index", "Integer Math.024", "Value"), )),
    "Integer Math.019": ("FunctionNodeIntegerMath", (234.05, -108.51), None, (("Value", "Group Input", "U Count"), ("Value#1", "Integer Math.028", "Value"), )),
    "Integer Math.024": ("FunctionNodeIntegerMath", (232.72, -68.89), None, (("Value", "Integer Math.019", "Value"), ("Value#1", "Group Input", "Index U"), )),
    "Integer Math.028": ("FunctionNodeIntegerMath", (49.04, -134.17), None, (("Value", "Integer Math.031", "Value"), ("Value#1", "Group Input", "Index V"), )),
    "Integer Math.031": ("FunctionNodeIntegerMath", (-124.47, -58.88), None, (("Value", "Group Input", "U Count"), )),
}