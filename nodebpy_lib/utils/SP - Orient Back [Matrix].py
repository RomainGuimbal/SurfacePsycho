from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Orient Back [Matrix]", arrange=None, clear=True) as tree:
    input = tree.inputs.geometry("Input")
    orient = tree.inputs.boolean("Orient", False)
    transform = tree.inputs.matrix("Transform")
    output = tree.outputs.geometry("Output")

    reroute = g.Reroute(input=input).props(width=19.0, hide=True)
    transform_geometry = g.TransformGeometry(geometry=reroute, transform=transform, mode="Matrix", translation=(0.0, 0.02, 0.001))
    orient.switch.geometry(reroute, transform_geometry) >> output

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-430.7, 53.79), None, ()),
    "Group Output": ("NodeGroupOutput", (361.6, 79.1), None, (("Output", "Switch.012", "Output"), )),
    "Reroute.044": ("NodeReroute", (-97.51, -10.82), None, (("Input", "Group Input", "Input"), )),
    "Switch.012": ("GeometryNodeSwitch", (170.45, 101.84), None, (("False", "Reroute.044", "Output"), ("Switch", "Group Input", "Orient"), ("True", "Transform Geometry.002", "Geometry"), )),
    "Transform Geometry.002": ("GeometryNodeTransform", (-29.05, -31.42), None, (("Geometry", "Reroute.044", "Output"), ("Transform", "Group Input", "Transform"), )),
}