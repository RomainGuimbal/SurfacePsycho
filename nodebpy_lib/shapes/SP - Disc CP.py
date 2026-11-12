from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPDiscCP(CustomGeometryGroup):
    _name = "SP - Disc CP"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        radius = tree.inputs.float("Radius", 0.0, min_value=-10_000.0, max_value=10_000.0)
        geometry = tree.outputs.geometry("Geometry")

        index_switch = g.IndexSwitch.vector(g.Index(), (g.CombineXYZ(radius), (0.0, 0.0, 0.0), g.CombineXYZ(y=radius)))
        (
            ((g.MeshLine(3) >> g.StoreNamedAttribute.point.integer(name="Type", value=3)).props(width=140.0) >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=g.IndexSwitch.boolean(g.Index(), (True, False, True)))).props(width=140.0)
            >> g.SetPosition(position=index_switch)
            >> geometry
        )