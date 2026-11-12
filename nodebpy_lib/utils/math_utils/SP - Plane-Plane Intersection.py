from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPPlanePlaneIntersection(CustomGeometryGroup):
    _name = "SP - Plane-Plane Intersection"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_plane_plane_intersection", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        with tree.inputs.panel("Plane 1"):
            point = tree.inputs.vector("Point", (0.0, 0.0, 0.0), hide_value=True)
            normal = tree.inputs.vector("Normal", (0.0, 0.0, 0.0), hide_value=True)
        with tree.inputs.panel("Plane 2"):
            point_1 = tree.inputs.vector("Point", (0.0, 0.0, 0.0), hide_value=True)
            normal_1 = tree.inputs.vector("Normal", (0.0, 0.0, 0.0), hide_value=True)
        line_point = tree.outputs.vector("Line Point")
        line_direction = tree.outputs.vector("Line Direction")

        vector_math = normal.dot(normal_1)
        math_1 = 1.0 - (vector_math * vector_math).props(hide=True)
        normal.cross(normal_1) >> line_direction
        reroute = g.Reroute(input=point.dot(normal)).props(label="d1", width=19.0)
        reroute_1 = g.Reroute(input=point_1.dot(normal_1)).props(label="d2", width=19.0)
        math_2 = ((reroute_1.o.output - (reroute.o.output * vector_math).props(hide=True)) / math_1).props(label="c2")
        math_3 = ((reroute.o.output - (reroute_1.o.output * vector_math).props(hide=True)) / math_1).props(label="c1")
        normal * math_3 + normal_1 * math_2 >> line_point

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-1249.55, 155.73), None, ()),
            "Group Output": ("NodeGroupOutput", (939.03, 38.21), None, (("Line Direction", "Vector Math.002", "Vector"), ("Line Point", "Vector Math.008", "Vector"), )),
            "Math": ("ShaderNodeMath", (-139.32, 196.05), None, (("Value", "Reroute.005", "Output"), ("Value#1", "Math.001", "Value"), )),
            "Math.001": ("ShaderNodeMath", (-313.62, 70.39), None, (("Value", "Reroute.006", "Output"), ("Value#1", "Vector Math", "Value"), )),
            "Math.002": ("ShaderNodeMath", (-139.32, -9.66), None, (("Value", "Reroute.006", "Output"), ("Value#1", "Math.005", "Value"), )),
            "Math.003": ("ShaderNodeMath", (-325.14, -260.43), None, (("Value", "Vector Math", "Value"), ("Value#1", "Vector Math", "Value"), )),
            "Math.004": ("ShaderNodeMath", (-132.48, -184.16), None, (("Value#1", "Math.003", "Value"), )),
            "Math.005": ("ShaderNodeMath", (-313.62, -129.7), None, (("Value", "Reroute.005", "Output"), ("Value#1", "Vector Math", "Value"), )),
            "Math.006": ("ShaderNodeMath", (118.07, -53.97), None, (("Value", "Math.002", "Value"), ("Value#1", "Math.004", "Value"), )),
            "Math.007": ("ShaderNodeMath", (116.89, 108.49), None, (("Value", "Math", "Value"), ("Value#1", "Math.004", "Value"), )),
            "Reroute.005": ("NodeReroute", (-504.05, 96.24), None, (("Input", "Vector Math.003", "Value"), )),
            "Reroute.006": ("NodeReroute", (-493.07, -65.16), None, (("Input", "Vector Math.004", "Value"), )),
            "Vector Math": ("ShaderNodeVectorMath", (-732.97, -174.12), None, (("Vector", "Group Input", "Normal"), ("Vector#1", "Group Input", "Normal#1"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (-713.37, -450.81), None, (("Vector", "Group Input", "Normal"), ("Vector#1", "Group Input", "Normal#1"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (-738.87, 133.16), None, (("Vector", "Group Input", "Point"), ("Vector#1", "Group Input", "Normal"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (-730.59, -13.21), None, (("Vector", "Group Input", "Point#1"), ("Vector#1", "Group Input", "Normal#1"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (357.59, 243.41), None, (("Scale", "Math.007", "Value"), ("Vector", "Group Input", "Normal"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (359.48, 103.63), None, (("Scale", "Math.006", "Value"), ("Vector", "Group Input", "Normal#1"), )),
            "Vector Math.008": ("ShaderNodeVectorMath", (610.75, 183.07), None, (("Vector", "Vector Math.006", "Vector"), ("Vector#1", "Vector Math.007", "Vector"), )),
        }