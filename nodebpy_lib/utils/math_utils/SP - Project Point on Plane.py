from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPProjectPointOnPlane(CustomGeometryGroup):
    _name = "SP - Project Point on Plane"
    _color_tag = "VECTOR"
    _tree_properties = {"default_group_node_width": 180, "node_tool_idname": "geometry.sp_project_point_on_plane", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        point_postion = tree.inputs.vector("Point postion", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
        normal = tree.inputs.vector("Normal", (0.0, 0.0, 0.0), hide_value=True)
        origin = tree.inputs.vector("Origin", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        projected_position = tree.outputs.vector("Projected Position")

        point_postion - normal * (point_postion - origin).dot(normal) >> projected_position

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-485.26, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (475.26, 0.0), None, (("Projected Position", "Vector Math.008", "Vector"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (-88.72, 129.75), None, (("Vector", "Vector Math.010", "Vector"), ("Vector#1", "Group Input", "Normal"), )),
            "Vector Math.008": ("ShaderNodeVectorMath", (263.19, 29.67), None, (("Vector", "Group Input", "Point postion"), ("Vector#1", "Vector Math.009", "Vector"), )),
            "Vector Math.009": ("ShaderNodeVectorMath", (92.72, 92.98), None, (("Scale", "Vector Math.007", "Value"), ("Vector", "Group Input", "Normal"), )),
            "Vector Math.010": ("ShaderNodeVectorMath", (-273.07, 150.19), None, (("Vector", "Group Input", "Point postion"), ("Vector#1", "Group Input", "Origin"), )),
        }