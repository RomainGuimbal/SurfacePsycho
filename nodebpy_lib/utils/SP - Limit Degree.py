from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Limit Degree", arrange=None, clear=True) as tree:
    degree_u = tree.inputs.integer("Degree U", 0, structure_type="SINGLE", force_non_field=True)
    degree_v = tree.inputs.integer("Degree V", 0, structure_type="SINGLE", force_non_field=True)
    u_count = tree.inputs.integer("U Count", 0, structure_type="SINGLE", force_non_field=True)
    v_count = tree.inputs.integer("V Count", 0, structure_type="SINGLE", force_non_field=True)
    clamped_u = tree.inputs.boolean("Clamped U", False, structure_type="SINGLE", force_non_field=True)
    clamped_v = tree.inputs.boolean("Clamped V", False, structure_type="SINGLE", force_non_field=True)
    cyclic_u = tree.inputs.boolean("Cyclic U", False, structure_type="SINGLE", force_non_field=True)
    cyclic_v = tree.inputs.boolean("Cyclic V", False, structure_type="SINGLE", force_non_field=True)
    degree_u_1 = tree.outputs.integer("Degree U")
    degree_v_1 = tree.outputs.integer("Degree V")

    integer_math = g.Reroute(input=degree_v).props(width=19.0).o.output.min(g.IntegerMath.subtract(v_count, ~(clamped_v & cyclic_v)).props(width=100.0, hide=True)).props(width=100.0, hide=True)
    integer_math.min(25).props(width=100.0) >> degree_v_1
    integer_math_1 = g.Reroute(input=degree_u).props(width=19.0).o.output.min(g.IntegerMath.subtract(u_count, ~(clamped_u & cyclic_u)).props(width=100.0, hide=True)).props(width=100.0, hide=True)
    integer_math_1.min(25).props(width=100.0) >> degree_u_1
    _warning = g.Warning(show=integer_math_1 > 25, message="Degree cannot exceed 25").props(width=174.53)

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Boolean Math": ("FunctionNodeBooleanMath", (-27.08, -85.97), None, (("Boolean", "Group Input", "Clamped U"), ("Boolean#1", "Group Input", "Cyclic U"), )),
    "Boolean Math.001": ("FunctionNodeBooleanMath", (125.95, -96.35), None, (("Boolean", "Boolean Math", "Boolean"), )),
    "Boolean Math.002": ("FunctionNodeBooleanMath", (-31.4, -217.46), None, (("Boolean", "Group Input", "Clamped V"), ("Boolean#1", "Group Input", "Cyclic V"), )),
    "Boolean Math.003": ("FunctionNodeBooleanMath", (121.63, -227.84), None, (("Boolean", "Boolean Math.002", "Boolean"), )),
    "Compare": ("FunctionNodeCompare", (744.7, 315.18), None, (("A", "Integer Math.003", "Value"), )),
    "Group Input": ("NodeGroupInput", (-367.33, 47.5), None, ()),
    "Group Output": ("NodeGroupOutput", (906.53, 44.9), None, (("Degree U", "Integer Math.004", "Value"), ("Degree V", "Integer Math.005", "Value"), )),
    "Integer Math": ("FunctionNodeIntegerMath", (405.9, -30.5), None, (("Value", "Group Input", "U Count"), ("Value#1", "Boolean Math.001", "Boolean"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (405.17, -63.16), None, (("Value", "Group Input", "V Count"), ("Value#1", "Boolean Math.003", "Boolean"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (579.99, -56.02), None, (("Value", "Reroute.036", "Output"), ("Value#1", "Integer Math.001", "Value"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (579.45, -23.47), None, (("Value", "Reroute.038", "Output"), ("Value#1", "Integer Math", "Value"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (739.76, 114.96), None, (("Value", "Integer Math.003", "Value"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (736.02, -15.99), None, (("Value", "Integer Math.002", "Value"), )),
    "Reroute.036": ("NodeReroute", (527.05, -3.52), None, (("Input", "Group Input", "Degree V"), )),
    "Reroute.038": ("NodeReroute", (536.79, 18.62), None, (("Input", "Group Input", "Degree U"), )),
    "Warning": ("GeometryNodeWarning", (910.28, 315.47), None, (("Show", "Compare", "Result"), )),
}