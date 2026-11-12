from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPAutoSelectSegment(CustomGeometryGroup):
    _name = "SP - Auto Select Segment "
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_auto_select_segment_", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        auto = tree.inputs.boolean("Auto", False, structure_type="SINGLE", force_non_field=True)
        manual_index = tree.inputs.integer("Manual Index", 0, structure_type="SINGLE", force_non_field=True)
        target_geometry = tree.inputs.geometry("Target Geometry")
        sample_position = tree.inputs.vector("Sample Position", (0.0, 0.0, 0.0), hide_value=True, structure_type="SINGLE", default_input="POSITION", force_non_field=True)
        segment_index = tree.outputs.integer("Segment Index")
        distance = tree.outputs.float("Distance")

        with g.Frame("Auto nearest"):
            points = g.Points(radius=0.0)
            reroute = g.Reroute(input=target_geometry).props(width=19.0)
            sample_index = g.SampleIndex.point.integer(points, g.SampleNearest.edge(reroute, sample_position))
            sample_index_1 = g.SampleIndex.edge.integer(reroute, g.NamedAttribute.integer("segment_id").o.attribute, sample_index)
            sample_index_2 = g.SampleIndex.edge.vector(reroute, g.Position(), sample_index)
        auto.switch.integer(manual_index, sample_index_1) >> segment_index
        sample_index_3 = g.SampleIndex.point.float(points, sample_position.distance(sample_index_2))

        sample_index_3 >> distance

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Frame.003": ("NodeFrame", (-341.6, 129.09), None, ()),
            "Group Input": ("NodeGroupInput", (-536.51, 208.18), None, ()),
            "Group Output": ("NodeGroupOutput", (798.3, 181.34), None, (("Distance", "Sample Index.007", "Value"), ("Segment Index", "Switch.010", "Output"), )),
            "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (256.12, -290.32), "Frame.003", ()),
            "Points": ("GeometryNodePoints", (59.38, -203.57), "Frame.003", ()),
            "Position": ("GeometryNodeInputPosition", (249.24, -423.28), "Frame.003", ()),
            "Reroute.011": ("NodeReroute", (35.21, -193.67), "Frame.003", (("Input", "Group Input", "Target Geometry"), )),
            "Sample Index.004": ("GeometryNodeSampleIndex", (468.67, -58.86), "Frame.003", (("Geometry", "Reroute.011", "Output"), ("Index", "Sample Index.005", "Value"), ("Value", "Named Attribute.002", "Attribute"), )),
            "Sample Index.005": ("GeometryNodeSampleIndex", (257.76, -76.79), "Frame.003", (("Geometry", "Points", "Points"), ("Value", "Sample Nearest", "Index"), )),
            "Sample Index.006": ("GeometryNodeSampleIndex", (467.84, -271.93), "Frame.003", (("Geometry", "Reroute.011", "Output"), ("Index", "Sample Index.005", "Value"), ("Value", "Position", "Position"), )),
            "Sample Index.007": ("GeometryNodeSampleIndex", (514.84, -18.03), None, (("Geometry", "Points", "Points"), ("Value", "Vector Math", "Value"), )),
            "Sample Nearest": ("GeometryNodeSampleNearest", (63.13, -55.89), "Frame.003", (("Geometry", "Reroute.011", "Output"), ("Sample Position", "Group Input", "Sample Position"), )),
            "Switch.010": ("GeometryNodeSwitch", (328.64, 259.2), None, (("False", "Group Input", "Manual Index"), ("Switch", "Group Input", "Auto"), ("True", "Sample Index.004", "Value"), )),
            "Vector Math": ("ShaderNodeVectorMath", (309.76, -72.22), None, (("Vector", "Group Input", "Sample Position"), ("Vector#1", "Sample Index.006", "Value"), )),
        }