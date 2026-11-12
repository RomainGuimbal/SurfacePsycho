from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Rebuild Patch Control Geom", arrange=None, clear=True) as tree:
    object_transform = tree.inputs.matrix("Object Transform")
    meshed_patch = tree.inputs.geometry("Meshed Patch")
    control_grid = tree.outputs.geometry("Control Grid")
    geom_info = tree.outputs.bundle("Geom Info")
    position_deprecated = tree.outputs.vector("Position DEPRECATED")
    degree_u = tree.outputs.integer("Degree U")
    degree_v = tree.outputs.integer("Degree V")
    u_count = tree.outputs.integer("U Count")
    v_count = tree.outputs.integer("V Count")
    periodic_u = tree.outputs.boolean("Periodic U")
    periodic_v = tree.outputs.boolean("Periodic V")
    flipped_normal = tree.outputs.boolean("Flipped Normal")

    index_switch = g.IndexSwitch.string(g.Index(), ("Knot U", "Knot V", "Multiplicity U", "Multiplicity V"))
    index = g.Index()
    named_attribute = g.NamedAttribute.vector("CP_NURBS_surf").props(width=255.38)
    named_attribute_1 = g.NamedAttribute.integer("CP_count").props(width=214.05)
    named_attribute_2 = g.NamedAttribute.float("Weight").props(width=100.0)
    named_attribute_3 = g.NamedAttribute.integer("Degrees").props(width=214.05)
    named_attribute_4 = g.NamedAttribute.boolean("IsPeriodic").props(width=214.05)
    named_attribute_5 = g.NamedAttribute.integer("Multiplicity U")
    named_attribute_6 = g.NamedAttribute.integer("Multiplicity V")
    reroute = g.Reroute(input=meshed_patch).props(width=19.0)
    with g.Frame("Is NURBS"):
        named_attribute_7 = g.NamedAttribute.integer("Degrees")
        reroute_1 = g.Reroute(input=reroute.o.output).props(width=19.0)
        compare = g.SampleIndex.point.integer(reroute_1, named_attribute_7.o.attribute).props(hide=True) > 0
        boolean_math = compare & g.SampleIndex.point.boolean(reroute_1, named_attribute_7.o.exists).props(hide=True)
    reroute_2 = g.Reroute(input=reroute.o.output).props(width=19.0)
    with g.Frame("Get geom bundle"):
        get_bundle_item = g.GetBundleItem.bundle(reroute_2.o.output.bundle(), "grid_info").props(width=183.68)
        get_bundle_item_1 = g.GetBundleItem.geometry(get_bundle_item.o.item, "Grid")
        transform_geometry = g.TransformGeometry(geometry=get_bundle_item_1.o.item, transform=object_transform, mode="Matrix")
        store_bundle_item = g.StoreBundleItem.geometry(get_bundle_item_1.o.bundle, "Grid", transform_geometry)
    reroute_3 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
    with g.Frame():
        reroute_4 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
        compare_1 = (g.SampleIndex.point.integer(reroute_4, named_attribute_5.o.attribute) > 1).props(hide=True)
        compare_2 = (g.SampleIndex.point.integer(reroute_4, named_attribute_5.o.attribute, 1) > 1).props(hide=True)
        boolean_math_1 = (compare_1 | compare_2).props(hide=True)
    with g.Frame():
        reroute_5 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
        compare_3 = (g.SampleIndex.point.integer(reroute_5, named_attribute_6.o.attribute) > 1).props(hide=True)
        compare_4 = (g.SampleIndex.point.integer(reroute_5, named_attribute_6.o.attribute, 1) > 1).props(hide=True)
        boolean_math_2 = (compare_3 | compare_4).props(hide=True)
    sample_index = g.SampleIndex.point.integer(reroute, named_attribute_1.o.attribute)
    sample_index_1 = g.SampleIndex.point.integer(reroute, named_attribute_1.o.attribute, 1)
    sample_index_2 = g.SampleIndex.point.float(reroute, named_attribute_2.o.attribute, index)
    sample_index_3 = g.SampleIndex.point.boolean(reroute, named_attribute_2.o.exists)
    _sample_index_4 = g.SampleIndex.point.float(reroute, g.NamedAttribute.float("Knot U").props(width=214.05).o.attribute, index)
    _sample_index_5 = g.SampleIndex.point.float(reroute, g.NamedAttribute.float("Knot V").props(width=214.05).o.attribute, index)
    _sample_index_6 = g.SampleIndex.point.integer(reroute, g.NamedAttribute.integer("Multiplicity U").props(width=214.05).o.attribute, index)
    _sample_index_7 = g.SampleIndex.point.integer(reroute, g.NamedAttribute.integer("Multiplicity V").props(width=214.05).o.attribute, index)
    sample_index_8 = g.SampleIndex.point.boolean(reroute, g.NamedAttribute.boolean("IsFlipped").props(width=214.05).o.attribute)
    switch = named_attribute.o.exists.switch.vector(g.NamedAttribute.vector("CP_any_order_surf").props(width=255.38).o.attribute, named_attribute.o.attribute)
    sample_index_9 = g.SampleIndex.point.vector(reroute, switch.transform(g.ObjectInfo(g.SelfObject().props(width=129.53)).o.transform.invert()), index)
    with g.Frame():
        grid = g.Grid(vertices_x=g.Reroute(input=sample_index_1.o.value).props(width=19.0), vertices_y=g.Reroute(input=sample_index.o.value).props(width=19.0))
        set_position = g.SetPosition(geometry=grid, position=g.Reroute(input=sample_index_9.o.value).props(width=19.0))
        store_named_attribute = g.StoreNamedAttribute.point.float(set_position, name="Weight", value=sample_index_2).props(width=140.0)
        switch_1 = (sample_index_3.o.value & boolean_math).props(hide=True).switch.geometry(set_position, store_named_attribute)
    transfer_attributes = (switch_1 >> g.TransferAttributes(source=reroute_2, attribute_names=g.FieldToList(count=4, items={"Names": index_switch}), pattern_mode="Exact")).props(warning_propagation="NONE")
    combine_bundle = g.CombineBundle(define_signature=True)
    combine_bundle.items.geometry(transfer_attributes.o.target, "Grid", structure_type="SINGLE")
    combine_bundle.items.integer(g.SampleIndex.point.integer(reroute, named_attribute_3.o.attribute), "Degree U", structure_type="SINGLE")
    combine_bundle.items.integer(g.SampleIndex.point.integer(reroute, named_attribute_3.o.attribute, 1), "Degree V", structure_type="SINGLE")
    combine_bundle.items.integer(sample_index, "U Count", structure_type="SINGLE")
    combine_bundle.items.integer(sample_index_1, "V Count", structure_type="SINGLE")
    combine_bundle.items.boolean(boolean_math_1, "Clamped U", structure_type="SINGLE")
    combine_bundle.items.boolean(boolean_math_2, "Clamped V", structure_type="SINGLE")
    combine_bundle.items.boolean(g.SampleIndex.point.boolean(reroute, named_attribute_4.o.attribute), "Cyclic U", structure_type="SINGLE")
    combine_bundle.items.boolean(g.SampleIndex.point.boolean(reroute, named_attribute_4.o.attribute, 1), "Cyclic V", structure_type="SINGLE")
    switch_2 = get_bundle_item.o.exists.switch.bundle(combine_bundle.o.bundle, store_bundle_item)
    separate_bundle = g.SeparateBundle(switch_2)
    grid_1 = separate_bundle.items.geometry("Grid", structure_type="SINGLE")
    degree_u_1 = separate_bundle.items.integer("Degree U", structure_type="SINGLE")
    degree_v_1 = separate_bundle.items.integer("Degree V", structure_type="SINGLE")
    u_count_1 = separate_bundle.items.integer("U Count", structure_type="SINGLE")
    v_count_1 = separate_bundle.items.integer("V Count", structure_type="SINGLE")
    separate_bundle.items.boolean("Clamped U", structure_type="SINGLE")
    separate_bundle.items.boolean("Clamped V", structure_type="SINGLE")
    cyclic_u = separate_bundle.items.boolean("Cyclic U", structure_type="SINGLE")
    cyclic_v = separate_bundle.items.boolean("Cyclic V", structure_type="SINGLE")
    reroute_6 = g.Reroute(input=grid_1.output).props(width=19.0)
    sample_index_10 = g.SampleIndex.point.vector(reroute_6, g.Position(), g.Index())

    reroute_6 >> control_grid
    switch_2 >> geom_info
    sample_index_10 >> position_deprecated
    degree_u_1.output >> degree_u
    degree_v_1.output >> degree_v
    u_count_1.output >> u_count
    v_count_1.output >> v_count
    cyclic_u.output >> periodic_u
    cyclic_v.output >> periodic_v
    sample_index_8 >> flipped_normal

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (555.24, -107.39), "Frame", (("Boolean", "Sample Index.006", "Value"), ("Boolean#1", "Boolean Math.001", "Boolean"), )),
    "Boolean Math.001": ("FunctionNodeBooleanMath", (597.35, -119.08), "Frame.003", (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Sample Index.012", "Value"), )),
    "Boolean Math.002": ("FunctionNodeBooleanMath", (462.0, -170.34), "Frame.016", (("Boolean", "Compare", "Result"), ("Boolean#1", "Compare.003", "Result"), )),
    "Boolean Math.003": ("FunctionNodeBooleanMath", (471.97, -159.2), "Frame.017", (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.005", "Result"), )),
    "Combine Bundle.004": ("NodeCombineBundle", (2844.2, -539.86), None, (("Clamped U", "Boolean Math.002", "Boolean"), ("Clamped V", "Boolean Math.003", "Boolean"), ("Cyclic U", "Sample Index.013", "Value"), ("Cyclic V", "Sample Index.014", "Value"), ("Degree U", "Sample Index.001", "Value"), ("Degree V", "Sample Index.003", "Value"), ("Grid", "Transfer Attributes", "Target"), ("U Count", "Sample Index", "Value"), ("V Count", "Sample Index.002", "Value"), )),
    "Compare": ("FunctionNodeCompare", (296.82, -148.32), "Frame.016", (("A", "Sample Index.016", "Value"), )),
    "Compare.001": ("FunctionNodeCompare", (441.57, -36.2), "Frame.003", (("A", "Sample Index.011", "Value"), )),
    "Compare.003": ("FunctionNodeCompare", (293.44, -196.07), "Frame.016", (("A", "Sample Index.017", "Value"), )),
    "Compare.004": ("FunctionNodeCompare", (294.4, -140.17), "Frame.017", (("A", "Sample Index.018", "Value"), )),
    "Compare.005": ("FunctionNodeCompare", (292.64, -194.03), "Frame.017", (("A", "Sample Index.019", "Value"), )),
    "Field to List": ("GeometryNodeFieldToList", (2219.56, -154.08), None, (("Names", "Index Switch", "Output"), )),
    "Frame": ("NodeFrame", (567.36, 2.65), None, ()),
    "Frame.001": ("NodeFrame", (2496.71, 399.74), None, ()),
    "Frame.003": ("NodeFrame", (163.06, -410.79), None, ()),
    "Frame.016": ("NodeFrame", (2007.86, -631.59), None, ()),
    "Frame.017": ("NodeFrame", (2007.86, -1117.06), None, ()),
    "Get Bundle Item": ("NodeGetBundleItem", (261.05, -62.32), "Frame.001", (("Bundle", "Get Geometry Bundle", "Bundle"), )),
    "Get Bundle Item.001": ("NodeGetBundleItem", (517.93, -82.21), "Frame.001", (("Bundle", "Get Bundle Item", "Item"), )),
    "Get Geometry Bundle": ("GeometryNodeGetGeometryBundle", (30.24, -35.82), "Frame.001", (("Geometry", "Reroute.007", "Output"), )),
    "Grid": ("GeometryNodeMeshGrid", (80.03, -30.26), "Frame", (("Vertices X", "Reroute.012", "Output"), ("Vertices Y", "Reroute.008", "Output"), )),
    "Group Input": ("NodeGroupInput", (-540.58, 149.21), None, ()),
    "Group Output": ("NodeGroupOutput", (4594.74, -175.31), None, (("Control Grid", "Reroute.005", "Output"), ("Degree U", "Separate Bundle", "Degree U"), ("Degree V", "Separate Bundle", "Degree V"), ("Flipped Normal", "Sample Index.015", "Value"), ("Geom Info", "Switch.002", "Output"), ("Periodic U", "Separate Bundle", "Cyclic U"), ("Periodic V", "Separate Bundle", "Cyclic V"), ("Position DEPRECATED", "Sample Index.020", "Value"), ("U Count", "Separate Bundle", "U Count"), ("V Count", "Separate Bundle", "V Count"), )),
    "Index": ("GeometryNodeInputIndex", (1848.52, -224.91), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (2046.03, -164.41), None, (("Index", "Index", "Index"), )),
    "Index.001": ("GeometryNodeInputIndex", (4084.73, -606.92), None, ()),
    "Index.006": ("GeometryNodeInputIndex", (-642.89, -799.34), None, ()),
    "Invert Matrix": ("FunctionNodeInvertMatrix", (-1084.17, -349.58), None, (("Matrix", "Object Info.002", "Transform"), )),
    "Named Attribute": ("GeometryNodeInputNamedAttribute", (-1397.15, -200.39), None, ()),
    "Named Attribute.001": ("GeometryNodeInputNamedAttribute", (-1395.37, -64.46), None, ()),
    "Named Attribute.002": ("GeometryNodeInputNamedAttribute", (30.2, -80.77), "Frame.003", ()),
    "Named Attribute.003": ("GeometryNodeInputNamedAttribute", (-563.74, -60.56), None, ()),
    "Named Attribute.004": ("GeometryNodeInputNamedAttribute", (-1065.33, -809.93), None, ()),
    "Named Attribute.005": ("GeometryNodeInputNamedAttribute", (-500.26, 516.52), None, ()),
    "Named Attribute.006": ("GeometryNodeInputNamedAttribute", (-1177.31, -941.2), None, ()),
    "Named Attribute.007": ("GeometryNodeInputNamedAttribute", (-1174.15, -1076.52), None, ()),
    "Named Attribute.008": ("GeometryNodeInputNamedAttribute", (-1167.56, -1208.19), None, ()),
    "Named Attribute.009": ("GeometryNodeInputNamedAttribute", (-1164.4, -1343.51), None, ()),
    "Named Attribute.010": ("GeometryNodeInputNamedAttribute", (-1154.32, -1490.99), None, ()),
    "Named Attribute.011": ("GeometryNodeInputNamedAttribute", (-1151.89, -1637.04), None, ()),
    "Named Attribute.012": ("GeometryNodeInputNamedAttribute", (1826.59, -749.79), None, ()),
    "Named Attribute.013": ("GeometryNodeInputNamedAttribute", (1805.88, -1206.95), None, ()),
    "Object Info.002": ("GeometryNodeObjectInfo", (-1256.26, -341.69), None, (("Object", "Self Object.001", "Self Object"), )),
    "Position": ("GeometryNodeInputPosition", (4085.86, -548.37), None, ()),
    "Reroute": ("NodeReroute", (122.2, -248.81), "Frame", (("Input", "Sample Index.004", "Value"), )),
    "Reroute.001": ("NodeReroute", (229.66, -101.14), "Frame.003", (("Input", "Reroute.043", "Output"), )),
    "Reroute.002": ("NodeReroute", (35.21, -230.43), "Frame.016", (("Input", "Reroute.003", "Output"), )),
    "Reroute.003": ("NodeReroute", (1947.48, -1071.14), None, (("Input", "Reroute.007", "Output"), )),
    "Reroute.004": ("NodeReroute", (35.21, -196.26), "Frame.017", (("Input", "Reroute.003", "Output"), )),
    "Reroute.005": ("NodeReroute", (4258.69, -235.67), None, (("Input", "Separate Bundle", "Grid"), )),
    "Reroute.007": ("NodeReroute", (1589.55, 79.71), None, (("Input", "Reroute.043", "Output"), )),
    "Reroute.008": ("NodeReroute", (35.21, -139.75), "Frame", (("Input", "Sample Index", "Value"), )),
    "Reroute.012": ("NodeReroute", (35.31, -164.52), "Frame", (("Input", "Sample Index.002", "Value"), )),
    "Reroute.043": ("NodeReroute", (-237.72, 96.98), None, (("Input", "Group Input", "Meshed Patch"), )),
    "Sample Index": ("GeometryNodeSampleIndex", (-145.98, 279.64), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.003", "Attribute"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (-139.49, 693.12), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.005", "Attribute"), )),
    "Sample Index.002": ("GeometryNodeSampleIndex", (-152.7, 73.94), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.003", "Attribute"), )),
    "Sample Index.003": ("GeometryNodeSampleIndex", (-146.21, 487.43), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.005", "Attribute"), )),
    "Sample Index.004": ("GeometryNodeSampleIndex", (-150.77, -139.17), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Transform Point", "Vector"), )),
    "Sample Index.005": ("GeometryNodeSampleIndex", (-151.65, -342.91), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.004", "Attribute"), )),
    "Sample Index.006": ("GeometryNodeSampleIndex", (-158.39, -545.42), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.004", "Exists"), )),
    "Sample Index.007": ("GeometryNodeSampleIndex", (-155.21, -747.85), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.006", "Attribute"), )),
    "Sample Index.008": ("GeometryNodeSampleIndex", (-156.28, -950.36), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.007", "Attribute"), )),
    "Sample Index.009": ("GeometryNodeSampleIndex", (-158.06, -1152.46), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.008", "Attribute"), )),
    "Sample Index.010": ("GeometryNodeSampleIndex", (-159.12, -1354.97), None, (("Geometry", "Reroute.043", "Output"), ("Index", "Index.006", "Index"), ("Value", "Named Attribute.009", "Attribute"), )),
    "Sample Index.011": ("GeometryNodeSampleIndex", (266.3, -137.08), "Frame.003", (("Geometry", "Reroute.001", "Output"), ("Value", "Named Attribute.002", "Attribute"), )),
    "Sample Index.012": ("GeometryNodeSampleIndex", (265.22, -174.2), "Frame.003", (("Geometry", "Reroute.001", "Output"), ("Value", "Named Attribute.002", "Exists"), )),
    "Sample Index.013": ("GeometryNodeSampleIndex", (-164.73, -1566.32), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.010", "Attribute"), )),
    "Sample Index.014": ("GeometryNodeSampleIndex", (-167.69, -1771.35), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.010", "Attribute"), )),
    "Sample Index.015": ("GeometryNodeSampleIndex", (-172.72, -1971.87), None, (("Geometry", "Reroute.043", "Output"), ("Value", "Named Attribute.011", "Attribute"), )),
    "Sample Index.016": ("GeometryNodeSampleIndex", (94.09, -30.4), "Frame.016", (("Geometry", "Reroute.002", "Output"), ("Value", "Named Attribute.012", "Attribute"), )),
    "Sample Index.017": ("GeometryNodeSampleIndex", (91.98, -234.86), "Frame.016", (("Geometry", "Reroute.002", "Output"), ("Value", "Named Attribute.012", "Attribute"), )),
    "Sample Index.018": ("GeometryNodeSampleIndex", (94.71, -30.39), "Frame.017", (("Geometry", "Reroute.004", "Output"), ("Value", "Named Attribute.013", "Attribute"), )),
    "Sample Index.019": ("GeometryNodeSampleIndex", (92.6, -234.85), "Frame.017", (("Geometry", "Reroute.004", "Output"), ("Value", "Named Attribute.013", "Attribute"), )),
    "Sample Index.020": ("GeometryNodeSampleIndex", (4326.04, -408.75), None, (("Geometry", "Reroute.005", "Output"), ("Index", "Index.001", "Index"), ("Value", "Position", "Position"), )),
    "Self Object.001": ("GeometryNodeSelfObject", (-1411.02, -474.82), None, ()),
    "Separate Bundle": ("NodeSeparateBundle", (3881.54, -192.02), None, (("Bundle", "Switch.002", "Output"), )),
    "Set Position": ("GeometryNodeSetPosition", (275.79, -76.13), "Frame", (("Geometry", "Grid", "Mesh"), ("Position", "Reroute", "Output"), )),
    "Store Bundle Item": ("NodeStoreBundleItem", (891.99, -87.49), "Frame.001", (("Bundle", "Get Bundle Item.001", "Bundle"), ("Item", "Transform Geometry", "Geometry"), )),
    "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (551.9, -177.26), "Frame", (("Geometry", "Set Position", "Geometry"), ("Value", "Sample Index.005", "Value"), )),
    "Switch": ("GeometryNodeSwitch", (810.17, -73.77), "Frame", (("False", "Set Position", "Geometry"), ("Switch", "Boolean Math", "Boolean"), ("True", "Store Named Attribute", "Geometry"), )),
    "Switch.001": ("GeometryNodeSwitch", (-1086.48, -65.38), None, (("False", "Named Attribute", "Attribute"), ("Switch", "Named Attribute.001", "Exists"), ("True", "Named Attribute.001", "Attribute"), )),
    "Switch.002": ("GeometryNodeSwitch", (3623.25, -403.35), None, (("False", "Combine Bundle.004", "Bundle"), ("Switch", "Get Bundle Item", "Exists"), ("True", "Store Bundle Item", "Bundle"), )),
    "Transfer Attributes": ("GeometryNodeTransferAttributes", (2448.81, 20.01), None, (("Attribute Names", "Field to List", "Names"), ("Source", "Reroute.007", "Output"), ("Target", "Switch", "Output"), )),
    "Transform Geometry": ("GeometryNodeTransform", (695.5, -179.77), "Frame.001", (("Geometry", "Get Bundle Item.001", "Item"), ("Transform", "Group Input", "Object Transform"), )),
    "Transform Point": ("FunctionNodeTransformPoint", (-887.72, -297.9), None, (("Transform", "Invert Matrix", "Matrix"), ("Vector", "Switch.001", "Output"), )),
}