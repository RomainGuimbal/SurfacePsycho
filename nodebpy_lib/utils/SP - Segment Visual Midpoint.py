from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Segment Visual Midpoint", arrange=None, clear=True) as tree:
    segment = tree.inputs.geometry("Segment")
    midpoint = tree.outputs.vector("Midpoint")

    domain_size = g.DomainSize(segment).props(hide=True, hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
    integer_math = (domain_size.o.point_count - 1).props(hide=True)
    integer_math_1 = integer_math // 2
    position = g.Position()
    sample_index = g.SampleIndex.point.vector(segment, position, integer_math_1).props(hide=True)
    sample_index_1 = g.SampleIndex.point.vector(segment, position, (integer_math_1 + 1).props(hide=True)).props(hide=True)
    switch = g.Switch.vector(g.IntegerMath.modulo(integer_math, 2), sample_index, g.Mix.vector(0.5, sample_index, sample_index_1, clamp_factor=False).props(hide=True).o.result_vector)

    switch >> midpoint

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Domain Size": ("GeometryNodeAttributeDomainSize", (-365.39, -73.56), None, (("Geometry", "Group Input", "Segment"), )),
    "Group Input": ("NodeGroupInput", (-611.52, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (632.41, 0.0), None, (("Midpoint", "Switch", "Output"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (-209.18, -151.94), None, (("Value", "Integer Math.003", "Value"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-2.06, -188.43), None, (("Value", "Integer Math", "Value"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (-208.56, -16.2), None, (("Value", "Integer Math.003", "Value"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (-364.54, -117.02), None, (("Value", "Domain Size", "Point Count"), )),
    "Mix": ("ShaderNodeMix", (400.54, -17.53), None, (("A#1", "Sample Index", "Value"), ("B#1", "Sample Index.001", "Value"), )),
    "Position": ("GeometryNodeInputPosition", (9.15, -35.51), None, ()),
    "Sample Index": ("GeometryNodeSampleIndex", (203.65, 28.09), None, (("Geometry", "Group Input", "Segment"), ("Index", "Integer Math", "Value"), ("Value", "Position", "Position"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (203.6, -17.64), None, (("Geometry", "Group Input", "Segment"), ("Index", "Integer Math.001", "Value"), ("Value", "Position", "Position"), )),
    "Switch": ("GeometryNodeSwitch", (402.35, 141.47), None, (("False", "Sample Index", "Value"), ("Switch", "Integer Math.002", "Value"), ("True", "Mix", "Result#1"), )),
}