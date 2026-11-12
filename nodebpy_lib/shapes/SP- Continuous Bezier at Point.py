from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP- Continuous Bezier at Point", arrange=None, clear=True) as tree:
    continuity_level = tree.inputs.integer("Continuity level", 3, min_value=0, max_value=4)
    position = tree.inputs.vector("Position", (0.0, 0.0, 0.0), hide_value=True, structure_type="SINGLE", force_non_field=True)
    velocity = tree.inputs.vector("Velocity", (0.0, 0.0, 0.0), hide_value=True, structure_type="SINGLE", force_non_field=True)
    acceleration = tree.inputs.vector("Acceleration", (0.0, 0.0, 0.0), hide_value=True, structure_type="SINGLE", force_non_field=True)
    jerk = tree.inputs.vector("Jerk", (0.0, 0.0, 0.0), hide_value=True, structure_type="SINGLE", force_non_field=True)
    snap = tree.inputs.vector("Snap", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True, structure_type="SINGLE", force_non_field=True)
    geometry = tree.outputs.geometry("Geometry")

    with g.Frame("Taylor serie"):
        with g.Frame():
            reroute = g.Reroute(input=position).props(width=19.0)
            reroute_1 = g.Reroute(input=continuity_level).props(width=19.0)
            integer_math = reroute_1.o.output * (reroute_1.o.output - 1)
            integer_math_1 = integer_math * (reroute_1.o.output - 2)
            vector_math = velocity / reroute_1
            vector_math_1 = acceleration / integer_math
            vector_math_2 = jerk / integer_math_1
            vector_math_3 = snap / (integer_math_1 * (reroute_1.o.output - 3))
        reroute_2 = g.Reroute(input=reroute.o.output).props(width=19.0)
        reroute_3 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
        reroute_4 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
        vector_math_4 = (reroute.o.output + vector_math).props(hide=True)
        reroute_5 = g.Reroute(input=vector_math_4).props(width=19.0)
        vector_math_5 = ((vector_math_4 * 2.0 + vector_math_1).props(hide=True) - reroute_2).props(hide=True)
        vector_math_6 = ((vector_math_5 * 3.0 + vector_math_2).props(hide=True) - reroute_5.o.output * 3.0).props(hide=True)
        vector_math_7 = (vector_math_6 + reroute_3).props(hide=True)
        vector_math_8 = ((vector_math_7 * 4.0 + vector_math_3).props(hide=True) - vector_math_5 * 6.0).props(hide=True)
        vector_math_9 = ((vector_math_8 + reroute_5.o.output * 4.0).props(hide=True) - reroute_4).props(hide=True)
        index_switch = g.IndexSwitch.vector(g.Index(), (reroute_4, reroute_5, vector_math_5, g.Reroute(input=vector_math_7).props(width=19.0), vector_math_9))
    mesh_line = g.MeshLine(g.Reroute(input=continuity_level).props(width=19.0).o.output + 1)
    set_position = g.SetPosition(geometry=mesh_line, position=index_switch)
    viewer = g.Viewer()
    viewer.items.geometry(mesh_line, "Mesh")
    viewer.items.vector(acceleration, "Curvature")

    set_position >> geometry

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Frame": ("NodeFrame", (30.18, -101.97), "Frame.001", ()),
    "Frame.001": ("NodeFrame", (-1632.18, 151.45), None, ()),
    "Group Input": ("NodeGroupInput", (-2078.64, -318.15), None, ()),
    "Group Output": ("NodeGroupOutput", (1772.34, 255.11), None, (("Geometry", "Set Position", "Geometry"), )),
    "Index": ("GeometryNodeInputIndex", (2657.56, -36.01), "Frame.001", ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (2888.25, -51.35), "Frame.001", (("0", "Reroute.004", "Output"), ("1", "Reroute.003", "Output"), ("2", "Vector Math.008", "Vector"), ("3", "Reroute.006", "Output"), ("4", "Vector Math.015", "Vector"), ("Index", "Index", "Index"), )),
    "Integer Math.001": ("FunctionNodeIntegerMath", (1094.58, 357.84), None, (("Value", "Reroute.005", "Output"), )),
    "Integer Math.002": ("FunctionNodeIntegerMath", (38.48, -624.93), "Frame", (("Value", "Reroute.008", "Output"), )),
    "Integer Math.003": ("FunctionNodeIntegerMath", (243.11, -494.74), "Frame", (("Value", "Reroute.008", "Output"), ("Value#1", "Integer Math.002", "Value"), )),
    "Integer Math.004": ("FunctionNodeIntegerMath", (435.42, -691.24), "Frame", (("Value", "Integer Math.003", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
    "Integer Math.005": ("FunctionNodeIntegerMath", (37.2, -766.37), "Frame", (("Value", "Reroute.008", "Output"), )),
    "Integer Math.006": ("FunctionNodeIntegerMath", (620.47, -903.61), "Frame", (("Value", "Integer Math.004", "Value"), ("Value#1", "Integer Math.007", "Value"), )),
    "Integer Math.007": ("FunctionNodeIntegerMath", (30.33, -905.36), "Frame", (("Value", "Reroute.008", "Output"), )),
    "Mesh Line": ("GeometryNodeMeshLine", (1264.9, 418.26), None, (("Count", "Integer Math.001", "Value"), )),
    "Reroute": ("NodeReroute", (978.29, -35.21), "Frame", (("Input", "Group Input", "Position"), )),
    "Reroute.001": ("NodeReroute", (1334.38, -137.6), "Frame.001", (("Input", "Reroute", "Output"), )),
    "Reroute.002": ("NodeReroute", (1973.12, -143.27), "Frame.001", (("Input", "Reroute.001", "Output"), )),
    "Reroute.003": ("NodeReroute", (1809.64, -239.09), "Frame.001", (("Input", "Vector Math.001", "Vector"), )),
    "Reroute.004": ("NodeReroute", (2594.9, -152.38), "Frame.001", (("Input", "Reroute.002", "Output"), )),
    "Reroute.005": ("NodeReroute", (-1156.99, 218.3), None, (("Input", "Group Input", "Continuity level"), )),
    "Reroute.006": ("NodeReroute", (2446.15, -307.56), "Frame.001", (("Input", "Vector Math.004", "Vector"), )),
    "Reroute.008": ("NodeReroute", (37.42, -441.32), "Frame", (("Input", "Group Input", "Continuity level"), )),
    "Set Position": ("GeometryNodeSetPosition", (1582.34, 328.56), None, (("Geometry", "Mesh Line", "Mesh"), ("Position", "Index Switch", "Output"), )),
    "Vector Math": ("ShaderNodeVectorMath", (852.53, -169.84), "Frame", (("Vector", "Group Input", "Velocity"), ("Vector#1", "Reroute.008", "Output"), )),
    "Vector Math.001": ("ShaderNodeVectorMath", (1176.99, -215.86), "Frame.001", (("Vector", "Reroute", "Output"), ("Vector#1", "Vector Math", "Vector"), )),
    "Vector Math.002": ("ShaderNodeVectorMath", (2085.76, -663.55), "Frame.001", (("Vector", "Vector Math.009", "Vector"), ("Vector#1", "Vector Math.042", "Vector"), )),
    "Vector Math.003": ("ShaderNodeVectorMath", (2093.53, -626.6), "Frame.001", (("Vector", "Vector Math.002", "Vector"), ("Vector#1", "Vector Math.010", "Vector"), )),
    "Vector Math.004": ("ShaderNodeVectorMath", (2094.79, -588.02), "Frame.001", (("Vector", "Vector Math.003", "Vector"), ("Vector#1", "Reroute.002", "Output"), )),
    "Vector Math.005": ("ShaderNodeVectorMath", (852.53, -397.41), "Frame", (("Vector", "Group Input", "Acceleration"), ("Vector#1", "Integer Math.003", "Value"), )),
    "Vector Math.006": ("ShaderNodeVectorMath", (1222.68, -327.24), "Frame.001", (("Vector", "Vector Math.001", "Vector"), )),
    "Vector Math.007": ("ShaderNodeVectorMath", (1416.98, -409.73), "Frame.001", (("Vector", "Vector Math.006", "Vector"), ("Vector#1", "Vector Math.005", "Vector"), )),
    "Vector Math.008": ("ShaderNodeVectorMath", (1419.12, -367.28), "Frame.001", (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Reroute.001", "Output"), )),
    "Vector Math.009": ("ShaderNodeVectorMath", (1875.04, -543.04), "Frame.001", (("Vector", "Vector Math.008", "Vector"), )),
    "Vector Math.010": ("ShaderNodeVectorMath", (1877.55, -402.52), "Frame.001", (("Vector", "Reroute.003", "Output"), )),
    "Vector Math.011": ("ShaderNodeVectorMath", (2677.89, -1032.4), "Frame.001", (("Vector", "Vector Math.012", "Vector"), ("Vector#1", "Vector Math.043", "Vector"), )),
    "Vector Math.012": ("ShaderNodeVectorMath", (2437.81, -881.85), "Frame.001", (("Vector", "Vector Math.004", "Vector"), )),
    "Vector Math.013": ("ShaderNodeVectorMath", (2685.17, -944.37), "Frame.001", (("Vector", "Vector Math.016", "Vector"), ("Vector#1", "Vector Math.014", "Vector"), )),
    "Vector Math.014": ("ShaderNodeVectorMath", (2449.9, -606.31), "Frame.001", (("Vector", "Reroute.003", "Output"), )),
    "Vector Math.015": ("ShaderNodeVectorMath", (2684.21, -901.09), "Frame.001", (("Vector", "Vector Math.013", "Vector"), ("Vector#1", "Reroute.004", "Output"), )),
    "Vector Math.016": ("ShaderNodeVectorMath", (2676.91, -989.81), "Frame.001", (("Vector", "Vector Math.011", "Vector"), ("Vector#1", "Vector Math.017", "Vector"), )),
    "Vector Math.017": ("ShaderNodeVectorMath", (2446.21, -742.22), "Frame.001", (("Vector", "Vector Math.008", "Vector"), )),
    "Vector Math.042": ("ShaderNodeVectorMath", (852.53, -624.99), "Frame", (("Vector", "Group Input", "Jerk"), ("Vector#1", "Integer Math.004", "Value"), )),
    "Vector Math.043": ("ShaderNodeVectorMath", (852.53, -852.57), "Frame", (("Vector", "Group Input", "Snap"), ("Vector#1", "Integer Math.006", "Value"), )),
    "Viewer": ("GeometryNodeViewer", (-1790.5, -245.28), None, (("Curvature", "Group Input", "Acceleration"), ("Mesh", "Mesh Line", "Mesh"), )),
}