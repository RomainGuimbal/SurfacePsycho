from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPNatrualContour(CustomGeometryGroup):
    _name = "SP - Natrual Contour"
    _color_tag = "INPUT"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        wire = tree.outputs.geometry("Wire")
        segment_index = tree.outputs.integer("Segment Index", attribute_domain="EDGE")
        segment_count = tree.outputs.integer("Segment Count")

        index = g.Index()
        index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)))
        integer = g.Integer(4)
        (
            ((g.MeshCircle(4).props(hide=True) >> g.SetPosition(position=index_switch)).props(hide_inputs=["Selection", "Offset"]) >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=True)).props(width=140.0)
            >> wire
        )

        index >> segment_index
        integer >> segment_count

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-594.53, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (435.83, 16.49), None, (("Segment Count", "Integer", "Integer"), ("Segment Index", "Index", "Index"), ("Wire", "Store Named Attribute", "Geometry"), )),
            "Index": ("GeometryNodeInputIndex", (212.0, -96.8), None, ()),
            "Index Switch": ("GeometryNodeIndexSwitch", (-201.36, -19.65), None, (("Index", "Index.001", "Index"), )),
            "Index.001": ("GeometryNodeInputIndex", (-384.38, -68.51), None, ()),
            "Integer": ("FunctionNodeInputInt", (215.51, -162.39), None, ()),
            "Mesh Circle": ("GeometryNodeMeshCircle", (-193.27, 24.61), None, ()),
            "Set Position": ("GeometryNodeSetPosition", (-4.47, 21.95), None, (("Geometry", "Mesh Circle", "Mesh"), ("Position", "Index Switch", "Output"), )),
            "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (210.21, 99.56), None, (("Geometry", "Set Position", "Geometry"), )),
        }