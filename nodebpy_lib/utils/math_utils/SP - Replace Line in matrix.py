from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPReplaceLineInMatrix(CustomGeometryGroup):
    _name = "SP - Replace Line in matrix"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_replace_line_in_matrix", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        matrix = tree.inputs.float("Matrix", 0.0)
        n = tree.inputs.integer("n", 0, min_value=1, structure_type="SINGLE", force_non_field=True)
        new_line = tree.inputs.float("New Line", 0.0)
        line_position = tree.inputs.integer("Line Position", 0, min_value=1)
        output = tree.outputs.float("Output")

        evaluate_at_index = new_line.point.at(g.Index().o.index - (n * line_position).props(hide=True))
        with g.Frame("Insert"):
            (
                g.Compare.integer.equal((g.Index().o.index // n).props(hide=True), line_position).o.result.switch.float(matrix, evaluate_at_index)
                >> output
            )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Compare.001": ("FunctionNodeCompare", (390.31, -35.94), "Frame", (("A", "Integer Math.003", "Value"), ("B", "Group Input", "Line Position"), )),
            "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (553.13, -14.19), None, (("Index", "Integer Math.004", "Value"), ("Value", "Group Input", "New Line"), )),
            "Frame": ("NodeFrame", (203.82, 269.51), None, ()),
            "Group Input": ("NodeGroupInput", (-280.86, 133.02), None, ()),
            "Group Output": ("NodeGroupOutput", (1068.39, 202.21), None, (("Output", "Switch.001", "Output"), )),
            "Index.002": ("GeometryNodeInputIndex", (30.34, -85.49), "Frame", ()),
            "Index.003": ("GeometryNodeInputIndex", (82.29, -99.79), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (83.08, -166.98), None, (("Value", "Group Input", "n"), ("Value#1", "Group Input", "Line Position"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (208.63, -134.72), "Frame", (("Value", "Index.002", "Index"), ("Value#1", "Group Input", "n"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (283.67, -112.16), None, (("Value", "Index.003", "Index"), ("Value#1", "Integer Math", "Value"), )),
            "Switch.001": ("GeometryNodeSwitch", (582.01, -61.3), "Frame", (("False", "Group Input", "Matrix"), ("Switch", "Compare.001", "Result"), ("True", "Evaluate at Index.001", "Value"), )),
        }