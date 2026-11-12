from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Common Point of 2 Segments", arrange=None, clear=True) as tree:
    segment_1 = tree.inputs.geometry("Segment 1")
    segment_2 = tree.inputs.geometry("Segment 2")
    max_distance = tree.inputs.float("Max Distance", 0.0, min_value=-10_000.0, max_value=10_000.0, subtype="DISTANCE")
    are_connected = tree.outputs.boolean("Are Connected")
    index_on_segment_1 = tree.outputs.integer("Index on Segment 1")
    index_on_segment_2 = tree.outputs.integer("Index on Segment 2")

    with g.Frame("Edge 1"):
        domain_size = g.DomainSize(segment_1).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        integer_math = (domain_size.o.point_count - 1).props(hide=True)
        position = g.Position()
        reroute = g.Reroute(input=segment_1).props(width=19.0)
        sample_index = g.SampleIndex.point.vector(reroute, position)
        sample_index_1 = g.SampleIndex.point.vector(reroute, position, integer_math)
    with g.Frame("Edge 2"):
        domain_size_1 = g.DomainSize(segment_2).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        integer_math_1 = (domain_size_1.o.point_count - 1).props(hide=True)
        position_1 = g.Position()
        reroute_1 = g.Reroute(input=segment_2).props(width=19.0)
        sample_index_2 = g.SampleIndex.point.vector(reroute_1, position_1)
        sample_index_3 = g.SampleIndex.point.vector(reroute_1, position_1, integer_math_1)
    with g.Frame():
        vector_math = sample_index.o.value.distance(sample_index_2)
        vector_math_1 = sample_index_1.o.value.distance(sample_index_2)
        math_1 = vector_math.min(vector_math_1)
        vector_math_2 = sample_index.o.value.distance(sample_index_3)
        math_2 = vector_math.min(vector_math_2)
        vector_math_3 = sample_index_1.o.value.distance(sample_index_3)
        math_3 = vector_math_2.min(vector_math_3)
        math_4 = vector_math_1.min(vector_math_3)
    with g.Frame():
        (math_1 > math_3).switch.integer(true=integer_math_1) >> index_on_segment_2
        (math_2 > math_4).switch.integer(true=integer_math) >> index_on_segment_1
    with g.Frame():
        compare = g.Compare.float.not_equal(math_1.min(math_3), 0.0, max_distance)
        ~compare.o.result >> are_connected
        _warning = g.Warning.warning(compare, "Segments NOT connected").props(width=245.62)

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (446.27, -190.46), "Frame.002", (("Boolean", "Compare.002", "Result"), )),
    "Compare.002": ("FunctionNodeCompare", (215.27, -31.4), "Frame.002", (("A", "Math.002", "Value"), ("Epsilon", "Group Input", "Max Distance"), )),
    "Compare.005": ("FunctionNodeCompare", (30.32, -236.36), "Frame.004", (("A", "Math", "Value"), ("B", "Math.001", "Value"), )),
    "Compare.007": ("FunctionNodeCompare", (38.01, -30.18), "Frame.004", (("A", "Math.003", "Value"), ("B", "Math.004", "Value"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (30.18, -357.62), "Frame", (("Geometry", "Group Input", "Segment 1"), )),
    "Domain Size.001": ("GeometryNodeAttributeDomainSize", (30.25, -358.96), "Frame.001", (("Geometry", "Group Input", "Segment 2"), )),
    "Frame": ("NodeFrame", (-846.53, 522.56), None, ()),
    "Frame.001": ("NodeFrame", (-851.29, -41.79), None, ()),
    "Frame.002": ("NodeFrame", (470.12, 633.71), None, ()),
    "Frame.003": ("NodeFrame", (-146.65, 344.12), None, ()),
    "Frame.004": ("NodeFrame", (511.94, 99.53), None, ()),
    "Group Input": ("NodeGroupInput", (-1226.0, -6.05), None, ()),
    "Group Output": ("NodeGroupOutput", (1284.92, 119.27), None, (("Are Connected", "Boolean Math", "Boolean"), ("Index on Segment 1", "Switch.001", "Output"), ("Index on Segment 2", "Switch", "Output"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (211.33, -442.69), "Frame", (("Value", "Domain Size", "Point Count"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (208.35, -468.74), "Frame.001", (("Value", "Domain Size.001", "Point Count"), )),
    "Math": ("ShaderNodeMath", (275.58, -380.42), "Frame.003", (("Value", "Vector Math.001", "Value"), ("Value#1", "Vector Math.003", "Value"), )),
    "Math.001": ("ShaderNodeMath", (276.0, -538.11), "Frame.003", (("Value", "Vector Math.005", "Value"), ("Value#1", "Vector Math.006", "Value"), )),
    "Math.002": ("ShaderNodeMath", (29.99, -30.28), "Frame.002", (("Value", "Math", "Value"), ("Value#1", "Math.001", "Value"), )),
    "Math.003": ("ShaderNodeMath", (268.69, -29.93), "Frame.003", (("Value", "Vector Math.001", "Value"), ("Value#1", "Vector Math.005", "Value"), )),
    "Math.004": ("ShaderNodeMath", (269.11, -187.62), "Frame.003", (("Value", "Vector Math.003", "Value"), ("Value#1", "Vector Math.006", "Value"), )),
    "Position": ("GeometryNodeInputPosition", (186.39, -269.06), "Frame", ()),
    "Position.001": ("GeometryNodeInputPosition", (188.26, -272.02), "Frame.001", ()),
    "Reroute.001": ("NodeReroute", (322.46, -252.16), "Frame", (("Input", "Group Input", "Segment 1"), )),
    "Reroute.002": ("NodeReroute", (330.9, -253.94), "Frame.001", (("Input", "Group Input", "Segment 2"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (413.21, -36.21), "Frame", (("Geometry", "Reroute.001", "Output"), ("Value", "Position", "Position"), )),
    "Sample Index.002": ("GeometryNodeSampleIndex", (413.21, -254.45), "Frame", (("Geometry", "Reroute.001", "Output"), ("Index", "Integer Math", "Value"), ("Value", "Position", "Position"), )),
    "Sample Index.003": ("GeometryNodeSampleIndex", (412.47, -35.78), "Frame.001", (("Geometry", "Reroute.002", "Output"), ("Value", "Position.001", "Position"), )),
    "Sample Index.004": ("GeometryNodeSampleIndex", (412.47, -252.95), "Frame.001", (("Geometry", "Reroute.002", "Output"), ("Index", "Integer Math.005", "Value"), ("Value", "Position.001", "Position"), )),
    "Switch": ("GeometryNodeSwitch", (250.84, -271.54), "Frame.004", (("Switch", "Compare.005", "Result"), ("True", "Integer Math.005", "Value"), )),
    "Switch.001": ("GeometryNodeSwitch", (254.82, -94.39), "Frame.004", (("Switch", "Compare.007", "Result"), ("True", "Integer Math", "Value"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (30.03, -56.04), "Frame.003", (("Vector", "Sample Index.001", "Value"), ("Vector#1", "Sample Index.003", "Value"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (30.03, -204.4), "Frame.003", (("Vector", "Sample Index.002", "Value"), ("Vector#1", "Sample Index.003", "Value"), )),
    "Vector Math.005": ("ShaderNodeVectorMath", (30.03, -352.22), "Frame.003", (("Vector", "Sample Index.001", "Value"), ("Vector#1", "Sample Index.004", "Value"), )),
    "Vector Math.006": ("ShaderNodeVectorMath", (30.03, -499.51), "Frame.003", (("Vector", "Sample Index.002", "Value"), ("Vector#1", "Sample Index.004", "Value"), )),
    "Warning.001": ("GeometryNodeWarning", (501.89, -65.04), "Frame.002", (("Show", "Compare.002", "Result"), )),
}