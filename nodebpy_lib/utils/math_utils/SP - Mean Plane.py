from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPMeanPlane(CustomGeometryGroup):
    _name = "SP - Mean Plane"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.sp_mean_plane", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        offset = tree.outputs.vector("Offset")
        normal = tree.outputs.vector("Normal")

        domain_size = g.DomainSize(geometry).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        position = g.Position()
        reroute = g.Reroute(input=geometry).props(width=19.0)
        with g.Frame("Newell's Method"):
            reroute_1 = g.Reroute(input=position.o.position).props(label="Current", width=19.0)
            reroute_2 = g.Reroute(input=position.o.position.point.at((g.Index().o.index - 1) % domain_size.o.point_count)).props(label="Prev", width=19.0)
            vector = reroute_2.o.output - reroute_1
            vector_1 = reroute_2.o.output + reroute_1
            vector_math = g.CombineXYZ(x=vector.y, y=vector.z, z=vector.x).o.vector * g.CombineXYZ(x=vector_1.z, y=vector_1.x, z=vector_1.y)
            attribute_statistic = g.AttributeStatistic.point.vector(reroute, attribute=vector_math)
        attribute_statistic_1 = g.AttributeStatistic.point.vector(reroute, attribute=position)
        attribute_statistic.o.sum.normalize() >> normal

        attribute_statistic_1 >> offset

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Attribute Statistic.001": ("GeometryNodeAttributeStatistic", (1093.52, 472.01), None, (("Attribute", "Position", "Position"), ("Geometry", "Reroute.045", "Output"), )),
            "Attribute Statistic.002": ("GeometryNodeAttributeStatistic", (1587.85, -35.91), "Frame", (("Attribute", "Vector Math.001", "Vector"), ("Geometry", "Reroute.045", "Output"), )),
            "Combine XYZ": ("ShaderNodeCombineXYZ", (1178.19, -188.32), "Frame", (("X", "Separate XYZ", "Z"), ("Y", "Separate XYZ", "X"), ("Z", "Separate XYZ", "Y"), )),
            "Combine XYZ.001": ("ShaderNodeCombineXYZ", (1176.48, -60.07), "Frame", (("X", "Separate XYZ.001", "Y"), ("Y", "Separate XYZ.001", "Z"), ("Z", "Separate XYZ.001", "X"), )),
            "Domain Size": ("GeometryNodeAttributeDomainSize", (-596.23, 581.91), None, (("Geometry", "Group Input", "Geometry"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (503.53, -128.67), "Frame", (("Index", "Integer Math.001", "Value"), ("Value", "Position", "Position"), )),
            "Frame": ("NodeFrame", (-481.76, 1144.62), None, ()),
            "Group Input": ("NodeGroupInput", (-1005.64, 436.17), None, ()),
            "Group Output": ("NodeGroupOutput", (1536.65, 445.83), None, (("Normal", "Vector Math.004", "Vector"), ("Offset", "Attribute Statistic.001", "Mean"), )),
            "Index": ("GeometryNodeInputIndex", (30.15, -173.25), "Frame", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (194.6, -130.53), "Frame", (("Value", "Index", "Index"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (351.57, -127.72), "Frame", (("Value", "Integer Math", "Value"), ("Value#1", "Domain Size", "Point Count"), )),
            "Position": ("GeometryNodeInputPosition", (-265.36, 614.51), None, ()),
            "Reroute": ("NodeReroute", (720.7, -295.19), "Frame", (("Input", "Position", "Position"), )),
            "Reroute.001": ("NodeReroute", (721.85, -168.43), "Frame", (("Input", "Evaluate at Index", "Value"), )),
            "Reroute.045": ("NodeReroute", (908.8, 415.94), None, (("Input", "Group Input", "Geometry"), )),
            "Separate XYZ": ("ShaderNodeSeparateXYZ", (957.72, -191.15), "Frame", (("Vector", "Vector Math.003", "Vector"), )),
            "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (957.55, -64.65), "Frame", (("Vector", "Vector Math", "Vector"), )),
            "Vector Math": ("ShaderNodeVectorMath", (771.73, -63.52), "Frame", (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (1357.16, -87.4), "Frame", (("Vector", "Combine XYZ.001", "Vector"), ("Vector#1", "Combine XYZ", "Vector"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (765.38, -210.17), "Frame", (("Vector", "Reroute.001", "Output"), ("Vector#1", "Reroute", "Output"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (1364.17, 609.67), None, (("Vector", "Attribute Statistic.002", "Sum"), )),
        }