from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPCentripetalParametrization(CustomGeometryGroup):
    _name = "SP - Centripetal Parametrization"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_centripetal_parametrization", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        segment_cp = tree.inputs.geometry("Segment CP")
        value = tree.outputs.float("Value")

        edge_vertices = g.EdgeVertices()
        accumulate_field = g.AccumulateField.edge.float(edge_vertices.o.position_1.distance(edge_vertices.o.position_2).sqrt())
        sample_index = g.SampleIndex.edge.float(segment_cp, accumulate_field.o.leading / accumulate_field.o.total, g.Index().o.index - 1)
        (
            sample_index.o.value.point.evaluate().min(1.0).props(label="Clamp slight overshoot", width=181.62)
            >> value
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (26.66, 140.75), None, (("Value", "Math.001", "Value"), )),
            "Edge Vertices": ("GeometryNodeInputMeshEdgeVertices", (-469.41, 77.75), None, ()),
            "Evaluate on Domain": ("GeometryNodeFieldOnDomain", (543.46, 27.59), None, (("Value", "Sample Index", "Value"), )),
            "Group Input": ("NodeGroupInput", (-657.56, -30.66), None, ()),
            "Group Output": ("NodeGroupOutput", (944.95, -14.48), None, (("Value", "Math.002", "Value"), )),
            "Index": ("GeometryNodeInputIndex", (43.65, -132.69), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (208.46, -86.02), None, (("Value", "Index", "Index"), )),
            "Math.001": ("ShaderNodeMath", (-134.8, 78.15), None, (("Value", "Vector Math", "Value"), )),
            "Math.002": ("ShaderNodeMath", (716.11, 13.09), None, (("Value", "Evaluate on Domain", "Value"), )),
            "Math.003": ("ShaderNodeMath", (204.65, 94.59), None, (("Value", "Accumulate Field", "Leading"), ("Value#1", "Accumulate Field", "Total"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (372.31, 59.94), None, (("Geometry", "Group Input", "Segment CP"), ("Index", "Integer Math", "Value"), ("Value", "Math.003", "Value"), )),
            "Vector Math": ("ShaderNodeVectorMath", (-296.89, 80.4), None, (("Vector", "Edge Vertices", "Position 1"), ("Vector#1", "Edge Vertices", "Position 2"), )),
        }