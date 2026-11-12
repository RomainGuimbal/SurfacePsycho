from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Evaluate NURBS [A, w]", arrange=None, clear=True) as tree:
    control_geom = tree.inputs.geometry("Control Geom")
    cp_count = tree.inputs.integer("CP Count", 0, structure_type="SINGLE", force_non_field=True)
    cp_index = tree.inputs.integer("CP Index", 0)
    t_index = tree.inputs.integer("t Index", 0)
    parametric_space_geom = tree.inputs.geometry("Parametric Space Geom")
    basis_support = tree.inputs.geometry("Basis support", description="Size : Parametric P Count x CP Count")
    basis = tree.inputs.float("Basis", 0.0)
    evaluated_geom = tree.outputs.geometry("Evaluated Geom")
    a = tree.outputs.vector("A")
    w = tree.outputs.float("w")

    capture = g.CaptureAttribute.point(geometry=basis_support)
    basis_1 = capture.items.float(basis, "Basis")
    index = g.Index()
    integer_math = g.Index().o.index * cp_count
    reroute = g.Reroute(input=parametric_space_geom).props(width=9.5)
    reroute_1 = g.Reroute(input=capture.o.geometry).props(width=9.5)
    reroute_2 = g.Reroute(input=t_index).props(width=9.5)
    sample_index = g.SampleIndex.point.float(reroute_1, basis_1.output.point.total(reroute_2), integer_math)
    sample_index_1 = g.SampleIndex.point.float(reroute, sample_index, index)
    vector_math = g.SampleIndex.point.vector(control_geom, g.Position(), cp_index).o.value * basis_1.output
    sample_index_2 = g.SampleIndex.point.vector(reroute, g.SampleIndex.point.vector(reroute_1, vector_math.point.total(reroute_2), integer_math), index)
    viewer = g.Viewer()
    viewer.items.geometry(reroute_1, "Geometry")
    viewer.items.float(basis, "Value")

    reroute >> evaluated_geom
    sample_index_2 >> a
    sample_index_1 >> w

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field": ("GeometryNodeAccumulateField", (-132.55, -75.74), None, (("Group ID", "Reroute.014", "Output"), ("Value", "Capture Attribute", "Basis"), )),
    "Accumulate Field.001": ("GeometryNodeAccumulateField", (-127.29, 135.57), None, (("Group ID", "Reroute.014", "Output"), ("Value", "Vector Math", "Vector"), )),
    "Capture Attribute": ("GeometryNodeCaptureAttribute", (-523.17, -145.43), None, (("Basis", "Group Input", "Basis"), ("Geometry", "Group Input", "Basis support"), )),
    "Group Input": ("NodeGroupInput", (-1004.32, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (753.26, 0.0), None, (("A", "Sample Index.006", "Value"), ("Evaluated Geom", "Reroute", "Output"), ("w", "Sample Index.007", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (186.56, -95.01), None, ()),
    "Index.003": ("GeometryNodeInputIndex", (-293.68, 245.53), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (-128.51, 277.8), None, (("Value", "Index.003", "Index"), ("Value#1", "Group Input", "CP Count"), )),
    "Position": ("GeometryNodeInputPosition", (-727.79, 50.04), None, ()),
    "Reroute": ("NodeReroute", (425.69, -95.2), None, (("Input", "Group Input", "Parametric Space Geom"), )),
    "Reroute.013": ("NodeReroute", (41.11, -329.92), None, (("Input", "Capture Attribute", "Geometry"), )),
    "Reroute.014": ("NodeReroute", (-186.91, -140.79), None, (("Input", "Group Input", "t Index"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (-515.17, 93.32), None, (("Geometry", "Group Input", "Control Geom"), ("Index", "Group Input", "CP Index"), ("Value", "Position", "Position"), )),
    "Sample Index.004": ("GeometryNodeSampleIndex", (185.29, 117.19), None, (("Geometry", "Reroute.013", "Output"), ("Index", "Integer Math", "Value"), ("Value", "Accumulate Field.001", "Total"), )),
    "Sample Index.005": ("GeometryNodeSampleIndex", (185.56, -182.8), None, (("Geometry", "Reroute.013", "Output"), ("Index", "Integer Math", "Value"), ("Value", "Accumulate Field", "Total"), )),
    "Sample Index.006": ("GeometryNodeSampleIndex", (467.97, 150.51), None, (("Geometry", "Reroute", "Output"), ("Index", "Index", "Index"), ("Value", "Sample Index.004", "Value"), )),
    "Sample Index.007": ("GeometryNodeSampleIndex", (466.06, -110.35), None, (("Geometry", "Reroute", "Output"), ("Index", "Index", "Index"), ("Value", "Sample Index.005", "Value"), )),
    "Vector Math": ("ShaderNodeVectorMath", (-309.96, 118.16), None, (("Scale", "Capture Attribute", "Basis"), ("Vector", "Sample Index", "Value"), )),
    "Viewer": ("GeometryNodeViewer", (137.07, -416.06), None, (("Geometry", "Reroute.013", "Output"), ("Value", "Group Input", "Basis"), )),
}