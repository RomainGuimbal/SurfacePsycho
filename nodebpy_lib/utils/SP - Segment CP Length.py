from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Segment CP Length", arrange=None, clear=True) as tree:
    total = tree.outputs.float("Total")

    edge_vertices = g.EdgeVertices()
    (
        edge_vertices.o.position_1.distance(edge_vertices.o.position_2).props(hide=True).edge.total()
        >> total
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field.001": ("GeometryNodeAccumulateField", (8.35, 61.91), None, (("Value", "Vector Math.002", "Value"), )),
    "Edge Vertices": ("GeometryNodeInputMeshEdgeVertices", (-324.98, 13.69), None, ()),
    "Group Output": ("NodeGroupOutput", (404.2, 0.0), None, (("Total", "Accumulate Field.001", "Total"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (-157.64, -66.35), None, (("Vector", "Edge Vertices", "Position 1"), ("Vector#1", "Edge Vertices", "Position 2"), )),
}