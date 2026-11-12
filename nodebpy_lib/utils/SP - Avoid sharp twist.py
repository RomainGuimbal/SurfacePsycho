from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Avoid sharp twist", arrange=None, clear=True) as tree:
    enable = tree.inputs.boolean("Enable", False)
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
    vector_1 = tree.outputs.vector("Vector")

    reroute = g.Reroute(input=vector).props(width=19.0)
    accumulate_field = g.AccumulateField.point.integer(reroute.o.output.dot(vector.point.at(g.Index().o.index - 1)) < 0.0)
    boolean_math = (g.Reroute(input=enable).props(width=19.0).o.output & accumulate_field.o.leading % 2.0).props(hide=True)
    (
        g.Reroute(input=reroute.o.output).props(width=19.0).o.output * boolean_math.switch.float(1.0, -1.0)
        >> vector_1
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field": ("GeometryNodeAccumulateField", (34.84, -57.02), None, (("Value", "Compare", "Result"), )),
    "Boolean Math": ("FunctionNodeBooleanMath", (427.34, -57.02), None, (("Boolean", "Reroute.003", "Output"), ("Boolean#1", "Math.002", "Value"), )),
    "Compare": ("FunctionNodeCompare", (-155.16, -57.02), None, (("A", "Vector Math", "Value"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (-547.66, -57.02), None, (("Index", "Integer Math", "Value"), ("Value", "Group Input", "Vector"), )),
    "Group Input": ("NodeGroupInput", (-752.39, 75.22), None, ()),
    "Group Output": ("NodeGroupOutput", (997.34, 14.19), None, (("Vector", "Vector Math.010", "Vector"), )),
    "Index.001": ("GeometryNodeInputIndex", (-940.16, -131.07), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (-747.78, -86.21), None, (("Value", "Index.001", "Index"), )),
    "Math.002": ("ShaderNodeMath", (224.84, -57.02), None, (("Value", "Accumulate Field", "Leading"), )),
    "Reroute.001": ("NodeReroute", (-407.66, 19.51), None, (("Input", "Group Input", "Vector"), )),
    "Reroute.003": ("NodeReroute", (367.82, 44.91), None, (("Input", "Group Input", "Enable"), )),
    "Reroute.004": ("NodeReroute", (757.34, 19.51), None, (("Input", "Reroute.001", "Output"), )),
    "Switch": ("GeometryNodeSwitch", (617.34, -57.02), None, (("Switch", "Boolean Math", "Boolean"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-345.16, -57.02), None, (("Vector", "Reroute.001", "Output"), ("Vector#1", "Evaluate at Index", "Value"), )),
    "Vector Math.010": ("ShaderNodeVectorMath", (807.34, 14.19), None, (("Scale", "Switch", "Output"), ("Vector", "Reroute.004", "Output"), )),
}