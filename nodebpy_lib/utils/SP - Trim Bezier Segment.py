from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Trim Bezier Segment", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    cp = tree.inputs.vector("CP", (0.0, 0.0, 0.0))
    factor = tree.inputs.float("Factor", 1.0, min_value=-10_000.0, max_value=10_000.0)
    rational = tree.inputs.boolean("Rational", False, structure_type="SINGLE", force_non_field=True)
    weight = tree.inputs.float("Weight", 0.0)
    support_geometry = tree.outputs.geometry("Support Geometry")
    position = tree.outputs.vector("Position", hide_value=True)
    weight_1 = tree.outputs.float("Weight")

    domain_size = g.DomainSize(geometry).props(hide=True, hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
    integer_math = (domain_size.o.point_count - 1).props(hide=True)
    with g.Frame("Non Rational"):
        repeat_zone = g.RepeatZone(integer_math)
        geometry_1 = repeat_zone.items.geometry(geometry, "Geometry")
        vector = repeat_zone.items.vector(cp, "Vector")
        mix = g.Mix.vector(factor, vector.current, vector.current.point.at(g.Index().o.index - 1), clamp_factor=False)
        switch = (g.Index() < (repeat_zone.iteration + 1).props(hide=True)).props(hide=True).switch.vector(mix.o.result_vector, vector.current)
        capture = g.CaptureAttribute.point(geometry=geometry_1.current)
        value = capture.items.vector(switch, "Value")
        capture.o.geometry >> geometry_1.next
        value.output >> vector.next
    with g.Frame("Rational"):
        integer_math_1 = g.Index().o.index - 1
        reroute = g.Reroute(input=weight).props(width=19.0)
        reroute_1 = g.Reroute(input=factor).props(width=19.0)
        repeat_zone_1 = g.RepeatZone(integer_math)
        geometry_2 = repeat_zone_1.items.geometry(geometry, "Geometry")
        vector_1 = repeat_zone_1.items.vector((cp * reroute).props(hide=True), "Vector")
        weight_2 = repeat_zone_1.items.float(reroute, "Weight")
        compare = (g.Index() < (repeat_zone_1.iteration + 1).props(hide=True)).props(hide=True)
        mix_1 = g.Mix.vector(reroute_1, vector_1.current, vector_1.current.point.at(integer_math_1), clamp_factor=False)
        mix_2 = g.Mix.float(reroute_1, weight_2.current, weight_2.current.point.at(integer_math_1), clamp_factor=False)
        capture_1 = g.CaptureAttribute.point(geometry=geometry_2.current)
        value_1 = capture_1.items.vector(compare.switch.vector(mix_1.o.result_vector, vector_1.current), "Value")
        result = capture_1.items.float(compare.switch.float(mix_2.o.result_float, weight_2.current), "Result")
        capture_1.o.geometry >> geometry_2.next
        value_1.output >> vector_1.next
        result.output >> weight_2.next
        vector_math = (vector_1.result / weight_2.result).props(hide=True)
    reroute_2 = g.Reroute(input=rational).props(width=19.0)
    compare_1 = g.Compare.float.equal(g.Reroute(input=factor).props(width=19.0), 0.0, 0.0).props(hide=True)
    (
        compare_1.o.result.switch.geometry(reroute_2.o.output.switch.geometry(geometry_1.result, geometry_2.result), geometry).props(hide=True)
        >> support_geometry
    )
    (
        compare_1.o.result.switch.float(reroute_2.o.output.switch.float(true=weight_2.result), weight).props(hide=True)
        >> weight_1
    )
    (
        compare_1.o.result.switch.vector(reroute_2.o.output.switch.vector(vector.result, vector_math), cp).props(hide=True)
        >> position
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Capture Attribute": ("GeometryNodeCaptureAttribute", (1051.7, -82.71), "Frame", (("Geometry", "Repeat Input", "Geometry"), ("Value", "Switch", "Output"), )),
    "Capture Attribute.001": ("GeometryNodeCaptureAttribute", (1117.6, -82.46), "Frame.001", (("Geometry", "Repeat Input.001", "Geometry"), ("Result", "Switch.005", "Output"), ("Value", "Switch.002", "Output"), )),
    "Compare": ("FunctionNodeCompare", (663.8, -104.69), "Frame", (("A", "Index.002", "Index"), ("B", "Integer Math.002", "Value"), )),
    "Compare.001": ("FunctionNodeCompare", (732.53, -105.15), "Frame.001", (("A", "Index.003", "Index"), ("B", "Integer Math.005", "Value"), )),
    "Compare.002": ("FunctionNodeCompare", (1322.23, -83.92), None, (("A", "Reroute.003", "Output"), )),
    "Domain Size.001": ("GeometryNodeAttributeDomainSize", (-641.0, 4.18), None, (("Geometry", "Group Input", "Geometry"), )),
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (434.59, -265.7), "Frame", (("Index", "Integer Math.001", "Value"), ("Value", "Repeat Input", "Vector"), )),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (528.4, -273.17), "Frame.001", (("Index", "Integer Math.004", "Value"), ("Value", "Repeat Input.001", "Vector"), )),
    "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (528.4, -404.61), "Frame.001", (("Index", "Integer Math.004", "Value"), ("Value", "Repeat Input.001", "Weight"), )),
    "Frame": ("NodeFrame", (-406.06, 286.98), None, ()),
    "Frame.001": ("NodeFrame", (-517.18, -294.32), None, ()),
    "Group Input": ("NodeGroupInput", (-816.04, -174.83), None, ()),
    "Group Output": ("NodeGroupOutput", (1737.33, -147.06), None, (("Position", "Switch.007", "Output"), ("Support Geometry", "Switch.001", "Output"), ("Weight", "Switch.008", "Output"), )),
    "Index.001": ("GeometryNodeInputIndex", (30.02, -320.77), "Frame", ()),
    "Index.002": ("GeometryNodeInputIndex", (663.8, -35.79), "Frame", ()),
    "Index.003": ("GeometryNodeInputIndex", (732.53, -36.24), "Frame.001", ()),
    "Index.004": ("GeometryNodeInputIndex", (124.33, -358.62), "Frame.001", ()),
    "Integer Math.001": ("FunctionNodeIntegerMath", (230.7, -270.06), "Frame", (("Value", "Index.001", "Index"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (504.41, -101.63), "Frame", (("Value", "Repeat Input", "Iteration"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (-638.25, -35.58), None, (("Value", "Domain Size.001", "Point Count"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (288.48, -313.9), "Frame.001", (("Value", "Index.004", "Index"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (528.4, -106.57), "Frame.001", (("Value", "Repeat Input.001", "Iteration"), )),
    "Mix": ("ShaderNodeMix", (663.8, -152.37), "Frame", (("A#1", "Repeat Input", "Vector"), ("B#1", "Evaluate at Index", "Value"), ("Factor", "Group Input", "Factor"), )),
    "Mix.001": ("ShaderNodeMix", (732.53, -152.82), "Frame.001", (("A#1", "Repeat Input.001", "Vector"), ("B#1", "Evaluate at Index.002", "Value"), ("Factor", "Reroute.002", "Output"), )),
    "Mix.005": ("ShaderNodeMix", (732.53, -374.0), "Frame.001", (("A", "Repeat Input.001", "Weight"), ("B", "Evaluate at Index.003", "Value"), ("Factor", "Reroute.002", "Output"), )),
    "Repeat Input": ("GeometryNodeRepeatInput", (167.61, -59.7), "Frame", (("Geometry", "Group Input", "Geometry"), ("Iterations", "Integer Math.003", "Value"), ("Vector", "Group Input", "CP"), )),
    "Repeat Input.001": ("GeometryNodeRepeatInput", (245.22, -65.54), "Frame.001", (("Geometry", "Group Input", "Geometry"), ("Iterations", "Integer Math.003", "Value"), ("Vector", "Vector Math", "Vector"), ("Weight", "Reroute.001", "Output"), )),
    "Repeat Output": ("GeometryNodeRepeatOutput", (1237.05, -111.49), "Frame", (("Geometry", "Capture Attribute", "Geometry"), ("Vector", "Capture Attribute", "Value"), )),
    "Repeat Output.001": ("GeometryNodeRepeatOutput", (1304.09, -110.79), "Frame.001", (("Geometry", "Capture Attribute.001", "Geometry"), ("Vector", "Capture Attribute.001", "Value"), ("Weight", "Capture Attribute.001", "Result"), )),
    "Reroute": ("NodeReroute", (1239.53, -254.99), None, (("Input", "Group Input", "Rational"), )),
    "Reroute.001": ("NodeReroute", (35.21, -187.48), "Frame.001", (("Input", "Group Input", "Weight"), )),
    "Reroute.002": ("NodeReroute", (528.4, -264.49), "Frame.001", (("Input", "Group Input", "Factor"), )),
    "Reroute.003": ("NodeReroute", (1182.2, -234.14), None, (("Input", "Group Input", "Factor"), )),
    "Switch": ("GeometryNodeSwitch", (857.65, -152.45), "Frame", (("False", "Mix", "Result#1"), ("Switch", "Compare", "Result"), ("True", "Repeat Input", "Vector"), )),
    "Switch.001": ("GeometryNodeSwitch", (1534.02, -147.6), None, (("False", "Switch.003", "Output"), ("Switch", "Compare.002", "Result"), ("True", "Group Input", "Geometry"), )),
    "Switch.002": ("GeometryNodeSwitch", (920.1, -157.31), "Frame.001", (("False", "Mix.001", "Result#1"), ("Switch", "Compare.001", "Result"), ("True", "Repeat Input.001", "Vector"), )),
    "Switch.003": ("GeometryNodeSwitch", (1322.23, -125.58), None, (("False", "Repeat Output", "Geometry"), ("Switch", "Reroute", "Output"), ("True", "Repeat Output.001", "Geometry"), )),
    "Switch.004": ("GeometryNodeSwitch", (1322.23, -301.02), None, (("False", "Repeat Output", "Vector"), ("Switch", "Reroute", "Output"), ("True", "Vector Math.001", "Vector"), )),
    "Switch.005": ("GeometryNodeSwitch", (920.1, -314.93), "Frame.001", (("False", "Mix.005", "Result"), ("Switch", "Compare.001", "Result"), ("True", "Repeat Input.001", "Weight"), )),
    "Switch.006": ("GeometryNodeSwitch", (1322.23, -465.75), None, (("Switch", "Reroute", "Output"), ("True", "Repeat Output.001", "Weight"), )),
    "Switch.007": ("GeometryNodeSwitch", (1534.02, -195.57), None, (("False", "Switch.004", "Output"), ("Switch", "Compare.002", "Result"), ("True", "Group Input", "CP"), )),
    "Switch.008": ("GeometryNodeSwitch", (1534.02, -243.55), None, (("False", "Switch.006", "Output"), ("Switch", "Compare.002", "Result"), ("True", "Group Input", "Weight"), )),
    "Vector Math": ("ShaderNodeVectorMath", (63.43, -149.19), "Frame.001", (("Scale", "Reroute.001", "Output"), ("Vector", "Group Input", "CP"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (1533.01, -146.91), "Frame.001", (("Vector", "Repeat Output.001", "Vector"), ("Vector#1", "Repeat Output.001", "Weight"), )),
}