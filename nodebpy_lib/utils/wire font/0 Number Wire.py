from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("0 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.2, 0.0), (0.1, 0.06, 0.0), (0.09, 0.03, 0.0), (0.065, 0.01, 0.0), (0.03, 0.0, 0.0), (-0.03, 0.0, 0.0), (-0.065, 0.01, 0.0), (-0.09, 0.03, 0.0), (-0.1, 0.06, 0.0), (-0.1, 0.2, 0.0), (-0.09, 0.23, 0.0), (-0.065, 0.25, 0.0), (-0.03, 0.26, 0.0), (0.03, 0.26, 0.0), (0.065, 0.25, 0.0), (0.09, 0.23, 0.0)))
    set_position = g.SetPosition(geometry=g.MeshCircle(16), position=index_switch)
    viewer = g.Viewer()
    viewer.items.geometry(set_position, "Geometry")

    set_position >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (543.06, 0.0), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (-177.37, 130.98), None, (("Index", "Index", "Index"), )),
    "Mesh Circle": ("GeometryNodeMeshCircle", (23.09, 157.8), None, ()),
    "Set Position": ("GeometryNodeSetPosition", (353.06, -56.03), None, (("Geometry", "Mesh Circle", "Mesh"), ("Position", "Index Switch", "Output"), )),
    "Viewer": ("GeometryNodeViewer", (514.29, 124.18), None, (("Geometry", "Set Position", "Geometry"), )),
}