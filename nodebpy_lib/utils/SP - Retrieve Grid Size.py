from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPRetrieveGridSize(CustomGeometryGroup):
    _name = "SP - Retrieve Grid Size"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160, "node_tool_idname": "geometry.sp_retrieve_grid_size", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        mesh_grid = tree.inputs.geometry("Mesh Grid")
        u_count = tree.outputs.integer("U Count")
        v_count = tree.outputs.integer("V Count")

        domain_size = g.DomainSize(mesh_grid).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        index = g.Index()
        boolean_math = ((index < domain_size.o.point_count // 2) & g.Compare.integer.not_equal(index, 0)).props(hide=True)
        boolean_math_1 = (g.Compare.integer.equal(g.VertexNeighbors().o.vertex_count, 2).o.result & boolean_math).props(hide=True)
        attribute_statistic = g.AttributeStatistic.point.float(mesh_grid, boolean_math_1, index).props(hide_outputs=["Mean", "Median", "Sum", "Min", "Range", "Standard Deviation", "Variance"])
        integer_math = g.IntegerMath(value=attribute_statistic.o.max, value_001=1).props(hide=True)
        integer_math_1 = g.IntegerMath.divide(domain_size.o.point_count, integer_math).props(hide=True)

        integer_math >> u_count
        integer_math_1 >> v_count

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Attribute Statistic": ("GeometryNodeAttributeStatistic", (462.81, -151.32), None, (("Attribute", "Index.002", "Index"), ("Geometry", "Group Input", "Mesh Grid"), ("Selection", "Boolean Math.004", "Boolean"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (235.39, -201.44), None, (("Boolean", "Compare.008", "Result"), ("Boolean#1", "Boolean Math.005", "Boolean"), )),
            "Boolean Math.005": ("FunctionNodeBooleanMath", (51.25, -202.59), None, (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
            "Compare.004": ("FunctionNodeCompare", (-143.61, -189.7), None, (("A", "Index.002", "Index"), ("B", "Integer Math.006", "Value"), )),
            "Compare.005": ("FunctionNodeCompare", (-144.19, -346.22), None, (("A", "Index.002", "Index"), )),
            "Compare.008": ("FunctionNodeCompare", (-137.57, -25.12), None, (("A", "Vertex Neighbors.002", "Vertex Count"), )),
            "Domain Size.001": ("GeometryNodeAttributeDomainSize", (-726.66, -316.05), None, (("Geometry", "Group Input", "Mesh Grid"), )),
            "Group Input": ("NodeGroupInput", (-1008.07, -229.9), None, ()),
            "Group Output": ("NodeGroupOutput", (1034.53, -225.99), None, (("U Count", "Integer Math.004", "Value"), ("V Count", "Integer Math.005", "Value"), )),
            "Index.002": ("GeometryNodeInputIndex", (-395.88, -416.48), None, ()),
            "Integer Math.004": ("FunctionNodeIntegerMath", (690.23, -232.98), None, (("Value", "Attribute Statistic", "Max"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (682.47, -334.79), None, (("Value", "Domain Size.001", "Point Count"), ("Value#1", "Integer Math.004", "Value"), )),
            "Integer Math.006": ("FunctionNodeIntegerMath", (-396.8, -278.41), None, (("Value", "Domain Size.001", "Point Count"), )),
            "Vertex Neighbors.002": ("GeometryNodeInputMeshVertexNeighbors", (-392.15, -185.31), None, ()),
        }