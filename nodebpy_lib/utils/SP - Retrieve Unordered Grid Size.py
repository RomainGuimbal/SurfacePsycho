from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPRetrieveUnorderedGridSize(CustomGeometryGroup):
    _name = "SP - Retrieve Unordered Grid Size"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_retrieve_unordered_grid_size", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.geometry("Input")
        short_side_count = tree.outputs.integer("Short side count")
        long_side_count = tree.outputs.integer("Long side count")

        reroute = g.Reroute(input=g.Reroute(input=input).props(width=19.0).o.output).props(width=19.0)
        vertex_neighbors = g.VertexNeighbors()
        compare = (vertex_neighbors.o.face_count < 4).props(label="contour")
        compare_1 = g.Compare.integer.equal(vertex_neighbors.o.face_count, 1).props(label="corner")
        with g.Frame("Distances from 1st corner"):
            index = g.Index()
            reroute_1 = g.Reroute(input=compare_1.o.result).props(width=19.0)
            accumulate_field = g.AccumulateField.point.integer(reroute_1)
            reroute_2 = g.Reroute(input=reroute_1.o.output).props(width=19.0)
            boolean_math = (reroute_2.o.output & g.Compare.integer.equal(accumulate_field.o.trailing, 0)).props(hide=True)
            boolean_math_1 = (reroute_2.o.output & g.Compare.integer.equal(accumulate_field.o.trailing, 1)).props(hide=True)
            boolean_math_2 = (reroute_2.o.output & g.Compare.integer.equal(accumulate_field.o.trailing, 2)).props(hide=True)
            boolean_math_3 = (reroute_2.o.output & g.Compare.integer.equal(accumulate_field.o.trailing, 3)).props(hide=True)
            accumulate_field_1 = g.IntegerMath.multiply(boolean_math_1, index).props(width=135.92, hide=True).o.value.point.total()
            accumulate_field_2 = g.IntegerMath.multiply(boolean_math_2, index).props(width=135.92, hide=True).o.value.point.total()
            accumulate_field_3 = g.IntegerMath.multiply(boolean_math_3, index).props(width=135.92, hide=True).o.value.point.total()
            shortest_edge_paths = g.ShortestEdgePaths(end_vertex=boolean_math, edge_cost=compare).props(width=140.0)
        sample_index = g.SampleIndex.point.integer(reroute, shortest_edge_paths.o.total_cost, g.SampleIndex.point.integer(reroute, accumulate_field_2).props(hide=True)).props(hide=True)
        sample_index_1 = g.SampleIndex.point.integer(reroute, shortest_edge_paths.o.total_cost, g.SampleIndex.point.integer(reroute, accumulate_field_1).props(hide=True)).props(hide=True)
        integer_math = sample_index_1.o.value.min(sample_index).props(hide=True)
        sample_index_2 = g.SampleIndex.point.integer(reroute, shortest_edge_paths.o.total_cost, g.SampleIndex.point.integer(reroute, accumulate_field_3).props(hide=True)).props(hide=True)
        integer_math_1 = sample_index_1.o.value.min(sample_index_2).props(hide=True)
        compare_2 = g.Compare.integer.not_equal(integer_math, integer_math_1).props(hide=True)
        integer_math_2 = sample_index.o.value.min(sample_index_2).props(hide=True)
        boolean_math_4 = (compare_2.o.result & g.Compare.integer.not_equal(integer_math_1, integer_math_2).props(hide=True)).props(hide=True)
        integer_math_3 = g.IntegerMath(value=g.IntegerMath.multiply((~compare_2.o.result).props(hide=True), 2), value_001=boolean_math_4).props(hide=True)
        index_switch = g.IndexSwitch.integer(integer_math_3, (integer_math, integer_math_1, integer_math_2)).props(label="Long side")
        index_switch_1 = g.IndexSwitch.integer((integer_math_3.o.value + 1) % 3, (integer_math, integer_math_1, integer_math_2)).props(label="Sort side")
        index_switch_1.o.output + 1 >> short_side_count
        index_switch.o.output + 1 >> long_side_count

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (35.3, -417.75), "Frame.001", (("Value", "Reroute.005", "Output"), )),
            "Accumulate Field.001": ("GeometryNodeAccumulateField", (733.33, -474.03), "Frame.001", (("Value", "Integer Math.010", "Value"), )),
            "Accumulate Field.002": ("GeometryNodeAccumulateField", (736.27, -272.35), "Frame.001", (("Value", "Integer Math.009", "Value"), )),
            "Accumulate Field.003": ("GeometryNodeAccumulateField", (733.33, -679.57), "Frame.001", (("Value", "Integer Math.011", "Value"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (746.66, -205.87), None, (("Boolean", "Compare.007", "Result"), ("Boolean#1", "Compare.011", "Result"), )),
            "Boolean Math.003": ("FunctionNodeBooleanMath", (459.6, -142.31), "Frame.001", (("Boolean", "Reroute.004", "Output"), ("Boolean#1", "Compare.006", "Result"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (614.15, -127.14), None, (("Boolean", "Compare.007", "Result"), )),
            "Boolean Math.005": ("FunctionNodeBooleanMath", (408.52, -328.82), "Frame.001", (("Boolean", "Reroute.004", "Output"), ("Boolean#1", "Compare.008", "Result"), )),
            "Boolean Math.006": ("FunctionNodeBooleanMath", (407.29, -504.51), "Frame.001", (("Boolean", "Reroute.004", "Output"), ("Boolean#1", "Compare.009", "Result"), )),
            "Boolean Math.007": ("FunctionNodeBooleanMath", (407.29, -710.06), "Frame.001", (("Boolean", "Reroute.004", "Output"), ("Boolean#1", "Compare.010", "Result"), )),
            "Compare": ("FunctionNodeCompare", (-1261.27, 411.82), None, (("A", "Vertex Neighbors", "Face Count"), )),
            "Compare.001": ("FunctionNodeCompare", (-1268.5, 251.56), None, (("A", "Vertex Neighbors", "Face Count"), )),
            "Compare.006": ("FunctionNodeCompare", (235.24, -252.31), "Frame.001", (("A", "Accumulate Field", "Trailing"), )),
            "Compare.007": ("FunctionNodeCompare", (572.26, -179.41), None, (("A", "Integer Math", "Value"), ("B", "Integer Math.001", "Value"), )),
            "Compare.008": ("FunctionNodeCompare", (230.62, -423.96), "Frame.001", (("A", "Accumulate Field", "Trailing"), )),
            "Compare.009": ("FunctionNodeCompare", (231.99, -592.73), "Frame.001", (("A", "Accumulate Field", "Trailing"), )),
            "Compare.010": ("FunctionNodeCompare", (228.22, -759.78), "Frame.001", (("A", "Accumulate Field", "Trailing"), )),
            "Compare.011": ("FunctionNodeCompare", (568.64, -223.05), None, (("A", "Integer Math.001", "Value"), ("B", "Integer Math.002", "Value"), )),
            "Frame.001": ("NodeFrame", (-1048.51, 253.3), None, ()),
            "Group Input": ("NodeGroupInput", (-1468.7, 522.5), None, ()),
            "Group Output": ("NodeGroupOutput", (1712.99, 0.0), None, (("Long side count", "Integer Math.008", "Value"), ("Short side count", "Integer Math.007", "Value"), )),
            "Index Switch.001": ("GeometryNodeIndexSwitch", (1333.03, -101.5), None, (("0", "Integer Math", "Value"), ("1", "Integer Math.001", "Value"), ("2", "Integer Math.002", "Value"), ("Index", "Integer Math.004", "Value"), )),
            "Index Switch.002": ("GeometryNodeIndexSwitch", (1330.5, 147.04), None, (("0", "Integer Math", "Value"), ("1", "Integer Math.001", "Value"), ("2", "Integer Math.002", "Value"), ("Index", "Integer Math.006", "Value"), )),
            "Index.001": ("GeometryNodeInputIndex", (416.21, -237.63), "Frame.001", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (379.13, -168.63), None, (("Value", "Sample Index.008", "Value"), ("Value#1", "Sample Index.007", "Value"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (379.13, -205.37), None, (("Value", "Sample Index.008", "Value"), ("Value#1", "Sample Index.009", "Value"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (379.13, -242.1), None, (("Value", "Sample Index.007", "Value"), ("Value#1", "Sample Index.009", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (626.1, 40.15), None, (("Value", "Boolean Math.004", "Boolean"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (829.77, 41.56), None, (("Value", "Integer Math.003", "Value"), ("Value#1", "Boolean Math.001", "Boolean"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (998.89, 176.15), None, (("Value", "Integer Math.004", "Value"), )),
            "Integer Math.006": ("FunctionNodeIntegerMath", (1161.64, 177.88), None, (("Value", "Integer Math.005", "Value"), )),
            "Integer Math.007": ("FunctionNodeIntegerMath", (1508.11, 110.04), None, (("Value", "Index Switch.002", "Output"), )),
            "Integer Math.008": ("FunctionNodeIntegerMath", (1513.15, -93.95), None, (("Value", "Index Switch.001", "Output"), )),
            "Integer Math.009": ("FunctionNodeIntegerMath", (576.62, -332.83), "Frame.001", (("Value", "Boolean Math.005", "Boolean"), ("Value#1", "Index.001", "Index"), )),
            "Integer Math.010": ("FunctionNodeIntegerMath", (575.2, -515.73), "Frame.001", (("Value", "Boolean Math.006", "Boolean"), ("Value#1", "Index.001", "Index"), )),
            "Integer Math.011": ("FunctionNodeIntegerMath", (575.66, -716.24), "Frame.001", (("Value", "Boolean Math.007", "Boolean"), ("Value#1", "Index.001", "Index"), )),
            "Reroute.002": ("NodeReroute", (-68.33, 69.76), None, (("Input", "Reroute.003", "Output"), )),
            "Reroute.003": ("NodeReroute", (-462.86, 488.69), None, (("Input", "Group Input", "Input"), )),
            "Reroute.004": ("NodeReroute", (370.27, -139.25), "Frame.001", (("Input", "Reroute.005", "Output"), )),
            "Reroute.005": ("NodeReroute", (35.21, -41.06), "Frame.001", (("Input", "Compare.001", "Result"), )),
            "Sample Index.004": ("GeometryNodeSampleIndex", (28.78, -201.01), None, (("Geometry", "Reroute.002", "Output"), ("Value", "Accumulate Field.001", "Total"), )),
            "Sample Index.005": ("GeometryNodeSampleIndex", (30.07, -155.48), None, (("Geometry", "Reroute.002", "Output"), ("Value", "Accumulate Field.002", "Total"), )),
            "Sample Index.006": ("GeometryNodeSampleIndex", (25.17, -249.92), None, (("Geometry", "Reroute.002", "Output"), ("Value", "Accumulate Field.003", "Total"), )),
            "Sample Index.007": ("GeometryNodeSampleIndex", (204.23, -208.22), None, (("Geometry", "Reroute.002", "Output"), ("Index", "Sample Index.004", "Value"), ("Value", "Shortest Edge Paths.001", "Total Cost"), )),
            "Sample Index.008": ("GeometryNodeSampleIndex", (206.53, -158.43), None, (("Geometry", "Reroute.002", "Output"), ("Index", "Sample Index.005", "Value"), ("Value", "Shortest Edge Paths.001", "Total Cost"), )),
            "Sample Index.009": ("GeometryNodeSampleIndex", (200.62, -257.13), None, (("Geometry", "Reroute.002", "Output"), ("Index", "Sample Index.006", "Value"), ("Value", "Shortest Edge Paths.001", "Total Cost"), )),
            "Shortest Edge Paths.001": ("GeometryNodeInputShortestEdgePaths", (732.29, -128.73), "Frame.001", (("Edge Cost", "Compare", "Result"), ("End Vertex", "Boolean Math.003", "Boolean"), )),
            "Vertex Neighbors": ("GeometryNodeInputMeshVertexNeighbors", (-1522.99, 314.12), None, ()),
        }