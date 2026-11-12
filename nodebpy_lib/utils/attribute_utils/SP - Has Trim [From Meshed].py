from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Has Trim [From Meshed]", arrange=None, clear=True) as tree:
    meshed_geom = tree.inputs.geometry("Meshed Geom")
    has_trim = tree.outputs.boolean("Has Trim")

    (
        (meshed_geom >> g.SampleIndex.point.boolean(value=g.NamedAttribute.vector("CP_trim_contour_UV").props(width=138.88).o.exists)).props(label="no wire index case")
        >> has_trim
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (280.62, 69.19), None, ()),
    "Group Output": ("NodeGroupOutput", (728.02, 66.82), None, (("Has Trim", "Sample Index.003", "Value"), )),
    "Named Attribute.007": ("GeometryNodeInputNamedAttribute", (299.23, -20.36), None, ()),
    "Sample Index.003": ("GeometryNodeSampleIndex", (540.45, 106.99), None, (("Geometry", "Group Input", "Meshed Geom"), ("Value", "Named Attribute.007", "Exists"), )),
}