from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Transfer Knot", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry", description="Geometry to store a new attribute with the given name on")
    from_ = tree.inputs.geometry("From")
    name = tree.inputs.string("Name", "Knot U", optional_label=True)
    name_1 = tree.inputs.string("Name", "Multiplicity U", optional_label=True)
    name_2 = tree.inputs.string("Name", "Knot", optional_label=True)
    name_3 = tree.inputs.string("Name", "Multiplicity", optional_label=True)
    geometry_1 = tree.outputs.geometry("Geometry")

    with g.Frame():
        reroute = g.Reroute(input=from_).props(width=19.0)
        sample_index = g.SampleIndex.point.integer(reroute, g.NamedAttribute.integer(name_1).o.attribute, g.Index())
        (
            ((geometry >> g.StoreNamedAttribute.point.float(name=name_2, value=g.SampleIndex.point.float(reroute, g.NamedAttribute.float(name).o.attribute, g.Index()))).props(width=140.0) >> g.StoreNamedAttribute.point.integer(name=name_3, value=sample_index)).props(width=140.0)
            >> geometry_1
        )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Frame": ("NodeFrame", (-268.41, 318.71), None, ()),
    "Group Input": ("NodeGroupInput", (-551.82, 234.35), None, ()),
    "Group Output": ("NodeGroupOutput", (740.53, 221.59), None, (("Geometry", "Store Named Attribute.001", "Geometry"), )),
    "Index.001": ("GeometryNodeInputIndex", (42.15, -410.04), "Frame", ()),
    "Index.002": ("GeometryNodeInputIndex", (54.04, -657.2), "Frame", ()),
    "Named Attribute": ("GeometryNodeInputNamedAttribute", (29.94, -261.67), "Frame", (("Name", "Group Input", "Name"), )),
    "Named Attribute.001": ("GeometryNodeInputNamedAttribute", (41.83, -508.84), "Frame", (("Name", "Group Input", "Name#1"), )),
    "Reroute.002": ("NodeReroute", (62.37, -160.54), "Frame", (("Input", "Group Input", "From"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (206.85, -185.28), "Frame", (("Geometry", "Reroute.002", "Output"), ("Index", "Index.001", "Index"), ("Value", "Named Attribute", "Attribute"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (218.74, -432.44), "Frame", (("Geometry", "Reroute.002", "Output"), ("Index", "Index.002", "Index"), ("Value", "Named Attribute.001", "Attribute"), )),
    "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (359.74, -80.79), "Frame", (("Geometry", "Group Input", "Geometry"), ("Name", "Group Input", "Name#2"), ("Value", "Sample Index", "Value"), )),
    "Store Named Attribute.001": ("GeometryNodeStoreNamedAttribute", (536.99, -30.43), "Frame", (("Geometry", "Store Named Attribute", "Geometry"), ("Name", "Group Input", "Name#3"), ("Value", "Sample Index.001", "Value"), )),
}