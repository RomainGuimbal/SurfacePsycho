from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPAutoCloseWire(CustomGeometryGroup):
    _name = "SP - Auto Close Wire"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 221, "node_tool_idname": "geometry.sp_auto_close_wire", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        wires = tree.inputs.geometry("Wires")
        wires_1 = tree.outputs.geometry("Wires")

        boolean_math = (g.EndpointSelection().o.selection | g.NamedAttribute.boolean("Endpoints").o.attribute).props(hide=True)
        (
            (wires >> g.MeshToCurve() >> g.StoreNamedAttribute.point.boolean(name="Endpoints", value=boolean_math)).props(width=140.0)
            >> g.SetSplineCyclic(cyclic=True)
            >> g.CurveToMesh()
            >> wires_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (236.02, -28.77), None, (("Boolean", "Endpoint Selection", "Selection"), ("Boolean#1", "Named Attribute", "Attribute"), )),
            "Curve to Mesh": ("GeometryNodeCurveToMesh", (792.13, 96.07), None, (("Curve", "Set Spline Cyclic", "Curve"), )),
            "Endpoint Selection": ("GeometryNodeCurveEndpointSelection", (21.01, -14.58), None, ()),
            "Group Input": ("NodeGroupInput", (12.27, 107.52), None, ()),
            "Group Output": ("NodeGroupOutput", (988.14, 88.8), None, (("Wires", "Curve to Mesh", "Mesh"), )),
            "Mesh to Curve": ("GeometryNodeMeshToCurve", (233.89, 129.47), None, (("Mesh", "Group Input", "Wires"), )),
            "Named Attribute": ("GeometryNodeInputNamedAttribute", (23.27, -119.45), None, ()),
            "Set Spline Cyclic": ("GeometryNodeSetSplineCyclic", (575.12, 65.02), None, (("Curve", "Store Named Attribute", "Geometry"), )),
            "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (402.85, 110.05), None, (("Geometry", "Mesh to Curve", "Curve"), ("Value", "Boolean Math", "Boolean"), )),
        }