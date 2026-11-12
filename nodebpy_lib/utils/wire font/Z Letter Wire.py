from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("Z Letter Wire", arrange=None, clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.5, 1.0, 0.0), (0.5, 1.0, 0.0), (-0.5, 0.0, 0.0), (0.5, 0.0, 0.0)))
    (
        g.MeshLine(count=4, offset=(1.0, 0.0, 0.0))
        >> g.SetPosition(position=index_switch.o.output * 0.1)
        >> geometry
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-494.54, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (483.43, 0.0), None, (("Geometry", "Set Position.002", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (-294.54, -155.53), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (-104.34, -122.84), None, (("Index", "Index", "Index"), )),
    "Mesh Line.003": ("GeometryNodeMeshLine", (-96.26, 158.95), None, ()),
    "Set Position.002": ("GeometryNodeSetPosition", (283.43, 35.47), None, (("Geometry", "Mesh Line.003", "Mesh"), ("Position", "Vector Math", "Vector"), )),
    "Vector Math": ("ShaderNodeVectorMath", (59.19, -101.2), None, (("Vector", "Index Switch", "Output"), )),
}