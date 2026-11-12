from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Object Type", arrange=None, clear=True) as tree:
    object_geometry = tree.inputs.geometry("Object Geometry")
    type = tree.outputs.integer("Type")

    sample_index = g.SampleIndex.point.boolean(object_geometry, g.NamedAttribute.vector("CP_curve").props(width=100.0).o.exists)
    sample_index_1 = g.SampleIndex.point.boolean(object_geometry, g.NamedAttribute.vector("CP_NURBS_surf").props(width=119.54).o.exists)
    sample_index_2 = g.SampleIndex.point.boolean(object_geometry, g.NamedAttribute.vector("CP_any_order_surf").props(width=148.77).o.exists)
    sample_index_3 = g.SampleIndex.point.boolean(object_geometry, g.NamedAttribute.vector("CP_planar").props(width=100.0).o.exists)
    switch = g.Switch.integer(false=sample_index_3.o.value.switch.integer(g.Integer(14).props(label="Default")), true=1)
    switch_1 = g.Switch.integer(false=g.Switch.integer(false=g.Switch.integer(false=switch, true=2), true=3), true=4)
    switch_2 = sample_index_1.o.value.switch.integer(sample_index_2.o.value.switch.integer(switch_1, 5), 6)
    switch_3 = g.Switch.integer(false=g.Switch.integer(false=g.Switch.integer(false=switch_2, true=7), true=8), true=9)
    switch_4 = g.Switch.integer(false=g.Switch.integer(false=sample_index.o.value.switch.integer(switch_3, 10), true=11), true=12)
    switch_5 = g.Switch.integer(false=switch_4, true=13)

    switch_5 >> type

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-79.81, 285.15), None, ()),
    "Group Output": ("NodeGroupOutput", (1310.05, -53.88), None, (("Type", "Switch.013", "Output"), )),
    "Integer": ("FunctionNodeInputInt", (260.27, 679.01), None, ()),
    "Named Attribute.003": ("GeometryNodeInputNamedAttribute", (-111.09, -891.52), None, ()),
    "Named Attribute.004": ("GeometryNodeInputNamedAttribute", (-150.3, -80.14), None, ()),
    "Named Attribute.005": ("GeometryNodeInputNamedAttribute", (-106.55, 116.72), None, ()),
    "Named Attribute.006": ("GeometryNodeInputNamedAttribute", (-127.28, -307.13), None, ()),
    "Sample Index.001": ("GeometryNodeSampleIndex", (172.72, -791.83), None, (("Geometry", "Group Input", "Object Geometry"), ("Value", "Named Attribute.003", "Exists"), )),
    "Sample Index.002": ("GeometryNodeSampleIndex", (170.72, -280.46), None, (("Geometry", "Group Input", "Object Geometry"), ("Value", "Named Attribute.006", "Exists"), )),
    "Sample Index.004": ("GeometryNodeSampleIndex", (170.72, -79.16), None, (("Geometry", "Group Input", "Object Geometry"), ("Value", "Named Attribute.004", "Exists"), )),
    "Sample Index.005": ("GeometryNodeSampleIndex", (179.26, 404.05), None, (("Geometry", "Group Input", "Object Geometry"), ("Value", "Named Attribute.005", "Exists"), )),
    "Switch": ("GeometryNodeSwitch", (559.49, 448.14), None, (("False", "Switch.001", "Output"), )),
    "Switch.001": ("GeometryNodeSwitch", (559.49, 599.45), None, (("False", "Switch.003", "Output"), )),
    "Switch.002": ("GeometryNodeSwitch", (559.49, 296.82), None, (("False", "Switch", "Output"), )),
    "Switch.003": ("GeometryNodeSwitch", (559.49, 750.77), None, (("False", "Integer", "Integer"), ("Switch", "Sample Index.005", "Value"), )),
    "Switch.004": ("GeometryNodeSwitch", (559.49, -157.14), None, (("False", "Switch.005", "Output"), ("Switch", "Sample Index.002", "Value"), )),
    "Switch.005": ("GeometryNodeSwitch", (559.49, -5.82), None, (("False", "Switch.006", "Output"), ("Switch", "Sample Index.004", "Value"), )),
    "Switch.006": ("GeometryNodeSwitch", (559.49, 145.5), None, (("False", "Switch.002", "Output"), )),
    "Switch.007": ("GeometryNodeSwitch", (559.49, -308.46), None, (("False", "Switch.004", "Output"), )),
    "Switch.008": ("GeometryNodeSwitch", (559.49, -762.41), None, (("False", "Switch.009", "Output"), ("Switch", "Sample Index.001", "Value"), )),
    "Switch.009": ("GeometryNodeSwitch", (559.49, -611.1), None, (("False", "Switch.010", "Output"), )),
    "Switch.010": ("GeometryNodeSwitch", (559.49, -459.78), None, (("False", "Switch.007", "Output"), )),
    "Switch.011": ("GeometryNodeSwitch", (559.49, -913.73), None, (("False", "Switch.008", "Output"), )),
    "Switch.013": ("GeometryNodeSwitch", (559.49, -1216.37), None, (("False", "Switch.014", "Output"), )),
    "Switch.014": ("GeometryNodeSwitch", (559.49, -1065.05), None, (("False", "Switch.011", "Output"), )),
}