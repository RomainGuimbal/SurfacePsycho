from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPIsAlreadyMeshed(CustomGeometryGroup):
    _name = "SP - Is Already Meshed"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160, "node_tool_idname": "geometry.sp_object_type", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        object_geometry = tree.inputs.geometry("Object Geometry")
        value = tree.outputs.boolean("Value")

        boolean_math = (g.NamedAttribute.vector("CP_curve").props(width=100.0).o.exists | g.NamedAttribute.vector("CP_planar").props(width=100.0).o.exists).props(width=100.0, hide=True)
        boolean_math_1 = (g.NamedAttribute.vector("CP_any_order_surf").props(width=148.77).o.exists | g.NamedAttribute.vector("CP_NURBS_surf").props(width=119.54).o.exists).props(hide=True)
        (
            object_geometry
            >> g.SampleIndex.point.boolean(value=(boolean_math_1 | boolean_math).props(hide=True))
            >> value
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (17.58, 27.06), None, (("Boolean", "Named Attribute.004", "Exists"), ("Boolean#1", "Named Attribute.006", "Exists"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (219.16, -119.05), None, (("Boolean", "Boolean Math", "Boolean"), ("Boolean#1", "Boolean Math.002", "Boolean"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (5.91, -214.82), None, (("Boolean", "Named Attribute.003", "Exists"), ("Boolean#1", "Named Attribute.005", "Exists"), )),
            "Group Input": ("NodeGroupInput", (-182.4, 254.02), None, ()),
            "Group Output": ("NodeGroupOutput", (744.67, 107.98), None, (("Value", "Sample Index.004", "Value"), )),
            "Named Attribute.003": ("GeometryNodeInputNamedAttribute", (-125.21, -115.02), None, ()),
            "Named Attribute.004": ("GeometryNodeInputNamedAttribute", (-174.08, 151.26), None, ()),
            "Named Attribute.005": ("GeometryNodeInputNamedAttribute", (-130.18, -258.88), None, ()),
            "Named Attribute.006": ("GeometryNodeInputNamedAttribute", (-144.82, 17.38), None, ()),
            "Sample Index.004": ("GeometryNodeSampleIndex", (434.34, 211.22), None, (("Geometry", "Group Input", "Object Geometry"), ("Value", "Boolean Math.001", "Boolean"), )),
        }