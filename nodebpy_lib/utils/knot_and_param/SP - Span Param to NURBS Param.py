from nodebpy import TreeBuilder

with TreeBuilder("SP - Span Param to NURBS Param", arrange=None, clear=True) as tree:
    segment_parameter = tree.inputs.float("Segment Parameter", 0.0)
    span_range = tree.inputs.float("Span Range", 0.5, min_value=-10_000.0, max_value=10_000.0)
    offset = tree.inputs.float("Offset", 0.5, min_value=-10_000.0, max_value=10_000.0)
    total_range = tree.inputs.float("Total Range", 0.5, description="Curve param range or knot ?", min_value=-10_000.0, max_value=10_000.0)
    wire_parameter = tree.outputs.float("Wire Parameter")

    (segment_parameter * span_range + offset) / total_range >> wire_parameter

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-444.44, 17.01), None, ()),
    "Group Output": ("NodeGroupOutput", (314.44, 36.58), None, (("Wire Parameter", "Math", "Value"), )),
    "Math": ("ShaderNodeMath", (99.17, 63.1), None, (("Value", "Math.001", "Value"), ("Value#1", "Group Input", "Total Range"), )),
    "Math.001": ("ShaderNodeMath", (-89.85, 106.58), None, (("Value", "Math.002", "Value"), ("Value#1", "Group Input", "Offset"), )),
    "Math.002": ("ShaderNodeMath", (-252.0, 122.29), None, (("Value", "Group Input", "Segment Parameter"), ("Value#1", "Group Input", "Span Range"), )),
}