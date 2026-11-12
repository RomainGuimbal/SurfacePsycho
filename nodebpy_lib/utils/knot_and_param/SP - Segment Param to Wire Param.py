from nodebpy import TreeBuilder

with TreeBuilder("SP - Segment Param to Wire Param", arrange=None, clear=True) as tree:
    segment_parameter = tree.inputs.float("Segment Parameter", 0.0)
    segment_count = tree.inputs.integer("Segment Count", 1)
    segment = tree.inputs.integer("Segment", 1, structure_type="SINGLE", force_non_field=True)
    wire_parameter = tree.outputs.float("Wire Parameter")

    (segment_parameter + segment) / segment_count >> wire_parameter

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-440.0, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (217.76, 36.58), None, (("Wire Parameter", "Math", "Value"), )),
    "Math": ("ShaderNodeMath", (2.49, 63.1), None, (("Value", "Math.001", "Value"), ("Value#1", "Group Input", "Segment Count"), )),
    "Math.001": ("ShaderNodeMath", (-186.16, 97.78), None, (("Value", "Group Input", "Segment Parameter"), ("Value#1", "Group Input", "Segment"), )),
}