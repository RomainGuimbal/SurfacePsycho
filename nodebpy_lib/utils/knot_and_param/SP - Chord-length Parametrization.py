from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Chord-length Parametrization", arrange=None, clear=True) as tree:
    segment_cp = tree.inputs.geometry("Segment CP")
    value = tree.outputs.float("Value")

    edge_vertices = g.EdgeVertices()
    accumulate_field = g.AccumulateField.edge.float(edge_vertices.o.position_1.distance(edge_vertices.o.position_2))
    math_1 = accumulate_field.o.leading / accumulate_field.o.total
    evaluate_on_domain = g.SampleIndex.edge.float(segment_cp, math_1, (g.Index().o.index - 1).props(hide=True)).o.value.point.evaluate()
    (
        evaluate_on_domain.min(1.0).props(label="Clamp slight overshoot", width=173.22)
        >> value
    )
    viewer = g.Viewer(domain="EDGE")
    viewer.items.geometry(segment_cp, "Segment CP")
    viewer.items.float(math_1, "Value")

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field": ("GeometryNodeAccumulateField", (-201.42, 128.67), None, (("Value", "Vector Math", "Value"), )),
    "Edge Vertices": ("GeometryNodeInputMeshEdgeVertices", (-544.02, 56.65), None, ()),
    "Evaluate on Domain": ("GeometryNodeFieldOnDomain", (338.11, 17.95), None, (("Value", "Sample Index", "Value"), )),
    "Group Input": ("NodeGroupInput", (-754.85, -53.24), None, ()),
    "Group Output": ("NodeGroupOutput", (774.95, -0.58), None, (("Value", "Math.001", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (-166.54, -112.1), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (4.32, -116.21), None, (("Value", "Index", "Index"), )),
    "Math": ("ShaderNodeMath", (-31.63, 82.17), None, (("Value", "Accumulate Field", "Leading"), ("Value#1", "Accumulate Field", "Total"), )),
    "Math.001": ("ShaderNodeMath", (507.58, 26.79), None, (("Value", "Evaluate on Domain", "Value"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (166.96, 50.3), None, (("Geometry", "Group Input", "Segment CP"), ("Index", "Integer Math", "Value"), ("Value", "Math", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-371.49, 59.29), None, (("Vector", "Edge Vertices", "Position 1"), ("Vector#1", "Edge Vertices", "Position 2"), )),
    "Viewer": ("GeometryNodeViewer", (143.53, 215.84), None, (("Segment CP", "Group Input", "Segment CP"), ("Value", "Math", "Value"), )),
}