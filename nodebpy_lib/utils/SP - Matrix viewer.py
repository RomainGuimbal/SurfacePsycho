import math
from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Matrix viewer", arrange=None, clear=True) as tree:
    m_row_count = tree.inputs.integer("m (row count)", 3, min_value=2, max_value=1000)
    n_col_count = tree.inputs.integer("n (col count)", 3, min_value=2, max_value=1000)
    matrix = tree.inputs.float("Matrix", 0.0, hide_value=True)
    dual_mesh = tree.outputs.geometry("Dual Mesh")
    value = tree.outputs.float("Value", hide_value=True, attribute_domain="FACE")

    grid = g.Grid(size_x=m_row_count * 0.3, size_y=n_col_count * 0.3, vertices_x=m_row_count + 1, vertices_y=n_col_count + 1)
    transform_geometry = g.TransformGeometry(geometry=grid, rotation=(0.0, 0.0, math.pi / 2), scale=(-1.0, -1.0, 1.0)).props(width=140.0, hide=True)
    capture = g.CaptureAttribute.face(geometry=transform_geometry)
    value_1 = capture.items.float(matrix, "Value")

    capture.o.geometry >> dual_mesh
    value_1.output >> value

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Capture Attribute.001": ("GeometryNodeCaptureAttribute", (831.3, -110.11), None, (("Geometry", "Transform Geometry.004", "Geometry"), ("Value", "Group Input", "Matrix"), )),
    "Grid.007": ("GeometryNodeMeshGrid", (315.76, 23.36), None, (("Size X", "Math", "Value"), ("Size Y", "Math.001", "Value"), ("Vertices X", "Integer Math", "Value"), ("Vertices Y", "Integer Math.001", "Value"), )),
    "Group Input": ("NodeGroupInput", (-587.56, -42.21), None, ()),
    "Group Output": ("NodeGroupOutput", (1323.01, 20.29), None, (("Dual Mesh", "Capture Attribute.001", "Geometry"), ("Value", "Capture Attribute.001", "Value"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (44.84, -84.11), None, (("Value", "Group Input", "m (row count)"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (43.25, -220.46), None, (("Value", "Group Input", "n (col count)"), )),
    "Math": ("ShaderNodeMath", (-170.97, 206.38), None, (("Value", "Group Input", "m (row count)"), )),
    "Math.001": ("ShaderNodeMath", (-170.97, 40.9), None, (("Value", "Group Input", "n (col count)"), )),
    "Transform Geometry.004": ("GeometryNodeTransform", (542.39, -20.97), None, (("Geometry", "Grid.007", "Mesh"), )),
}