from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class GridCoordinatesToIndex(CustomGeometryGroup):
    _name = "Grid Coordinates to Index"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        u_count = tree.inputs.integer("U Count", 0)
        u = tree.inputs.integer("U", 0)
        v = tree.inputs.integer("V", 0, description="Index of the current iteration. Starts counting at zero")
        value = tree.outputs.integer("Value")

        ((u_count * v).props(width=100.0) + u).props(width=100.0) >> value

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-274.61, 20.03), None, ()),
            "Group Output": ("NodeGroupOutput", (104.32, 25.53), None, (("Value", "Integer Math.024", "Value"), )),
            "Integer Math.019": ("FunctionNodeIntegerMath", (-54.36, -43.98), None, (("Value", "Group Input", "U Count"), ("Value#1", "Group Input", "V"), )),
            "Integer Math.024": ("FunctionNodeIntegerMath", (-55.68, -4.36), None, (("Value", "Integer Math.019", "Value"), ("Value#1", "Group Input", "U"), )),
        }