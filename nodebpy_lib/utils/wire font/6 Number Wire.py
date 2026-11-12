from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("6 Number Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    reroute = g.Reroute(input=g.Index().o.index).props(width=100.0)
    index_switch = g.IndexSwitch.vector(reroute, ((0.1, 0.26, 0.0), (0.055, 0.26, 0.0), (-0.01000001, 0.23, 0.0), (-0.06, 0.18, 0.0), (-0.09, 0.1, 0.0), (-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.03, 0.0, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.03, 0.0), (0.1, 0.06, 0.0), (0.1, 0.1, 0.0), (0.075, 0.125, 0.0), (0.03, 0.14, 0.0), (-0.075, 0.14, 0.0)))
    _index_switch_1 = g.IndexSwitch.vector(reroute, ((-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.030000005, 0.00000000745058, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.02999999, 0.0), (0.1, 0.07000002, 0.0), (0.1, 0.12, 0.0), (0.075, 0.155, 0.0), (0.03, 0.17, 0.0), (-0.06, 0.17, 0.0)))
    g.MeshLine(16) >> g.SetPosition(position=index_switch) >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Output": ("NodeGroupOutput", (984.48, 69.44), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (163.52, -51.53), None, (("Index", "Reroute", "Output"), )),
    "Index Switch.002": ("GeometryNodeIndexSwitch", (318.72, -479.02), None, (("Index", "Reroute", "Output"), )),
    "Mesh Line": ("GeometryNodeMeshLine", (510.17, 311.32), None, ()),
    "Reroute": ("NodeReroute", (119.19, -117.13), None, (("Input", "Index", "Index"), )),
    "Set Position": ("GeometryNodeSetPosition", (794.48, 13.41), None, (("Geometry", "Mesh Line", "Mesh"), ("Position", "Index Switch.001", "Output"), )),
}