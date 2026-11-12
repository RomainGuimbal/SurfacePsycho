from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPMirrorPoint(CustomGeometryGroup):
    _name = "SP - Mirror Point"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_mirror_vector_relative", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        point = tree.inputs.vector("Point", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        with tree.inputs.panel("Mirror Plane"):
            plane_normal = tree.inputs.vector("Plane Normal", (0.0, 1.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
            plane_origin = tree.inputs.vector("Plane Origin", (0.0, 0.0, 0.0), hide_value=True)
        result = tree.outputs.vector("Result")

        (
            ((point - plane_origin).reflect(plane_normal) + plane_origin).props(hide=True)
            >> result
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-383.52, 57.23), None, ()),
            "Group Output": ("NodeGroupOutput", (472.27, 54.56), None, (("Result", "Vector Math.006", "Vector"), )),
            "Vector Math": ("ShaderNodeVectorMath", (111.99, 158.9), None, (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Group Input", "Plane Normal"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (293.81, 32.6), None, (("Vector", "Vector Math", "Vector"), ("Vector#1", "Group Input", "Plane Origin"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (-104.43, 155.24), None, (("Vector", "Group Input", "Point"), ("Vector#1", "Group Input", "Plane Origin"), )),
        }