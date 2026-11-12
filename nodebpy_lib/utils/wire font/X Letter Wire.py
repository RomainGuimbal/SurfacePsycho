from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class XLetterWire(CustomGeometryGroup):
    _name = "X Letter Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((-0.5, 1.0, 0.0), (0.5, 0.0, 0.0), (-0.5, 0.0, 0.0), (0.5, 1.0, 0.0)))
        mesh_line = g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True)
        (
            g.JoinGeometry((mesh_line, g.Reroute(input=mesh_line.o.mesh).props(width=19.0)))
            >> g.SetPosition(position=index_switch.o.output * 0.1)
            >> geometry
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-529.58, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (521.52, 0.0), None, (("Geometry", "Set Position.002", "Geometry"), )),
            "Index Switch.001": ("GeometryNodeIndexSwitch", (-139.38, -34.66), None, (("Index", "Index.001", "Index"), )),
            "Index.001": ("GeometryNodeInputIndex", (-329.58, -67.35), None, ()),
            "Join Geometry.001": ("GeometryNodeJoinGeometry", (69.12, 64.66), None, (("Geometry", "Mesh Line.004", "Mesh"), ("Geometry", "Reroute.001", "Output"), )),
            "Mesh Line.004": ("GeometryNodeMeshLine", (-199.63, 65.7), None, ()),
            "Reroute.001": ("NodeReroute", (14.76, 20.47), None, (("Input", "Mesh Line.004", "Mesh"), )),
            "Set Position.002": ("GeometryNodeSetPosition", (321.52, 63.8), None, (("Geometry", "Join Geometry.001", "Geometry"), ("Position", "Vector Math.001", "Vector"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (24.15, -13.02), None, (("Vector", "Index Switch.001", "Output"), )),
        }