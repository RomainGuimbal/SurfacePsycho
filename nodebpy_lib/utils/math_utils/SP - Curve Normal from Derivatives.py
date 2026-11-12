from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPCurveNormalFromDerivatives(CustomGeometryGroup):
    _name = "SP - Curve Normal from Derivatives"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 240, "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        velocity = tree.inputs.vector("Velocity", (0.0, 0.0, 0.0), hide_value=True)
        acceleration = tree.inputs.vector("Acceleration", (1.0, 1.0, 1.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        normal = tree.outputs.vector("Normal")

        reroute = g.Reroute(input=velocity).props(width=19.0)
        acceleration.cross(reroute).cross(reroute).normalize() >> normal

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-206.82, 29.54), None, ()),
            "Group Output": ("NodeGroupOutput", (252.93, 0.0), None, (("Normal", "Vector Math.033", "Vector"), )),
            "Reroute.009": ("NodeReroute", (2.34, -32.13), None, (("Input", "Group Input", "Velocity"), )),
            "Vector Math.030": ("ShaderNodeVectorMath", (32.86, 22.57), None, (("Vector", "Group Input", "Acceleration"), ("Vector#1", "Reroute.009", "Output"), )),
            "Vector Math.032": ("ShaderNodeVectorMath", (30.03, -20.79), None, (("Vector", "Vector Math.030", "Vector"), ("Vector#1", "Reroute.009", "Output"), )),
            "Vector Math.033": ("ShaderNodeVectorMath", (30.03, -62.79), None, (("Vector", "Vector Math.032", "Vector"), )),
        }