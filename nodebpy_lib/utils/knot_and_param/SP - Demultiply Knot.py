from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Demultiply Knot", arrange=None, clear=True) as tree:
    unique_knot = tree.inputs.float("Unique Knot", 0.5, min_value=-10_000.0, max_value=10_000.0)
    multiplicity = tree.inputs.integer("Multiplicity", 0)
    multiplicity_length = tree.inputs.integer("Multiplicity Length", 23, min_value=0)
    knot = tree.outputs.float("Knot", 0.5, min_value=-10_000.0, max_value=10_000.0)

    with g.Frame("Mult always 1 (or 0 on tail)"):
        boolean_math = (g.Compare.integer.equal(multiplicity, 0).o.result | g.Compare.integer.equal(multiplicity, 1)).props(hide=True)
        compare = g.Compare.integer.equal(g.AccumulateField.point.integer((~boolean_math).props(hide=True)).o.total, 0)
    index = g.Index()
    repeat_zone = g.RepeatZone(multiplicity_length)
    repeat_zone.output.node.inspection_index = 1
    index_1 = repeat_zone.items.integer(name="Index")
    offset = repeat_zone.items.integer(name="Offset")
    integer_math = (offset.current + multiplicity.point.at(repeat_zone.iteration).max(1)).props(width=100.0, hide=True)
    boolean_math_1 = ((index >= offset.current).props(hide=True) & (index < integer_math).props(hide=True)).props(width=100.0, hide=True)
    (
        boolean_math_1.switch.integer(index_1.current, repeat_zone.iteration)
        >> index_1.next
    )
    integer_math >> offset.next
    (
        compare.o.result.switch.float(unique_knot.point.at(index_1.result), unique_knot).props(label="Skip")
        >> knot
    )
    viewer = g.Viewer()
    viewer.items.boolean(compare, "Result")

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field": ("GeometryNodeAccumulateField", (368.43, -46.17), "Frame.001", (("Value", "Boolean Math.002", "Boolean"), )),
    "Boolean Math": ("FunctionNodeBooleanMath", (201.02, -54.2), "Frame.001", (("Boolean", "Compare", "Result"), ("Boolean#1", "Compare.002", "Result"), )),
    "Boolean Math.002": ("FunctionNodeBooleanMath", (206.59, -94.01), "Frame.001", (("Boolean", "Boolean Math", "Boolean"), )),
    "Boolean Math.003": ("FunctionNodeBooleanMath", (772.83, -34.82), None, (("Boolean", "Compare.006", "Result"), ("Boolean#1", "Compare.007", "Result"), )),
    "Compare": ("FunctionNodeCompare", (30.84, -36.28), "Frame.001", (("A", "Group Input", "Multiplicity"), )),
    "Compare.002": ("FunctionNodeCompare", (30.48, -193.05), "Frame.001", (("A", "Group Input", "Multiplicity"), )),
    "Compare.003": ("FunctionNodeCompare", (524.78, -50.8), "Frame.001", (("A", "Accumulate Field", "Total"), )),
    "Compare.006": ("FunctionNodeCompare", (611.4, -20.53), None, (("A", "Index.001", "Index"), ("B", "Repeat Input.001", "Offset"), )),
    "Compare.007": ("FunctionNodeCompare", (607.01, -57.66), None, (("A", "Index.001", "Index"), ("B", "Integer Math.003", "Value"), )),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (1404.74, 223.52), None, (("Index", "Repeat Output.001", "Index"), ("Value", "Group Input", "Unique Knot"), )),
    "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (134.24, -171.82), None, (("Index", "Repeat Input.001", "Iteration"), ("Value", "Group Input", "Multiplicity"), )),
    "Frame.001": ("NodeFrame", (130.76, 552.74), None, ()),
    "Group Input": ("NodeGroupInput", (-861.57, 111.89), None, ()),
    "Group Output": ("NodeGroupOutput", (2247.33, 153.34), None, (("Knot", "Switch.001", "Output"), )),
    "Index.001": ("GeometryNodeInputIndex", (419.5, 7.97), None, ()),
    "Integer Math.003": ("FunctionNodeIntegerMath", (479.36, -148.78), None, (("Value", "Repeat Input.001", "Offset"), ("Value#1", "Integer Math.004", "Value"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (289.34, -175.69), None, (("Value", "Evaluate at Index.003", "Value"), )),
    "Repeat Input.001": ("GeometryNodeRepeatInput", (-192.36, -50.57), None, (("Iterations", "Group Input", "Multiplicity Length"), )),
    "Repeat Output.001": ("GeometryNodeRepeatOutput", (1094.45, -90.79), None, (("Index", "Switch.002", "Output"), ("Offset", "Integer Math.003", "Value"), )),
    "Switch.001": ("GeometryNodeSwitch", (1920.31, 201.59), None, (("False", "Evaluate at Index.002", "Value"), ("Switch", "Compare.003", "Result"), ("True", "Group Input", "Unique Knot"), )),
    "Switch.002": ("GeometryNodeSwitch", (913.62, 4.77), None, (("False", "Repeat Input.001", "Index"), ("Switch", "Boolean Math.003", "Boolean"), ("True", "Repeat Input.001", "Iteration"), )),
    "Viewer": ("GeometryNodeViewer", (915.87, 516.74), None, (("Result", "Compare.003", "Result"), )),
}