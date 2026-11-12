from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class MengerCurvature(CustomGeometryGroup):
    _name = "Menger curvature"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.menger_curvature", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        p1 = tree.inputs.vector("P1", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
        center = tree.inputs.vector("Center", (0.0, 0.0, 0.0))
        p2 = tree.inputs.vector("P2", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
        menger_curvature = tree.outputs.float("Menger curvature")

        reroute = g.Reroute(input=center).props(width=19.0)
        reroute_1 = g.Reroute(input=p1).props(width=19.0)
        reroute_2 = g.Reroute(input=p2).props(width=19.0)
        reroute_3 = g.Reroute(input=center).props(width=19.0)
        math_1 = (reroute_1.o.output.distance(reroute_3) * reroute_3.o.output.distance(reroute_2)).props(hide=True)
        (
            (p1 - reroute).cross(p2 - reroute).length() * 2.0 / (math_1 * reroute_1.o.output.distance(reroute_2)).props(hide=True)
            >> menger_curvature
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-683.21, -248.39), None, ()),
            "Group Output": ("NodeGroupOutput", (761.81, -61.46), None, (("Menger curvature", "Math.001", "Value"), )),
            "Math": ("ShaderNodeMath", (268.11, 189.47), None, (("Value", "Vector Math.006", "Value"), )),
            "Math.001": ("ShaderNodeMath", (546.61, -58.26), None, (("Value", "Math", "Value"), ("Value#1", "Math.003", "Value"), )),
            "Math.002": ("ShaderNodeMath", (174.47, -319.93), None, (("Value", "Vector Math.003", "Value"), ("Value#1", "Vector Math.004", "Value"), )),
            "Math.003": ("ShaderNodeMath", (170.74, -370.68), None, (("Value", "Math.002", "Value"), ("Value#1", "Vector Math.005", "Value"), )),
            "Reroute": ("NodeReroute", (-339.48, -85.64), None, (("Input", "Group Input", "Center"), )),
            "Reroute.001": ("NodeReroute", (-349.79, -283.92), None, (("Input", "Group Input", "P1"), )),
            "Reroute.002": ("NodeReroute", (-357.54, -393.79), None, (("Input", "Group Input", "P2"), )),
            "Reroute.003": ("NodeReroute", (-351.79, -341.57), None, (("Input", "Group Input", "Center"), )),
            "Vector Math": ("ShaderNodeVectorMath", (-120.39, 45.43), None, (("Vector", "Vector Math.001", "Vector"), ("Vector#1", "Vector Math.002", "Vector"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (-307.33, 84.83), None, (("Vector", "Group Input", "P1"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (-295.96, -84.47), None, (("Vector", "Group Input", "P2"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (-59.8, -148.93), None, (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute.003", "Output"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (-62.75, -286.91), None, (("Vector", "Reroute.003", "Output"), ("Vector#1", "Reroute.002", "Output"), )),
            "Vector Math.005": ("ShaderNodeVectorMath", (-62.84, -421.0), None, (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute.002", "Output"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (61.88, 47.8), None, (("Vector", "Vector Math", "Vector"), )),
        }