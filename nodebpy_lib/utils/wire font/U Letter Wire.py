from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class ULetterWire(CustomGeometryGroup):
    _name = "U Letter Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.2, 0.0), (0.1, 0.0, 0.0), (0.09, -0.03, 0.0), (0.065, -0.05, 0.0), (0.03, -0.06, 0.0), (-0.03, -0.06, 0.0), (-0.065, -0.05, 0.0), (-0.09, -0.03, 0.0), (-0.1, 0.0, 0.0), (-0.1, 0.2, 0.0)))
        g.MeshLine() >> g.SetPosition(position=index_switch.o.output * 0.2) >> geometry

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-553.06, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (543.06, 0.0), None, (("Geometry", "Set Position", "Geometry"), )),
            "Index": ("GeometryNodeInputIndex", (-353.06, 55.6), None, ()),
            "Index Switch": ("GeometryNodeIndexSwitch", (-177.37, 130.98), None, (("Index", "Index", "Index"), )),
            "Mesh Line.001": ("GeometryNodeMeshLine", (6.53, 144.44), None, ()),
            "Set Position": ("GeometryNodeSetPosition", (353.06, -56.03), None, (("Geometry", "Mesh Line.001", "Mesh"), ("Position", "Vector Math", "Vector"), )),
            "Vector Math": ("ShaderNodeVectorMath", (0.43, -144.44), None, (("Vector", "Index Switch", "Output"), )),
        }