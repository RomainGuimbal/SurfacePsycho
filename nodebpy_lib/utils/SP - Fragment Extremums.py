from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Fragment Extremums", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry", description="Geometry to sort the elements of")
    value = tree.inputs.float("Value", 0.5, min_value=-10_000.0, max_value=10_000.0)
    value_1 = tree.inputs.boolean("Value", False)
    min = tree.outputs.float("Min")
    max = tree.outputs.float("Max")

    with g.Frame():
        index = g.Index()
        math_1 = (value * value_1).props(hide=True)
        sample_index = (
            (geometry >> g.SortElements.point(sort_weight=(0.0 - math_1).props(hide=True))).props(hide=True)
            >> g.SampleIndex.point.float(value=math_1, index=index.o.index - 1)
        )
        switch = g.Compare.integer.equal(index, 0).o.result.switch.float(sample_index, 1.0)
        switch.point.at(g.Index().o.index + 1) >> min

    switch >> max

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare": ("FunctionNodeCompare", (246.78, -29.92), "Frame.002", (("A", "Index", "Index"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (884.5, -124.45), "Frame.002", (("Index", "Integer Math.002", "Value"), ("Value", "Switch", "Output"), )),
    "Frame.002": ("NodeFrame", (-420.35, 244.06), None, ()),
    "Group Input": ("NodeGroupInput", (-620.22, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (790.38, 8.06), None, (("Max", "Switch", "Output"), ("Min", "Evaluate at Index", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (30.03, -117.26), "Frame.002", ()),
    "Index.001": ("GeometryNodeInputIndex", (464.76, -488.27), "Frame.002", ()),
    "Integer Math.001": ("FunctionNodeIntegerMath", (247.47, -193.04), "Frame.002", (("Value", "Index", "Index"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (648.72, -429.86), "Frame.002", (("Value", "Index.001", "Index"), )),
    "Math": ("ShaderNodeMath", (269.06, -486.82), "Frame.002", (("Value", "Group Input", "Value"), ("Value#1", "Group Input", "Value#1"), )),
    "Math.001": ("ShaderNodeMath", (268.24, -442.11), "Frame.002", (("Value#1", "Math", "Value"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (465.69, -283.38), "Frame.002", (("Geometry", "Sort Elements", "Geometry"), ("Index", "Integer Math.001", "Value"), ("Value", "Math", "Value"), )),
    "Sort Elements": ("GeometryNodeSortElements", (273.39, -391.42), "Frame.002", (("Geometry", "Group Input", "Geometry"), ("Sort Weight", "Math.001", "Value"), )),
    "Switch": ("GeometryNodeSwitch", (672.89, -222.45), "Frame.002", (("False", "Sample Index", "Value"), ("Switch", "Compare", "Result"), )),
}