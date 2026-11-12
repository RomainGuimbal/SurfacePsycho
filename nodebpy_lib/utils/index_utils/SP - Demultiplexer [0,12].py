from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPDemultiplexer012(CustomGeometryGroup):
    _name = "SP - Demultiplexer [0,12]"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_demultiplexer_0_12_", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), hide_value=True, subtype="XYZ")
        u_count = tree.inputs.integer("U Count", 0, min_value=0)
        v = tree.inputs.integer("V", 0, min_value=0)
        n_0 = tree.outputs.vector("0")
        n_1 = tree.outputs.vector("1")
        n_2 = tree.outputs.vector("2")
        n_3 = tree.outputs.vector("3")
        n_4 = tree.outputs.vector("4")
        n_5 = tree.outputs.vector("5")
        n_6 = tree.outputs.vector("6")
        n_7 = tree.outputs.vector("7")
        n_8 = tree.outputs.vector("8")
        n_9 = tree.outputs.vector("9")
        n_10 = tree.outputs.vector("10")
        n_11 = tree.outputs.vector("11")
        n_12 = tree.outputs.vector("12")

        integer_math = (u_count * v).props(hide=True)
        vector.point.at((integer_math + 0).props(mute=True)) >> n_0
        vector.point.at(integer_math + 1) >> n_1
        vector.point.at(integer_math + 2) >> n_2
        vector.point.at(integer_math + 3) >> n_3
        vector.point.at(integer_math + 4) >> n_4
        vector.point.at(integer_math + 5) >> n_5
        vector.point.at(integer_math + 6) >> n_6
        vector.point.at(integer_math + 7) >> n_7
        vector.point.at(integer_math + 8) >> n_8
        vector.point.at(integer_math + 9) >> n_9
        vector.point.at(integer_math + 10) >> n_10
        vector.point.at(integer_math + 11) >> n_11
        vector.point.at(integer_math + 12) >> n_12