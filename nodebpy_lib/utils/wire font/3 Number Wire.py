from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Group3NumberWire(CustomGeometryGroup):
    _name = "3 Number Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), ((-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.030000005, 0.00000000745058, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.02999999, 0.0), (0.1, 0.06000002, 0.0), (0.09, 0.1, 0.0), (0.055, 0.125, 0.0), (0.02, 0.13, 0.0), (0.055, 0.135, 0.0), (0.09, 0.16, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0)))
        g.MeshLine(19) >> g.SetPosition(position=index_switch) >> geometry