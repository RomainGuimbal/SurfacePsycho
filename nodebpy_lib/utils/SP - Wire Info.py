from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPWireInfo(CustomGeometryGroup):
    _name = "SP - Wire Info"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_wire_info", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        is_closed = tree.inputs.boolean("Is Closed", False, structure_type="SINGLE", force_non_field=True)
        segment_index = tree.outputs.integer("Segment Index", attribute_domain="EDGE")
        segment_count = tree.outputs.integer("Segment Count")
        is_endpoint = tree.outputs.boolean("Is Endpoint")
        is_chain_end = tree.outputs.boolean("Is Chain End")
        index_of_first_point = tree.outputs.integer("Index of First Point", description="Wrong on unprepared wires")
        unclamped_periodic = tree.outputs.boolean("Unclamped periodic")

        boolean_math = (~is_closed).props(hide=True)
        with g.Frame("endpoints"):
            named_attribute = g.NamedAttribute.boolean("Endpoints")
            compare = g.Compare.integer.equal(g.VertexNeighbors().props(hide_outputs=["Face Count"]).o.vertex_count, 1).props(width=100.0, hide=True)
            boolean_math_1 = (named_attribute.o.attribute | compare).props(width=100.0, hide=True)
        accumulate_field = g.AccumulateField.point.integer(boolean_math_1)
        with g.Frame():
            evaluate_on_domain = accumulate_field.o.trailing.point.at(g.Index().o.index + 1).edge.evaluate()
            switch = g.Compare.integer.equal(evaluate_on_domain, 0).o.result.switch.integer(evaluate_on_domain, accumulate_field.o.total.edge.evaluate())
            integer_math = switch - 1
        with g.Frame():
            accumulate_field_1 = g.AccumulateField.point.integer(((~compare.o.result).props(hide=True) & named_attribute.o.attribute).props(hide=True))
            (
                boolean_math.switch.integer(g.AccumulateField.point.integer(accumulate_field_1.o.leading <= 0).o.total)
                >> index_of_first_point
            )
        with g.Frame("Closed and no endpoints : unclamped periodic"):
            (
                (g.Compare.integer.equal(accumulate_field.o.total, 0).o.result & is_closed)
                >> unclamped_periodic
            )
        with g.Frame("seg count"):
            integer_math_1 = g.IntegerMath.subtract(accumulate_field.o.total, boolean_math)
            evaluate_on_domain_1 = integer_math_1.o.value.edge.evaluate()
            integer_math_1.o.value.max(1) >> segment_count
        (
            is_closed.switch.integer(integer_math, integer_math % evaluate_on_domain_1)
            >> segment_index
        )

        boolean_math_1 >> is_endpoint
        compare >> is_chain_end

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Accumulate Field": ("GeometryNodeAccumulateField", (-104.84, 115.71), None, (("Value", "Boolean Math", "Boolean"), )),
            "Accumulate Field.001": ("GeometryNodeAccumulateField", (203.58, -58.89), "Frame", (("Value", "Boolean Math.004", "Boolean"), )),
            "Accumulate Field.002": ("GeometryNodeAccumulateField", (523.85, -51.64), "Frame", (("Value", "Compare.003", "Result"), )),
            "Boolean Math": ("FunctionNodeBooleanMath", (335.2, -149.7), "Frame.002", (("Boolean", "Named Attribute.001", "Attribute"), ("Boolean#1", "Compare.001", "Result"), )),
            "Boolean Math.001": ("FunctionNodeBooleanMath", (217.49, -89.15), "Frame.004", (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Group Input", "Is Closed"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (354.87, -593.99), None, (("Boolean", "Group Input", "Is Closed"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (30.22, -162.26), "Frame", (("Boolean", "Boolean Math.005", "Boolean"), ("Boolean#1", "Named Attribute.001", "Attribute"), )),
            "Boolean Math.005": ("FunctionNodeBooleanMath", (36.47, -124.98), "Frame", (("Boolean", "Compare.001", "Result"), )),
            "Compare.001": ("FunctionNodeCompare", (210.55, -181.23), "Frame.002", (("A", "Vertex Neighbors", "Vertex Count"), )),
            "Compare.002": ("FunctionNodeCompare", (736.97, -30.18), "Frame.003", (("A", "Evaluate on Domain.002", "Value"), )),
            "Compare.003": ("FunctionNodeCompare", (364.14, -53.73), "Frame", (("A", "Accumulate Field.001", "Leading"), )),
            "Compare.004": ("FunctionNodeCompare", (30.1, -35.89), "Frame.004", (("A", "Accumulate Field", "Total"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (393.14, -132.27), "Frame.003", (("Index", "Integer Math", "Value"), ("Value", "Accumulate Field", "Trailing"), )),
            "Evaluate on Domain.002": ("GeometryNodeFieldOnDomain", (549.59, -142.41), "Frame.003", (("Value", "Evaluate at Index", "Value"), )),
            "Evaluate on Domain.003": ("GeometryNodeFieldOnDomain", (723.56, -204.52), "Frame.003", (("Value", "Accumulate Field", "Total"), )),
            "Evaluate on Domain.004": ("GeometryNodeFieldOnDomain", (233.11, -36.06), "Frame.001", (("Value", "Integer Math.001", "Value"), )),
            "Frame": ("NodeFrame", (333.0, -720.53), None, ()),
            "Frame.001": ("NodeFrame", (643.76, -323.96), None, ()),
            "Frame.002": ("NodeFrame", (-630.53, 46.09), None, ()),
            "Frame.003": ("NodeFrame", (-12.71, 531.53), None, ()),
            "Frame.004": ("NodeFrame", (474.88, 136.62), None, ()),
            "Group Input": ("NodeGroupInput", (-599.78, -442.89), None, ()),
            "Group Output": ("NodeGroupOutput", (1972.57, -152.38), None, (("Index of First Point", "Switch.002", "Output"), ("Is Chain End", "Compare.001", "Result"), ("Is Endpoint", "Boolean Math", "Boolean"), ("Segment Count", "Integer Math.002", "Value"), ("Segment Index", "Switch", "Output"), ("Unclamped periodic", "Boolean Math.001", "Boolean"), )),
            "Index": ("GeometryNodeInputIndex", (30.2, -114.85), "Frame.003", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (222.69, -134.19), "Frame.003", (("Value", "Index", "Index"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (30.07, -127.92), "Frame.001", (("Value", "Accumulate Field", "Total"), ("Value#1", "Boolean Math.002", "Boolean"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (232.94, -146.63), "Frame.001", (("Value", "Integer Math.001", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (1328.56, 84.06), None, (("Value", "Integer Math.004", "Value"), ("Value#1", "Evaluate on Domain.004", "Value"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (1077.93, -93.4), "Frame.003", (("Value", "Switch.001", "Output"), )),
            "Named Attribute.001": ("GeometryNodeInputNamedAttribute", (40.83, -35.87), "Frame.002", ()),
            "Switch": ("GeometryNodeSwitch", (1680.68, 54.25), None, (("False", "Integer Math.004", "Value"), ("Switch", "Group Input", "Is Closed"), ("True", "Integer Math.003", "Value"), )),
            "Switch.001": ("GeometryNodeSwitch", (912.46, -81.48), "Frame.003", (("False", "Evaluate on Domain.002", "Value"), ("Switch", "Compare.002", "Result"), ("True", "Evaluate on Domain.003", "Value"), )),
            "Switch.002": ("GeometryNodeSwitch", (685.01, -30.38), "Frame", (("False", "Accumulate Field.002", "Total"), ("Switch", "Boolean Math.002", "Boolean"), )),
            "Vertex Neighbors": ("GeometryNodeInputMeshVertexNeighbors", (30.32, -166.71), "Frame.002", ()),
        }