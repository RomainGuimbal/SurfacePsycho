from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("Y Letter Wire", arrange=None, clear=True) as tree:
    scale = tree.inputs.float("Scale", 0.1, min_value=-10_000.0, max_value=10_000.0)
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.5, 1.0, 0.0), (0.0, 0.5, 0.0), (-0.5, 0.0, 0.0), (0.5, 1.0, 0.0)))
    mesh_line = g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True)
    (
        g.JoinGeometry((mesh_line, g.Reroute(input=mesh_line.o.mesh).props(width=19.0)))
        >> g.SetPosition(position=index_switch.o.output * scale)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-517.98, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (489.43, 0.0), None, (("Geometry", "Set Position.003", "Geometry"), )),
    "Index Switch.002": ("GeometryNodeIndexSwitch", (-127.77, -58.13), None, (("Index", "Index.002", "Index"), )),
    "Index.002": ("GeometryNodeInputIndex", (-317.98, -90.82), None, ()),
    "Join Geometry.002": ("GeometryNodeJoinGeometry", (29.57, 39.11), None, (("Geometry", "Mesh Line.006", "Mesh"), ("Geometry", "Reroute.001", "Output"), )),
    "Mesh Line.006": ("GeometryNodeMeshLine", (-243.88, 38.85), None, ()),
    "Reroute.001": ("NodeReroute", (-38.71, 1.97), None, (("Input", "Mesh Line.006", "Mesh"), )),
    "Set Position.003": ("GeometryNodeSetPosition", (289.43, 89.76), None, (("Geometry", "Join Geometry.002", "Geometry"), ("Position", "Vector Math.002", "Vector"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (35.75, -36.49), None, (("Scale", "Group Input", "Scale"), ("Vector", "Index Switch.002", "Output"), )),
}