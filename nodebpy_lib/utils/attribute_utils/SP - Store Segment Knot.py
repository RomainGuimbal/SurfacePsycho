from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPStoreSegmentKnot(CustomGeometryGroup):
    _name = "SP - Store Segment Knot"
    _color_tag = "ATTRIBUTE"
    _tree_properties = {"default_group_node_width": 180, "node_tool_idname": "geometry.sp_store_segment_knot", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        segment_cp = tree.inputs.geometry("Segment CP", description="Geometry to store a new attribute with the given name on")
        knot_support = tree.inputs.geometry("Knot support", description="Geometry to sample a value on")
        unique_knot = tree.inputs.float("Unique Knot", 0.0)
        multiplicity = tree.inputs.integer("Multiplicity", 0)
        knot_name = tree.inputs.string("Knot Name", "Knot", optional_label=True)
        multiplicity_name = tree.inputs.string("Multiplicity Name", "Multiplicity", optional_label=True)
        segment_cp_1 = tree.outputs.geometry("Segment CP")

        domain_size = g.DomainSize(segment_cp).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        integer_math = domain_size.o.point_count - 1
        compare = g.Index() < integer_math
        integer_math_1 = (integer_math + g.Index()).props(hide=True)
        reroute = g.Reroute(input=multiplicity_name).props(width=19.0)
        reroute_1 = g.Reroute(input=knot_name).props(width=19.0)
        string = g.String("_extension")
        switch = compare.switch.float(true=g.SampleIndex.point.float(knot_support, unique_knot, integer_math_1))
        switch_1 = compare.switch.integer(true=g.SampleIndex.point.integer(knot_support, multiplicity, integer_math_1))
        (
            (((g.StoreNamedAttribute.point.float(segment_cp, name=reroute_1, value=compare.switch.float(true=unique_knot)).props(width=140.0) >> g.StoreNamedAttribute.point.float(name=g.JoinStrings((reroute_1, string)), value=switch)).props(width=140.0) >> g.StoreNamedAttribute.point.integer(name=reroute, value=compare.switch.integer(true=multiplicity))).props(width=140.0) >> g.StoreNamedAttribute.point.integer(name=g.JoinStrings((reroute, string)), value=switch_1)).props(width=140.0)
            >> segment_cp_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Compare": ("FunctionNodeCompare", (159.73, 295.95), None, (("A", "Index.001", "Index"), ("B", "Integer Math.001", "Value"), )),
            "Domain Size": ("GeometryNodeAttributeDomainSize", (-401.49, 169.47), None, (("Geometry", "Group Input", "Segment CP"), )),
            "Group Input": ("NodeGroupInput", (-597.84, -12.47), None, ()),
            "Group Output": ("NodeGroupOutput", (1566.55, 68.26), None, (("Segment CP", "Store Named Attribute.006", "Geometry"), )),
            "Index": ("GeometryNodeInputIndex", (143.43, -188.84), None, ()),
            "Index.001": ("GeometryNodeInputIndex", (-28.22, 266.4), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (150.24, -257.79), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Index", "Index"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-223.77, 178.38), None, (("Value", "Domain Size", "Point Count"), )),
            "Join Strings": ("GeometryNodeStringJoin", (332.32, -482.84), None, (("Strings", "Reroute.001", "Output"), ("Strings", "String", "String"), )),
            "Join Strings.001": ("GeometryNodeStringJoin", (332.32, -571.54), None, (("Strings", "Reroute", "Output"), ("Strings", "String", "String"), )),
            "Reroute": ("NodeReroute", (204.57, -511.78), None, (("Input", "Group Input", "Multiplicity Name"), )),
            "Reroute.001": ("NodeReroute", (213.49, -490.2), None, (("Input", "Group Input", "Knot Name"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (332.32, -27.44), None, (("Geometry", "Group Input", "Knot support"), ("Index", "Integer Math", "Value"), ("Value", "Group Input", "Unique Knot"), )),
            "Sample Index.001": ("GeometryNodeSampleIndex", (332.32, -258.1), None, (("Geometry", "Group Input", "Knot support"), ("Index", "Integer Math", "Value"), ("Value", "Group Input", "Multiplicity"), )),
            "Store Named Attribute.003": ("GeometryNodeStoreNamedAttribute", (1188.02, 211.93), None, (("Geometry", "Group Input", "Segment CP"), ("Name", "Reroute.001", "Output"), ("Value", "Switch.002", "Output"), )),
            "Store Named Attribute.004": ("GeometryNodeStoreNamedAttribute", (1176.32, -199.6), None, (("Geometry", "Store Named Attribute.005", "Geometry"), ("Name", "Reroute", "Output"), ("Value", "Switch.003", "Output"), )),
            "Store Named Attribute.005": ("GeometryNodeStoreNamedAttribute", (1181.84, 6.17), None, (("Geometry", "Store Named Attribute.003", "Geometry"), ("Name", "Join Strings", "String"), ("Value", "Switch.001", "Output"), )),
            "Store Named Attribute.006": ("GeometryNodeStoreNamedAttribute", (1171.45, -405.39), None, (("Geometry", "Store Named Attribute.004", "Geometry"), ("Name", "Join Strings.001", "String"), ("Value", "Switch.004", "Output"), )),
            "String": ("FunctionNodeInputString", (70.03, -565.51), None, ()),
            "Switch.001": ("GeometryNodeSwitch", (692.06, 312.57), None, (("Switch", "Compare", "Result"), ("True", "Sample Index", "Value"), )),
            "Switch.002": ("GeometryNodeSwitch", (692.06, 479.89), None, (("Switch", "Compare", "Result"), ("True", "Group Input", "Unique Knot"), )),
            "Switch.003": ("GeometryNodeSwitch", (692.06, 149.05), None, (("Switch", "Compare", "Result"), ("True", "Group Input", "Multiplicity"), )),
            "Switch.004": ("GeometryNodeSwitch", (692.06, -6.59), None, (("Switch", "Compare", "Result"), ("True", "Sample Index.001", "Value"), )),
        }