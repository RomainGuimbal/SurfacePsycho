from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Move UVMap to Point Domain", arrange=None, clear=True) as tree:
    inverted = tree.inputs.geometry("Inverted", description="The parts of the geometry not in the selection")
    geometry = tree.outputs.geometry("Geometry")

    evaluate_at_index = g.NamedAttribute.vector("UVMap").o.attribute.corner.at(g.CornersOfVertex().props(hide=True).o.corner_index)
    capture = g.CaptureAttribute.point(geometry=inverted)
    value = capture.items.vector(evaluate_at_index, "Value")
    (
        capture.o.geometry
        >> g.RemoveNamedAttribute(name="UVMap")
        >> g.StoreNamedAttribute.point.vector(name="UVMap", value=value.output)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Capture Attribute": ("GeometryNodeCaptureAttribute", (-21.62, 33.7), None, (("Geometry", "Group Input", "Inverted"), ("Value", "Evaluate at Index.005", "Value"), )),
    "Corners of Vertex.001": ("GeometryNodeCornersOfVertex", (-369.04, -102.28), None, ()),
    "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (-188.23, 20.31), None, (("Index", "Corners of Vertex.001", "Corner Index"), ("Value", "Named Attribute.002", "Attribute"), )),
    "Group Input": ("NodeGroupInput", (-601.24, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (614.47, 0.0), None, (("Geometry", "Store Named Attribute", "Geometry"), )),
    "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (-371.32, 36.93), None, ()),
    "Remove Named Attribute": ("GeometryNodeRemoveAttribute", (147.58, 14.08), None, (("Geometry", "Capture Attribute", "Geometry"), )),
    "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (364.19, 27.98), None, (("Geometry", "Remove Named Attribute", "Geometry"), ("Value", "Capture Attribute", "Value"), )),
}