from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Disc CP", arrange=None, clear=True) as tree:
    radius = tree.inputs.float("Radius", 0.0, min_value=-10_000.0, max_value=10_000.0)
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), (g.CombineXYZ(radius), (0.0, 0.0, 0.0), g.CombineXYZ(y=radius)))
    (
        ((g.MeshLine(3) >> g.StoreNamedAttribute.point.integer(name="Type", value=3)).props(width=140.0) >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=g.IndexSwitch.boolean(g.Index(), (True, False, True)))).props(width=140.0)
        >> g.SetPosition(position=index_switch)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Combine XYZ.001": ("ShaderNodeCombineXYZ", (-124.7, 49.87), None, (("X", "Group Input", "Radius"), )),
    "Combine XYZ.002": ("ShaderNodeCombineXYZ", (-124.7, -113.28), None, (("Y", "Group Input", "Radius"), )),
    "Group Input": ("NodeGroupInput", (-333.53, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (1172.89, -31.01), None, (("Geometry", "Set Position.001", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-133.53, 113.28), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (133.53, 79.71), None, (("0", "Combine XYZ.001", "Vector"), ("2", "Combine XYZ.002", "Vector"), ("Index", "Index", "Index"), )),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (297.7, 392.32), None, (("Index", "Index.001", "Index"), )),
    "Index.001": ("GeometryNodeInputIndex", (102.22, 327.37), None, ()),
    "Mesh Line": ("GeometryNodeMeshLine", (113.95, 630.35), None, ()),
    "Set Position.001": ("GeometryNodeSetPosition", (762.33, 213.03), None, (("Geometry", "Store Named Attribute.001", "Geometry"), ("Position", "Index Switch", "Output"), )),
    "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (307.8, 598.77), None, (("Geometry", "Mesh Line", "Mesh"), )),
    "Store Named Attribute.001": ("GeometryNodeStoreNamedAttribute", (520.29, 569.77), None, (("Geometry", "Store Named Attribute", "Geometry"), ("Value", "Index Switch.001", "Output"), )),
}