from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Rebuild Wire Knot", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    segment_count = tree.inputs.integer("Segment count", 0)
    segment_offset = tree.inputs.integer("Segment Offset", 0, description="Index offset for multi wires", structure_type="SINGLE", force_non_field=True)
    knot_segment = tree.inputs.integer("Knot Segment", 0, hide_value=True, structure_type="LIST")
    knot = tree.inputs.float("Knot", 0.0, hide_value=True)
    multiplicity = tree.inputs.integer("Multiplicity", 0, hide_value=True)
    count_per_segment = tree.inputs.integer("Count per Segment", 0)
    p_count_accumulate = tree.inputs.integer("P Count Accumulate", 14)
    output = tree.outputs.geometry("Output")

    capture = g.CaptureAttribute.point(geometry=geometry)
    count_per_segment_1 = capture.items.integer(count_per_segment, "Count per Segment")
    p_count_accumulate_1 = capture.items.integer(p_count_accumulate, "P Count Accumulate")
    index = g.Index().props(hide=True)
    repeat_zone = g.RepeatZone(segment_count)
    repeat_zone.output.node.inspection_index = 1
    output_1 = repeat_zone.items.geometry(capture.o.geometry, "Output")
    compare = g.Compare.integer.equal((repeat_zone.iteration + segment_offset).props(hide=True), knot_segment).props(hide=True)
    filter_list = multiplicity.filter(compare).props(hide=True)
    filter_list_1 = knot.filter(compare).props(hide=True)
    reroute = g.Reroute(input=output_1.current).props(width=19.0)
    compare_1 = g.Compare.integer.equal(g.Reroute(input=filter_list_1).props(width=19.0).o.output.list_length().props(hide=True), 0).props(hide=True)
    reroute_1 = g.Reroute(input=capture.o.geometry).props(width=19.0)
    reroute_2 = g.Reroute(input=repeat_zone.iteration).props(width=19.0)
    sample_index = g.SampleIndex.point.integer(reroute_1, count_per_segment_1.output, reroute_2).props(hide=True)
    integer_math = (sample_index.o.value - 1).props(hide=True)
    with g.Frame():
        index_1 = g.Index().props(hide=True)
        get_list_item = filter_list_1[index_1].props(hide=True)
        get_list_item_1 = filter_list[index_1].props(hide=True)
        integer_math_1 = (index_1.o.index + integer_math).props(hide=True)
        get_list_item_2 = filter_list_1[integer_math_1].props(hide=True)
        get_list_item_3 = filter_list[integer_math_1].props(hide=True)
    sample_index_1 = g.SampleIndex.point.integer(reroute_1, p_count_accumulate_1.output, (reroute_2.o.output - 1).props(hide=True)).props(hide=True)
    integer_math_2 = g.Index().props(hide=True).o.index - sample_index_1
    reroute_3 = g.Reroute(input=(index >= sample_index_1) & (index < (integer_math + sample_index_1).props(hide=True))).props(width=19.0)
    string = g.String("_extension")
    string_1 = g.String("Knot").props(label="Knot Name")
    string_2 = g.String("Multiplicity").props(label="Multiplicity Name")
    store_named_attribute = (((g.StoreNamedAttribute.point.float(reroute, reroute_3, string_1, get_list_item.point.at(integer_math_2).props(hide=True)).props(width=140.0, hide=True) >> g.StoreNamedAttribute.point.float(selection=reroute_3, name=g.JoinStrings((string_1, string)), value=get_list_item_2.point.at(integer_math_2).props(hide=True))).props(width=140.0, hide=True) >> g.StoreNamedAttribute.point.integer(selection=reroute_3, name=string_2, value=get_list_item_1.point.at(integer_math_2).props(hide=True))).props(width=140.0, hide=True) >> g.StoreNamedAttribute.point.integer(selection=reroute_3, name=g.JoinStrings((string_2, string)), value=get_list_item_3.point.at(integer_math_2).props(hide=True))).props(width=140.0, hide=True)
    compare_1.o.result.switch.geometry(store_named_attribute, reroute) >> output_1.next

    output_1.result >> output

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (975.69, 228.51), None, (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
    "Capture Attribute.001": ("GeometryNodeCaptureAttribute", (-682.8, -57.77), None, (("Count per Segment", "Group Input", "Count per Segment"), ("Geometry", "Group Input", "Geometry"), ("P Count Accumulate", "Group Input", "P Count Accumulate"), )),
    "Compare": ("FunctionNodeCompare", (-40.16, -480.12), None, (("A", "Integer Math.005", "Value"), ("B", "Group Input", "Knot Segment"), )),
    "Compare.003": ("FunctionNodeCompare", (1625.05, -10.68), None, (("A", "List Length", "Length"), )),
    "Compare.004": ("FunctionNodeCompare", (669.45, 281.28), None, (("A", "Index.001", "Index"), ("B", "Sample Index.001", "Value"), )),
    "Compare.005": ("FunctionNodeCompare", (676.44, 108.8), None, (("A", "Index.001", "Index"), ("B", "Integer Math.004", "Value"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (1458.33, -337.85), None, (("Index", "Integer Math.002", "Value"), ("Value", "Get List Item.005", "Value"), )),
    "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (1458.33, -372.46), None, (("Index", "Integer Math.002", "Value"), ("Value", "Get List Item.003", "Value"), )),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (1458.33, -407.08), None, (("Index", "Integer Math.002", "Value"), ("Value", "Get List Item.006", "Value"), )),
    "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (1458.33, -441.69), None, (("Index", "Integer Math.002", "Value"), ("Value", "Get List Item.004", "Value"), )),
    "Filter List": ("GeometryNodeFilterList", (194.39, -604.83), None, (("List", "Group Input", "Multiplicity"), ("Selection", "Compare", "Result"), )),
    "Filter List.001": ("GeometryNodeFilterList", (193.7, -567.56), None, (("List", "Group Input", "Knot"), ("Selection", "Compare", "Result"), )),
    "Frame.002": ("NodeFrame", (688.24, -248.51), None, ()),
    "Get List Item.003": ("GeometryNodeListGetItem", (429.35, -115.08), "Frame.002", (("Index", "Integer Math", "Value"), ("List", "Filter List.001", "Selection"), )),
    "Get List Item.004": ("GeometryNodeListGetItem", (429.35, -192.62), "Frame.002", (("Index", "Integer Math", "Value"), ("List", "Filter List", "Selection"), )),
    "Get List Item.005": ("GeometryNodeListGetItem", (429.35, -76.32), "Frame.002", (("Index", "Index", "Index"), ("List", "Filter List.001", "Selection"), )),
    "Get List Item.006": ("GeometryNodeListGetItem", (429.35, -153.85), "Frame.002", (("Index", "Index", "Index"), ("List", "Filter List", "Selection"), )),
    "Group Input": ("NodeGroupInput", (-1319.71, -196.28), None, ()),
    "Group Output": ("NodeGroupOutput", (2748.31, -92.39), None, (("Output", "Repeat Output.002", "Output"), )),
    "Index": ("GeometryNodeInputIndex", (30.29, -109.71), "Frame.002", ()),
    "Index.001": ("GeometryNodeInputIndex", (188.52, 103.53), None, ()),
    "Index.002": ("GeometryNodeInputIndex", (972.69, -687.71), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (239.77, -34.14), "Frame.002", (("Value", "Index", "Index"), ("Value#1", "Integer Math.001", "Value"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (404.13, -205.46), None, (("Value", "Sample Index", "Value"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (1164.5, -645.25), None, (("Value", "Index.002", "Index"), ("Value#1", "Sample Index.001", "Value"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (2.59, -243.0), None, (("Value", "Reroute.004", "Output"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (419.49, -157.04), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Sample Index.001", "Value"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (-191.22, -428.39), None, (("Value", "Repeat Input.002", "Iteration"), ("Value#1", "Group Input", "Segment Offset"), )),
    "Join Strings": ("GeometryNodeStringJoin", (1441.91, -948.42), None, (("Strings", "String", "String"), ("Strings", "String.001", "String"), )),
    "Join Strings.001": ("GeometryNodeStringJoin", (1441.91, -1037.12), None, (("Strings", "String", "String"), ("Strings", "String.002", "String"), )),
    "List Length": ("GeometryNodeListLength", (1625.68, 26.04), None, (("List", "Reroute.001", "Output"), )),
    "Repeat Input.002": ("GeometryNodeRepeatInput", (-425.85, 8.71), None, (("Iterations", "Group Input", "Segment count"), ("Output", "Capture Attribute.001", "Geometry"), )),
    "Repeat Output.002": ("GeometryNodeRepeatOutput", (2362.95, -94.43), None, (("Output", "Switch", "Output"), )),
    "Reroute": ("NodeReroute", (1763.29, -139.56), None, (("Input", "Repeat Input.002", "Output"), )),
    "Reroute.001": ("NodeReroute", (932.01, 21.6), None, (("Input", "Filter List.001", "Selection"), )),
    "Reroute.002": ("NodeReroute", (107.78, -194.52), None, (("Input", "Capture Attribute.001", "Geometry"), )),
    "Reroute.003": ("NodeReroute", (1663.47, -170.96), None, (("Input", "Boolean Math", "Boolean"), )),
    "Reroute.004": ("NodeReroute", (-45.84, -229.32), None, (("Input", "Repeat Input.002", "Iteration"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (175.15, -181.62), None, (("Geometry", "Reroute.002", "Output"), ("Index", "Reroute.004", "Output"), ("Value", "Capture Attribute.001", "Count per Segment"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (175.55, -224.77), None, (("Geometry", "Reroute.002", "Output"), ("Index", "Integer Math.003", "Value"), ("Value", "Capture Attribute.001", "P Count Accumulate"), )),
    "Store Named Attribute.003": ("GeometryNodeStoreNamedAttribute", (1839.43, -223.0), None, (("Geometry", "Reroute", "Output"), ("Name", "String.001", "String"), ("Selection", "Reroute.003", "Output"), ("Value", "Evaluate at Index", "Value"), )),
    "Store Named Attribute.004": ("GeometryNodeStoreNamedAttribute", (1839.43, -347.45), None, (("Geometry", "Store Named Attribute.005", "Geometry"), ("Name", "String.002", "String"), ("Selection", "Reroute.003", "Output"), ("Value", "Evaluate at Index.002", "Value"), )),
    "Store Named Attribute.005": ("GeometryNodeStoreNamedAttribute", (1839.43, -285.23), None, (("Geometry", "Store Named Attribute.003", "Geometry"), ("Name", "Join Strings", "String"), ("Selection", "Reroute.003", "Output"), ("Value", "Evaluate at Index.001", "Value"), )),
    "Store Named Attribute.006": ("GeometryNodeStoreNamedAttribute", (1839.43, -409.68), None, (("Geometry", "Store Named Attribute.004", "Geometry"), ("Name", "Join Strings.001", "String"), ("Selection", "Reroute.003", "Output"), ("Value", "Evaluate at Index.003", "Value"), )),
    "String": ("FunctionNodeInputString", (1179.62, -1031.09), None, ()),
    "String.001": ("FunctionNodeInputString", (1178.35, -901.53), None, ()),
    "String.002": ("FunctionNodeInputString", (1178.35, -965.7), None, ()),
    "Switch": ("GeometryNodeSwitch", (2112.54, -66.39), None, (("False", "Store Named Attribute.006", "Geometry"), ("Switch", "Compare.003", "Result"), ("True", "Reroute", "Output"), )),
}