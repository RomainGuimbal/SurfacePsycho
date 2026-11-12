from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Group4NumberWire(CustomGeometryGroup):
    _name = "4 Number Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (0.0, 0.13, 0.0), (0.0, 0.26, 0.0), (-0.1, 0.07, 0.0), (0.1, 0.07, 0.0)))
        _mesh_line = g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True)
        (
            g.JoinGeometry((g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True), g.MeshLine(count=3, offset=(1.0, 0.0, 0.0))))
            >> g.SetPosition(position=index_switch)
            >> geometry
        )