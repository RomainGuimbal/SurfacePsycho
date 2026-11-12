from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPHasTrimFromMeshed(CustomGeometryGroup):
    _name = "SP - Has Trim [From Meshed]"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 200, "node_tool_idname": "geometry.sp_object_type", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        meshed_geom = tree.inputs.geometry("Meshed Geom")
        has_trim = tree.outputs.boolean("Has Trim")

        (
            (meshed_geom >> g.SampleIndex.point.boolean(value=g.NamedAttribute.vector("CP_trim_contour_UV").props(width=138.88).o.exists)).props(label="no wire index case")
            >> has_trim
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (280.62, 69.19), None, ()),
            "Group Output": ("NodeGroupOutput", (728.02, 66.82), None, (("Has Trim", "Sample Index.003", "Value"), )),
            "Named Attribute.007": ("GeometryNodeInputNamedAttribute", (299.23, -20.36), None, ()),
            "Sample Index.003": ("GeometryNodeSampleIndex", (540.45, 106.99), None, (("Geometry", "Group Input", "Meshed Geom"), ("Value", "Named Attribute.007", "Exists"), )),
        }