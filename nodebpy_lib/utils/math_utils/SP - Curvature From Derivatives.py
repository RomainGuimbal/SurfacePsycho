from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPCurvatureFromDerivatives(CustomGeometryGroup):
    _name = "SP - Curvature From Derivatives"
    _color_tag = "VECTOR"
    _tree_properties = {"default_group_node_width": 200, "node_tool_idname": "geometry.sp_curvature_from_derivatives", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tangent = tree.inputs.vector("Tangent", (0.0, 0.0, 0.0), hide_value=True)
        acceleration = tree.inputs.vector("Acceleration", (0.0, 0.0, 0.0), hide_value=True)
        curvature = tree.outputs.vector("Curvature")

        reroute = g.Reroute(input=g.Reroute(input=acceleration).props(width=19.0).o.output).props(width=19.0)
        vector_math = tangent.dot(tangent).props(hide=True)
        vector_math_1 = g.Reroute(input=g.Reroute(input=tangent).props(width=19.0).o.output).props(width=19.0).o.output * (tangent.dot(acceleration) / vector_math)
        (
            (reroute.o.output - vector_math_1) / g.Reroute(input=vector_math).props(width=19.0)
            >> curvature
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-589.07, 63.16), None, ()),
            "Group Output": ("NodeGroupOutput", (588.43, 41.7), None, (("Curvature", "Vector Math.009", "Vector"), )),
            "Math.006": ("ShaderNodeMath", (-184.07, 13.65), None, (("Value", "Vector Math.016", "Value"), ("Value#1", "Vector Math.006", "Value"), )),
            "Reroute": ("NodeReroute", (-386.57, 149.81), None, (("Input", "Group Input", "Tangent"), )),
            "Reroute.001": ("NodeReroute", (-44.07, 149.81), None, (("Input", "Reroute", "Output"), )),
            "Reroute.002": ("NodeReroute", (-386.57, -183.53), None, (("Input", "Group Input", "Acceleration"), )),
            "Reroute.003": ("NodeReroute", (158.43, -183.53), None, (("Input", "Reroute.002", "Output"), )),
            "Reroute.004": ("NodeReroute", (348.43, 77.8), None, (("Input", "Vector Math.006", "Value"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (-386.57, 87.73), None, (("Vector", "Group Input", "Tangent"), ("Vector#1", "Group Input", "Tangent"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (208.43, -43.35), None, (("Vector", "Reroute.003", "Output"), ("Vector#1", "Vector Math.008", "Vector"), )),
            "Vector Math.008": ("ShaderNodeVectorMath", (18.43, 13.65), None, (("Scale", "Math.006", "Value"), ("Vector", "Reroute.001", "Output"), )),
            "Vector Math.009": ("ShaderNodeVectorMath", (398.43, 41.7), None, (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Reroute.004", "Output"), )),
            "Vector Math.016": ("ShaderNodeVectorMath", (-386.57, 13.65), None, (("Vector", "Group Input", "Tangent"), ("Vector#1", "Group Input", "Acceleration"), )),
        }