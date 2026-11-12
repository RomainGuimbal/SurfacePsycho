from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Invert 2x2 Matrix", arrange=None, clear=True) as tree:
    a = tree.inputs.float("a", 0.0)
    b = tree.inputs.float("b", 0.0)
    c_ = tree.inputs.float("c", 0.0)
    d = tree.inputs.float("d", 0.0)
    a_1 = tree.outputs.float("a")
    b_1 = tree.outputs.float("b")
    c__1 = tree.outputs.float("c")
    d_1 = tree.outputs.float("d")

    with g.Frame("Determinant"):
        math_1 = ((a * d).props(hide=True) - (b * c_).props(hide=True)).props(hide=True)
    ((0.0 - g.Reroute(input=b).props(width=19.0)) / math_1).props(hide=True) >> b_1
    (g.Reroute(input=a).props(width=19.0).o.output / math_1).props(hide=True) >> d_1
    ((0.0 - g.Reroute(input=c_).props(width=19.0)) / math_1).props(hide=True) >> c__1
    (g.Reroute(input=d).props(width=19.0).o.output / math_1).props(hide=True) >> a_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Frame": ("NodeFrame", (-166.76, -259.06), None, ()),
    "Group Input": ("NodeGroupInput", (-462.46, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (632.93, 4.66), None, (("a", "Math.008", "Value"), ("b", "Math.009", "Value"), ("c", "Math.010", "Value"), ("d", "Math.011", "Value"), )),
    "Math": ("ShaderNodeMath", (-62.63, 138.82), None, (("Value#1", "Reroute", "Output"), )),
    "Math.001": ("ShaderNodeMath", (-62.63, -92.5), None, (("Value#1", "Reroute.002", "Output"), )),
    "Math.002": ("ShaderNodeMath", (30.19, -40.26), "Frame", (("Value", "Group Input", "a"), ("Value#1", "Group Input", "d"), )),
    "Math.003": ("ShaderNodeMath", (30.19, -78.85), "Frame", (("Value", "Group Input", "b"), ("Value#1", "Group Input", "c"), )),
    "Math.004": ("ShaderNodeMath", (200.72, -60.63), "Frame", (("Value", "Math.002", "Value"), ("Value#1", "Math.003", "Value"), )),
    "Math.008": ("ShaderNodeMath", (443.59, 3.22), None, (("Value", "Reroute.003", "Output"), ("Value#1", "Math.004", "Value"), )),
    "Math.009": ("ShaderNodeMath", (443.59, -30.25), None, (("Value", "Math", "Value"), ("Value#1", "Math.004", "Value"), )),
    "Math.010": ("ShaderNodeMath", (443.59, -63.73), None, (("Value", "Math.001", "Value"), ("Value#1", "Math.004", "Value"), )),
    "Math.011": ("ShaderNodeMath", (443.59, -97.21), None, (("Value", "Reroute.001", "Output"), ("Value#1", "Math.004", "Value"), )),
    "Reroute": ("NodeReroute", (-161.14, -51.67), None, (("Input", "Group Input", "b"), )),
    "Reroute.001": ("NodeReroute", (-161.14, -28.68), None, (("Input", "Group Input", "a"), )),
    "Reroute.002": ("NodeReroute", (-161.14, -74.66), None, (("Input", "Group Input", "c"), )),
    "Reroute.003": ("NodeReroute", (-161.14, -97.65), None, (("Input", "Group Input", "d"), )),
}