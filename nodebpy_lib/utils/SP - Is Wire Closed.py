from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPIsWireClosed(CustomGeometryGroup):
    _name = "SP - Is Wire Closed"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_is_wire_closed", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        wire_control_geom = tree.inputs.geometry("Wire Control Geom")
        is_closed = tree.outputs.boolean("Is Closed")

        (
            (wire_control_geom >> g.MeshToCurve() >> g.SampleIndex.spline.boolean(value=g.IsSplineCyclic())).props(hide=True)
            >> is_closed
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-284.87, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (280.61, 54.63), None, (("Is Closed", "Sample Index", "Value"), )),
            "Is Spline Cyclic": ("GeometryNodeInputSplineCyclic", (-84.87, -65.44), None, ()),
            "Mesh to Curve.004": ("GeometryNodeMeshToCurve", (-72.53, 61.08), None, (("Mesh", "Group Input", "Wire Control Geom"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (108.46, 20.46), None, (("Geometry", "Mesh to Curve.004", "Curve"), ("Value", "Is Spline Cyclic", "Cyclic"), )),
        }