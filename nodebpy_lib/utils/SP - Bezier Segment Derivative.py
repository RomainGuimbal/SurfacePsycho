from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Bezier Segment Derivative", arrange=None, clear=True) as tree:
    position = tree.inputs.vector("Position", (0.0, 0.0, 0.0), default_input="POSITION")
    cp_count = tree.inputs.integer("CP count", 0)
    vector = tree.outputs.vector("Vector")
    cp_count_1 = tree.outputs.integer("CP count -1")

    integer_math = (cp_count - 1).props(hide=True)
    with g.Frame():
        reroute = g.Reroute(input=position).props(width=19.0)
        vector_math = (reroute.o.output.point.at((g.Index().o.index + 1).props(hide=True)) - reroute).props(label="P_i+1 - P_i")
        vector_math_1 = (vector_math * integer_math).props(label="*n")
    (
        (g.Index() < integer_math).props(hide=True).switch.vector((0.0, 0.0, 0.0), vector_math_1)
        >> vector
    )

    integer_math >> cp_count_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare": ("FunctionNodeCompare", (527.46, -20.81), None, (("A", "Index.001", "Index"), ("B", "Integer Math.001", "Value"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (206.13, -30.15), "Frame.001", (("Index", "Integer Math", "Value"), ("Value", "Reroute.001", "Output"), )),
    "Frame.001": ("NodeFrame", (92.12, 246.18), None, ()),
    "Group Input": ("NodeGroupInput", (-105.21, -17.57), None, ()),
    "Group Output": ("NodeGroupOutput", (1129.04, -25.14), None, (("CP count -1", "Integer Math.001", "Value"), ("Vector", "Switch.001", "Output"), )),
    "Index": ("GeometryNodeInputIndex", (30.43, -31.23), "Frame.001", ()),
    "Index.001": ("GeometryNodeInputIndex", (323.54, 0.25), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (30.06, -95.03), "Frame.001", (("Value", "Index", "Index"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (321.45, -68.67), None, (("Value", "Group Input", "CP count"), )),
    "Reroute.001": ("NodeReroute", (135.15, -181.49), "Frame.001", (("Input", "Group Input", "Position"), )),
    "Switch.001": ("GeometryNodeSwitch", (897.85, 147.84), None, (("Switch", "Compare", "Result"), ("True", "Vector Math.001", "Vector"), )),
    "Vector Math": ("ShaderNodeVectorMath", (363.98, -65.96), "Frame.001", (("Vector", "Evaluate at Index", "Value"), ("Vector#1", "Reroute.001", "Output"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (532.17, -67.49), "Frame.001", (("Scale", "Integer Math.001", "Value"), ("Vector", "Vector Math", "Vector"), )),
}