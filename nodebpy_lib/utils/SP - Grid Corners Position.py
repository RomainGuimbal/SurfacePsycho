from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPGridCornersPosition(CustomGeometryGroup):
    _name = "SP - Grid Corners Position"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_grid_corners_position", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        cp = tree.inputs.geometry("CP")
        u_count = tree.inputs.integer("U Count", 0)
        v_count = tree.inputs.integer("V Count", 1)
        corner_0 = tree.outputs.vector("Corner 0")
        corner_1 = tree.outputs.vector("Corner 1")
        corner_2 = tree.outputs.vector("Corner 2")
        corner_3 = tree.outputs.vector("Corner 3")

        integer_math = u_count - 1
        integer_math_1 = (u_count * v_count).props(hide=True) - 1
        position = g.Position()
        reroute = g.Reroute(input=cp).props(width=18.0)
        sample_index = g.SampleIndex.point.vector(reroute, position).props(hide=True)
        sample_index_1 = g.SampleIndex.point.vector(reroute, position, integer_math).props(hide=True)
        sample_index_2 = g.SampleIndex.point.vector(reroute, position, integer_math_1).props(hide=True)
        sample_index_3 = g.SampleIndex.point.vector(reroute, position, integer_math_1 - integer_math).props(hide=True)

        sample_index >> corner_0
        sample_index_1 >> corner_1
        sample_index_2 >> corner_2
        sample_index_3 >> corner_3

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-484.39, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (474.39, 0.0), None, (("Corner 0", "Sample Index", "Value"), ("Corner 1", "Sample Index.001", "Value"), ("Corner 2", "Sample Index.002", "Value"), ("Corner 3", "Sample Index.003", "Value"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-133.22, 80.67), None, (("Value", "Group Input", "U Count"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (60.77, -45.84), None, (("Value", "Integer Math.005", "Value"), ("Value#1", "Integer Math.002", "Value"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (-284.39, -98.55), None, (("Value", "Group Input", "U Count"), ("Value#1", "Group Input", "V Count"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (-126.91, -53.04), None, (("Value", "Integer Math.004", "Value"), )),
            "Position": ("GeometryNodeInputPosition", (83.87, 98.55), None, ()),
            "Reroute.007": ("NodeReroute", (213.92, -29.04), None, (("Input", "Group Input", "CP"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (284.39, 53.74), None, (("Geometry", "Reroute.007", "Output"), ("Value", "Position", "Position"), )),
            "Sample Index.001": ("GeometryNodeSampleIndex", (284.39, 15.02), None, (("Geometry", "Reroute.007", "Output"), ("Index", "Integer Math.002", "Value"), ("Value", "Position", "Position"), )),
            "Sample Index.002": ("GeometryNodeSampleIndex", (284.39, -23.71), None, (("Geometry", "Reroute.007", "Output"), ("Index", "Integer Math.005", "Value"), ("Value", "Position", "Position"), )),
            "Sample Index.003": ("GeometryNodeSampleIndex", (284.39, -62.43), None, (("Geometry", "Reroute.007", "Output"), ("Index", "Integer Math.003", "Value"), ("Value", "Position", "Position"), )),
        }