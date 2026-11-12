from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Retrieve FlatPatch Orientation", arrange=None, clear=True) as tree:
    meshed = tree.inputs.geometry("Meshed")
    object_rotation = tree.inputs.rotation("Object rotation", (0.0, 0.0, 0.0), structure_type="SINGLE", force_non_field=True)
    oriented = tree.outputs.boolean("Oriented")
    normal = tree.outputs.vector("Normal")
    offset = tree.outputs.vector("Offset")

    named_attribute = g.NamedAttribute.vector("planar_orient").props(width=196.25)
    named_attribute_1 = g.NamedAttribute.vector("planar_offset").props(width=196.25)
    reroute = g.Reroute(input=meshed).props(width=19.0)
    sample_index = g.SampleIndex.point.boolean(reroute, named_attribute.o.exists).props(hide=True)
    switch = sample_index.o.value.switch.vector((0.0, 0.0, 1.0), g.SampleIndex.point.vector(reroute, named_attribute.o.attribute).props(hide=True))
    switch.rotate(object_rotation) >> normal
    (
        g.SampleIndex.point.boolean(reroute, named_attribute_1.o.exists).props(hide=True).o.value.switch.vector((0.0, 0.0, 0.0), g.SampleIndex.point.vector(reroute, named_attribute_1.o.attribute).props(hide=True))
        >> offset
    )

    sample_index >> oriented

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-613.84, -24.1), None, ()),
    "Group Output": ("NodeGroupOutput", (524.69, -3.11), None, (("Normal", "Rotate Vector.002", "Vector"), ("Offset", "Switch.007", "Output"), ("Oriented", "Sample Index.001", "Value"), )),
    "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (-377.67, 102.26), None, ()),
    "Named Attribute.003": ("GeometryNodeInputNamedAttribute", (-369.12, -156.03), None, ()),
    "Reroute.018": ("NodeReroute", (-168.83, -59.9), None, (("Input", "Group Input", "Meshed"), )),
    "Rotate Vector.002": ("FunctionNodeRotateVector", (251.2, -31.63), None, (("Rotation", "Group Input", "Object rotation"), ("Vector", "Switch.006", "Output"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (-128.87, 47.58), None, (("Geometry", "Reroute.018", "Output"), ("Value", "Named Attribute.002", "Attribute"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (-131.63, -0.7), None, (("Geometry", "Reroute.018", "Output"), ("Value", "Named Attribute.002", "Exists"), )),
    "Sample Index.002": ("GeometryNodeSampleIndex", (-120.32, -210.71), None, (("Geometry", "Reroute.018", "Output"), ("Value", "Named Attribute.003", "Attribute"), )),
    "Sample Index.003": ("GeometryNodeSampleIndex", (-123.08, -258.99), None, (("Geometry", "Reroute.018", "Output"), ("Value", "Named Attribute.003", "Exists"), )),
    "Switch.006": ("GeometryNodeSwitch", (79.5, 132.37), None, (("Switch", "Sample Index.001", "Value"), ("True", "Sample Index", "Value"), )),
    "Switch.007": ("GeometryNodeSwitch", (88.05, -125.92), None, (("Switch", "Sample Index.003", "Value"), ("True", "Sample Index.002", "Value"), )),
}