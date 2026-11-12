from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("8 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index = g.Index()
    index_switch = g.IndexSwitch.vector(index, ((0.09, 0.09, 0.0), (0.1, 0.06, 0.0), (0.09, 0.03, 0.0), (0.065, 0.01, 0.0), (0.03, 0.0, 0.0), (-0.03, 0.0, 0.0), (-0.065, 0.01, 0.0), (-0.09, 0.03, 0.0), (-0.1, 0.06, 0.0), (-0.09, 0.09, 0.0), (-0.065, 0.115, 0.0), (0.065, 0.145, 0.0), (0.09, 0.17, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0), (-0.1, 0.2, 0.0), (-0.09, 0.17, 0.0), (-0.065, 0.145, 0.0), (0.065, 0.115, 0.0)))
    set_position = g.SetPosition(geometry=g.MeshCircle(24), position=index_switch)
    viewer = g.Viewer()
    viewer.items.geometry(set_position, "Geometry")
    viewer.items.integer(index, "Index")

    set_position >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (542.32, 10.34), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-202.91, 91.74), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (81.3, -3.16), None, (("Index", "Index", "Index"), )),
    "Mesh Circle": ("GeometryNodeMeshCircle", (80.54, 129.33), None, ()),
    "Set Position": ("GeometryNodeSetPosition", (344.62, 38.66), None, (("Geometry", "Mesh Circle", "Mesh"), ("Position", "Index Switch", "Output"), )),
    "Viewer": ("GeometryNodeViewer", (547.44, 140.2), None, (("Geometry", "Set Position", "Geometry"), ("Index", "Index", "Index"), )),
}