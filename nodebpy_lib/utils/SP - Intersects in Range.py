from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPIntersectsInRange(CustomGeometryGroup):
    _name = "SP - Intersects in Range"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 220}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        t1 = tree.inputs.float("t1", 0.0)
        t2 = tree.inputs.float("t2", 0.0)
        boolean = tree.outputs.boolean("Boolean")

        reroute = g.Reroute(input=t1).props(width=19.0)
        reroute_1 = g.Reroute(input=t2).props(width=19.0)
        (
            ((reroute >= 0.0) & (reroute <= 1.0) & ((reroute_1 >= 0.0) & (reroute_1 <= 1.0)))
            >> boolean
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (22.58, 163.67), None, (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Compare.003", "Result"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (217.48, 27.62), None, (("Boolean", "Boolean Math", "Boolean"), ("Boolean#1", "Boolean Math.006", "Boolean"), )),
            "Boolean Math.006": ("FunctionNodeBooleanMath", (37.55, -157.97), None, (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
            "Compare.002": ("FunctionNodeCompare", (-137.79, 218.94), None, (("A", "Reroute.044", "Output"), )),
            "Compare.003": ("FunctionNodeCompare", (-137.79, 60.94), None, (("A", "Reroute.044", "Output"), )),
            "Compare.004": ("FunctionNodeCompare", (-137.79, -97.06), None, (("A", "Reroute.045", "Output"), )),
            "Compare.005": ("FunctionNodeCompare", (-137.79, -255.06), None, (("A", "Reroute.045", "Output"), )),
            "Group Input": ("NodeGroupInput", (-417.48, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (437.57, 0.0), None, (("Boolean", "Boolean Math.001", "Boolean"), )),
            "Reroute.044": ("NodeReroute", (-182.28, 13.09), None, (("Input", "Group Input", "t1"), )),
            "Reroute.045": ("NodeReroute", (-182.28, -214.5), None, (("Input", "Group Input", "t2"), )),
        }