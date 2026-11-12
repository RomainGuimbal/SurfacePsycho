from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPLinePlaneIntersection(CustomGeometryGroup):
    _name = "SP - Line-Plane Intersection"
    _color_tag = "VECTOR"
    _tree_properties = {"show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        with tree.inputs.panel("Line"):
            first_point = tree.inputs.vector("First Point", (0.0, 0.0, 0.0), hide_value=True)
            last_point = tree.inputs.vector("Last Point", (0.0, 0.0, 0.0), hide_value=True)
        with tree.inputs.panel("Plane"):
            normal = tree.inputs.vector("Normal", (0.0, 0.0, 0.0), hide_value=True)
            point = tree.inputs.vector("Point", (0.0, 0.0, 0.0), hide_value=True)
        vector = tree.outputs.vector("Vector")

        reroute = g.Reroute(input=g.Reroute(input=normal).props(width=19.0).o.output).props(width=19.0)
        reroute_1 = g.Reroute(input=g.Reroute(input=first_point).props(width=19.0).o.output).props(width=19.0)
        math_1 = ((first_point - point).props(hide=True).dot(reroute).props(hide=True) / (first_point - last_point).dot(reroute).props(hide=True)).props(hide=True)
        vector_math = (g.Reroute(input=last_point - first_point).props(width=19.0).o.output * math_1).props(hide=True)
        reroute_1.o.output + vector_math >> vector

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-238.09, -23.08), None, ()),
            "Group Output": ("NodeGroupOutput", (976.91, 79.13), None, (("Vector", "Vector Math.004", "Vector"), )),
            "Math": ("ShaderNodeMath", (369.41, -212.13), None, (("Value", "Vector Math.002", "Value"), ("Value#1", "Vector Math.003", "Value"), )),
            "Reroute": ("NodeReroute", (-23.09, -283.15), None, (("Input", "Group Input", "Normal"), )),
            "Reroute.001": ("NodeReroute", (116.91, -283.15), None, (("Input", "Reroute", "Output"), )),
            "Reroute.002": ("NodeReroute", (509.41, 115.5), None, (("Input", "Vector Math.005", "Vector"), )),
            "Reroute.003": ("NodeReroute", (-23.09, 208.28), None, (("Input", "Group Input", "First Point"), )),
            "Reroute.004": ("NodeReroute", (724.41, 208.28), None, (("Input", "Reroute.003", "Output"), )),
            "Vector Math": ("ShaderNodeVectorMath", (584.41, -55.29), None, (("Scale", "Math", "Value"), ("Vector", "Reroute.002", "Output"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (-23.09, -199.45), None, (("Vector", "Group Input", "First Point"), ("Vector#1", "Group Input", "Point"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (179.41, -133.97), None, (("Vector", "Vector Math.001", "Vector"), ("Vector#1", "Reroute.001", "Output"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (179.41, -212.13), None, (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Reroute.001", "Output"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (786.91, 79.13), None, (("Vector", "Reroute.004", "Output"), ("Vector#1", "Vector Math", "Vector"), )),
            "Vector Math.005": ("ShaderNodeVectorMath", (-23.09, 150.28), None, (("Vector", "Group Input", "Last Point"), ("Vector#1", "Group Input", "First Point"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (-23.09, -23.08), None, (("Vector", "Group Input", "First Point"), ("Vector#1", "Group Input", "Last Point"), )),
        }