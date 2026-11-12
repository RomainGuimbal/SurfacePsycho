from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Group1NumberWire(CustomGeometryGroup):
    _name = "1 Number Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (0.0, 0.26, 0.0), (-0.1, 0.2, 0.0), (-0.1, 0.0, 0.0), (0.1, 0.0, 0.0)))
        mesh_line = g.MeshLine(count=2, start_location=(-0.1, 0.0, 0.0), offset=(0.1, 0.0, 0.0)).props(hide=True)
        (
            g.JoinGeometry((g.MeshLine(count=3, offset=(1.0, 0.0, 0.0)), mesh_line))
            >> g.SetPosition(position=index_switch)
            >> geometry
        )