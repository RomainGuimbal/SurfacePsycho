from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Group6NumberWire(CustomGeometryGroup):
    _name = "6 Number Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.26, 0.0), (0.055, 0.26, 0.0), (-0.01000001, 0.23, 0.0), (-0.06, 0.18, 0.0), (-0.09, 0.1, 0.0), (-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.03, 0.0, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.03, 0.0), (0.1, 0.06, 0.0), (0.1, 0.1, 0.0), (0.075, 0.125, 0.0), (0.03, 0.14, 0.0), (-0.075, 0.14, 0.0)))
        g.MeshLine(16) >> g.SetPosition(position=index_switch) >> geometry