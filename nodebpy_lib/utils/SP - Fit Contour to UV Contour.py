from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPFitContourToUVContour(CustomGeometryGroup):
    _name = "SP - Fit Contour to UV Contour"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry", description="Geometry to transform")
        geometry_1 = tree.outputs.geometry("Geometry")

        with g.Frame():
            transform_geometry = g.TransformGeometry(geometry=geometry, scale=(1.0, 1.0, 0.0)).props(width=140.0, hide=True)
            attribute_statistic = g.AttributeStatistic.point.vector(transform_geometry, attribute=g.Position()).props(hide_inputs=["Selection"], hide_outputs=["Mean", "Median", "Sum", "Max", "Standard Deviation", "Variance"])
            (
                (g.TransformGeometry(geometry=transform_geometry, translation=((0.0, 0.0, 0.0) - attribute_statistic.o.min).props(hide=True)).props(width=140.0) >> g.TransformGeometry(scale=((1.0, 1.0, 1.0) / attribute_statistic.o.range).props(hide=True))).props(width=140.0)
                >> geometry_1
            )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Attribute Statistic": ("GeometryNodeAttributeStatistic", (238.05, -164.25), "Frame", (("Attribute", "Position", "Position"), ("Geometry", "Transform Geometry.002", "Geometry"), )),
            "Frame": ("NodeFrame", (-406.59, 146.53), None, ()),
            "Group Input": ("NodeGroupInput", (-606.47, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (626.88, 0.0), None, (("Geometry", "Transform Geometry", "Geometry"), )),
            "Position": ("GeometryNodeInputPosition", (47.62, -287.98), "Frame", ()),
            "Transform Geometry": ("GeometryNodeTransform", (813.06, -96.94), "Frame", (("Geometry", "Transform Geometry.001", "Geometry"), ("Scale", "Vector Math", "Vector"), )),
            "Transform Geometry.001": ("GeometryNodeTransform", (625.37, -50.36), "Frame", (("Geometry", "Transform Geometry.002", "Geometry"), ("Translation", "Vector Math.003", "Vector"), )),
            "Transform Geometry.002": ("GeometryNodeTransform", (30.07, -143.81), "Frame", (("Geometry", "Group Input", "Geometry"), )),
            "Vector Math": ("ShaderNodeVectorMath", (420.62, -292.82), "Frame", (("Vector#1", "Attribute Statistic", "Range"), )),
            "Vector Math.003": ("ShaderNodeVectorMath", (421.27, -250.89), "Frame", (("Vector#1", "Attribute Statistic", "Min"), )),
        }