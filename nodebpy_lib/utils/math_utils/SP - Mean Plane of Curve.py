from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Mean Plane of Curve", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    offset = tree.outputs.vector("Offset")
    normal = tree.outputs.vector("Normal")

    position = g.Position()
    reroute = g.Reroute(input=geometry).props(width=19.0)
    with g.Frame("Newell's Method"):
        integer_math = (g.Index().o.index - 1) % g.DomainSize(geometry=geometry, component="CURVE").props(hide_outputs=["Spline Count"]).o.point_count
        reroute_1 = g.Reroute(input=position.o.position).props(label="Current", width=19.0)
        reroute_2 = g.Reroute(input=position.o.position.point.at(integer_math)).props(label="Prev", width=19.0)
        vector = (reroute_2.o.output - reroute_1).props(width=100.0, hide=True)
        vector_1 = (reroute_2.o.output + reroute_1).props(width=100.0, hide=True)
        vector_math = (g.CombineXYZ(x=vector.y, y=vector.z, z=vector.x).o.vector * g.CombineXYZ(x=vector_1.z, y=vector_1.x, z=vector_1.y)).props(width=102.5, hide=True)
        attribute_statistic = g.AttributeStatistic.point.vector(reroute, attribute=vector_math).props(hide_inputs=["Selection"], hide_outputs=["Mean", "Median", "Min", "Max", "Range", "Standard Deviation", "Variance"])
    attribute_statistic_1 = g.AttributeStatistic.point.vector(reroute, attribute=position).props(hide_inputs=["Selection"], hide_outputs=["Median", "Sum", "Min", "Max", "Range", "Standard Deviation", "Variance"])
    vector_math_1 = attribute_statistic.o.sum.normalize()
    viewer = g.Viewer()
    viewer.items.geometry(geometry, "Geometry")
    viewer.items.vector(vector_math_1, "Vector")

    attribute_statistic_1 >> offset
    vector_math_1 >> normal

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Attribute Statistic.001": ("GeometryNodeAttributeStatistic", (1051.78, 413.87), None, (("Attribute", "Position", "Position"), ("Geometry", "Reroute.045", "Output"), )),
    "Attribute Statistic.002": ("GeometryNodeAttributeStatistic", (1521.98, -140.73), "Frame", (("Attribute", "Vector Math.001", "Vector"), ("Geometry", "Reroute.045", "Output"), )),
    "Combine XYZ": ("ShaderNodeCombineXYZ", (1144.5, -164.35), "Frame", (("X", "Separate XYZ", "Z"), ("Y", "Separate XYZ", "X"), ("Z", "Separate XYZ", "Y"), )),
    "Combine XYZ.001": ("ShaderNodeCombineXYZ", (1142.79, -36.1), "Frame", (("X", "Separate XYZ.001", "Y"), ("Y", "Separate XYZ.001", "Z"), ("Z", "Separate XYZ.001", "X"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (189.27, -202.62), "Frame", (("Geometry", "Group Input", "Geometry"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (531.38, -102.64), "Frame", (("Index", "Integer Math.001", "Value"), ("Value", "Position", "Position"), )),
    "Frame": ("NodeFrame", (-480.71, 897.39), None, ()),
    "Group Input": ("NodeGroupInput", (-1132.2, 308.18), None, ()),
    "Group Output": ("NodeGroupOutput", (1584.02, 477.77), None, (("Normal", "Vector Math.004", "Vector"), ("Offset", "Attribute Statistic.001", "Mean"), )),
    "Index": ("GeometryNodeInputIndex", (29.99, -106.58), "Frame", ()),
    "Integer Math": ("FunctionNodeIntegerMath", (193.28, -59.26), "Frame", (("Value", "Index", "Index"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (356.48, -58.56), "Frame", (("Value", "Integer Math", "Value"), ("Value#1", "Domain Size", "Point Count"), )),
    "Position": ("GeometryNodeInputPosition", (-249.79, 444.69), None, ()),
    "Reroute": ("NodeReroute", (711.47, -271.22), "Frame", (("Input", "Position", "Position"), )),
    "Reroute.001": ("NodeReroute", (712.62, -144.45), "Frame", (("Input", "Evaluate at Index", "Value"), )),
    "Reroute.045": ("NodeReroute", (893.6, 329.2), None, (("Input", "Group Input", "Geometry"), )),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (924.03, -167.17), "Frame", (("Vector", "Vector Math.003", "Vector"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (923.86, -40.67), "Frame", (("Vector", "Vector Math", "Vector"), )),
    "Vector Math": ("ShaderNodeVectorMath", (770.65, -137.41), "Frame", (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute", "Output"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (1347.92, -137.64), "Frame", (("Vector", "Combine XYZ.001", "Vector"), ("Vector#1", "Combine XYZ", "Vector"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (771.63, -252.25), "Frame", (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute", "Output"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (1301.59, 615.67), None, (("Vector", "Attribute Statistic.002", "Sum"), )),
    "Viewer": ("GeometryNodeViewer", (1463.91, 698.79), None, (("Geometry", "Group Input", "Geometry"), ("Vector", "Vector Math.004", "Vector"), )),
}