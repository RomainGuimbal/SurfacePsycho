from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Smooth Shading Pass Through", arrange=None, clear=True) as tree:
    new = tree.inputs.geometry("New")
    reference = tree.inputs.geometry("Reference")
    new_1 = tree.outputs.geometry("New")

    (
        new
        >> g.SetShadeSmooth.face(shade_smooth=g.SampleIndex.face.boolean(reference, g.IsFaceSmooth()))
        >> new_1
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-270.37, 82.15), None, ()),
    "Group Output": ("NodeGroupOutput", (404.18, 0.0), None, (("New", "Set Shade Smooth", "Mesh"), )),
    "Is Shade Smooth": ("GeometryNodeInputShadeSmooth", (-134.03, -101.32), None, ()),
    "Sample Index": ("GeometryNodeSampleIndex", (43.12, 29.36), None, (("Geometry", "Group Input", "Reference"), ("Value", "Is Shade Smooth", "Smooth"), )),
    "Set Shade Smooth": ("GeometryNodeSetShadeSmooth", (214.18, 128.42), None, (("Mesh", "Group Input", "New"), ("Shade Smooth", "Sample Index", "Value"), )),
}