from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPCyclicKnotWrap(CustomGeometryGroup):
    _name = "SP - Cyclic Knot Wrap"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 200, "node_tool_idname": "geometry.sp_cyclic_knot_wrap", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        knot = tree.inputs.float("Knot", 0.0)
        cp_count = tree.inputs.integer("CP Count", 0)
        wrapped_knot = tree.outputs.float("Wrapped Knot")

        _mesh_line = g.MeshLine(31)
        reroute = g.Reroute(input=knot).props(width=19.0)
        reroute_1 = g.Reroute(input=reroute.o.output).props(width=19.0)
        with g.Frame("Derivative"):
            evaluate_at_index = (reroute_1.o.output.point.at(g.Index().o.index + 1) - reroute_1).point.at(g.Index().o.index % cp_count)
        (
            (evaluate_at_index.point.trailing() + reroute.o.output.point.at().props(label="Last knot")).props(hide=True)
            >> wrapped_knot
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (651.4, -344.37), None, (("Value", "Evaluate at Index.001", "Value"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (539.05, -199.93), "Frame", (("Index", "Integer Math.004", "Value"), ("Value", "Reroute.001", "Output"), )),
            "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (900.26, -93.08), "Frame", (("Index", "Integer Math.010", "Value"), ("Value", "Math.001", "Value"), )),
            "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (-62.77, -515.63), None, (("Value", "Reroute.028", "Output"), )),
            "Frame": ("NodeFrame", (-481.24, -34.38), None, ()),
            "Group Input": ("NodeGroupInput", (-647.37, -499.47), None, ()),
            "Group Output": ("NodeGroupOutput", (1158.32, -575.49), None, (("Wrapped Knot", "Math.002", "Value"), )),
            "Index.001": ("GeometryNodeInputIndex", (29.94, -248.61), "Frame", ()),
            "Index.005": ("GeometryNodeInputIndex", (502.83, -81.55), "Frame", ()),
            "Integer Math.004": ("FunctionNodeIntegerMath", (203.29, -190.1), "Frame", (("Value", "Index.001", "Index"), )),
            "Integer Math.010": ("FunctionNodeIntegerMath", (688.59, -35.89), "Frame", (("Value", "Index.005", "Index"), ("Value#1", "Group Input", "CP Count"), )),
            "Math.001": ("ShaderNodeMath", (706.26, -171.5), "Frame", (("Value", "Evaluate at Index", "Value"), ("Value#1", "Reroute.001", "Output"), )),
            "Math.002": ("ShaderNodeMath", (845.16, -544.44), None, (("Value", "Accumulate Field", "Trailing"), ("Value#1", "Evaluate at Index.002", "Value"), )),
            "Mesh Line": ("GeometryNodeMeshLine", (651.08, 13.66), None, ()),
            "Reroute.001": ("NodeReroute", (23.5, -450.72), None, (("Input", "Reroute.028", "Output"), )),
            "Reroute.028": ("NodeReroute", (-231.41, -535.79), None, (("Input", "Group Input", "Knot"), )),
        }