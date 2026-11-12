from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class CatmullRomToBezier(CustomGeometryGroup):
    _name = "Catmull-Rom to Bezier"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.catmull_rom_to_bezier", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        p0 = tree.inputs.vector("P0'", (0.0, 0.0, 0.0), hide_value=True)
        p1 = tree.inputs.vector("P1'", (0.0, 0.0, 0.0), hide_value=True)
        p2 = tree.inputs.vector("P2'", (0.0, 0.0, 0.0), hide_value=True)
        p3 = tree.inputs.vector("P3'", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        tension = tree.inputs.float("Tension", 1.0, min_value=-10_000.0, max_value=10_000.0)
        p0_1 = tree.outputs.vector("P0")
        p1_1 = tree.outputs.vector("P1")
        p2_1 = tree.outputs.vector("P2")
        p3_1 = tree.outputs.vector("P3")

        math_1 = tension * 6.0
        (
            g.Reroute(input=g.Reroute(input=p1).props(width=9.5).o.output).props(width=9.5)
            >> p0_1
        )
        reroute = g.Reroute(input=p2).props(width=9.5)
        reroute_1 = g.Reroute(input=reroute.o.output).props(width=9.5)
        g.Reroute(input=reroute_1.o.output).props(width=9.5) >> p3_1
        (reroute.o.output - p0) / math_1 + p1 >> p1_1
        reroute_1.o.output - (p3 - p1) / math_1 >> p2_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-421.34, 18.25), None, ()),
            "Group Output": ("NodeGroupOutput", (745.12, 105.45), None, (("P0", "Reroute.002", "Output"), ("P1", "Vector Math", "Vector"), ("P2", "Vector Math.005", "Vector"), ("P3", "Reroute.003", "Output"), )),
            "Math.005": ("ShaderNodeMath", (22.86, -214.17), None, (("Value", "Group Input", "Tension"), )),
            "Reroute": ("NodeReroute", (23.43, 169.3), None, (("Input", "Group Input", "P1'"), )),
            "Reroute.001": ("NodeReroute", (393.2, -165.57), None, (("Input", "Reroute.008", "Output"), )),
            "Reroute.002": ("NodeReroute", (546.97, 169.3), None, (("Input", "Reroute", "Output"), )),
            "Reroute.003": ("NodeReroute", (587.55, -165.57), None, (("Input", "Reroute.001", "Output"), )),
            "Reroute.008": ("NodeReroute", (-51.58, -165.57), None, (("Input", "Group Input", "P2'"), )),
            "Vector Math": ("ShaderNodeVectorMath", (440.3, 135.87), None, (("Vector", "Vector Math.002", "Vector"), ("Vector#1", "Group Input", "P1'"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (25.3, 135.87), None, (("Vector", "Reroute.008", "Output"), ("Vector#1", "Group Input", "P0'"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (232.8, 134.37), None, (("Vector", "Vector Math.001", "Vector"), ("Vector#1", "Math.005", "Value"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (231.94, -14.44), None, (("Vector", "Vector Math.004", "Vector"), ("Vector#1", "Math.005", "Value"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (24.44, -12.94), None, (("Vector", "Group Input", "P3'"), ("Vector#1", "Group Input", "P1'"), )),
            "Vector Math.005": ("ShaderNodeVectorMath", (439.44, -12.94), None, (("Vector", "Reroute.001", "Output"), ("Vector#1", "Vector Math.003", "Vector"), )),
        }