from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Is Line Segment", arrange=None, clear=True) as tree:
    segment_info = tree.inputs.bundle("Segment Info")
    boolean = tree.outputs.boolean("Boolean")

    separate_bundle = g.SeparateBundle(segment_info)
    separate_bundle.items.string("Type", structure_type="SINGLE")
    segment_type = separate_bundle.items.integer("Segment Type", structure_type="SINGLE")
    point_count = separate_bundle.items.integer("Point Count", structure_type="SINGLE")
    separate_bundle.items.integer("Degree", structure_type="SINGLE")
    separate_bundle.items.integer("Resolution", structure_type="SINGLE")
    separate_bundle.items.geometry("Knot Support", structure_type="SINGLE")
    separate_bundle.items.float("Knot", structure_type="FIELD")
    separate_bundle.items.float("Unique Knot", structure_type="FIELD")
    separate_bundle.items.integer("Multiplicity", structure_type="FIELD")
    separate_bundle.items.integer("Compact Knot Length", structure_type="SINGLE")
    separate_bundle.items.matrix("Scaled Basis", structure_type="SINGLE")
    separate_bundle.items.float("Min Parameter", structure_type="SINGLE")
    separate_bundle.items.float("Max Parameter", structure_type="SINGLE")
    separate_bundle.items.boolean("Rational", structure_type="SINGLE")
    separate_bundle.items.boolean("Clamped", structure_type="SINGLE")
    separate_bundle.items.boolean("Cyclic", structure_type="SINGLE")
    (
        (g.Compare.integer.equal(segment_type.output, 0).o.result & g.Compare.integer.equal(point_count.output, 2))
        >> boolean
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (197.0, 17.1), None, (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Compare", "Result"), )),
    "Compare": ("FunctionNodeCompare", (-13.16, -79.09), None, (("A", "Separate Bundle", "Point Count"), )),
    "Compare.001": ("FunctionNodeCompare", (-9.2, 79.09), None, (("A", "Separate Bundle", "Segment Type"), )),
    "Group Input": ("NodeGroupInput", (-397.0, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (387.0, 0.0), None, (("Boolean", "Boolean Math", "Boolean"), )),
    "Separate Bundle": ("NodeSeparateBundle", (-196.48, -17.86), None, (("Bundle", "Group Input", "Segment Info"), )),
}