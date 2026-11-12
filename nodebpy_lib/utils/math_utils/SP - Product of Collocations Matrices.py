from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Product of Collocations Matrices", arrange=None, clear=True) as tree:
    cp_count = tree.inputs.integer("CP Count", 0)
    t_count = tree.inputs.integer("t Count", 0)
    u_count = tree.inputs.integer("U Count", 0)
    basis_u = tree.inputs.float("Basis U", 0.0, hide_value=True)
    basis_v = tree.inputs.float("Basis V", 0.0, hide_value=True)
    basis_support = tree.outputs.geometry("Basis Support")
    value = tree.outputs.float("Value")

    index = g.Index()
    points = g.Points(count=(cp_count * t_count).props(hide=True), radius=0.0).props(hide=True)
    reroute = g.Reroute(input=u_count).props(width=19.0)
    integer_math = (((index.o.index // cp_count).props(hide=True) * reroute).props(hide=True) + (index.o.index % reroute).props(hide=True)).props(hide=True)
    math_1 = (basis_u.point.at(integer_math) * basis_v.point.at((index.o.index // reroute).props(hide=True))).props(hide=True)
    sample_index = g.SampleIndex.point.float(points, math_1, g.Index())

    points >> basis_support
    sample_index >> value

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (319.62, -36.58), None, (("Index", "Integer Math.015", "Value"), ("Value", "Group Input", "Basis U"), )),
    "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (319.95, -166.71), None, (("Index", "Integer Math.005", "Value"), ("Value", "Group Input", "Basis V"), )),
    "Group Input": ("NodeGroupInput", (-583.15, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (907.36, 103.57), None, (("Basis Support", "Points", "Points"), ("Value", "Sample Index.007", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (513.63, -170.72), None, ()),
    "Index.005": ("GeometryNodeInputIndex", (-523.39, -242.16), None, ()),
    "Integer Math.005": ("FunctionNodeIntegerMath", (73.48, -269.24), None, (("Value", "Index.005", "Index"), ("Value#1", "Reroute.025", "Output"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (223.67, 85.18), None, (("Value", "Group Input", "CP Count"), ("Value#1", "Group Input", "t Count"), )),
    "Integer Math.012": ("FunctionNodeIntegerMath", (-235.37, -70.52), None, (("Value", "Index.005", "Index"), ("Value#1", "Group Input", "CP Count"), )),
    "Integer Math.013": ("FunctionNodeIntegerMath", (-48.86, -120.14), None, (("Value", "Integer Math.012", "Value"), ("Value#1", "Reroute.025", "Output"), )),
    "Integer Math.014": ("FunctionNodeIntegerMath", (-47.68, -159.8), None, (("Value", "Index.005", "Index"), ("Value#1", "Reroute.025", "Output"), )),
    "Integer Math.015": ("FunctionNodeIntegerMath", (114.28, -143.21), None, (("Value", "Integer Math.013", "Value"), ("Value#1", "Integer Math.014", "Value"), )),
    "Math.002": ("ShaderNodeMath", (510.95, -125.17), None, (("Value", "Evaluate at Index", "Value"), ("Value#1", "Evaluate at Index.001", "Value"), )),
    "Points": ("GeometryNodePoints", (377.86, 81.16), None, (("Count", "Integer Math.007", "Value"), )),
    "Reroute.025": ("NodeReroute", (-108.9, -148.1), None, (("Input", "Group Input", "U Count"), )),
    "Sample Index.007": ("GeometryNodeSampleIndex", (700.21, 5.12), None, (("Geometry", "Points", "Points"), ("Index", "Index", "Index"), ("Value", "Math.002", "Value"), )),
}