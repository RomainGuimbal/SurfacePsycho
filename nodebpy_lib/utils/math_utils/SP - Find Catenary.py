from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Sinh(CustomGeometryGroup):
    _name = "Sinh"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.float("Input", 0.0)
        result = tree.outputs.float("Result")

        mix = g.Mix.float(0.5, g.Math.exponent(input), (0.0 - g.Math.exponent((0.0 - input).props(hide=True))).props(hide=True)).props(hide=True)

        mix >> result

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-387.07, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (554.85, -1.41), None, (("Result", "Mix", "Result"), )),
            "Math": ("ShaderNodeMath", (23.82, 75.03), None, (("Value", "Group Input", "Input"), )),
            "Math.001": ("ShaderNodeMath", (-152.24, -75.03), None, (("Value#1", "Group Input", "Input"), )),
            "Math.002": ("ShaderNodeMath", (19.09, -71.34), None, (("Value", "Math.001", "Value"), )),
            "Math.003": ("ShaderNodeMath", (180.74, -106.24), None, (("Value#1", "Math.002", "Value"), )),
            "Mix": ("ShaderNodeMix", (364.85, -31.51), None, (("A", "Math", "Value"), ("B", "Math.003", "Value"), )),
        }


class Cosh(CustomGeometryGroup):
    _name = "Cosh"
    _color_tag = "CONVERTER"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

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


