import math
from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Foley Parametrization", arrange=None, clear=True) as tree:
    input = tree.inputs.geometry("Input")
    value = tree.outputs.float("Value")

    with g.Frame("Q"):
        position = g.Position()
        vector_math = (position.o.position - position.o.position.point.mean().props(hide=True)).props(hide=True)
        with g.Frame("Covariance matrix"):
            reroute = g.Reroute(input=vector_math).props(width=19.0)
            field_average = (reroute.o.output * reroute.o.output.x).props(hide=True).point.mean().props(hide=True, hide_outputs=["Median"])
            field_average_1 = (reroute.o.output * reroute.o.output.y).props(hide=True).point.mean().props(hide=True, hide_outputs=["Median"])
            field_average_2 = (reroute.o.output * reroute.o.output.z).props(hide=True).point.mean().props(hide=True, hide_outputs=["Median"])
            combine_matrix = g.CombineMatrix(column_1_row_1=field_average.x, column_1_row_2=field_average.y, column_1_row_3=field_average.z, column_2_row_1=field_average_1.x, column_2_row_2=field_average_1.y, column_2_row_3=field_average_1.z, column_3_row_1=field_average_2.x, column_3_row_2=field_average_2.y, column_3_row_3=field_average_2.z)
        sample_index = g.SampleIndex.point.matrix(input, combine_matrix)
        compare = g.Compare.float.equal(sample_index.o.value.determinant(), 0.0, 0.0000000001).props(hide=True)
        switch = compare.o.result.switch.matrix(sample_index.o.value.invert(), g.CombineTransform().props(hide_inputs=["Translation", "Rotation", "Scale"]))
    index = g.Index().props(hide=True)
    integer_math = (index.o.index - 1).props(hide=True)
    integer_math_1 = (index.o.index + 1).props(width=136.88, hide=True)
    _math_1 = g.Math.arccosine()
    reroute_1 = g.Reroute(input=integer_math_1).props(width=19.0)
    reroute_2 = g.Reroute(input=input).props(width=19.0)
    reroute_3 = g.Reroute(input=integer_math).props(width=19.0)
    reroute_4 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
    reroute_5 = g.Reroute(input=switch).props(width=19.0)
    with g.Frame("Nielsen Metric"):
        edge_vertices = g.EdgeVertices().props(label="t(i+1)-ti", hide_outputs=["Vertex Index 1", "Vertex Index 2"])
        vector_math_1 = (edge_vertices.o.position_1 - edge_vertices.o.position_2).props(width=100.0, hide=True)
        vector_math_2 = vector_math_1.transform(reroute_5).dot(vector_math_1)
        reroute_6 = g.Reroute(input=vector_math_2.sqrt().props(hide=True)).props(label="di", width=19.0)
    reroute_7 = g.Reroute(input=reroute_6.o.output.edge.at(reroute_3).props(hide=True)).props(label="di-1", width=19.0)
    reroute_8 = g.Reroute(input=reroute_6.o.output).props(label="di", width=19.0)
    with g.Frame("teta on points"):
        with g.Frame("Nielsen Metric for points arround corner (squared)"):
            position_1 = g.Position()
            vector_math_3 = (position_1.o.position.point.at(integer_math).props(hide=True) - position_1.o.position.point.at(integer_math_1).props(hide=True)).props(width=100.0, hide=True)
            vector_math_4 = vector_math_3.transform(reroute_5).dot(vector_math_3)
        reroute_9 = g.Reroute(input=vector_math_4).props(width=19.0)
        with g.Frame("d²i + d²i-1 - M"):
            reroute_10 = g.Reroute(input=vector_math_2).props(label="d²i", width=19.0)
            reroute_11 = g.Reroute(input=reroute_10.o.output.edge.at(reroute_3).props(hide=True)).props(label="d²i-1", width=19.0)
            math_2 = (g.Reroute(input=reroute_10.o.output).props(width=19.0).o.output + reroute_11).props(width=100.0, hide=True)
            math_3 = (math_2 - reroute_9).props(width=100.0, hide=True)
        with g.Frame("/2.di.di-1"):
            math_4 = (reroute_7.o.output * reroute_8).props(width=100.0, hide=True)
            math_5 = (math_3 / (math_4 + math_4).props(label="*2", width=100.0, hide=True)).props(width=100.0, hide=True)
        math_6 = math.pi - math_5.acos()
    reroute_12 = g.Reroute(input=reroute_6.o.output.edge.at(reroute_1).props(hide=True)).props(label="di+1", width=19.0)
    with g.Frame():
        reroute_13 = g.Reroute(input=math_6.min(math.pi / 2).props(label="têta")).props(label="têta i", width=19.0)
        reroute_14 = g.Reroute(input=reroute_13.o.output.edge.at(reroute_1)).props(label="têta i+1", width=19.0)
        reroute_15 = g.Reroute(input=reroute_13.o.output).props(width=19.0)
    _reroute_16 = g.Reroute(input=reroute_9.o.output).props(width=19.0)
    reroute_17 = g.Reroute(input=reroute_14.o.output).props(width=19.0)
    with g.Frame("delta ti"):
        reroute_18 = g.Reroute(input=reroute_12.o.output).props(width=19.0)
        reroute_19 = g.Reroute(input=reroute_7.o.output).props(width=19.0)
        reroute_20 = g.Reroute(input=reroute_8.o.output).props(width=19.0)
        reroute_21 = g.Reroute(input=g.Reroute(input=reroute_20.o.output).props(width=19.0).o.output).props(width=19.0)
        math_7 = ((reroute_18.o.output * reroute_17).props(hide=True) / (reroute_20.o.output + reroute_18).props(hide=True)).props(hide=True)
        math_8 = ((reroute_19.o.output * reroute_15).props(hide=True) / (reroute_19.o.output + reroute_20).props(hide=True)).props(hide=True)
        math_9 = (1.0 + ((math_8 + math_7).props(hide=True) * 1.5).props(label="3/2", hide=True)).props(hide=True)
        sample_index_1 = g.SampleIndex.edge.float(reroute_4, (reroute_21.o.output * math_9).props(hide=True), g.Index())
    accumulate_field = g.AccumulateField.point.float(sample_index_1)
    _sample_index_2 = (
        g.Reroute(input=reroute_2.o.output).props(width=19.0)
        >> g.SampleIndex.edge.float(value=math_6, index=g.Index())
    )
    sample_index_3 = g.SampleIndex.point.float(reroute_4, (accumulate_field.o.trailing / accumulate_field.o.total).props(hide=True), g.Index())
    (
        sample_index_3.o.value.point.evaluate().min(1.0).props(label="Clip slight overshoot", width=173.22)
        >> value
    )
    _points = g.Points(count=g.DomainSize(input).props(hide_outputs=["Face Count", "Face Corner Count"]).o.point_count, position=g.CombineXYZ(sample_index_3), radius=0.01)

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Accumulate Field.007": ("GeometryNodeAccumulateField", (3672.38, -476.45), None, (("Value", "Sample Index.007", "Value"), )),
    "Combine Matrix.001": ("FunctionNodeCombineMatrix", (843.47, -45.34), "Frame.008", (("Column 1 Row 1", "Separate XYZ.001", "X"), ("Column 1 Row 2", "Separate XYZ.001", "Y"), ("Column 1 Row 3", "Separate XYZ.001", "Z"), ("Column 2 Row 1", "Separate XYZ.002", "X"), ("Column 2 Row 2", "Separate XYZ.002", "Y"), ("Column 2 Row 3", "Separate XYZ.002", "Z"), ("Column 3 Row 1", "Separate XYZ.003", "X"), ("Column 3 Row 2", "Separate XYZ.003", "Y"), ("Column 3 Row 3", "Separate XYZ.003", "Z"), )),
    "Combine Transform": ("FunctionNodeCombineTransform", (1796.77, -311.73), "Frame.001", ()),
    "Combine XYZ": ("ShaderNodeCombineXYZ", (4372.04, -240.85), None, (("X", "Sample Index.009", "Value"), )),
    "Compare": ("FunctionNodeCompare", (1808.53, -136.74), "Frame.001", (("A", "Matrix Determinant", "Determinant"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (-769.62, -143.23), None, (("Geometry", "Group Input", "Input"), )),
    "Edge Vertices.001": ("GeometryNodeInputMeshEdgeVertices", (30.08, -103.38), "Frame.002", ()),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (1194.13, -500.64), None, (("Index", "Reroute.010", "Output"), ("Value", "Reroute.004", "Output"), )),
    "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (1194.13, -601.34), None, (("Index", "Reroute.002", "Output"), ("Value", "Reroute.004", "Output"), )),
    "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (45.39, -92.37), "Frame.007", (("Index", "Reroute.010", "Output"), ("Value", "Reroute.011", "Output"), )),
    "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (224.55, -118.69), "Frame.006", (("Index", "Reroute.002", "Output"), ("Value", "Reroute.024", "Output"), )),
    "Evaluate at Index.007": ("GeometryNodeFieldAtIndex", (201.84, -104.82), "Frame.003", (("Index", "Integer Math.002", "Value"), ("Value", "Position.001", "Position"), )),
    "Evaluate at Index.008": ("GeometryNodeFieldAtIndex", (201.0, -138.62), "Frame.003", (("Index", "Integer Math.003", "Value"), ("Value", "Position.001", "Position"), )),
    "Evaluate on Domain": ("GeometryNodeFieldOnDomain", (4223.33, -424.86), None, (("Value", "Sample Index.009", "Value"), )),
    "Field Average": ("GeometryNodeFieldAverage", (200.75, -284.47), "Frame.001", (("Value", "Position", "Position"), )),
    "Field Average.001": ("GeometryNodeFieldAverage", (464.35, -45.34), "Frame.008", (("Value", "Vector Math.007", "Vector"), )),
    "Field Average.002": ("GeometryNodeFieldAverage", (464.35, -85.34), "Frame.008", (("Value", "Vector Math.008", "Vector"), )),
    "Field Average.003": ("GeometryNodeFieldAverage", (464.35, -125.34), "Frame.008", (("Value", "Vector Math.009", "Vector"), )),
    "Frame": ("NodeFrame", (1300.24, -89.19), "Frame.005", ()),
    "Frame.001": ("NodeFrame", (-1908.53, -383.26), None, ()),
    "Frame.002": ("NodeFrame", (357.88, -493.38), None, ()),
    "Frame.003": ("NodeFrame", (30.18, -36.04), "Frame.005", ()),
    "Frame.004": ("NodeFrame", (2341.37, -436.68), None, ()),
    "Frame.005": ("NodeFrame", (223.94, -907.34), None, ()),
    "Frame.006": ("NodeFrame", (1787.29, -615.71), None, ()),
    "Frame.007": ("NodeFrame", (901.31, -107.19), "Frame.005", ()),
    "Frame.008": ("NodeFrame", (551.25, -211.71), "Frame.001", ()),
    "Group Input": ("NodeGroupInput", (-981.05, -51.63), None, ()),
    "Group Output": ("NodeGroupOutput", (4634.41, -409.47), None, (("Value", "Math.002", "Value"), )),
    "Index": ("GeometryNodeInputIndex", (936.88, -191.63), "Frame.004", ()),
    "Index.001": ("GeometryNodeInputIndex", (2325.39, -1083.36), None, ()),
    "Index.002": ("GeometryNodeInputIndex", (240.0, -731.31), None, ()),
    "Index.006": ("GeometryNodeInputIndex", (4039.33, -611.4), None, ()),
    "Integer Math.002": ("FunctionNodeIntegerMath", (241.92, -765.43), None, (("Value", "Index.002", "Index"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (240.96, -798.5), None, (("Value", "Index.002", "Index"), )),
    "Invert Matrix.001": ("FunctionNodeInvertMatrix", (1796.51, -199.4), "Frame.001", (("Matrix", "Sample Index.001", "Value"), )),
    "Math": ("ShaderNodeMath", (546.95, -58.72), "Frame.002", (("Value", "Vector Math.003", "Value"), )),
    "Math.002": ("ShaderNodeMath", (4392.81, -401.9), None, (("Value", "Evaluate on Domain", "Value"), )),
    "Math.003": ("ShaderNodeMath", (938.03, -145.52), "Frame.004", (("Value", "Reroute.021", "Output"), ("Value#1", "Math.004", "Value"), )),
    "Math.004": ("ShaderNodeMath", (768.24, -145.52), "Frame.004", (("Value#1", "Math.025", "Value"), )),
    "Math.011": ("ShaderNodeMath", (256.7, -79.95), "Frame.007", (("Value", "Reroute.012", "Output"), ("Value#1", "Reroute.013", "Output"), )),
    "Math.012": ("ShaderNodeMath", (258.62, -39.8), "Frame.007", (("Value", "Math.011", "Value"), ("Value#1", "Reroute.008", "Output"), )),
    "Math.013": ("ShaderNodeMath", (30.05, -113.5), "Frame", (("Value", "Math.012", "Value"), ("Value#1", "Math.026", "Value"), )),
    "Math.016": ("ShaderNodeMath", (129.6, -63.36), "Frame.004", (("Value", "Reroute.017", "Output"), ("Value#1", "Reroute.027", "Output"), )),
    "Math.019": ("ShaderNodeMath", (129.6, -105.74), "Frame.004", (("Value", "Reroute.017", "Output"), ("Value#1", "Reroute.018", "Output"), )),
    "Math.021": ("ShaderNodeMath", (129.6, -173.79), "Frame.004", (("Value", "Reroute.016", "Output"), ("Value#1", "Reroute.026", "Output"), )),
    "Math.024": ("ShaderNodeMath", (129.6, -216.84), "Frame.004", (("Value", "Reroute.018", "Output"), ("Value#1", "Reroute.016", "Output"), )),
    "Math.025": ("ShaderNodeMath", (608.73, -145.16), "Frame.004", (("Value", "Math.032", "Value"), )),
    "Math.026": ("ShaderNodeMath", (31.42, -77.59), "Frame", (("Value", "Math.027", "Value"), ("Value#1", "Math.027", "Value"), )),
    "Math.027": ("ShaderNodeMath", (30.05, -39.84), "Frame", (("Value", "Reroute.001", "Output"), ("Value#1", "Reroute.009", "Output"), )),
    "Math.028": ("ShaderNodeMath", (1471.66, -116.97), "Frame.005", (("Value", "Math.013", "Value"), )),
    "Math.029": ("ShaderNodeMath", (1636.59, -106.05), "Frame.005", (("Value#1", "Math.028", "Value"), )),
    "Math.030": ("ShaderNodeMath", (30.11, -30.02), "Frame.006", (("Value", "Math.029", "Value"), )),
    "Math.031": ("ShaderNodeMath", (3839.26, -533.05), None, (("Value", "Accumulate Field.007", "Trailing"), ("Value#1", "Accumulate Field.007", "Total"), )),
    "Math.032": ("ShaderNodeMath", (448.25, -142.31), "Frame.004", (("Value", "Math.033", "Value"), ("Value#1", "Math.034", "Value"), )),
    "Math.033": ("ShaderNodeMath", (294.9, -122.46), "Frame.004", (("Value", "Math.016", "Value"), ("Value#1", "Math.019", "Value"), )),
    "Math.034": ("ShaderNodeMath", (294.28, -157.58), "Frame.004", (("Value", "Math.021", "Value"), ("Value#1", "Math.024", "Value"), )),
    "Math.035": ("ShaderNodeMath", (2185.37, -1151.04), None, ()),
    "Matrix Determinant": ("FunctionNodeMatrixDeterminant", (1809.81, -35.81), "Frame.001", (("Matrix", "Sample Index.001", "Value"), )),
    "Points": ("GeometryNodePoints", (4559.13, -204.69), None, (("Count", "Domain Size", "Point Count"), ("Position", "Combine XYZ", "Vector"), )),
    "Position": ("GeometryNodeInputPosition", (30.0, -238.51), "Frame.001", ()),
    "Position.001": ("GeometryNodeInputPosition", (30.03, -105.0), "Frame.003", ()),
    "Reroute.001": ("NodeReroute", (1384.13, -512.28), None, (("Input", "Evaluate at Index.002", "Value"), )),
    "Reroute.002": ("NodeReroute", (1057.07, -810.34), None, (("Input", "Integer Math.003", "Value"), )),
    "Reroute.003": ("NodeReroute", (2314.64, -126.14), None, (("Input", "Group Input", "Input"), )),
    "Reroute.004": ("NodeReroute", (720.09, -70.17), "Frame.002", (("Input", "Math", "Value"), )),
    "Reroute.005": ("NodeReroute", (2231.16, -976.62), None, (("Input", "Reroute.008", "Output"), )),
    "Reroute.006": ("NodeReroute", (300.76, -623.87), None, (("Input", "Switch", "Output"), )),
    "Reroute.008": ("NodeReroute", (1119.26, -76.91), "Frame.005", (("Input", "Vector Math.005", "Value"), )),
    "Reroute.009": ("NodeReroute", (1382.26, -557.87), None, (("Input", "Reroute.004", "Output"), )),
    "Reroute.010": ("NodeReroute", (1057.07, -778.48), None, (("Input", "Integer Math.002", "Value"), )),
    "Reroute.011": ("NodeReroute", (35.21, -53.61), "Frame.007", (("Input", "Vector Math.003", "Value"), )),
    "Reroute.012": ("NodeReroute", (225.52, -60.58), "Frame.007", (("Input", "Reroute.011", "Output"), )),
    "Reroute.013": ("NodeReroute", (219.52, -103.7), "Frame.007", (("Input", "Evaluate at Index.005", "Value"), )),
    "Reroute.014": ("NodeReroute", (35.21, -61.75), "Frame.008", (("Input", "Vector Math.002", "Vector"), )),
    "Reroute.015": ("NodeReroute", (1378.4, -609.56), None, (("Input", "Evaluate at Index.003", "Value"), )),
    "Reroute.016": ("NodeReroute", (42.0, -157.87), "Frame.004", (("Input", "Reroute.015", "Output"), )),
    "Reroute.017": ("NodeReroute", (35.21, -81.32), "Frame.004", (("Input", "Reroute.001", "Output"), )),
    "Reroute.018": ("NodeReroute", (37.59, -119.28), "Frame.004", (("Input", "Reroute.009", "Output"), )),
    "Reroute.019": ("NodeReroute", (3398.24, -140.16), None, (("Input", "Reroute.003", "Output"), )),
    "Reroute.020": ("NodeReroute", (2364.5, -882.84), None, (("Input", "Reroute.003", "Output"), )),
    "Reroute.021": ("NodeReroute", (801.78, -41.81), "Frame.004", (("Input", "Reroute.023", "Output"), )),
    "Reroute.022": ("NodeReroute", (411.2, -88.13), "Frame.006", (("Input", "Evaluate at Index.006", "Value"), )),
    "Reroute.023": ("NodeReroute", (118.14, -41.06), "Frame.004", (("Input", "Reroute.018", "Output"), )),
    "Reroute.024": ("NodeReroute", (209.83, -90.67), "Frame.006", (("Input", "Math.030", "Value"), )),
    "Reroute.026": ("NodeReroute", (2276.05, -661.94), None, (("Input", "Reroute.022", "Output"), )),
    "Reroute.027": ("NodeReroute", (418.34, -38.58), "Frame.006", (("Input", "Reroute.024", "Output"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (1617.13, -205.68), "Frame.001", (("Geometry", "Group Input", "Input"), ("Value", "Combine Matrix.001", "Matrix"), )),
    "Sample Index.007": ("GeometryNodeSampleIndex", (1114.89, -56.67), "Frame.004", (("Geometry", "Reroute.019", "Output"), ("Index", "Index", "Index"), ("Value", "Math.003", "Value"), )),
    "Sample Index.008": ("GeometryNodeSampleIndex", (2518.85, -926.36), None, (("Geometry", "Reroute.020", "Output"), ("Index", "Index.001", "Index"), ("Value", "Math.029", "Value"), )),
    "Sample Index.009": ("GeometryNodeSampleIndex", (4040.58, -408.24), None, (("Geometry", "Reroute.019", "Output"), ("Index", "Index.006", "Index"), ("Value", "Math.031", "Value"), )),
    "Separate XYZ": ("ShaderNodeSeparateXYZ", (47.97, -102.22), "Frame.008", (("Vector", "Reroute.014", "Output"), )),
    "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (640.3, -45.34), "Frame.008", (("Vector", "Field Average.001", "Mean"), )),
    "Separate XYZ.002": ("ShaderNodeSeparateXYZ", (640.3, -105.34), "Frame.008", (("Vector", "Field Average.002", "Mean"), )),
    "Separate XYZ.003": ("ShaderNodeSeparateXYZ", (640.3, -165.34), "Frame.008", (("Vector", "Field Average.003", "Mean"), )),
    "Switch": ("GeometryNodeSwitch", (2028.39, -115.61), "Frame.001", (("False", "Invert Matrix.001", "Matrix"), ("Switch", "Compare", "Result"), ("True", "Combine Transform", "Transform"), )),
    "Transform Point": ("FunctionNodeTransformPoint", (207.2, -35.96), "Frame.002", (("Transform", "Reroute.006", "Output"), ("Vector", "Vector Math.001", "Vector"), )),
    "Transform Point.001": ("FunctionNodeTransformPoint", (494.44, -62.94), "Frame.003", (("Transform", "Reroute.006", "Output"), ("Vector", "Vector Math.004", "Vector"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (194.3, -139.4), "Frame.002", (("Vector", "Edge Vertices.001", "Position 1"), ("Vector#1", "Edge Vertices.001", "Position 2"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (373.21, -267.39), "Frame.001", (("Vector", "Position", "Position"), ("Vector#1", "Field Average", "Mean"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (371.01, -38.57), "Frame.002", (("Vector", "Transform Point", "Vector"), ("Vector#1", "Vector Math.001", "Vector"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (371.86, -133.16), "Frame.003", (("Vector", "Evaluate at Index.007", "Value"), ("Vector#1", "Evaluate at Index.008", "Value"), )),
    "Vector Math.005": ("ShaderNodeVectorMath", (672.29, -36.07), "Frame.003", (("Vector", "Transform Point.001", "Vector"), ("Vector#1", "Vector Math.004", "Vector"), )),
    "Vector Math.007": ("ShaderNodeVectorMath", (287.97, -42.22), "Frame.008", (("Scale", "Separate XYZ", "X"), ("Vector", "Reroute.014", "Output"), )),
    "Vector Math.008": ("ShaderNodeVectorMath", (287.97, -82.22), "Frame.008", (("Scale", "Separate XYZ", "Y"), ("Vector", "Reroute.014", "Output"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (287.97, -122.22), "Frame.008", (("Scale", "Separate XYZ", "Z"), ("Vector", "Reroute.014", "Output"), )),
}