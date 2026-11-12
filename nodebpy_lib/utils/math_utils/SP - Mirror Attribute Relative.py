from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPMirrorAttributeRelative(CustomGeometryGroup):
    _name = "SP - Mirror Attribute Relative"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_mirror_attribute_relative", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        attribute = tree.inputs.vector("Attribute", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        axis = tree.inputs.menu("Axis", "X", optional_label=True)
        mirror_object = tree.inputs.object("Mirror Object")
        result = tree.outputs.vector("Result")

        menu_switch = g.MenuSwitch.vector(axis, {"X": (1.0, 0.0, 0.0), "Y": (0.0, 1.0, 0.0), "Z": (0.0, 0.0, 1.0)}).props(label="Axis")
        object_info = g.ObjectInfo(object=mirror_object, transform_space="RELATIVE")
        vector_math = (attribute - object_info.o.location).reflect(menu_switch.o.output.rotate(object_info.o.rotation))
        (vector_math + object_info.o.location).props(hide=True) >> result

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-509.39, 97.57), None, ()),
            "Group Output": ("NodeGroupOutput", (503.11, -11.1), None, (("Result", "Vector Math.006", "Vector"), )),
            "Menu Switch.001": ("GeometryNodeMenuSwitch", (-306.89, 122.32), None, (("Menu", "Group Input", "Axis"), )),
            "Object Info.005": ("GeometryNodeObjectInfo", (-306.89, -295.62), None, (("Object", "Group Input", "Mirror Object"), )),
            "Rotate Vector": ("FunctionNodeRotateVector", (-91.89, 106.79), None, (("Rotation", "Object Info.005", "Rotation"), ("Vector", "Menu Switch.001", "Output"), )),
            "Vector Math": ("ShaderNodeVectorMath", (98.11, 245.42), None, (("Vector", "Vector Math.007", "Vector"), ("Vector#1", "Rotate Vector", "Vector"), )),
            "Vector Math.006": ("ShaderNodeVectorMath", (313.11, -36.24), None, (("Vector", "Vector Math", "Vector"), ("Vector#1", "Object Info.005", "Location"), )),
            "Vector Math.007": ("ShaderNodeVectorMath", (-91.89, 280.14), None, (("Vector", "Group Input", "Attribute"), ("Vector#1", "Object Info.005", "Location"), )),
        }