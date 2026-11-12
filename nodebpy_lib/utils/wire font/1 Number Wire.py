from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("1 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (0.0, 0.26, 0.0), (-0.1, 0.2, 0.0), (-0.1, 0.0, 0.0), (0.1, 0.0, 0.0)))
    mesh_line = g.MeshLine(count=2, start_location=(-0.1, 0.0, 0.0), offset=(0.1, 0.0, 0.0)).props(hide=True)
    (
        g.JoinGeometry((g.MeshLine(count=3, offset=(1.0, 0.0, 0.0)), mesh_line))
        >> g.SetPosition(position=index_switch)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (543.06, 0.0), None, (("Geometry", "Set Position.002", "Geometry"), )),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (-237.37, -156.79), None, (("Index", "Index.001", "Index"), )),
    "Index.001": ("GeometryNodeInputIndex", (-520.67, -212.87), None, ()),
    "Join Geometry.001": ("GeometryNodeJoinGeometry", (71.61, 138.54), None, (("Geometry", "Mesh Line.004", "Mesh"), ("Geometry", "Mesh Line.005", "Mesh"), )),
    "Mesh Line.004": ("GeometryNodeMeshLine", (-93.23, -18.85), None, ()),
    "Mesh Line.005": ("GeometryNodeMeshLine", (-249.67, 187.16), None, ()),
    "Set Position.002": ("GeometryNodeSetPosition", (275.38, 5.58), None, (("Geometry", "Join Geometry.001", "Geometry"), ("Position", "Index Switch.001", "Output"), )),
}