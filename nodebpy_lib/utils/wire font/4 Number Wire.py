from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("4 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (0.0, 0.13, 0.0), (0.0, 0.26, 0.0), (-0.1, 0.07, 0.0), (0.1, 0.07, 0.0)))
    (
        g.JoinGeometry((g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True), g.MeshLine(count=3, offset=(1.0, 0.0, 0.0))))
        >> g.SetPosition(position=index_switch)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (543.06, 0.0), None, (("Geometry", "Set Position.002", "Geometry"), )),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (-237.37, -156.79), None, (("Index", "Index.001", "Index"), )),
    "Index.001": ("GeometryNodeInputIndex", (-520.67, -212.87), None, ()),
    "Join Geometry.001": ("GeometryNodeJoinGeometry", (67.4, 173.39), None, (("Geometry", "Mesh Line.005", "Mesh"), ("Geometry", "Mesh Line.006", "Mesh"), )),
    "Mesh Line.005": ("GeometryNodeMeshLine", (-145.37, 189.5), None, ()),
    "Mesh Line.006": ("GeometryNodeMeshLine", (-141.68, 234.84), None, ()),
    "Set Position.002": ("GeometryNodeSetPosition", (275.38, 5.58), None, (("Geometry", "Join Geometry.001", "Geometry"), ("Position", "Index Switch.001", "Output"), )),
}