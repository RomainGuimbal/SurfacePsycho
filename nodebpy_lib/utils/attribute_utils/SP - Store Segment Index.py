from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Store Segment Index", arrange=None, clear=True) as tree:
    uv_mesh = tree.inputs.geometry("UV Mesh")
    contour = tree.inputs.geometry("Contour")
    uv_mesh_1 = tree.outputs.geometry("UV Mesh")

    sample_index = g.SampleIndex.edge.integer(contour, g.NamedAttribute.integer("segment_id").o.attribute, g.Index())
    (
        (uv_mesh >> g.StoreNamedAttribute.edge.integer(name="segment_id", value=sample_index.o.value.point.at(g.SampleNearest.edge(contour)))).props(width=140.0)
        >> uv_mesh_1
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (101.11, 25.54), None, (("Index", "Sample Nearest", "Index"), ("Value", "Sample Index.005", "Value"), )),
    "Group Input": ("NodeGroupInput", (-298.07, 105.8), None, ()),
    "Group Output": ("NodeGroupOutput", (502.59, 72.64), None, (("UV Mesh", "Store Named Attribute.001", "Geometry"), )),
    "Index.001": ("GeometryNodeInputIndex", (-284.08, -300.17), None, ()),
    "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (-288.98, -145.37), None, ()),
    "Sample Index.005": ("GeometryNodeSampleIndex", (-72.63, 25.44), None, (("Geometry", "Group Input", "Contour"), ("Index", "Index.001", "Index"), ("Value", "Named Attribute.002", "Attribute"), )),
    "Sample Nearest": ("GeometryNodeSampleNearest", (-71.61, -194.43), None, (("Geometry", "Group Input", "Contour"), )),
    "Store Named Attribute.001": ("GeometryNodeStoreNamedAttribute", (282.24, 146.29), None, (("Geometry", "Group Input", "UV Mesh"), ("Value", "Evaluate at Index.001", "Value"), )),
}