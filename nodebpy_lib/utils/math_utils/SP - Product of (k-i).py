from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Product of (k-i)", arrange=None, clear=True) as tree:
    k = tree.inputs.integer("k", 0)
    k_1_k_2_k_3 = tree.outputs.integer("(k-1)(k-2)(k-3)")
    k_1_k_2 = tree.outputs.integer("(k-1)(k-2)")
    k_1 = tree.outputs.integer("k-1")

    with g.Frame():
        with g.Frame():
            with g.Frame("k(k-1)"):
                reroute = g.Reroute(input=k).props(width=19.0)
                integer_math = (reroute.o.output - 1) * reroute
            integer_math_1 = (reroute.o.output - 2) * integer_math
        (reroute.o.output - 3) * integer_math_1 >> k_1_k_2_k_3

    integer_math_1 >> k_1_k_2
    integer_math >> k_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Frame.002": ("NodeFrame", (30.18, -181.28), "Frame.005", ()),
    "Frame.005": ("NodeFrame", (30.18, -181.06), "Frame.008", ()),
    "Frame.008": ("NodeFrame", (-565.35, 869.82), None, ()),
    "Group Input": ("NodeGroupInput", (-781.56, 505.93), None, ()),
    "Group Output": ("NodeGroupOutput", (435.22, 482.68), None, (("(k-1)(k-2)", "Integer Math.005", "Value"), ("(k-1)(k-2)(k-3)", "Integer Math.006", "Value"), ("k-1", "Integer Math.004", "Value"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (462.08, -30.0), "Frame.008", (("Value", "Reroute.001", "Output"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (343.02, -40.06), "Frame.005", (("Value", "Reroute.001", "Output"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (97.06, -69.11), "Frame.002", (("Value", "Reroute.001", "Output"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (268.61, -63.37), "Frame.002", (("Value", "Integer Math.003", "Value"), ("Value#1", "Reroute.001", "Output"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (522.6, -30.44), "Frame.005", (("Value", "Integer Math.002", "Value"), ("Value#1", "Integer Math.004", "Value"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (631.69, -33.71), "Frame.008", (("Value", "Integer Math.001", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
    "Reroute.001": ("NodeReroute", (35.21, -41.06), "Frame.002", (("Input", "Group Input", "k"), )),
}