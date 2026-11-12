from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("3 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.030000005, 0.00000000745058, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.02999999, 0.0), (0.1, 0.06000002, 0.0), (0.09, 0.1, 0.0), (0.055, 0.125, 0.0), (0.02, 0.13, 0.0), (0.055, 0.135, 0.0), (0.09, 0.16, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0)))
    g.MeshLine(19) >> g.SetPosition(position=index_switch) >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (984.48, 69.44), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (-60.33, -78.6), None, (("Index", "Index", "Index"), )),
    "Mesh Line": ("GeometryNodeMeshLine", (510.17, 311.32), None, ()),
    "Set Position": ("GeometryNodeSetPosition", (794.48, 13.41), None, (("Geometry", "Mesh Line", "Mesh"), ("Position", "Index Switch.001", "Output"), )),
}