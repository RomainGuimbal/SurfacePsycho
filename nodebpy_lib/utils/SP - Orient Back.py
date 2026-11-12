from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Orient Back", arrange=None, clear=True) as tree:
    input = tree.inputs.geometry("Input")
    orient = tree.inputs.boolean("Orient", False)
    offset = tree.inputs.vector("Offset", (0.0, 0.0, 0.0), subtype="TRANSLATION")
    normal = tree.inputs.vector("Normal", (0.0, 0.0, 1.0))
    output = tree.outputs.geometry("Output")

    reroute = g.Reroute(input=input).props(width=19.0, hide=True)
    transform_geometry = g.TransformGeometry(geometry=reroute, translation=offset, rotation=g.AlignRotationToVector(vector=normal)).props(width=140.0)
    orient.switch.geometry(reroute, transform_geometry) >> output

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Align Rotation to Vector": ("FunctionNodeAlignRotationToVector", (-184.72, -116.29), None, (("Vector", "Group Input", "Normal"), )),
    "Group Input": ("NodeGroupInput", (-430.7, 53.79), None, ()),
    "Group Output": ("NodeGroupOutput", (361.6, 79.1), None, (("Output", "Switch.012", "Output"), )),
    "Reroute.044": ("NodeReroute", (-97.51, -10.82), None, (("Input", "Group Input", "Input"), )),
    "Switch.012": ("GeometryNodeSwitch", (170.45, 101.84), None, (("False", "Reroute.044", "Output"), ("Switch", "Group Input", "Orient"), ("True", "Transform Geometry.011", "Geometry"), )),
    "Transform Geometry.011": ("GeometryNodeTransform", (-1.9, -10.34), None, (("Geometry", "Reroute.044", "Output"), ("Rotation", "Align Rotation to Vector", "Rotation"), ("Translation", "Group Input", "Offset"), )),
}