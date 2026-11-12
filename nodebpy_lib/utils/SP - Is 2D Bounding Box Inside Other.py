from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Is 2D Bounding Box Inside Other", arrange=None, clear=True) as tree:
    child = tree.inputs.geometry("Child", description="Geometry to compute the bounding box of. Instances have to be realized before the full bounding box can be computed")
    parent = tree.inputs.geometry("Parent", description="Geometry to compute the bounding box of. Instances have to be realized before the full bounding box can be computed")
    intersects = tree.outputs.boolean("Intersects")

    bounding_box = g.BoundingBox(geometry=child, use_radius=False)
    bounding_box_1 = g.BoundingBox(geometry=parent, use_radius=False)
    compare = bounding_box.o.max * (1.0, 1.0, 0.0) < bounding_box_1.o.max.mul_add((1.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    compare_1 = bounding_box.o.min * (1.0, 1.0, 0.0) > bounding_box_1.o.min.mul_add((1.0, 1.0, 0.0), (0.0, 0.0, -1.0))
    (compare_1 & compare) >> intersects

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math.003": ("FunctionNodeBooleanMath", (530.01, 15.54), None, (("Boolean", "Compare.007", "Result"), ("Boolean#1", "Compare.006", "Result"), )),
    "Bounding Box.002": ("GeometryNodeBoundBox", (-184.65, 53.44), None, (("Geometry", "Group Input", "Child"), )),
    "Bounding Box.003": ("GeometryNodeBoundBox", (-185.63, -104.07), None, (("Geometry", "Group Input", "Parent"), )),
    "Compare.006": ("FunctionNodeCompare", (312.61, -81.41), None, (("A", "Vector Math.001", "Vector"), ("B", "Vector Math.002", "Vector"), )),
    "Compare.007": ("FunctionNodeCompare", (306.42, 166.87), None, (("A", "Vector Math", "Vector"), ("B", "Vector Math.003", "Vector"), )),
    "Group Input": ("NodeGroupInput", (-385.63, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (710.95, -1.1), None, (("Intersects", "Boolean Math.003", "Boolean"), )),
    "Vector Math": ("ShaderNodeVectorMath", (22.34, 249.73), None, (("Vector", "Bounding Box.002", "Min"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (22.34, 57.04), None, (("Vector", "Bounding Box.002", "Max"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (20.92, -427.44), None, (("Vector", "Bounding Box.003", "Max"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (20.23, -146.74), None, (("Vector", "Bounding Box.003", "Min"), )),
}