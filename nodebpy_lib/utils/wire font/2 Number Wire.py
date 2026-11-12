from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("2 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.0, 0.0), (-0.1, 0.0, 0.0), (-0.09, 0.05, 0.0), (-0.065, 0.085, 0.0), (0.065, 0.145, 0.0), (0.09, 0.17, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0)))
    g.MeshLine(13) >> g.SetPosition(position=index_switch) >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (543.06, 0.0), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (-60.33, -78.6), None, (("Index", "Index", "Index"), )),
    "Mesh Line": ("GeometryNodeMeshLine", (68.75, 241.88), None, ()),
    "Set Position": ("GeometryNodeSetPosition", (353.06, -56.03), None, (("Geometry", "Mesh Line", "Mesh"), ("Position", "Index Switch.001", "Output"), )),
}