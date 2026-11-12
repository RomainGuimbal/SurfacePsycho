from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPCyclicClampedUniformKnot(CustomGeometryGroup):
    _name = "SP - Cyclic-Clamped Uniform Knot"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_cyclic_clamped", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        p_count = tree.inputs.integer("P Count", 0, structure_type="SINGLE", force_non_field=True)
        degree = tree.inputs.integer("Degree", 0, structure_type="SINGLE", force_non_field=True)
        knot = tree.outputs.integer("Knot")

        index = g.Index()
        integer_math = g.IntegerMath(value=(index.o.index - degree).max(0).min(p_count - degree), value_001=index > 0)
        integer_math_1 = p_count + degree
        switch = g.Compare.integer.equal(index, integer_math_1).o.result.switch.integer(integer_math, integer_math.o.value + 1)
        (index > integer_math_1).switch.integer(switch) >> knot