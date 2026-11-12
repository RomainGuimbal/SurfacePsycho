from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Isolate Segment", arrange=None, clear=True) as tree:
    wire = tree.inputs.geometry("Wire")
    segment_index = tree.inputs.integer("Segment index", 0, structure_type="FIELD")
    segment_count = tree.inputs.integer("Segment Count", 0, structure_type="SINGLE", force_non_field=True)
    closed_wire = tree.inputs.boolean("Closed Wire", False, structure_type="SINGLE", force_non_field=True)
    segment = tree.inputs.integer("Segment", 0, structure_type="SINGLE", force_non_field=True)
    segment_1 = tree.outputs.geometry("Segment")
    inverted = tree.outputs.geometry("Inverted")
    point_indices_in_curve = tree.outputs.integer("Point Indices in Curve")

    capture = g.CaptureAttribute.point(geometry=wire)
    index = capture.items.integer(g.Index(), "Index")
    reroute = g.Reroute(input=index.output).props(width=19.0)
    reroute_1 = g.Reroute(input=closed_wire).props(width=19.0)
    with g.Frame("Flip"):
        reroute_2 = g.Reroute(input=segment_count).props(width=19.0)
        compare = g.Compare.integer.equal((reroute_2.o.output - 1).props(width=100.0, hide=True), segment).props(hide=True)
        boolean_math = compare.o.result & (reroute_2 > 1).props(hide=True)
    reroute_3 = g.Reroute(input=boolean_math).props(width=19.0)
    separate_geometry = (
        capture.o.geometry
        >> g.SeparateGeometry.edge(selection=g.Compare.integer.equal(segment_index, segment % segment_count).props(hide=True))
    )
    with g.Frame():
        domain_size = g.DomainSize(separate_geometry.o.selection).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        evaluate_at_index = reroute.o.output.point.at(domain_size.o.point_count - 1 - g.Index())
    reroute_4 = g.Reroute(input=separate_geometry.o.selection).props(width=19.0)
    curve_to_mesh = (g.MeshToCurve(reroute_4).props(width=100.0, hide=True) >> g.ReverseCurve(selection=reroute_3) >> g.CurveToMesh()).props(hide=True)
    (
        (reroute_1.o.output.switch.geometry(reroute_4, curve_to_mesh) >> g.SeparateComponents()).props(width=140.0)
        >> segment_1
    )
    (
        reroute_1.o.output.switch.integer(index.output, reroute_3.o.output.switch.integer(reroute, evaluate_at_index))
        >> point_indices_in_curve
    )

    separate_geometry.o.inverted >> inverted

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math.001": ("FunctionNodeBooleanMath", (418.15, -36.15), "Frame.001", (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Compare", "Result"), )),
    "Capture Attribute": ("GeometryNodeCaptureAttribute", (205.93, 313.3), None, (("Geometry", "Group Input", "Wire"), ("Index", "Index", "Index"), )),
    "Compare": ("FunctionNodeCompare", (230.86, -130.63), "Frame.001", (("A", "Reroute.002", "Output"), )),
    "Compare.001": ("FunctionNodeCompare", (192.83, 135.59), None, (("A", "Group Input", "Segment index"), ("B", "Integer Math.001", "Value"), )),
    "Compare.002": ("FunctionNodeCompare", (231.2, -85.0), "Frame.001", (("A", "Integer Math.003", "Value"), ("B", "Group Input", "Segment"), )),
    "Curve to Mesh": ("GeometryNodeCurveToMesh", (1359.1, 389.66), None, (("Curve", "Reverse Curve", "Curve"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (30.23, -95.87), "Frame", (("Geometry", "Separate Geometry", "Selection"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (564.87, -30.24), "Frame", (("Index", "Integer Math.002", "Value"), ("Value", "Reroute", "Output"), )),
    "Frame": ("NodeFrame", (687.71, 51.35), None, ()),
    "Frame.001": ("NodeFrame", (114.8, 719.51), None, ()),
    "Group Input": ("NodeGroupInput", (-465.81, 543.87), None, ()),
    "Group Output": ("NodeGroupOutput", (2092.7, 393.3), None, (("Inverted", "Separate Geometry", "Inverted"), ("Point Indices in Curve", "Switch.004", "Output"), ("Segment", "Separate Components", "Mesh"), )),
    "Index": ("GeometryNodeInputIndex", (18.98, 265.81), None, ()),
    "Index.001": ("GeometryNodeInputIndex", (187.57, -249.02), "Frame", ()),
    "Integer Math": ("FunctionNodeIntegerMath", (190.06, -108.57), "Frame", (("Value", "Domain Size", "Point Count"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-0.35, 157.05), None, (("Value", "Group Input", "Segment"), ("Value#1", "Group Input", "Segment Count"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (374.71, -131.16), "Frame", (("Value", "Integer Math", "Value"), ("Value#1", "Index.001", "Index"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (96.36, -81.15), "Frame.001", (("Value", "Reroute.002", "Output"), )),
    "Mesh to Curve": ("GeometryNodeMeshToCurve", (1074.79, 389.93), None, (("Mesh", "Reroute.004", "Output"), )),
    "Reroute": ("NodeReroute", (965.14, 70.42), None, (("Input", "Capture Attribute", "Index"), )),
    "Reroute.001": ("NodeReroute", (1672.38, 455.11), None, (("Input", "Group Input", "Closed Wire"), )),
    "Reroute.002": ("NodeReroute", (35.21, -130.25), "Frame.001", (("Input", "Group Input", "Segment Count"), )),
    "Reroute.003": ("NodeReroute", (877.03, 350.22), None, (("Input", "Boolean Math.001", "Boolean"), )),
    "Reroute.004": ("NodeReroute", (946.83, 422.0), None, (("Input", "Separate Geometry", "Selection"), )),
    "Reverse Curve": ("GeometryNodeReverseCurve", (1200.38, 413.96), None, (("Curve", "Mesh to Curve", "Curve"), ("Selection", "Reroute.003", "Output"), )),
    "Separate Components": ("GeometryNodeSeparateComponents", (1887.75, 557.93), None, (("Geometry", "Switch.002", "Output"), )),
    "Separate Geometry": ("GeometryNodeSeparateGeometry", (412.23, 328.33), None, (("Geometry", "Capture Attribute", "Geometry"), ("Selection", "Compare.001", "Result"), )),
    "Switch": ("GeometryNodeSwitch", (1517.64, 177.27), None, (("False", "Reroute", "Output"), ("Switch", "Reroute.003", "Output"), ("True", "Evaluate at Index", "Value"), )),
    "Switch.002": ("GeometryNodeSwitch", (1725.62, 535.21), None, (("False", "Reroute.004", "Output"), ("Switch", "Reroute.001", "Output"), ("True", "Curve to Mesh", "Mesh"), )),
    "Switch.004": ("GeometryNodeSwitch", (1723.1, 317.32), None, (("False", "Capture Attribute", "Index"), ("Switch", "Reroute.001", "Output"), ("True", "Switch", "Output"), )),
}