class SPFindCatenary(CustomGeometryGroup):
    _name = "SP - Find Catenary"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_find_inflexion_points", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        iterations = tree.inputs.integer("Iterations", 12, min_value=0)
        tolerence_exponent = tree.inputs.integer("Tolerence Exponent", -6, min_value=-10, max_value=16, structure_type="SINGLE", force_non_field=True)
        k = tree.inputs.float("K", 2.0, min_value=0.0, max_value=10_000.0, structure_type="SINGLE", force_non_field=True)
        initial_guess = tree.inputs.float("Initial Guess", 0.0, structure_type="SINGLE", force_non_field=True)
        parameter = tree.outputs.float("Parameter")
        achieved_tolerance = tree.outputs.boolean("Achieved Tolerance", description="Per  Vertex")

        repeat_zone = g.RepeatZone(iterations)
        repeat_zone.output.node.inspection_index = 1
        parameter_guess = repeat_zone.items.float(initial_guess, "Parameter Guess")
        marching_step = repeat_zone.items.float(name="Marching step")
        reroute = g.Reroute(input=parameter_guess.current).props(width=19.0)
        reroute_1 = g.Reroute(input=tolerence_exponent).props(width=19.0)
        with g.Frame("NEWTON STEP"):
            reroute_2 = g.Reroute(input=parameter_guess.current).props(label="z", width=19.0)
            compare = reroute_2 < 0.01
            sinh = Sinh(Input=reroute_2)
            reroute_3 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
            with g.Frame("f'"):
                reroute_4 = g.Reroute(input=reroute_2.o.output).props(width=19.0)
                math_1 = (((Cosh(Input=reroute_4).o.result * reroute_4).props(hide=True) - sinh).props(hide=True) / (reroute_4.o.output * reroute_4).props(label="z**2", hide=True)).props(hide=True)
                with g.Frame("Taylor expansion for small values"):
                    reroute_5 = g.Reroute(input=reroute_4.o.output).props(width=19.0)
                    math_2 = ((reroute_5.o.output / 3.0 + reroute_5.o.output ** 3.0 / 30.0).props(hide=True) + reroute_5.o.output ** 5.0 / 840.0).props(hide=True)
                switch = compare.switch.float(math_1, math_2)
            reroute_6 = g.Reroute(input=k).props(width=19.0)
            with g.Frame("f"):
                with g.Frame("Taylor expansion for small values"):
                    reroute_7 = g.Reroute(input=reroute_3.o.output).props(width=19.0)
                    math_3 = ((reroute_7.o.output + reroute_7.o.output ** 3.0 / 6.0).props(hide=True) + reroute_7.o.output ** 5.0 / 120.0).props(hide=True)
                math_4 = ((compare.switch.float(sinh, math_3) / reroute_3).props(hide=True) - reroute_6).props(hide=True)
            math_5 = (math_4 / switch).props(hide=True)
        math_6 = (reroute.o.output - math_5).props(width=152.55)
        with g.Frame():
            math_7 = (math_6 - reroute).props(width=100.0, hide=True)
        math_6 >> parameter_guess.next
        math_7 >> marching_step.next
        with g.Frame("Tolerence check"):
            compare_1 = (abs(marching_step.result).props(hide=True) < (10.0 ** reroute_1).props(hide=True)).props(hide=True)
            _warning = g.Warning.warning((~compare_1).props(hide=True), g.String("Did not Achieved Tolerance"))

        parameter_guess.result >> parameter
        compare_1 >> achieved_tolerance

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (378.65, -104.37), "Frame", (("Boolean", "Compare", "Result"), )),
            "Compare": ("FunctionNodeCompare", (207.25, -78.69), "Frame", (("A", "Math.005", "Value"), ("B", "Math.007", "Value"), )),
            "Compare.003": ("FunctionNodeCompare", (987.26, -757.71), "Frame.001", (("A", "Reroute.003", "Output"), )),
            "Frame": ("NodeFrame", (840.18, -164.29), None, ()),
            "Frame.001": ("NodeFrame", (-1885.66, 1723.87), None, ()),
            "Frame.002": ("NodeFrame", (30.18, -36.04), "Frame.006", ()),
            "Frame.003": ("NodeFrame", (184.64, -248.29), "Frame.004", ()),
            "Frame.004": ("NodeFrame", (151.23, -933.95), "Frame.001", ()),
            "Frame.005": ("NodeFrame", (255.18, -69.56), None, ()),
            "Frame.006": ("NodeFrame", (459.23, -36.04), "Frame.001", ()),
            "Group Input": ("NodeGroupInput", (-2806.52, 46.62), None, ()),
            "Group Output": ("NodeGroupOutput", (1914.61, -80.29), None, (("Achieved Tolerance", "Compare", "Result"), ("Parameter", "Repeat Output", "Parameter Guess"), )),
            "Group.002": ("GeometryNodeGroup", (278.19, -771.28), "Frame.001", (("Input", "Reroute.003", "Output"), )),
            "Group.003": ("GeometryNodeGroup", (135.64, -36.01), "Frame.004", (("Input", "Reroute.004", "Output"), )),
            "Math": ("ShaderNodeMath", (1710.52, -907.15), "Frame.001", (("Value", "Math.006", "Value"), ("Value#1", "Switch", "Output"), )),
            "Math.001": ("ShaderNodeMath", (94.59, 167.37), None, (("Value", "Reroute.001", "Output"), ("Value#1", "Math", "Value"), )),
            "Math.002": ("ShaderNodeMath", (977.65, -623.71), "Frame.006", (("Value", "Switch.001", "Output"), ("Value#1", "Reroute", "Output"), )),
            "Math.003": ("ShaderNodeMath", (530.0, -53.08), "Frame.004", (("Value", "Math.010", "Value"), ("Value#1", "Group.002", "Result"), )),
            "Math.004": ("ShaderNodeMath", (30.05, -34.12), "Frame.005", (("Value", "Math.001", "Value"), ("Value#1", "Reroute.001", "Output"), )),
            "Math.005": ("ShaderNodeMath", (35.65, -39.94), "Frame", (("Value", "Repeat Output", "Marching step"), )),
            "Math.006": ("ShaderNodeMath", (977.65, -661.5), "Frame.006", (("Value", "Math.002", "Value"), ("Value#1", "Reroute.005", "Output"), )),
            "Math.007": ("ShaderNodeMath", (30.01, -85.99), "Frame", (("Value#1", "Reroute.002", "Output"), )),
            "Math.008": ("ShaderNodeMath", (767.48, -190.46), "Frame.004", (("Value", "Math.003", "Value"), ("Value#1", "Math.009", "Value"), )),
            "Math.009": ("ShaderNodeMath", (143.41, -201.61), "Frame.004", (("Value", "Reroute.004", "Output"), ("Value#1", "Reroute.004", "Output"), )),
            "Math.010": ("ShaderNodeMath", (312.82, -132.77), "Frame.004", (("Value", "Group.003", "Result"), ("Value#1", "Reroute.004", "Output"), )),
            "Math.011": ("ShaderNodeMath", (518.37, -146.1), "Frame.002", (("Value", "Reroute.006", "Output"), ("Value#1", "Math.013", "Value"), )),
            "Math.012": ("ShaderNodeMath", (124.18, -38.19), "Frame.002", (("Value", "Reroute.006", "Output"), )),
            "Math.013": ("ShaderNodeMath", (291.25, -35.82), "Frame.002", (("Value", "Math.012", "Value"), )),
            "Math.014": ("ShaderNodeMath", (516.6, -179.87), "Frame.002", (("Value", "Math.011", "Value"), ("Value#1", "Math.015", "Value"), )),
            "Math.015": ("ShaderNodeMath", (282.96, -189.9), "Frame.002", (("Value", "Math.016", "Value"), )),
            "Math.016": ("ShaderNodeMath", (120.62, -195.83), "Frame.002", (("Value", "Reroute.006", "Output"), )),
            "Math.017": ("ShaderNodeMath", (488.68, -312.57), "Frame.003", (("Value", "Math.023", "Value"), ("Value#1", "Math.019", "Value"), )),
            "Math.018": ("ShaderNodeMath", (101.41, -190.12), "Frame.003", (("Value", "Reroute.007", "Output"), )),
            "Math.019": ("ShaderNodeMath", (257.41, -192.21), "Frame.003", (("Value", "Math.018", "Value"), )),
            "Math.020": ("ShaderNodeMath", (486.9, -346.35), "Frame.003", (("Value", "Math.017", "Value"), ("Value#1", "Math.022", "Value"), )),
            "Math.021": ("ShaderNodeMath", (97.85, -347.76), "Frame.003", (("Value", "Reroute.007", "Output"), )),
            "Math.022": ("ShaderNodeMath", (257.41, -348.27), "Frame.003", (("Value", "Math.021", "Value"), )),
            "Math.023": ("ShaderNodeMath", (257.41, -36.14), "Frame.003", (("Value", "Reroute.007", "Output"), )),
            "Repeat Input": ("GeometryNodeRepeatInput", (-2363.16, 11.65), None, (("Iterations", "Group Input", "Iterations"), ("Parameter Guess", "Group Input", "Initial Guess"), )),
            "Repeat Output": ("GeometryNodeRepeatOutput", (665.45, -9.43), None, (("Marching step", "Math.004", "Value"), ("Parameter Guess", "Math.001", "Value"), )),
            "Reroute": ("NodeReroute", (240.82, -685.92), "Frame.001", (("Input", "Reroute.003", "Output"), )),
            "Reroute.001": ("NodeReroute", (-57.18, -103.9), None, (("Input", "Repeat Input", "Parameter Guess"), )),
            "Reroute.002": ("NodeReroute", (-2166.08, -361.12), None, (("Input", "Group Input", "Tolerence Exponent"), )),
            "Reroute.003": ("NodeReroute", (61.39, -892.4), "Frame.001", (("Input", "Repeat Input", "Parameter Guess"), )),
            "Reroute.004": ("NodeReroute", (35.21, -160.16), "Frame.004", (("Input", "Reroute.003", "Output"), )),
            "Reroute.005": ("NodeReroute", (35.21, -728.55), "Frame.001", (("Input", "Group Input", "K"), )),
            "Reroute.006": ("NodeReroute", (35.21, -236.62), "Frame.002", (("Input", "Reroute", "Output"), )),
            "Reroute.007": ("NodeReroute", (35.21, -171.63), "Frame.003", (("Input", "Reroute.004", "Output"), )),
            "String": ("FunctionNodeInputString", (383.72, -153.9), "Frame", ()),
            "Switch": ("GeometryNodeSwitch", (1100.89, -107.83), "Frame.004", (("False", "Math.008", "Value"), ("Switch", "Compare.003", "Result"), ("True", "Math.020", "Value"), )),
            "Switch.001": ("GeometryNodeSwitch", (790.48, -428.19), "Frame.006", (("False", "Group.002", "Result"), ("Switch", "Compare.003", "Result"), ("True", "Math.014", "Value"), )),
            "Warning": ("GeometryNodeWarning", (599.73, -85.56), "Frame", (("Message", "String", "String"), ("Show", "Boolean Math", "Boolean"), )),
        }