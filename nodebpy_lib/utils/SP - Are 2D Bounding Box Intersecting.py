from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Are 2D Bounding Box Intersecting", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry", description="Geometry to compute the bounding box of. Instances have to be realized before the full bounding box can be computed")
    geometry_1 = tree.inputs.geometry("Geometry", description="Geometry to compute the bounding box of. Instances have to be realized before the full bounding box can be computed")
    intersects = tree.outputs.boolean("Intersects")

    bounding_box = g.BoundingBox(geometry=geometry, use_radius=False)
    bounding_box_1 = g.BoundingBox(geometry=geometry_1, use_radius=False)
    compare = bounding_box.o.min * (1.0, 1.0, 0.0) < bounding_box_1.o.max.mul_add((1.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    compare_1 = bounding_box_1.o.min * (1.0, 1.0, 0.0) < bounding_box.o.max.mul_add((1.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    (compare & compare_1) >> intersects
    viewer = g.Viewer()
    viewer.items.geometry(bounding_box_1.o.bounding_box, "Bounding Box")

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math.003": ("FunctionNodeBooleanMath", (445.85, -17.35), None, (("Boolean", "Compare.005", "Result"), ("Boolean#1", "Compare.006", "Result"), )),
    "Bounding Box.002": ("GeometryNodeBoundBox", (-184.65, 53.44), None, (("Geometry", "Group Input", "Geometry"), )),
    "Bounding Box.003": ("GeometryNodeBoundBox", (-185.63, -104.07), None, (("Geometry", "Group Input", "Geometry#1"), )),
    "Compare.005": ("FunctionNodeCompare", (279.86, 88.2), None, (("A", "Vector Math", "Vector"), ("B", "Vector Math.002", "Vector"), )),
    "Compare.006": ("FunctionNodeCompare", (276.54, -94.1), None, (("A", "Vector Math.003", "Vector"), ("B", "Vector Math.001", "Vector"), )),
    "Group Input": ("NodeGroupInput", (-385.63, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (626.79, -33.99), None, (("Intersects", "Boolean Math.003", "Boolean"), )),
    "Vector Math": ("ShaderNodeVectorMath", (22.34, 249.73), None, (("Vector", "Bounding Box.002", "Min"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (22.34, 57.04), None, (("Vector", "Bounding Box.002", "Max"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (22.34, -217.99), None, (("Vector", "Bounding Box.003", "Max"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (22.34, -493.02), None, (("Vector", "Bounding Box.003", "Min"), )),
    "Viewer": ("GeometryNodeViewer", (218.0, 190.53), None, (("Bounding Box", "Bounding Box.003", "Bounding Box"), )),
}