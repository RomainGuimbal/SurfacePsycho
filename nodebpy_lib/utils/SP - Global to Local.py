from nodebpy import TreeBuilder

with TreeBuilder("SP - Global to Local", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
    object_transform = tree.inputs.matrix("Object Transform")
    vector_1 = tree.outputs.vector("Vector")

    vector.transform(object_transform.invert()) >> vector_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-380.04, 115.87), None, ()),
    "Group Output": ("NodeGroupOutput", (208.7, 134.83), None, (("Vector", "Transform Point", "Vector"), )),
    "Invert Matrix": ("FunctionNodeInvertMatrix", (-189.94, 21.94), None, (("Matrix", "Group Input", "Object Transform"), )),
    "Transform Point": ("FunctionNodeTransformPoint", (1.49, 152.01), None, (("Transform", "Invert Matrix", "Matrix"), ("Vector", "Group Input", "Vector"), )),
}