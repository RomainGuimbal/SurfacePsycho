from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPInputFromNURBSAttributes(CustomGeometryGroup):
    _name = "SP - Input from NURBS Attributes"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_input_from_nurbs_attributes", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.geometry("Input")
        degree_u = tree.inputs.integer("Degree U", 0, structure_type="SINGLE", force_non_field=True)
        degree_v = tree.inputs.integer("Degree V", 0, structure_type="SINGLE", force_non_field=True)
        clamped_u = tree.inputs.boolean("Clamped U", False, structure_type="SINGLE", force_non_field=True)
        clamped_v = tree.inputs.boolean("Clamped V", False, structure_type="SINGLE", force_non_field=True)
        cyclic_u = tree.inputs.boolean("Cyclic U", False, structure_type="SINGLE", force_non_field=True)
        cyclic_v = tree.inputs.boolean("Cyclic V", False, structure_type="SINGLE", force_non_field=True)
        degree_u_1 = tree.outputs.integer("Degree U", 2, min_value=1, max_value=20)
        degree_v_1 = tree.outputs.integer("Degree V", 2, min_value=1, max_value=20)
        clamped_u_1 = tree.outputs.boolean("Clamped U")
        clamped_v_1 = tree.outputs.boolean("Clamped V")
        cyclic_u_1 = tree.outputs.boolean("Cyclic U")
        cyclic_v_1 = tree.outputs.boolean("Cyclic V")

        named_attribute = g.NamedAttribute.integer("Degrees")
        named_attribute_1 = g.NamedAttribute.boolean("IsClamped")
        named_attribute_2 = g.NamedAttribute.boolean("IsPeriodic")
        reroute = g.Reroute(input=input).props(width=19.0)
        reroute_1 = g.Reroute(input=input).props(width=19.0)
        reroute_2 = g.Reroute(input=input).props(width=19.0)
        sample_index = g.SampleIndex.point.boolean(reroute_1, named_attribute_1.o.exists)
        sample_index_1 = g.SampleIndex.point.integer(reroute, named_attribute.o.attribute)
        sample_index_2 = g.SampleIndex.point.integer(reroute, named_attribute.o.attribute, 1)
        boolean_math = (sample_index_1 > 0) & (sample_index_2 > 0) & g.SampleIndex.point.boolean(reroute, named_attribute.o.exists)
        sample_index_3 = g.SampleIndex.point.boolean(reroute_2, named_attribute_2.o.exists)
        (
            boolean_math.switch.integer(g.Reroute(input=degree_u).props(width=19.0), sample_index_1)
            >> degree_u_1
        )
        (
            boolean_math.switch.integer(g.Reroute(input=degree_v).props(width=19.0), sample_index_2)
            >> degree_v_1
        )
        (
            sample_index.o.value.switch.boolean(g.Reroute(input=clamped_u).props(width=19.0), g.SampleIndex.point.boolean(reroute_1, named_attribute_1.o.attribute))
            >> clamped_u_1
        )
        (
            sample_index.o.value.switch.boolean(g.Reroute(input=clamped_v).props(width=19.0), g.SampleIndex.point.boolean(reroute_1, named_attribute_1.o.attribute, 1))
            >> clamped_v_1
        )
        (
            sample_index_3.o.value.switch.boolean(g.Reroute(input=cyclic_u).props(width=19.0), g.SampleIndex.point.boolean(reroute_2, named_attribute_2.o.attribute))
            >> cyclic_u_1
        )
        (
            sample_index_3.o.value.switch.boolean(g.Reroute(input=cyclic_v).props(width=19.0), g.SampleIndex.point.boolean(reroute_2, named_attribute_2.o.attribute, 1))
            >> cyclic_v_1
        )
        viewer = g.Viewer()
        viewer.items.boolean(sample_index, "Value")

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math.006": ("FunctionNodeBooleanMath", (258.47, 173.94), None, (("Boolean", "Boolean Math.007", "Boolean"), ("Boolean#1", "Sample Index", "Value"), )),
            "Boolean Math.007": ("FunctionNodeBooleanMath", (85.95, 277.34), None, (("Boolean", "Compare.006", "Result"), ("Boolean#1", "Compare.007", "Result"), )),
            "Compare.006": ("FunctionNodeCompare", (-91.44, 404.87), None, (("A", "Sample Index.002", "Value"), )),
            "Compare.007": ("FunctionNodeCompare", (-95.34, 243.82), None, (("A", "Sample Index.003", "Value"), )),
            "Group Input": ("NodeGroupInput", (-765.49, -176.07), None, ()),
            "Group Output": ("NodeGroupOutput", (1259.68, -186.7), None, (("Clamped U", "Switch.005", "Output"), ("Clamped V", "Switch.006", "Output"), ("Cyclic U", "Switch.007", "Output"), ("Cyclic V", "Switch.008", "Output"), ("Degree U", "Switch.003", "Output"), ("Degree V", "Switch.004", "Output"), )),
            "Named Attribute.001": ("GeometryNodeInputNamedAttribute", (-604.82, 130.22), None, ()),
            "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (-296.69, -690.21), None, ()),
            "Named Attribute.003": ("GeometryNodeInputNamedAttribute", (-317.98, -1260.66), None, ()),
            "Reroute": ("NodeReroute", (248.9, -297.14), None, (("Input", "Group Input", "Clamped U"), )),
            "Reroute.001": ("NodeReroute", (248.9, -320.16), None, (("Input", "Group Input", "Clamped V"), )),
            "Reroute.002": ("NodeReroute", (248.9, -366.19), None, (("Input", "Group Input", "Cyclic V"), )),
            "Reroute.003": ("NodeReroute", (248.9, -343.18), None, (("Input", "Group Input", "Cyclic U"), )),
            "Reroute.063": ("NodeReroute", (248.9, -251.11), None, (("Input", "Group Input", "Degree U"), )),
            "Reroute.064": ("NodeReroute", (248.9, -274.13), None, (("Input", "Group Input", "Degree V"), )),
            "Reroute.087": ("NodeReroute", (-405.02, -31.55), None, (("Input", "Group Input", "Input"), )),
            "Reroute.088": ("NodeReroute", (-53.8, -782.83), None, (("Input", "Group Input", "Input"), )),
            "Reroute.089": ("NodeReroute", (-54.92, -1398.11), None, (("Input", "Group Input", "Input"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (85.74, 100.57), None, (("Geometry", "Reroute.087", "Output"), ("Value", "Named Attribute.001", "Exists"), )),
            "Sample Index.001": ("GeometryNodeSampleIndex", (12.07, -424.54), None, (("Geometry", "Reroute.088", "Output"), ("Value", "Named Attribute.002", "Exists"), )),
            "Sample Index.002": ("GeometryNodeSampleIndex", (-322.03, 287.0), None, (("Geometry", "Reroute.087", "Output"), ("Value", "Named Attribute.001", "Attribute"), )),
            "Sample Index.003": ("GeometryNodeSampleIndex", (-322.03, 77.82), None, (("Geometry", "Reroute.087", "Output"), ("Value", "Named Attribute.001", "Attribute"), )),
            "Sample Index.004": ("GeometryNodeSampleIndex", (20.85, -629.73), None, (("Geometry", "Reroute.088", "Output"), ("Value", "Named Attribute.002", "Attribute"), )),
            "Sample Index.005": ("GeometryNodeSampleIndex", (18.39, -833.16), None, (("Geometry", "Reroute.088", "Output"), ("Value", "Named Attribute.002", "Attribute"), )),
            "Sample Index.006": ("GeometryNodeSampleIndex", (10.71, -1241.73), None, (("Geometry", "Reroute.089", "Output"), ("Value", "Named Attribute.003", "Attribute"), )),
            "Sample Index.007": ("GeometryNodeSampleIndex", (8.25, -1445.17), None, (("Geometry", "Reroute.089", "Output"), ("Value", "Named Attribute.003", "Attribute"), )),
            "Sample Index.008": ("GeometryNodeSampleIndex", (10.95, -1039.82), None, (("Geometry", "Reroute.089", "Output"), ("Value", "Named Attribute.003", "Exists"), )),
            "Switch.003": ("GeometryNodeSwitch", (544.47, 144.58), None, (("False", "Reroute.063", "Output"), ("Switch", "Boolean Math.006", "Boolean"), ("True", "Sample Index.002", "Value"), )),
            "Switch.004": ("GeometryNodeSwitch", (552.82, -45.91), None, (("False", "Reroute.064", "Output"), ("Switch", "Boolean Math.006", "Boolean"), ("True", "Sample Index.003", "Value"), )),
            "Switch.005": ("GeometryNodeSwitch", (548.27, -546.44), None, (("False", "Reroute", "Output"), ("Switch", "Sample Index.001", "Value"), ("True", "Sample Index.004", "Value"), )),
            "Switch.006": ("GeometryNodeSwitch", (547.59, -698.78), None, (("False", "Reroute.001", "Output"), ("Switch", "Sample Index.001", "Value"), ("True", "Sample Index.005", "Value"), )),
            "Switch.007": ("GeometryNodeSwitch", (547.15, -1161.72), None, (("False", "Reroute.003", "Output"), ("Switch", "Sample Index.008", "Value"), ("True", "Sample Index.006", "Value"), )),
            "Switch.008": ("GeometryNodeSwitch", (546.47, -1314.07), None, (("False", "Reroute.002", "Output"), ("Switch", "Sample Index.008", "Value"), ("True", "Sample Index.007", "Value"), )),
            "Viewer": ("GeometryNodeViewer", (710.42, -465.49), None, (("Value", "Sample Index.001", "Value"), )),
        }