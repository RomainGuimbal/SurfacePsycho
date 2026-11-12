from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPTransposeMatrixList(CustomGeometryGroup):
    _name = "SP - Transpose Matrix [List]"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 180, "node_tool_idname": "geometry.sp_transpose_matrix", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        m = tree.inputs.integer("m", 0)
        n = tree.inputs.integer("n", 0)
        matrix = tree.inputs.float("Matrix", 0.0, hide_value=True)
        n_1 = tree.outputs.integer("n")
        m_1 = tree.outputs.integer("m")
        matrix_1 = tree.outputs.float("Matrix")

        index = g.Index()
        integer_math = (((index.o.index % m).props(label="U", hide=True) * n).props(hide=True) + (index.o.index // m).props(hide=True)).props(hide=True)
        (
            g.FieldToList(count=(m * n).props(hide=True), items={"Value": g.GetListItem.float(matrix, integer_math)})
            >> matrix_1
        )

        n >> n_1
        m >> m_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Field to List": ("GeometryNodeFieldToList", (733.81, -210.38), None, (("Count", "Integer Math.003", "Value"), ("Value", "Get List Item", "Value"), )),
            "Get List Item": ("GeometryNodeListGetItem", (522.97, -182.59), None, (("Index", "Integer Math.001", "Value"), ("List", "Group Input", "Matrix"), )),
            "Group Input": ("NodeGroupInput", (-268.72, -54.23), None, ()),
            "Group Output": ("NodeGroupOutput", (996.14, -100.15), None, (("Matrix", "Field to List", "Value"), ("m", "Group Input", "m"), ("n", "Group Input", "n"), )),
            "Index.004": ("GeometryNodeInputIndex", (6.79, 123.07), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (464.91, 23.69), None, (("Value", "Integer Math.002", "Value"), ("Value#1", "Group Input", "n"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (466.25, -12.15), None, (("Value", "Integer Math", "Value"), ("Value#1", "Integer Math.004", "Value"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (195.83, 59.78), None, (("Value", "Index.004", "Index"), ("Value#1", "Group Input", "m"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (466.51, -54.24), None, (("Value", "Group Input", "m"), ("Value#1", "Group Input", "n"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (192.68, 21.58), None, (("Value", "Index.004", "Index"), ("Value#1", "Group Input", "m"), )),
        }