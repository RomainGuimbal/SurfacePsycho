from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Binomial Coefficient", arrange=None, clear=True) as tree:
    n = tree.inputs.integer("n", 0)
    k = tree.inputs.integer("k", 0)
    output = tree.outputs.integer("Output")

    with g.Frame("Special cases"):
        reroute = g.Reroute(input=k).props(width=19.0)
        reroute_1 = g.Reroute(input=n).props(width=19.0)
        boolean_math = (reroute < 0) | (reroute > reroute_1)
        boolean_math_1 = g.Compare.integer.equal(reroute, 0).o.result | g.Compare.integer.equal(reroute, reroute_1)
    reroute_2 = g.Reroute(input=k).props(width=19.0)
    with g.Frame("nth row"):
        index = g.Index()
        index_switch = g.IndexSwitch.integer(g.Index(), (1, 16, 120, 560, 1820, 4368, 8008, 11440, 12870, 11440, 8008, 4368, 1820, 560, 120, 16, 1))
        reroute_3 = g.Reroute(input=n).props(width=19.0)
        integer_math = (reroute_3.o.output + 1).props(hide=True)
        repeat_zone = g.RepeatZone(reroute_3.o.output - 16)
        integer = repeat_zone.items.integer(g.FieldToList(count=integer_math, items={"Integer": index_switch}).o.integer, "Integer")
        integer_math_1 = (integer.current[index.o.index - 1].props(hide=True) + integer.current[index].props(hide=True)).props(hide=True)
        g.FieldToList(count=integer_math, items={"Integer": integer_math_1}) >> integer.next
        get_list_item = integer.result[reroute_2]
    index_switch_1 = g.IndexSwitch.integer(reroute_2, (1, 12, 66, 220, 495, 792, 924, 792, 495, 220, 66, 12, 1))
    index_switch_2 = g.IndexSwitch.integer(reroute_2, (1, 13, 78, 286, 715, 1287, 1716, 1716, 1287, 715, 286, 78, 13, 1))
    index_switch_3 = g.IndexSwitch.integer(reroute_2, (1, 14, 91, 364, 1001, 2002, 3003, 3432, 3003, 2002, 1001, 364, 91, 14, 1))
    index_switch_4 = g.IndexSwitch.integer(reroute_2, (1, 15, 105, 455, 1365, 3003, 5005, 6435, 6435, 5005, 3003, 1365, 455, 105, 15, 1))
    index_switch_5 = g.IndexSwitch.integer(reroute_2, (1, 16, 120, 560, 1820, 4368, 8008, 11440, 12870, 11440, 8008, 4368, 1820, 560, 120, 16, 1))
    index_switch_6 = g.IndexSwitch.integer(g.Reroute(input=n).props(width=19.0).o.output.min(17), (1, 1, g.IndexSwitch.integer(reroute_2, (1, 2, 1)), g.IndexSwitch.integer(reroute_2, (1, 3, 3, 1)), g.IndexSwitch.integer(reroute_2, (1, 4, 6, 4, 1)), g.IndexSwitch.integer(reroute_2, (1, 5, 10, 10, 5, 1)), g.IndexSwitch.integer(reroute_2, (1, 6, 15, 20, 15, 6, 1)), g.IndexSwitch.integer(reroute_2, (1, 7, 21, 35, 35, 21, 7, 1)), g.IndexSwitch.integer(reroute_2, (1, 8, 28, 56, 70, 56, 28, 8, 1)), g.IndexSwitch.integer(reroute_2, (1, 9, 36, 84, 126, 126, 84, 36, 8, 1)), g.IndexSwitch.integer(reroute_2, (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)), g.IndexSwitch.integer(reroute_2, (1, 11, 55, 165, 330, 462, 462, 330, 165, 55, 11, 1)), index_switch_1, index_switch_2, index_switch_3, index_switch_4, index_switch_5, get_list_item))
    (
        boolean_math.switch.integer(boolean_math_1.switch.integer(index_switch_6, 1))
        >> output
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (344.96, -119.22), "Frame", (("Boolean", "Compare", "Result"), ("Boolean#1", "Compare.001", "Result"), )),
    "Boolean Math.001": ("FunctionNodeBooleanMath", (347.05, -481.7), "Frame", (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Compare.003", "Result"), )),
    "Compare": ("FunctionNodeCompare", (166.29, -35.92), "Frame", (("A", "Reroute", "Output"), )),
    "Compare.001": ("FunctionNodeCompare", (159.9, -204.91), "Frame", (("A", "Reroute", "Output"), ("B", "Reroute.002", "Output"), )),
    "Compare.002": ("FunctionNodeCompare", (156.6, -387.91), "Frame", (("A", "Reroute", "Output"), )),
    "Compare.003": ("FunctionNodeCompare", (153.56, -554.01), "Frame", (("A", "Reroute", "Output"), ("B", "Reroute.002", "Output"), )),
    "Field to List": ("GeometryNodeFieldToList", (388.43, -172.02), "Frame.002", (("Count", "Integer Math.001", "Value"), ("Integer", "Index Switch.017", "Output"), )),
    "Field to List.001": ("GeometryNodeFieldToList", (1422.98, -248.61), "Frame.002", (("Count", "Integer Math.001", "Value"), ("Integer", "Integer Math.007", "Value"), )),
    "Frame": ("NodeFrame", (1534.91, 311.33), None, ()),
    "Frame.002": ("NodeFrame", (722.12, -1605.14), None, ()),
    "Get List Item": ("GeometryNodeListGetItem", (1770.85, -151.27), "Frame.002", (("Index", "Reroute.003", "Output"), ("List", "Repeat Output", "Integer"), )),
    "Get List Item.001": ("GeometryNodeListGetItem", (1035.72, -353.27), "Frame.002", (("Index", "Index", "Index"), ("List", "Repeat Input", "Integer"), )),
    "Get List Item.002": ("GeometryNodeListGetItem", (1036.09, -312.96), "Frame.002", (("Index", "Integer Math", "Value"), ("List", "Repeat Input", "Integer"), )),
    "Group Input": ("NodeGroupInput", (-474.63, -338.78), None, ()),
    "Group Output": ("NodeGroupOutput", (3284.72, -381.44), None, (("Output", "Switch", "Output"), )),
    "Index": ("GeometryNodeInputIndex", (656.79, -419.77), "Frame.002", ()),
    "Index Switch.001": ("GeometryNodeIndexSwitch", (2680.28, -397.24), None, (("10", "Index Switch.010", "Output"), ("11", "Index Switch.011", "Output"), ("12", "Index Switch.012", "Output"), ("13", "Index Switch.013", "Output"), ("14", "Index Switch.014", "Output"), ("15", "Index Switch.015", "Output"), ("16", "Index Switch.016", "Output"), ("17", "Get List Item", "Value"), ("2", "Index Switch.002", "Output"), ("3", "Index Switch.003", "Output"), ("4", "Index Switch.004", "Output"), ("5", "Index Switch.005", "Output"), ("6", "Index Switch.006", "Output"), ("7", "Index Switch.007", "Output"), ("8", "Index Switch.008", "Output"), ("9", "Index Switch.009", "Output"), ("Index", "Integer Math.004", "Value"), )),
    "Index Switch.002": ("GeometryNodeIndexSwitch", (-65.84, -533.81), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.003": ("GeometryNodeIndexSwitch", (100.45, -588.47), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.004": ("GeometryNodeIndexSwitch", (266.75, -635.66), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.005": ("GeometryNodeIndexSwitch", (433.05, -662.1), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.006": ("GeometryNodeIndexSwitch", (599.34, -720.56), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.007": ("GeometryNodeIndexSwitch", (765.64, -774.27), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.008": ("GeometryNodeIndexSwitch", (931.93, -794.22), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.009": ("GeometryNodeIndexSwitch", (1098.23, -839.12), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.010": ("GeometryNodeIndexSwitch", (1264.53, -894.79), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.011": ("GeometryNodeIndexSwitch", (1430.82, -931.15), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.012": ("GeometryNodeIndexSwitch", (1597.12, -966.13), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.013": ("GeometryNodeIndexSwitch", (1763.41, -979.95), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.014": ("GeometryNodeIndexSwitch", (1929.71, -1021.78), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.015": ("GeometryNodeIndexSwitch", (2096.01, -1066.46), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.016": ("GeometryNodeIndexSwitch", (2262.3, -1095.43), None, (("Index", "Reroute.003", "Output"), )),
    "Index Switch.017": ("GeometryNodeIndexSwitch", (192.48, -358.4), "Frame.002", (("Index", "Index.001", "Index"), )),
    "Index.001": ("GeometryNodeInputIndex", (29.96, -413.14), "Frame.002", ()),
    "Integer Math": ("FunctionNodeIntegerMath", (842.47, -304.17), "Frame.002", (("Value", "Index", "Index"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (171.91, -263.03), "Frame.002", (("Value", "Reroute.005", "Output"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (2485.36, -409.02), None, (("Value", "Reroute.001", "Output"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (386.07, -36.15), "Frame.002", (("Value", "Reroute.005", "Output"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (1227.11, -309.31), "Frame.002", (("Value", "Get List Item.002", "Value"), ("Value#1", "Get List Item.001", "Value"), )),
    "Repeat Input": ("GeometryNodeRepeatInput", (604.48, -101.14), "Frame.002", (("Integer", "Field to List", "Integer"), ("Iterations", "Integer Math.005", "Value"), )),
    "Repeat Output": ("GeometryNodeRepeatOutput", (1591.55, -275.95), "Frame.002", (("Integer", "Field to List.001", "Integer"), )),
    "Reroute": ("NodeReroute", (66.67, -430.27), "Frame", (("Input", "Group Input", "k"), )),
    "Reroute.001": ("NodeReroute", (-120.11, -491.99), None, (("Input", "Group Input", "n"), )),
    "Reroute.002": ("NodeReroute", (35.21, -393.47), "Frame", (("Input", "Group Input", "n"), )),
    "Reroute.003": ("NodeReroute", (-196.95, -907.56), None, (("Input", "Group Input", "k"), )),
    "Reroute.005": ("NodeReroute", (216.05, -100.23), "Frame.002", (("Input", "Group Input", "n"), )),
    "Switch": ("GeometryNodeSwitch", (3091.02, -327.23), None, (("False", "Switch.001", "Output"), ("Switch", "Boolean Math", "Boolean"), )),
    "Switch.001": ("GeometryNodeSwitch", (2910.89, -325.47), None, (("False", "Index Switch.001", "Output"), ("Switch", "Boolean Math.001", "Boolean"), )),
}