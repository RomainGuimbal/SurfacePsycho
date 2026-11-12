import math
from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Chebyshev Parametrization", arrange=None, clear=True) as tree:
    input = tree.inputs.geometry("Input")
    value = tree.outputs.float("Value")

    domain_size = g.DomainSize(input).props(width=105.73, hide=True, hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
    index = g.Index()
    math_1 = (index.o.index * math.pi / (domain_size.o.point_count - 1).props(hide=True)).cos().props(hide=True)
    sample_index = g.SampleIndex.point.float(input, ((1.0 - math_1) / 2.0).min(1.0).props(label="Clamp slight overshoot", width=181.62), index)

    sample_index >> value

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Domain Size.001": ("GeometryNodeAttributeDomainSize", (-226.28, -893.27), None, (("Geometry", "Group Input", "Input"), )),
    "Group Input": ("NodeGroupInput", (-436.23, -595.54), None, ()),
    "Group Output": ("NodeGroupOutput", (1320.14, -591.45), None, (("Value", "Sample Index.001", "Value"), )),
    "Index.001": ("GeometryNodeInputIndex", (-247.05, -645.59), None, ()),
    "Integer Math.001": ("FunctionNodeIntegerMath", (-75.24, -900.41), None, (("Value", "Domain Size.001", "Point Count"), )),
    "Math.001": ("ShaderNodeMath", (877.84, -714.06), None, (("Value", "Math.006", "Value"), )),
    "Math.002": ("ShaderNodeMath", (159.26, -744.68), None, (("Value", "Math.004", "Value"), ("Value#1", "Integer Math.001", "Value"), )),
    "Math.003": ("ShaderNodeMath", (332.74, -763.9), None, (("Value", "Math.002", "Value"), )),
    "Math.004": ("ShaderNodeMath", (-59.32, -722.6), None, (("Value", "Index.001", "Index"), )),
    "Math.005": ("ShaderNodeMath", (511.89, -716.99), None, (("Value#1", "Math.003", "Value"), )),
    "Math.006": ("ShaderNodeMath", (688.04, -721.08), None, (("Value", "Math.005", "Value"), )),
    "Sample Index.001": ("GeometryNodeSampleIndex", (1103.68, -508.75), None, (("Geometry", "Group Input", "Input"), ("Index", "Index.001", "Index"), ("Value", "Math.001", "Value"), )),
}