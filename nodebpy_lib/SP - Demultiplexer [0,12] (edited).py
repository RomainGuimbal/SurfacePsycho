from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Demultiplexer [0,12] (edited)", arrange=None, clear=True) as tree:
    vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), hide_value=True, subtype="XYZ")
    u_count = tree.inputs.integer("U Count", 0, min_value=0)
    v = tree.inputs.integer("V", 0, min_value=0)
    n_0 = tree.outputs.vector("0")
    n_1 = tree.outputs.vector("1")
    n_2 = tree.outputs.vector("2")
    n_3 = tree.outputs.vector("3")
    n_4 = tree.outputs.vector("4")
    n_5 = tree.outputs.vector("5")
    n_6 = tree.outputs.vector("6")
    n_7 = tree.outputs.vector("7")
    n_8 = tree.outputs.vector("8")
    n_9 = tree.outputs.vector("9")
    n_10 = tree.outputs.vector("10")
    n_11 = tree.outputs.vector("11")
    n_12 = tree.outputs.vector("12")

    reroute = g.Reroute(input=vector).props(width=9.5)
    reroute_1 = g.Reroute(input=(u_count * v).props(hide=True)).props(width=9.5)
    reroute.o.output.point.at((reroute_1.o.output + 0).props(mute=True)) >> n_0
    reroute.o.output.point.at(reroute_1.o.output + 1) >> n_1
    reroute.o.output.point.at(reroute_1.o.output + 2) >> n_2
    reroute.o.output.point.at(reroute_1.o.output + 3) >> n_3
    reroute.o.output.point.at(reroute_1.o.output + 4) >> n_4
    reroute.o.output.point.at(reroute_1.o.output + 5) >> n_5
    reroute.o.output.point.at(reroute_1.o.output + 6) >> n_6
    reroute.o.output.point.at(reroute_1.o.output + 7) >> n_7
    reroute.o.output.point.at(reroute_1.o.output + 8) >> n_8
    reroute.o.output.point.at(reroute_1.o.output + 9) >> n_9
    reroute.o.output.point.at(reroute_1.o.output + 10) >> n_10
    reroute.o.output.point.at(reroute_1.o.output + 11) >> n_11
    reroute.o.output.point.at(reroute_1.o.output + 12) >> n_12

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Evaluate at Index": ("GeometryNodeFieldAtIndex", (2.03, 859.84), None, (("Index", "Integer Math.001", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (2.03, 718.61), None, (("Index", "Integer Math.002", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (2.03, 577.37), None, (("Index", "Integer Math.003", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.003": ("GeometryNodeFieldAtIndex", (2.03, 436.14), None, (("Index", "Integer Math.004", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.004": ("GeometryNodeFieldAtIndex", (2.03, 294.9), None, (("Index", "Integer Math.005", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.005": ("GeometryNodeFieldAtIndex", (2.03, 153.67), None, (("Index", "Integer Math.006", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (0.31, 3.42), None, (("Index", "Integer Math.007", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.007": ("GeometryNodeFieldAtIndex", (0.31, -137.82), None, (("Index", "Integer Math.008", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.008": ("GeometryNodeFieldAtIndex", (0.31, -279.06), None, (("Index", "Integer Math.009", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.009": ("GeometryNodeFieldAtIndex", (0.31, -420.29), None, (("Index", "Integer Math.010", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.010": ("GeometryNodeFieldAtIndex", (0.31, -561.53), None, (("Index", "Integer Math.011", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.011": ("GeometryNodeFieldAtIndex", (0.31, -702.76), None, (("Index", "Integer Math.012", "Value"), ("Value", "Reroute", "Output"), )),
    "Evaluate at Index.012": ("GeometryNodeFieldAtIndex", (-2.03, -859.84), None, (("Index", "Integer Math.013", "Value"), ("Value", "Reroute", "Output"), )),
    "Group Input": ("NodeGroupInput", (-736.95, -25.82), None, ()),
    "Group Output": ("NodeGroupOutput", (331.98, 168.2), None, (("0", "Evaluate at Index", "Value"), ("1", "Evaluate at Index.001", "Value"), ("10", "Evaluate at Index.010", "Value"), ("11", "Evaluate at Index.011", "Value"), ("12", "Evaluate at Index.012", "Value"), ("2", "Evaluate at Index.002", "Value"), ("3", "Evaluate at Index.003", "Value"), ("4", "Evaluate at Index.004", "Value"), ("5", "Evaluate at Index.005", "Value"), ("6", "Evaluate at Index.006", "Value"), ("7", "Evaluate at Index.007", "Value"), ("8", "Evaluate at Index.008", "Value"), ("9", "Evaluate at Index.009", "Value"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (-533.78, -81.37), None, (("Value", "Group Input", "U Count"), ("Value#1", "Group Input", "V"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-198.33, 840.76), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (-195.01, 705.51), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (-192.92, 561.88), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (-190.82, 418.25), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (-188.72, 274.62), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (-186.63, 130.98), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (-184.53, -12.65), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.008": ("FunctionNodeIntegerMath", (-182.43, -156.28), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.009": ("FunctionNodeIntegerMath", (-180.34, -299.91), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.010": ("FunctionNodeIntegerMath", (-178.24, -443.54), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.011": ("FunctionNodeIntegerMath", (-176.15, -587.17), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.012": ("FunctionNodeIntegerMath", (-174.05, -730.81), None, (("Value", "Reroute.002", "Output"), )),
    "Integer Math.013": ("FunctionNodeIntegerMath", (-171.95, -874.44), None, (("Value", "Reroute.002", "Output"), )),
    "Reroute": ("NodeReroute", (-261.97, -65.81), None, (("Input", "Group Input", "Vector"), )),
    "Reroute.002": ("NodeReroute", (-320.8, -96.65), None, (("Input", "Integer Math", "Value"), )),
}