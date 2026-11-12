from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Grid UV Map", arrange=None, clear=True, is_modifier=True) as tree:
    u_count = tree.inputs.integer("U Count", 4, min_value=0)
    v_count = tree.inputs.integer("V Count", 4, min_value=0)
    index = tree.inputs.integer("Index", 0, min_value=0, default_input="INDEX")
    uv_map = tree.outputs.vector("UV Map")

    math_1 = ((index // u_count).props(hide=True) / (v_count - 1.0).props(hide=True)).props(hide=True)
    combine_xyz = g.CombineXYZ(x=((index % u_count).props(hide=True) / (u_count - 1.0).props(hide=True)).props(hide=True), y=math_1).props(hide_inputs=["Z"])

    combine_xyz >> uv_map

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Combine XYZ.001": ("ShaderNodeCombineXYZ", (138.22, 20.86), None, (("X", "Math.005", "Value"), ("Y", "Math.004", "Value"), )),
    "Group Input": ("NodeGroupInput", (-627.8, 56.92), None, ()),
    "Group Output": ("NodeGroupOutput", (323.83, 25.18), None, (("UV Map", "Combine XYZ.001", "Vector"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (-280.28, 42.67), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-285.93, 3.66), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
    "Math.004": ("ShaderNodeMath", (-45.13, -44.42), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Math.007", "Value"), )),
    "Math.005": ("ShaderNodeMath", (-39.09, -1.71), None, (("Value", "Integer Math", "Value"), ("Value#1", "Math.006", "Value"), )),
    "Math.006": ("ShaderNodeMath", (-282.77, -39.28), None, (("Value", "Group Input", "U Count"), )),
    "Math.007": ("ShaderNodeMath", (-281.34, -77.96), None, (("Value", "Group Input", "V Count"), )),
}