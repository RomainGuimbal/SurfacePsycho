from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Evaluate Ellipse at Parameter", arrange=None, clear=True) as tree:
    scaled_basis = tree.inputs.matrix("Scaled Basis")
    parameter = tree.inputs.float("Parameter", 0.5, description="Pseudo angle", min_value=-10_000.0, max_value=10_000.0)
    vector = tree.outputs.vector("Vector", subtype="XYZ")

    combine_xyz = g.CombineXYZ(x=parameter.cos().props(hide=True), y=parameter.sin().props(hide=True)).props(hide_inputs=["Z"])
    combine_xyz.o.vector.transform(scaled_basis) >> vector

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Combine XYZ.001": ("ShaderNodeCombineXYZ", (179.59, -53.11), None, (("X", "Math.011", "Value"), ("Y", "Math.005", "Value"), )),
    "Group Input": ("NodeGroupInput", (-220.79, -9.61), None, ()),
    "Group Output": ("NodeGroupOutput", (544.09, 0.6), None, (("Vector", "Transform Point.001", "Vector"), )),
    "Math.005": ("ShaderNodeMath", (14.63, -123.25), None, (("Value", "Group Input", "Parameter"), )),
    "Math.011": ("ShaderNodeMath", (12.91, -89.82), None, (("Value", "Group Input", "Parameter"), )),
    "Transform Point.001": ("FunctionNodeTransformPoint", (368.69, 16.34), None, (("Transform", "Group Input", "Scaled Basis"), ("Vector", "Combine XYZ.001", "Vector"), )),
}