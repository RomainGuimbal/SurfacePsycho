from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPDetectedSegmentTypesToType(CustomGeometryGroup):
    _name = "SP - Detected Segment Types to Type"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_dectected_segment_types_to_type", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        is_ellipse = tree.inputs.boolean("Is Ellipse", False)
        is_ellipse_arc = tree.inputs.boolean("Is Ellipse Arc", False)
        is_circle = tree.inputs.boolean("Is Circle", False)
        is_arc = tree.inputs.boolean("Is Arc", False)
        is_nurbs = tree.inputs.boolean("Is NURBS", False)
        segment_type = tree.outputs.integer("Segment Type")

        with g.Frame():
            _reroute = g.Reroute().props(label="0 Bezier", width=9.5)
            _reroute_1 = g.Reroute().props(label="1 Nurbs", width=9.5)
            _reroute_2 = g.Reroute().props(label="2 Circle Arc", width=9.5)
            _reroute_3 = g.Reroute().props(label="3 Circle", width=9.5)
            _reroute_4 = g.Reroute().props(label="4 Ellipse Arc", width=9.5)
            _reroute_5 = g.Reroute().props(label="5 Ellipse", width=9.5)
        switch = is_ellipse_arc.switch.integer(is_circle.switch.integer(is_arc.switch.integer(is_nurbs.switch.integer(true=1), 2), 3), 4)
        is_ellipse.switch.integer(switch, 5) >> segment_type

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Frame.004": ("NodeFrame", (370.02, -88.47), None, ()),
            "Group Input": ("NodeGroupInput", (-522.97, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (509.0, 186.9), None, (("Segment Type", "Switch.010", "Output"), )),
            "Reroute.002": ("NodeReroute", (36.14, -35.21), "Frame.004", ()),
            "Reroute.003": ("NodeReroute", (36.14, -71.33), "Frame.004", ()),
            "Reroute.005": ("NodeReroute", (36.14, -106.8), "Frame.004", ()),
            "Reroute.006": ("NodeReroute", (36.14, -144.46), "Frame.004", ()),
            "Reroute.020": ("NodeReroute", (35.21, -181.75), "Frame.004", ()),
            "Reroute.021": ("NodeReroute", (35.21, -219.4), "Frame.004", ()),
            "Switch.007": ("GeometryNodeSwitch", (-6.95, -15.02), None, (("False", "Switch.012", "Output"), ("Switch", "Group Input", "Is Circle"), )),
            "Switch.009": ("GeometryNodeSwitch", (149.0, 93.31), None, (("False", "Switch.007", "Output"), ("Switch", "Group Input", "Is Ellipse Arc"), )),
            "Switch.010": ("GeometryNodeSwitch", (304.58, 202.16), None, (("False", "Switch.009", "Output"), ("Switch", "Group Input", "Is Ellipse"), )),
            "Switch.011": ("GeometryNodeSwitch", (-318.83, -231.68), None, (("Switch", "Group Input", "Is NURBS"), )),
            "Switch.012": ("GeometryNodeSwitch", (-162.89, -123.35), None, (("False", "Switch.011", "Output"), ("Switch", "Group Input", "Is Arc"), )),
        }