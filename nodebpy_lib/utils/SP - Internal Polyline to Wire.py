from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Internal Polyline to Wire", arrange=None, clear=True) as tree:
    curve = tree.inputs.geometry("Curve", description="Curve to convert to a mesh using the given profile")
    geometry = tree.outputs.geometry("Geometry")

    (
        (curve >> g.CurveToMesh() >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=True)).props(width=140.0)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Curve to Mesh.001": ("GeometryNodeCurveToMesh", (-81.49, -14.64), None, (("Curve", "Group Input", "Curve"), )),
    "Group Input": ("NodeGroupInput", (-281.49, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (271.49, 0.0), None, (("Geometry", "Store Named Attribute", "Geometry"), )),
    "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (81.49, 14.64), None, (("Geometry", "Curve to Mesh.001", "Mesh"), )),
}