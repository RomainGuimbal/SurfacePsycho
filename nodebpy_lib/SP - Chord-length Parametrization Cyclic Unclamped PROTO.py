from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Chord-length Parametrization Cyclic Unclamped PROTO", arrange=None, clear=True) as tree:
    segment_cp = tree.inputs.geometry("Segment CP")
    degree = tree.inputs.integer("Degree", 5)
    value = tree.outputs.float("Value")

    edge_vertices = g.EdgeVertices()
    sample_index = g.SampleIndex.edge.float(segment_cp, edge_vertices.o.position_1.distance(edge_vertices.o.position_2), (g.Index().o.index - degree) % g.DomainSize(segment_cp).o.point_count)
    accumulate_field = g.AccumulateField.point.float(sample_index)
    (
        (accumulate_field.o.leading / accumulate_field.o.total).props(mute=True).point.at(g.Index().o.index - 1)
        >> value
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field.001": ("GeometryNodeAccumulateField", (1773.77, 51.1), None, (("Value", "Sample Index", "Value"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (1046.65, -393.26), None, (("Geometry", "Group Input", "Segment CP"), )),
    "Edge Vertices": ("GeometryNodeInputMeshEdgeVertices", (1224.8, -93.21), None, ()),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (2197.47, -6.44), None, (("Index", "Integer Math.004", "Value"), ("Value", "Math", "Value"), )),
    "Group Input": ("NodeGroupInput", (662.17, -38.74), None, ()),
    "Group Output": ("NodeGroupOutput", (2388.36, -26.44), None, (("Value", "Evaluate at Index", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (1784.29, -191.92), None, ()),
    "Index.004": ("GeometryNodeInputIndex", (1045.55, -308.18), None, ()),
    "Integer Math.001": ("FunctionNodeIntegerMath", (1243.94, -222.28), None, (("Value", "Index.004", "Index"), ("Value#1", "Group Input", "Degree"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (1401.11, -234.29), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Domain Size", "Point Count"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (1956.03, -136.75), None, (("Value", "Index", "Index"), )),
    "Math": ("ShaderNodeMath", (1945.52, 51.13), None, (("Value", "Accumulate Field.001", "Leading"), ("Value#1", "Accumulate Field.001", "Total"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (1603.48, 40.79), None, (("Geometry", "Group Input", "Segment CP"), ("Index", "Integer Math.002", "Value"), ("Value", "Vector Math", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (1397.33, -90.56), None, (("Vector", "Edge Vertices", "Position 1"), ("Vector#1", "Edge Vertices", "Position 2"), )),
}