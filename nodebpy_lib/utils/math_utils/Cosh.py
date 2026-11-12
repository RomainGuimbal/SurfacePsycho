from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("Cosh", arrange=None, clear=True) as tree:
    input = tree.inputs.float("Input", 0.0)
    result = tree.outputs.float("Result")

    mix = g.Mix.float(0.5, g.Math.exponent(input), g.Math.exponent((0.0 - input).props(hide=True))).props(hide=True)

    mix >> result

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-387.07, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (480.29, 0.0), None, (("Result", "Mix", "Result"), )),
    "Math": ("ShaderNodeMath", (23.82, 75.03), None, (("Value", "Group Input", "Input"), )),
    "Math.001": ("ShaderNodeMath", (-152.24, -75.03), None, (("Value#1", "Group Input", "Input"), )),
    "Math.002": ("ShaderNodeMath", (19.09, -71.34), None, (("Value", "Math.001", "Value"), )),
    "Mix": ("ShaderNodeMix", (290.29, -30.1), None, (("A", "Math", "Value"), ("B", "Math.002", "Value"), )),
}