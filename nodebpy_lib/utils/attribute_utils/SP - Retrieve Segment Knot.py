from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPRetrieveSegmentKnot(CustomGeometryGroup):
    _name = "SP - Retrieve Segment Knot"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 230, "node_tool_idname": "geometry.sp_retrieve_segment_knot", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        segment = tree.inputs.geometry("Segment")
        knot_name = tree.inputs.string("Knot Name", "Knot", optional_label=True)
        multiplicity_name = tree.inputs.string("Multiplicity Name", "Multiplicity", optional_label=True)
        custom_knot_unique = tree.outputs.float("Custom Knot Unique")
        custom_knot_exists = tree.outputs.boolean("Custom knot exists")
        custom_multiplicity = tree.outputs.integer("Custom Multiplicity")
        uses_existing_mult = tree.outputs.boolean("Uses Existing Mult")

        with g.Frame():
            integer_math = g.DomainSize(segment).o.point_count - 1
            compare = g.Index() >= integer_math
            integer_math_1 = (g.Index().props(hide=True).o.index - integer_math).props(hide=True)
        named_attribute = g.NamedAttribute.float(knot_name)
        compare_1 = g.Compare.float.equal(named_attribute.o.attribute, 340_282_350_000_000_000_000_000_000_000_000_000_000.0, 0.0).props(width=100.0, hide=True)
        boolean_math = ((~compare_1.o.result).props(width=100.0, hide=True) & named_attribute.o.exists).props(width=100.0, hide=True)
        reroute = g.Reroute(input=segment).props(width=19.0)
        reroute_1 = g.Reroute(input=reroute.o.output).props(width=19.0)
        sample_index = g.SampleIndex.point.boolean(reroute_1, boolean_math).props(hide=True)
        with g.Frame("Get existing mult"):
            named_attribute_1 = g.NamedAttribute.integer(multiplicity_name).props(width=108.65)
            reroute_2 = g.Reroute(input=reroute.o.output).props(width=19.0)
            sample_index_1 = g.SampleIndex.point.integer(reroute_2, named_attribute_1.o.attribute, g.Index().props(hide=True)).props(hide=True)
            (
                (sample_index.o.value & g.SampleIndex.point.boolean(reroute_2, named_attribute_1.o.exists).props(hide=True)).props(width=100.0, hide=True)
                >> uses_existing_mult
            )
            named_attribute_2 = g.NamedAttribute.integer(g.JoinStrings((multiplicity_name, g.String("_extension"))).props(hide=True)).props(width=108.65)
            sample_index_2 = g.SampleIndex.point.integer(reroute_2, named_attribute_2.o.attribute, integer_math_1).props(hide=True)
            compare.switch.integer(sample_index_1, sample_index_2) >> custom_multiplicity
        sample_index_3 = g.SampleIndex.point.float(reroute_1, named_attribute.o.attribute, g.Index().props(hide=True)).props(hide=True)
        named_attribute_3 = g.NamedAttribute.float(g.JoinStrings((knot_name, g.String("_extension"))).props(hide=True))
        sample_index_4 = g.SampleIndex.point.float(reroute_1, named_attribute_3.o.attribute, integer_math_1).props(hide=True)
        reroute_3 = g.Reroute(input=compare.switch.float(sample_index_3, sample_index_4)).props(width=19.0)
        compare_2 = g.Compare.float.equal(reroute_3, 340_282_350_000_000_000_000_000_000_000_000_000_000.0, 0.0).props(width=100.0, hide=True)
        (
            compare_2.o.result.switch.float(reroute_3, 1.0).props(hide=True)
            >> custom_knot_unique
        )

        sample_index >> custom_knot_exists

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math.001": ("FunctionNodeBooleanMath", (1108.57, -40.16), "Frame.007", (("Boolean", "Sample Index.017", "Value"), ("Boolean#1", "Sample Index.020", "Value"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (-4.76, 69.71), None, (("Boolean", "Compare.001", "Result"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (-4.18, 33.56), None, (("Boolean", "Boolean Math.002", "Boolean"), ("Boolean#1", "Named Attribute.005", "Exists"), )),
            "Compare": ("FunctionNodeCompare", (554.65, 439.59), None, (("A", "Reroute.071", "Output"), )),
            "Compare.001": ("FunctionNodeCompare", (-15.23, 108.89), None, (("A", "Named Attribute.005", "Attribute"), )),
            "Compare.002": ("FunctionNodeCompare", (432.15, -30.16), "Frame", (("A", "Index", "Index"), ("B", "Integer Math", "Value"), )),
            "Domain Size": ("GeometryNodeAttributeDomainSize", (30.1, -112.46), "Frame", (("Geometry", "Group Input", "Segment"), )),
            "Frame": ("NodeFrame", (-778.76, 957.71), None, ()),
            "Frame.007": ("NodeFrame", (-705.18, -93.35), None, ()),
            "Group Input": ("NodeGroupInput", (-1010.95, 1.66), None, ()),
            "Group Output": ("NodeGroupOutput", (912.39, -53.24), None, (("Custom Knot Unique", "Switch.010", "Output"), ("Custom Multiplicity", "Switch.017", "Output"), ("Custom knot exists", "Sample Index.017", "Value"), ("Uses Existing Mult", "Boolean Math.001", "Boolean"), )),
            "Index": ("GeometryNodeInputIndex", (182.72, -68.0), "Frame", ()),
            "Index.005": ("GeometryNodeInputIndex", (-141.5, 514.13), None, ()),
            "Index.006": ("GeometryNodeInputIndex", (663.19, -129.29), "Frame.007", ()),
            "Index.007": ("GeometryNodeInputIndex", (212.55, -272.68), "Frame", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (183.61, -128.37), "Frame", (("Value", "Domain Size", "Point Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (422.23, -206.06), "Frame", (("Value", "Index.007", "Index"), ("Value#1", "Integer Math", "Value"), )),
            "Join Strings": ("GeometryNodeStringJoin", (-731.78, 318.49), None, (("Strings", "Group Input", "Knot Name"), ("Strings", "String", "String"), )),
            "Join Strings.001": ("GeometryNodeStringJoin", (29.95, -239.52), "Frame.007", (("Strings", "Group Input", "Multiplicity Name"), ("Strings", "String.001", "String"), )),
            "Named Attribute.005": ("GeometryNodeInputNamedAttribute", (-484.17, 567.7), None, (("Name", "Group Input", "Knot Name"), )),
            "Named Attribute.006": ("GeometryNodeInputNamedAttribute", (-494.55, 413.69), None, (("Name", "Join Strings", "String"), )),
            "Named Attribute.008": ("GeometryNodeInputNamedAttribute", (373.22, -46.38), "Frame.007", (("Name", "Group Input", "Multiplicity Name"), )),
            "Named Attribute.009": ("GeometryNodeInputNamedAttribute", (371.56, -179.48), "Frame.007", (("Name", "Join Strings.001", "String"), )),
            "Reroute.003": ("NodeReroute", (820.58, -93.48), "Frame.007", (("Input", "Reroute.048", "Output"), )),
            "Reroute.032": ("NodeReroute", (-40.99, 413.34), None, (("Input", "Reroute.048", "Output"), )),
            "Reroute.048": ("NodeReroute", (-331.1, -40.71), None, (("Input", "Group Input", "Segment"), )),
            "Reroute.071": ("NodeReroute", (527.32, 435.48), None, (("Input", "Switch.016", "Output"), )),
            "Sample Index.017": ("GeometryNodeSampleIndex", (166.46, 43.05), None, (("Geometry", "Reroute.032", "Output"), ("Value", "Boolean Math.004", "Boolean"), )),
            "Sample Index.018": ("GeometryNodeSampleIndex", (51.17, 526.13), None, (("Geometry", "Reroute.032", "Output"), ("Index", "Index.005", "Index"), ("Value", "Named Attribute.005", "Attribute"), )),
            "Sample Index.019": ("GeometryNodeSampleIndex", (856.41, -110.76), "Frame.007", (("Geometry", "Reroute.003", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.008", "Attribute"), )),
            "Sample Index.020": ("GeometryNodeSampleIndex", (866.29, -61.47), "Frame.007", (("Geometry", "Reroute.003", "Output"), ("Value", "Named Attribute.008", "Exists"), )),
            "Sample Index.021": ("GeometryNodeSampleIndex", (55.77, 389.84), None, (("Geometry", "Reroute.032", "Output"), ("Index", "Integer Math.001", "Value"), ("Value", "Named Attribute.006", "Attribute"), )),
            "Sample Index.022": ("GeometryNodeSampleIndex", (856.41, -193.41), "Frame.007", (("Geometry", "Reroute.003", "Output"), ("Index", "Integer Math.001", "Value"), ("Value", "Named Attribute.009", "Attribute"), )),
            "String": ("FunctionNodeInputString", (-738.06, 278.25), None, ()),
            "String.001": ("FunctionNodeInputString", (44.46, -279.76), "Frame.007", ()),
            "Switch.010": ("GeometryNodeSwitch", (551.17, 385.61), None, (("False", "Reroute.071", "Output"), ("Switch", "Compare", "Result"), )),
            "Switch.016": ("GeometryNodeSwitch", (325.45, 539.73), None, (("False", "Sample Index.018", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Sample Index.021", "Value"), )),
            "Switch.017": ("GeometryNodeSwitch", (1095.75, -129.17), "Frame.007", (("False", "Sample Index.019", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Sample Index.022", "Value"), )),
        }