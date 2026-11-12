from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPInternalPolylineToWire(CustomGeometryGroup):
    _name = "SP - Internal Polyline to Wire"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 270, "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        curve = tree.inputs.geometry("Curve", description="Curve to convert to a mesh using the given profile")
        geometry = tree.outputs.geometry("Geometry")

        (
            (curve >> g.CurveToMesh() >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=True)).props(width=140.0)
            >> geometry
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Curve to Mesh.001": ("GeometryNodeCurveToMesh", (-81.49, -14.64), None, (("Curve", "Group Input", "Curve"), )),
            "Group Input": ("NodeGroupInput", (-281.49, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (271.49, 0.0), None, (("Geometry", "Store Named Attribute", "Geometry"), )),
            "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (81.49, 14.64), None, (("Geometry", "Curve to Mesh.001", "Mesh"), )),
        }