from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPMergeToWireAndPreserveAttribute(CustomGeometryGroup):
    _name = "SP - Merge to Wire and Preserve Attribute"
    _color_tag = "ATTRIBUTE"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        wire_fragments = tree.inputs.geometry("Wire Fragments", description="Geometry whose instances are (partially) realized")
        distance = tree.inputs.float("Distance", 0.0001, min_value=0.0, subtype="DISTANCE")
        geometry = tree.outputs.geometry("Geometry")

        for_each = g.ForEachGeometryElementZone.instance(geometry=wire_fragments)
        geometry_1 = for_each.generated_items.geometry(name="Geometry")
        realize_instances = g.RealizeInstances(for_each.input.o.element)
        domain_size = g.DomainSize(realize_instances).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        store_named_attribute = g.StoreNamedAttribute.point.boolean(realize_instances, g.Compare.integer.equal(g.Index(), 0), "Endpoints", True).props(width=140.0)
        transfer_attributes = g.TransferAttributes(target=g.MeshLine(domain_size.o.point_count - 1).props(hide=True), source=store_named_attribute, attribute_names=g.GetAttributeNames(store_named_attribute).props(hide=True), pattern_mode="Exact")
        transfer_attributes >> geometry_1.input
        get_attribute_names = g.GetAttributeNames(geometry_1.output).props(hide=True)
        list_length = get_attribute_names.o.names.list_length()
        field_to_list = g.FieldToList(count=(list_length - 1).props(hide=True), items={"Value": get_attribute_names.o.names[g.Index()]})
        curve_to_mesh = ((g.RealizeInstances(wire_fragments) >> g.MergeByDistance(selection=g.VertexNeighbors().o.vertex_count <= 1, distance=distance) >> g.MeshToCurve()).props(hide=True) >> g.CurveToMesh()).props(hide=True)
        reroute = g.Reroute(input=curve_to_mesh.o.mesh).props(width=19.0)
        transfer_attributes_1 = g.TransferAttributes(target=reroute, source=geometry_1.output, attribute_names=field_to_list, pattern_mode="Exact")
        (
            (list_length > 0).props(hide=True).switch.geometry(reroute, transfer_attributes_1).props(hide=True)
            >> geometry
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Compare": ("FunctionNodeCompare", (-525.07, 874.26), None, (("A", "Vertex Neighbors", "Vertex Count"), )),
            "Compare.001": ("FunctionNodeCompare", (1495.06, 734.89), None, (("A", "List Length", "Length"), )),
            "Compare.003": ("FunctionNodeCompare", (-487.47, 388.44), None, (("A", "Index.001", "Index"), )),
            "Curve to Mesh": ("GeometryNodeCurveToMesh", (291.58, 800.9), None, (("Curve", "Mesh to Curve.004", "Curve"), )),
            "Domain Size": ("GeometryNodeAttributeDomainSize", (-369.23, 637.51), None, (("Geometry", "Realize Instances.003", "Geometry"), )),
            "Field to List": ("GeometryNodeFieldToList", (1274.52, 418.82), None, (("Count", "Integer Math", "Value"), ("Value", "Get List Item", "Value"), )),
            "For Each Geometry Element Input.003": ("GeometryNodeForeachGeometryElementInput", (-844.2, 559.49), None, (("Geometry", "Group Input", "Wire Fragments"), )),
            "For Each Geometry Element Output.003": ("GeometryNodeForeachGeometryElementOutput", (464.39, 570.56), None, (("Geometry", "Transfer Attributes.001", "Target"), )),
            "Get Attribute Names": ("GeometryNodeGetAttributeNames", (642.59, 376.82), None, (("Geometry", "For Each Geometry Element Output.003", "Geometry#1"), )),
            "Get Attribute Names.001": ("GeometryNodeGetAttributeNames", (-69.08, 358.29), None, (("Geometry", "Store Named Attribute.008", "Geometry"), )),
            "Get List Item": ("GeometryNodeListGetItem", (888.71, 411.68), None, (("Index", "Index.002", "Index"), ("List", "Get Attribute Names", "Names"), )),
            "Group Input": ("NodeGroupInput", (-1109.26, 644.35), None, ()),
            "Group Output": ("NodeGroupOutput", (1951.72, 653.97), None, (("Geometry", "Switch", "Output"), )),
            "Index.001": ("GeometryNodeInputIndex", (-673.61, 315.51), None, ()),
            "Index.002": ("GeometryNodeInputIndex", (646.22, 314.13), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (1082.62, 276.83), None, (("Value", "List Length", "Length"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-210.34, 650.87), None, (("Value", "Domain Size", "Point Count"), )),
            "List Length": ("GeometryNodeListLength", (885.31, 275.22), None, (("List", "Get Attribute Names", "Names"), )),
            "Merge by Distance.001": ("GeometryNodeMergeByDistance", (-166.35, 861.55), None, (("Distance", "Group Input", "Distance"), ("Geometry", "Realize Instances", "Geometry"), ("Selection", "Compare", "Result"), )),
            "Mesh Line": ("GeometryNodeMeshLine", (-30.69, 610.52), None, (("Count", "Integer Math.003", "Value"), )),
            "Mesh to Curve.004": ("GeometryNodeMeshToCurve", (129.9, 807.65), None, (("Mesh", "Merge by Distance.001", "Geometry"), )),
            "Realize Instances": ("GeometryNodeRealizeInstances", (-516.33, 1022.62), None, (("Geometry", "Group Input", "Wire Fragments"), )),
            "Realize Instances.003": ("GeometryNodeRealizeInstances", (-654.39, 518.54), None, (("Geometry", "For Each Geometry Element Input.003", "Element"), )),
            "Reroute": ("NodeReroute", (1342.31, 671.42), None, (("Input", "Curve to Mesh", "Mesh"), )),
            "Store Named Attribute.008": ("GeometryNodeStoreNamedAttribute", (-286.16, 487.05), None, (("Geometry", "Realize Instances.003", "Geometry"), ("Selection", "Compare.003", "Result"), )),
            "Switch": ("GeometryNodeSwitch", (1710.02, 684.34), None, (("False", "Reroute", "Output"), ("Switch", "Compare.001", "Result"), ("True", "Transfer Attributes", "Target"), )),
            "Transfer Attributes": ("GeometryNodeTransferAttributes", (1493.45, 658.22), None, (("Attribute Names", "Field to List", "Value"), ("Source", "For Each Geometry Element Output.003", "Geometry#1"), ("Target", "Reroute", "Output"), )),
            "Transfer Attributes.001": ("GeometryNodeTransferAttributes", (216.5, 562.92), None, (("Attribute Names", "Get Attribute Names.001", "Names"), ("Source", "Store Named Attribute.008", "Geometry"), ("Target", "Mesh Line", "Mesh"), )),
            "Vertex Neighbors": ("GeometryNodeInputMeshVertexNeighbors", (-688.69, 800.27), None, ()),
        }