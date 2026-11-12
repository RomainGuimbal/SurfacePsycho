from nodebpy import TreeBuilder

with TreeBuilder("Soft Max", arrange=None, clear=True) as tree:
    value = tree.inputs.float("Value", 0.5, min_value=-10_000.0, max_value=10_000.0)
    max = tree.inputs.float("Max", 0.0)
    hardness = tree.inputs.float("Hardness", 1.2, min_value=1.0)
    value_1 = tree.outputs.float("Value")

    max - (1.0 + hardness ** (0.0 - value + max)).log(hardness) >> value_1

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-856.01, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (689.47, -3.22), None, (("Value", "Math.005", "Value"), )),
    "Math": ("ShaderNodeMath", (257.34, 145.46), None, (("Value", "Math.001", "Value"), ("Value#1", "Group Input", "Hardness"), )),
    "Math.001": ("ShaderNodeMath", (54.05, 168.64), None, (("Value#1", "Math.002", "Value"), )),
    "Math.002": ("ShaderNodeMath", (-161.7, 150.39), None, (("Value", "Group Input", "Hardness"), ("Value#1", "Math.004", "Value"), )),
    "Math.003": ("ShaderNodeMath", (-569.64, 143.32), None, (("Value#1", "Group Input", "Value"), )),
    "Math.004": ("ShaderNodeMath", (-362.36, 228.44), None, (("Value", "Math.003", "Value"), ("Value#1", "Group Input", "Max"), )),
    "Math.005": ("ShaderNodeMath", (458.37, -0.46), None, (("Value", "Group Input", "Max"), ("Value#1", "Math", "Value"), )),
}