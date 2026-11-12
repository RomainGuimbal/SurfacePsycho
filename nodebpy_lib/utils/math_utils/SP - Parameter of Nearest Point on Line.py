from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPParameterOfNearestPointOnLine(CustomGeometryGroup):
    _name = "SP - Parameter of Nearest Point on Line"
    _color_tag = "VECTOR"
    _tree_properties = {"default_group_node_width": 240}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        position = tree.inputs.vector("Position", (0.0, 0.0, 0.0))
        with tree.inputs.panel("Line"):
            origin = tree.inputs.vector("Origin", (0.0, 0.0, 0.0), hide_value=True)
            direction = tree.inputs.vector("Direction", (0.0, 0.0, 0.0), hide_value=True)
        value = tree.outputs.float("Value")

        (
            (position - origin).props(width=100.0).dot(direction) / direction.dot(direction)
            >> value
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-422.13, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (385.45, -34.12), None, (("Value", "Math.002", "Value"), )),
            "Math.002": ("ShaderNodeMath", (207.07, -57.49), None, (("Value", "Vector Math", "Value"), ("Value#1", "Vector Math.002", "Value"), )),
            "Vector Math": ("ShaderNodeVectorMath", (-6.02, -37.66), None, (("Vector", "Vector Math.012", "Vector"), ("Vector#1", "Group Input", "Direction"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (-8.93, -77.47), None, (("Vector", "Group Input", "Direction"), ("Vector#1", "Group Input", "Direction"), )),
            "Vector Math.012": ("ShaderNodeVectorMath", (-184.18, -14.16), None, (("Vector", "Group Input", "Position"), ("Vector#1", "Group Input", "Origin"), )),
        }