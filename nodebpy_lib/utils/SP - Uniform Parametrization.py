from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPUniformParametrization(CustomGeometryGroup):
    _name = "SP - Uniform Parametrization"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_uniform_parametrization", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.geometry("Input")
        value = tree.outputs.float("Value")

        index = g.Index()
        reroute = g.Reroute(input=input).props(width=19.0)
        domain_size = g.DomainSize(reroute).props(hide=True, hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        sample_index = g.SampleIndex.point.float(reroute, (index.o.index / (domain_size.o.point_count - 1).props(hide=True)).props(hide=True), index).props(hide=True)

        sample_index >> value

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Domain Size": ("GeometryNodeAttributeDomainSize", (-204.78, -4.67), None, (("Geometry", "Reroute.001", "Output"), )),
            "Group Input": ("NodeGroupInput", (-451.71, -14.38), None, ()),
            "Group Output": ("NodeGroupOutput", (481.85, -13.11), None, (("Value", "Sample Index", "Value"), )),
            "Index": ("GeometryNodeInputIndex", (-41.77, 66.34), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (-41.01, -3.89), None, (("Value", "Domain Size", "Point Count"), )),
            "Math": ("ShaderNodeMath", (135.7, 8.28), None, (("Value", "Index", "Index"), ("Value#1", "Integer Math", "Value"), )),
            "Reroute.001": ("NodeReroute", (-243.43, -45.51), None, (("Input", "Group Input", "Input"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (298.02, -44.27), None, (("Geometry", "Reroute.001", "Output"), ("Index", "Index", "Index"), ("Value", "Math", "Value"), )),
        }