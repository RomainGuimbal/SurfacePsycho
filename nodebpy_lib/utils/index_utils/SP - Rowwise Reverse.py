from nodebpy import TreeBuilder

with TreeBuilder("SP - Rowwise Reverse", arrange=None, clear=True, collapse=True) as tree:
    u_count = tree.inputs.integer("U Count", 0)
    v_count = tree.inputs.integer("V Count", 0)
    index = tree.inputs.integer("Index", 0, min_value=0, hide_value=True, default_input="INDEX")
    index_1 = tree.outputs.integer("Index")

    (
        (v_count - 1 - index % u_count + (v_count * (index // u_count)).props(width=100.0)).props(width=100.0)
        >> index_1
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-306.08, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (465.71, 14.96), None, (("Index", "Integer Math.024", "Value"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (-79.34, -46.3), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-79.34, -85.31), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
    "Integer Math.019": ("FunctionNodeIntegerMath", (174.61, -78.93), None, (("Value", "Group Input", "V Count"), ("Value#1", "Integer Math.001", "Value"), )),
    "Integer Math.024": ("FunctionNodeIntegerMath", (318.61, -49.08), None, (("Value", "Integer Math.029", "Value"), ("Value#1", "Integer Math.019", "Value"), )),
    "Integer Math.029": ("FunctionNodeIntegerMath", (133.11, -15.53), None, (("Value", "Integer Math.031", "Value"), ("Value#1", "Integer Math", "Value"), )),
    "Integer Math.031": ("FunctionNodeIntegerMath", (-73.19, 4.65), None, (("Value", "Group Input", "V Count"), )),
}