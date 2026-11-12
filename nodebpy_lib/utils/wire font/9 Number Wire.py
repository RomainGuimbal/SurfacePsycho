from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("9 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.09, 0.06, 0.0), (-0.08, 0.03, 0.0), (-0.05, 0.01, 0.0), (-0.015, 0.0, 0.0), (0.065, 0.0, 0.0), (0.09, 0.019999996, 0.0), (0.1, 0.05000001, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0), (-0.1, 0.19, 0.0), (-0.09, 0.16, 0.0), (-0.07, 0.145, 0.0), (-0.04000001, 0.14, 0.0), (0.1, 0.14, 0.0)))
    _index_switch_1 = g.IndexSwitch.vector(items=((-0.09, 0.06, 0.0), (-0.08, 0.03, 0.0), (-0.05, 0.01, 0.0), (-0.015, 0.0, 0.0), (0.065, 0.0, 0.0), (0.1, 0.07, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0)))
    g.MeshLine(19) >> g.SetPosition(position=index_switch) >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (984.48, 69.44), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
    "Index Switch.002": ("GeometryNodeIndexSwitch", (335.26, -157.25), None, (("Index", "Index", "Index"), )),
    "Index Switch.003": ("GeometryNodeIndexSwitch", (492.35, -244.89), None, ()),
    "Mesh Line": ("GeometryNodeMeshLine", (510.17, 311.32), None, ()),
    "Set Position": ("GeometryNodeSetPosition", (794.48, 13.41), None, (("Geometry", "Mesh Line", "Mesh"), ("Position", "Index Switch.002", "Output"), )),
}