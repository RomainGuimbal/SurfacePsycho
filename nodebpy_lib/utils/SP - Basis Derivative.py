from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Basis Derivative", arrange=None, clear=True) as tree:
    n_i_p_1 = tree.inputs.float("N_(i,p-1)", 0.0)
    cp_index = tree.inputs.integer("CP Index", 0)
    degree = tree.inputs.integer("Degree", 0)
    knot = tree.inputs.float("Knot", 0.0)
    n_i_p = tree.outputs.float("N'_(i,p)")

    reroute = g.Reroute(input=knot).props(width=9.5)
    reroute_1 = g.Reroute(input=degree).props(label="Degree", width=9.5)
    reroute_2 = g.Reroute(input=reroute_1.o.output).props(width=9.5)
    reroute_3 = g.Reroute(input=cp_index).props(label="i", width=9.5)
    reroute_4 = g.Reroute(input=n_i_p_1).props(width=9.5)
    with g.Frame():
        integer_math = (cp_index + 1).props(label="i+1", width=100.0, hide=True)
        evaluate_at_index = reroute_4.o.output.point.at((g.Index().props(width=100.0, hide=True).o.index + 1).props(width=100.0, hide=True)).props(label="N_(i+1,p-1)", hide=True)
        reroute_5 = g.Reroute(input=reroute.o.output).props(width=9.5)
        evaluate_at_index_1 = reroute_5.o.output.point.at((reroute_2.o.output + integer_math).props(label="i+p+1", width=100.0, hide=True)).props(label="u_(i+p+1)", hide=True)
        math_1 = (evaluate_at_index_1 - reroute_5.o.output.point.at(integer_math).props(label="u_(i+1)", hide=True)).props(hide=True)
        math_2 = evaluate_at_index / math_1
    with g.Frame():
        reroute_6 = g.Reroute(input=reroute.o.output).props(width=9.5)
        evaluate_at_index_2 = reroute_6.o.output.point.at((reroute_2.o.output + reroute_3).props(label="p+i", width=100.0, hide=True)).props(label="u_(i+p)", hide=True)
        math_3 = (evaluate_at_index_2 - reroute_6.o.output.point.at(reroute_3).props(label="u_i", hide=True)).props(hide=True)
        math_4 = reroute_4.o.output / math_3
    (
        (reroute_1.o.output * (math_4 - math_2).props(hide=True)).props(label="*p", hide=True)
        >> n_i_p
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (178.08, -108.84), "Frame.001", (("Index", "Integer Math.008", "Value"), ("Value", "Reroute.002", "Output"), )),
    "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (176.99, -152.91), "Frame.001", (("Index", "Reroute.039", "Output"), ("Value", "Reroute.002", "Output"), )),
    "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (287.86, -127.66), "Frame", (("Index", "Integer Math.013", "Value"), ("Value", "Reroute.041", "Output"), )),
    "Evaluate at Index.007": ("GeometryNodeFieldAtIndex", (480.39, -42.03), "Frame", (("Index", "Integer Math.012", "Value"), ("Value", "Reroute.040", "Output"), )),
    "Evaluate at Index.008": ("GeometryNodeFieldAtIndex", (286.77, -171.73), "Frame", (("Index", "Integer Math.014", "Value"), ("Value", "Reroute.041", "Output"), )),
    "Frame": ("NodeFrame", (-465.35, -377.68), None, ()),
    "Frame.001": ("NodeFrame", (-373.24, -137.12), None, ()),
    "Group Input": ("NodeGroupInput", (-782.53, -38.29), None, ()),
    "Group Output": ("NodeGroupOutput", (808.67, 0.0), None, (("N'_(i,p)", "Math.002", "Value"), )),
    "Index.001": ("GeometryNodeInputIndex", (244.1, -33.88), "Frame", ()),
    "Integer Math.008": ("FunctionNodeIntegerMath", (29.9, -90.87), "Frame.001", (("Value", "Reroute", "Output"), ("Value#1", "Reroute.039", "Output"), )),
    "Integer Math.012": ("FunctionNodeIntegerMath", (357.33, -41.01), "Frame", (("Value", "Index.001", "Index"), )),
    "Integer Math.013": ("FunctionNodeIntegerMath", (151.94, -111.77), "Frame", (("Value", "Reroute", "Output"), ("Value#1", "Integer Math.014", "Value"), )),
    "Integer Math.014": ("FunctionNodeIntegerMath", (30.67, -160.57), "Frame", (("Value", "Group Input", "CP Index"), )),
    "Math": ("ShaderNodeMath", (550.64, -30.35), "Frame.001", (("Value", "Reroute.040", "Output"), ("Value#1", "Math.005", "Value"), )),
    "Math.001": ("ShaderNodeMath", (660.69, -33.71), "Frame", (("Value", "Evaluate at Index.007", "Value"), ("Value#1", "Math.004", "Value"), )),
    "Math.002": ("ShaderNodeMath", (592.53, -38.16), None, (("Value", "Reroute.024", "Output"), ("Value#1", "Math.003", "Value"), )),
    "Math.003": ("ShaderNodeMath", (430.53, -359.16), None, (("Value", "Math", "Value"), ("Value#1", "Math.001", "Value"), )),
    "Math.004": ("ShaderNodeMath", (462.8, -146.0), "Frame", (("Value", "Evaluate at Index.006", "Value"), ("Value#1", "Evaluate at Index.008", "Value"), )),
    "Math.005": ("ShaderNodeMath", (347.8, -126.09), "Frame.001", (("Value", "Evaluate at Index.001", "Value"), ("Value#1", "Evaluate at Index.005", "Value"), )),
    "Reroute": ("NodeReroute", (-402.78, -234.85), None, (("Input", "Reroute.024", "Output"), )),
    "Reroute.001": ("NodeReroute", (-421.32, -320.12), None, (("Input", "Group Input", "Knot"), )),
    "Reroute.002": ("NodeReroute", (129.29, -176.03), "Frame.001", (("Input", "Reroute.001", "Output"), )),
    "Reroute.024": ("NodeReroute", (-425.08, -32.51), None, (("Input", "Group Input", "Degree"), )),
    "Reroute.039": ("NodeReroute", (-408.12, -293.61), None, (("Input", "Group Input", "CP Index"), )),
    "Reroute.040": ("NodeReroute", (-123.45, -75.52), None, (("Input", "Group Input", "N_(i,p-1)"), )),
    "Reroute.041": ("NodeReroute", (234.78, -155.3), "Frame", (("Input", "Reroute.001", "Output"), )),
}