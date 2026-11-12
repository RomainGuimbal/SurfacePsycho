from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class ListArgmax(CustomGeometryGroup):
    _name = "List Argmax"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.argmax", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        attribute = tree.inputs.float("Attribute", 0.0, structure_type="LIST")
        argmax = tree.outputs.integer("Argmax")
        value = tree.outputs.float("Value")

        list_length = attribute.list_length()
        sort_list = g.FieldToList(count=list_length, items={"Index": g.Index()}).o.index.sort(attribute)
        get_list_item = sort_list[(list_length - 1).props(hide=True)]
        attribute[get_list_item] >> value
        viewer = g.Viewer()
        viewer.items.integer(sort_list, "List")

        get_list_item >> argmax

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Field to List": ("GeometryNodeFieldToList", (646.08, 234.82), None, (("Count", "List Length", "Length"), ("Index", "Index", "Index"), )),
            "Get List Item": ("GeometryNodeListGetItem", (1217.18, 146.19), None, (("Index", "Get List Item.001", "Value"), ("List", "Group Input", "Attribute"), )),
            "Get List Item.001": ("GeometryNodeListGetItem", (1019.07, 200.88), None, (("Index", "Integer Math", "Value"), ("List", "Sort List", "List"), )),
            "Group Input": ("NodeGroupInput", (201.49, 95.98), None, ()),
            "Group Output": ("NodeGroupOutput", (1404.67, 220.7), None, (("Argmax", "Get List Item.001", "Value"), ("Value", "Get List Item", "Value"), )),
            "Index": ("GeometryNodeInputIndex", (431.19, 167.1), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (863.75, -14.78), None, (("Value", "List Length", "Length"), )),
            "List Length": ("GeometryNodeListLength", (433.16, 275.06), None, (("List", "Group Input", "Attribute"), )),
            "Sort List": ("GeometryNodeSortList", (853.32, 221.22), None, (("List", "Field to List", "Index"), ("Sort Weight", "Group Input", "Attribute"), )),
            "Viewer": ("GeometryNodeViewer", (1014.59, 326.59), None, (("List", "Sort List", "List"), )),
        }