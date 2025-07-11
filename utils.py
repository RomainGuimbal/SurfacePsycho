import bpy

# import bmesh
import numpy as np
from mathutils import Vector, Matrix, Quaternion
import math
from math import isclose
from typing import List, Tuple
from os.path import dirname, abspath, join
from enum import Enum
from dataclasses import dataclass
import dataclasses
import re

from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import (
    GeomAbs_Plane,
    GeomAbs_Cylinder,
    GeomAbs_Cone,
    GeomAbs_Sphere,
    GeomAbs_Torus,
    GeomAbs_BezierSurface,
    GeomAbs_BSplineSurface,
    GeomAbs_SurfaceOfRevolution,
    GeomAbs_SurfaceOfExtrusion,
    GeomAbs_OffsetSurface,
    GeomAbs_OtherSurface,
)
from OCP.GeomAdaptor import GeomAdaptor_Curve
from OCP.TopAbs import TopAbs_FORWARD, TopAbs_EDGE, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import (
    TopoDS,
    TopoDS_Wire,
    TopoDS_Edge,
    TopoDS_Face,
    TopoDS_Shape,
    TopoDS_Compound,
    TopoDS_Iterator,
    TopoDS_Shell,
    TopoDS_Solid,
)
from OCP.TColStd import TColStd_Array1OfReal
from OCP.gp import (
    gp_Pnt,
    gp_Quaternion,
    gp_Dir,
    gp_Pln,
    gp_Trsf,
    gp_Ax1,
    gp_Ax2,
    gp_Circ,
    gp_Ax2d,
    gp_Pnt2d,
    gp_Trsf,
    gp_Circ2d,
    gp_Dir2d,
    gp_Vec,
)
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array2OfPnt
from OCP.TColStd import (
    TColStd_Array1OfInteger,
    TColStd_Array1OfReal,
    TColStd_HArray1OfReal,
    TColStd_HArray1OfInteger,
)
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorGen
from OCP.Quantity import Quantity_Color
from OCP.BRepCheck import BRepCheck_Analyzer
import OCP.TopAbs as TopAbs
import OCP.GeomAbs as GeomAbs

addonpath = dirname(abspath(__file__))  # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"


class SP_obj_type(Enum):
    PLANE = 0
    CYLINDER = 1
    CONE = 2
    SPHERE = 3
    TORUS = 4
    BEZIER_SURFACE = 5
    BSPLINE_SURFACE = 6
    SURFACE_OF_REVOLUTION = 7
    SURFACE_OF_EXTRUSION = 8
    OFFSET_SURFACE = 9
    OTHER_SURFACE = 10
    INSTANCE = 11
    EMPTY = 12
    CURVE = 13
    COMPOUND = 14


TYPES_FROM_CP_ATTR = {
    "CP_any_order_surf": SP_obj_type.BEZIER_SURFACE,
    "CP_NURBS_surf": SP_obj_type.BSPLINE_SURFACE,
    "CP_planar": SP_obj_type.PLANE,
    "CP_curve": SP_obj_type.CURVE,
    "axis3_cylinder": SP_obj_type.CYLINDER,
    "axis3_torus": SP_obj_type.TORUS,
    "axis3_cone": SP_obj_type.CONE,
    "axis3_sphere": SP_obj_type.SPHERE,
    "CP_swept_surf": SP_obj_type.SURFACE_OF_EXTRUSION,
    "CP_revolution_surf": SP_obj_type.SURFACE_OF_REVOLUTION,
}

geom_to_sp_type = {
    GeomAbs_Plane: SP_obj_type.PLANE,
    GeomAbs_Cylinder: SP_obj_type.CYLINDER,
    GeomAbs_Cone: SP_obj_type.CONE,
    GeomAbs_Sphere: SP_obj_type.SPHERE,
    GeomAbs_Torus: SP_obj_type.TORUS,
    GeomAbs_BezierSurface: SP_obj_type.BEZIER_SURFACE,
    GeomAbs_BSplineSurface: SP_obj_type.BSPLINE_SURFACE,
    GeomAbs_SurfaceOfRevolution: SP_obj_type.SURFACE_OF_REVOLUTION,
    GeomAbs_SurfaceOfExtrusion: SP_obj_type.SURFACE_OF_EXTRUSION,
    GeomAbs_OffsetSurface: SP_obj_type.OFFSET_SURFACE,
    GeomAbs_OtherSurface: SP_obj_type.OTHER_SURFACE,
}


# to replace with official index
class SP_segment_type(Enum):
    BEZIER = 0
    NURBS = 1
    CIRCLE_ARC = 2
    CIRCLE = 3
    ELLIPSE_ARC = 4
    ELLIPSE = 5


def get_face_sp_type(TopoDSface: TopoDS_Face):
    adapt_surf = BRepAdaptor_Surface(TopoDSface)
    surface_type = adapt_surf.GetType()
    return geom_to_sp_type.get(surface_type, f"Unknown type: {surface_type}")


def sp_type_of_object(o: bpy.types.Object, context: bpy.types.Context) -> SP_obj_type:
    if o.type == "EMPTY":
        if o.instance_collection != None:
            return SP_obj_type.INSTANCE
        else:
            return SP_obj_type.EMPTY

    for m in o.modifiers:
        if m.type == "NODES" and m.node_group:
            if m.node_group.name == "SP - Compound Meshing":
                return SP_obj_type.COMPOUND

    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    if hasattr(ob.data, "attributes"):
        for k in TYPES_FROM_CP_ATTR.keys():
            if k in ob.data.attributes.keys():
                return TYPES_FROM_CP_ATTR[k]

    return None


def read_attribute_by_name(object, name, len_attr=None):
    att = object.data.attributes[name]
    type = att.data_type
    match type:
        case "BOOLEAN":
            len_raw = len(att.data)
            if len_attr == None:
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = [bool(a) for a in attribute]

        case "INT":
            len_raw = len(att.data)
            if len_attr == None:
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = [int(a) for a in attribute]

        case "FLOAT":
            len_raw = len(att.data)
            if len_attr == None:
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]

        case "FLOAT_VECTOR":
            len_raw = len(att.data)
            if len_attr == None:
                len_attr = len_raw
            attribute = np.empty(3 * len_raw)
            att.data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]

        case "FLOAT2":
            len_raw = len(att.data)
            if len_attr == None:
                len_attr = len_raw
            attribute = np.empty(2 * len_raw)
            att.data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 2))[0:len_attr]

        case _:
            raise Exception(f"Unknown attribute type: {type}")

    return attribute


def append_object_by_name(obj_name, context):  # for importing from the asset file
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name == obj_name]

    cursor_loc = context.scene.cursor.location

    o = data_to.objects[0]
    if o is not None:
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        context.collection.objects.link(o)
        o.location = cursor_loc
        o.asset_clear()
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        # Iterate through all objects and their geometry node modifiers
        for mod in o.modifiers:
            if mod.type == "NODES" and mod.node_group:
                mod.node_group.asset_clear()


def classify_strings_by_prefix(strings):
    import re

    strings.sort()
    object_dict = {}
    for string in strings:
        # Use regex to extract the common prefix
        match = re.match(r"(\D+)(\d*.*)", string)
        if match:
            prefix = match.group(1)
            if prefix not in object_dict:
                object_dict[prefix] = [string]
            else:
                object_dict[prefix].append(string)
    return object_dict


def highest_suffix_of_each_object_name(names):
    classified_objects = classify_strings_by_prefix(names)
    last_string = []
    for key, value in classified_objects.items():
        if value:
            last_string += [value[-1]]
    return last_string


def create_grid(vertices):
    n, m = np.shape(vertices)
    vertices_flat = vertices.reshape(-1)
    return (
        vertices_flat,
        [],
        [(i, i + 1, i + m + 1, i + m) for i in range((n - 1) * m) if (i + 1) % m != 0],
    )


def change_node_socket_value(
    ob: bpy.types.Object, value, potential_names, socket_type, context
):
    for m in ob.modifiers:
        if m.type == "NODES" and m.node_group.name[:5] == "SP - ":
            for it in m.node_group.interface.items_tree:
                if it.name in potential_names and it.socket_type == socket_type:
                    input_id = it.identifier
                    m[input_id] = value
                    m.node_group.interface_update(context)


def change_GN_modifier_settings(modifier, settings_dict):
    for key, value in settings_dict.items():
        try:
            id = modifier.node_group.interface.items_tree[key].identifier
            modifier[id] = value
        except Exception:
            raise Exception("Modifier settings failed to apply")


def add_vertex_group(object: bpy.types.Object, name, values):
    if name not in object.vertex_groups:
        object.vertex_groups.new(name=name)
    vg = object.vertex_groups[name]

    if len(object.data.vertices) < len(values):
        print(f"Error : {len(values)} values on {len(object.data.vertices)} vertices")
        return False

    for i, v in enumerate(values):
        if v > 1.0:
            v = 1
            print("Warning : vertex group value clamped to 1")
        object.data.vertices
        if v != 0.0:
            vg.add([i], v, "ADD")

    return True


def add_float_attribute(object: bpy.types.Object, name, values, fallback_value=0.0):
    if name not in object.data.attributes:
        object.data.attributes.new(name=name, type="FLOAT", domain="POINT")
        object.data.update()

    length_diff = len(object.data.vertices) - len(values)
    att = object.data.attributes[name]

    if length_diff == 0:
        att.data.foreach_set("value", values)
    elif length_diff > 0:
        values.extend([fallback_value] * length_diff)
        att.data.foreach_set("value", values)
    elif length_diff < 0:
        print(f"Error : {len(values)} values on {len(object.data.vertices)} vertices")
        return False

    return True


def add_int_attribute(object: bpy.types.Object, name, values, fallback_value=0):
    if name not in object.data.attributes:
        object.data.attributes.new(name=name, type="INT", domain="POINT")
        object.data.update()

    length_diff = len(object.data.vertices) - len(values)
    att = object.data.attributes[name]

    if length_diff == 0:
        att.data.foreach_set("value", values)
    elif length_diff > 0:
        values.extend([fallback_value] * length_diff)
        att.data.foreach_set("value", values)
    elif length_diff < 0:
        print(f"Error : {len(values)} values on {len(object.data.vertices)} vertices")
        return False

    return True


def add_bool_attribute(object: bpy.types.Object, name, values, fallback_value=False):
    if name not in object.data.attributes:
        object.data.attributes.new(name=name, type="BOOLEAN", domain="POINT")
        object.data.update()

    length_diff = len(object.data.vertices) - len(values)
    att = object.data.attributes[name]

    if length_diff == 0:
        att.data.foreach_set("value", values)
    elif length_diff > 0:
        values.extend([fallback_value] * length_diff)
        att.data.foreach_set("value", values)
    elif length_diff < 0:
        print(f"Error : {len(values)} values on {len(object.data.vertices)} vertices")
        return False

    return True


def set_attribute(context, att_name, value, fallback_type):
    objs = context.objects_in_mode
    for o in objs:
        # Switch to object mode
        bpy.ops.object.mode_set(mode="OBJECT")

        if att_name not in o.data.attributes:
            o.data.attributes.new(name=att_name, type=fallback_type, domain="POINT")
            o.data.update()

        # Get attribute
        att = o.data.attributes[att_name]

        # Init values (To complete for vectors if needed)
        if att.data_type == "BOOLEAN":
            values = [False] * len(o.data.vertices)
        elif att.data_type == "FLOAT":
            values = [0.0] * len(o.data.vertices)
        elif att.data_type == "INT":
            values = [0] * len(o.data.vertices)

        # Fill with existing values
        att.data.foreach_get("value", values)

        # Update values
        for i, v in enumerate(o.data.vertices):
            if v.select:
                values[i] = value
                # To improve one day to change all verts between endpoints

        # Set new
        att.data.foreach_set("value", values)

        bpy.ops.object.mode_set(mode="EDIT")
    return True


def set_segment_type(context, type):
    return set_attribute(context, "Type", type, "INT")


def toggle_bool_attribute(o, att_name):
    bpy.ops.object.mode_set(mode="OBJECT")

    # Get attribute
    att = o.data.attributes[att_name]
    if att.data_type != "BOOLEAN":
        bpy.ops.object.mode_set(mode="EDIT")
        return False

    # Init values
    values = [False] * len(o.data.vertices)

    # Fill with existing values
    att.data.foreach_get("value", values)

    # Make values the opposite of first found value
    value = None
    for i, v in enumerate(o.data.vertices):
        if v.select:
            if value == None:
                value = not values[i]
            values[i] = value

    # Set new
    att.data.foreach_set("value", values)

    bpy.ops.object.mode_set(mode="EDIT")
    return True


def toggle_pseudo_bool_attribute(o, att_name):
    # Get attribute
    bpy.ops.object.mode_set(mode="OBJECT")
    att = o.data.attributes[att_name]

    # Init values
    data_type = att.data_type
    if data_type not in ["FLOAT", "INT"]:
        bpy.ops.object.mode_set(mode="EDIT")
        return False

    if data_type == "FLOAT":
        values = [0.0] * len(o.data.vertices)
    elif data_type == "INT":
        values = [0] * len(o.data.vertices)

    # Fill values with existing values
    att.data.foreach_get("value", values)

    # Update values
    value = None
    for i, v in enumerate(o.data.vertices):
        if v.select:
            if value == None:
                if data_type == "FLOAT":
                    value = 1.0 if values[i] <= 0.6 else 0.0
                elif data_type == "INT":
                    value = 1 if values[i] <= 0.6 else 0

            values[i] = value

    # Set new
    att.data.foreach_set("value", values)

    bpy.ops.object.mode_set(mode="EDIT")
    return True


def toggle_pseudo_bool_vertex_group(o, vg_name):
    bpy.ops.object.mode_set(mode="OBJECT")
    vg = o.vertex_groups[vg_name]

    # Toggle selected vertices of the vertex group
    for v in o.data.vertices:
        if v.select:
            try:
                # keep old behaviour because timesaver
                if vg.weight(v.index) > 0.6:
                    vg.remove([v.index])
                else:
                    vg.add([v.index], 1.0, "REPLACE")
            except RuntimeError:
                vg.add([v.index], 1.0, "REPLACE")

    bpy.ops.object.mode_set(mode="EDIT")
    return True


def tcolstd_array1_to_list(array):
    # Check if it's a handle and extract the array
    if isinstance(array, TColStd_HArray1OfReal) or isinstance(
        array, TColStd_HArray1OfInteger
    ):
        return list(array)
    else:
        return [array.Value(i) for i in range(array.Lower(), array.Upper() + 1)]


def gp_list_to_arrayofpnt(array: list):
    tcol = TColgp_Array1OfPnt(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, gp_Pnt(array[i].X(), array[i].Y(), array[i].Z()))
    return tcol


def float_list_to_tcolstd(array: list):
    tcol = TColStd_Array1OfReal(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, array[i])
    return tcol


def vec_list_to_gp_pnt2d(array: list):
    tcol = TColgp_Array1OfPnt2d(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, gp_Pnt2d(array[i][0], array[i][1]))
    return tcol


def vec_list_to_gp_pnt(array: list):
    tcol = TColgp_Array1OfPnt(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, gp_Pnt(array[i][0], array[i][1], array[i][2]))
    return tcol


def blender_to_gp_vec(vec: Vector):
    return gp_Vec(vec.x, vec.y, vec.z)


def gp_pnt_to_blender_vec(vec: gp_Pnt):
    return Vector((vec.X(), vec.Y(), vec.Z()))


def gp_pnt2d_to_blender_vec(vec: gp_Pnt2d):
    return Vector((vec.X(), vec.Y(), 0))


def gp_pnt_to_blender_vec_list(vecs: list[gp_Pnt]) -> list[Vector]:
    try:
        res = [Vector((vec.X(), vec.Y(), vec.Z())) for vec in vecs]
    except Exception:
        res = [Vector((vec.X(), vec.Y(), 0)) for vec in vecs]
    return res


# def gp_pnt2d_to_blender_vec_list(vecs: list):
#     return [Vector((vec.X(), vec.Y(), 0)) for vec in vecs]


def normalize_array(array):
    mini = min(array)
    return ((np.array(array) - mini) / (max(array) - mini)).tolist()


def list_geometry_node_groups():
    geometry_node_groups = []

    for node_group in bpy.data.node_groups:
        if node_group.type == "GEOMETRY":
            geometry_node_groups.append(node_group.name)
    return geometry_node_groups


def append_node_group(asset_name, force=False):
    # check if asset is already imported
    if force:
        asset_already = False
    else:
        groups_list = list_geometry_node_groups()
        asset_already = asset_name in groups_list

    # if not, import
    if not asset_already:
        # Load the asset file
        with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
            # Find the node group in the file
            if asset_name in data_from.node_groups:
                data_to.node_groups = [asset_name]
                return True
            else:
                print(f"Asset '{asset_name}' not found")
                return False


def append_multiple_node_groups(ng_names: set):
    # Get the current node group names
    existing_node_groups = set(bpy.data.node_groups.keys())

    # Append the new node groups
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        # Filter the node groups that exist in the asset file
        valid_node_groups = [name for name in ng_names if name in data_from.node_groups]

        # Append the valid node groups
        data_to.node_groups = valid_node_groups

    # Find the newly added node groups
    new_node_groups = []
    new_node_groups_keys = set(bpy.data.node_groups.keys()) - existing_node_groups
    for k in new_node_groups_keys:
        new_node_groups.append(bpy.data.node_groups[k])

    # return new_node_groups


def add_node_group_modifier_from_asset(
    obj, asset_name, settings_dict={}, pin=False, add_mode=False
):
    if add_mode:
        append_node_group(asset_name)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=asset_name, type="NODES")
    modifier.node_group = bpy.data.node_groups.get(asset_name)
    modifier.use_pin_to_last = pin

    # Change settings
    change_GN_modifier_settings(modifier, settings_dict)


def add_sp_modifier(ob, name: str, settings_dict={}, pin=False, add_mode=False):
    add_node_group_modifier_from_asset(
        ob, name, settings_dict, pin=pin, add_mode=add_mode
    )


def join_mesh_entities(verts1, edges1, faces1, verts2, edges2, faces2):
    len1 = len(verts1)
    verts3 = verts1.copy()
    verts3.extend(verts2)
    edges3 = edges1.copy()
    edges3.extend([(e[0] + len1, e[1] + len1) for e in edges2])
    faces3 = faces1.copy()
    faces3.extend([[i + len1 for i in f] for f in faces2])

    return verts3, edges3, faces3


def flatten_list_of_lists(list_of_lists):
    flat_list = []
    for row in list_of_lists:
        flat_list.extend(row)
    return flat_list


def get_wires_from_face(face: TopoDS_Face):
    wires = []
    explorer = TopExp_Explorer(face, TopAbs_WIRE)
    while explorer.More():
        wire = explorer.Current()
        # wire = TopoDS_Wire.Cast(explorer.Current())
        if wire.ShapeType() == TopAbs_WIRE and wire.Closed():
            wires.append(wire)
        explorer.Next()
    return wires


def get_edges_from_wire(wire: TopoDS_Wire) -> List[TopoDS_Edge]:
    edges = []
    explorer = TopExp_Explorer(wire, TopAbs_EDGE)

    while explorer.More():
        edge = explorer.Current()
        if edge.ShapeType() == TopAbs_EDGE:
            edges.append(TopoDS.Edge_s(edge))
        explorer.Next()

    return edges


def get_shape_transform(shape, scale=1):
    gp_trsf = shape.Location().Transformation()
    matrix = gp_trsf_to_blender_matrix(gp_trsf, scale)
    return matrix


def gp_trsf_to_blender_matrix(gp_trsf, scale=1):
    matrix = Matrix()
    for i in range(3):  # row
        for j in range(4):  # col
            if j == 3:
                matrix[i][j] = gp_trsf.Value(i + 1, j + 1) * scale
            else:
                matrix[i][j] = gp_trsf.Value(i + 1, j + 1)
    return matrix


def blender_matrix_to_gp_trsf(mat: Matrix, scale=1):
    gp_trsf = gp_Trsf()
    gp_trsf.SetValues(
        mat[0][0],
        mat[0][1],
        mat[0][2],
        mat[0][3] * scale,
        mat[1][0],
        mat[1][1],
        mat[1][2],
        mat[1][3] * scale,
        mat[2][0],
        mat[2][1],
        mat[2][2],
        mat[2][3] * scale,
    )
    return gp_trsf


# def get_scale_of_transform_matrix(mat : Matrix):
#     x = math.sqrt(mat[0][0]**2 + mat[0][1]**2 + mat[0][2]**2)
#     y = math.sqrt(mat[1][0]**2 + mat[1][1]**2 + mat[1][2]**2)
#     z = math.sqrt(mat[2][0]**2 + mat[2][1]**2 + mat[2][2]**2)
#     return x,y,z


def blender_to_gp_quaternion(rot: Quaternion):
    return gp_Quaternion(rot[0], rot[1], rot[2], rot[3])


def get_shape_name_and_color(shape, doc):
    name = None
    color = (0.8, 0.8, 0.8)
    if doc != None:
        # Get shape label
        label = TDF_Label()
        if XCAFDoc_DocumentTool.ShapeTool_GetID(doc).FindShape(shape, label):
            # Get name
            name_attr = TDataStd_Name()
            if label.FindAttribute(TDataStd_Name.GetID_(), name_attr):
                name = name_attr.Get().PrintToString()

            # Get color
            color_tool = XCAFDoc_DocumentTool.ColorTool_(doc.Main())
            color = Quantity_Color()
            if color_tool.GetColor(shape, XCAFDoc_ColorGen, color):
                color = (color.Red(), color.Green(), color.Blue())
    return name, color


EDGES_TYPES = {
    "line": 0,  # Not absurd
    "bezier": 0,
    "nurbs": 1,
    "circle_arc": 2,
    "circle": 3,
    "ellipse_arc": 4,
    "ellipse": 5,
}


def replace_all_instances_of_node_group(target_node_group_name, new_node_group_name):
    # Get the target node group
    prefix, suffix = target_node_group_name[:-2], target_node_group_name[-2:]

    if suffix == ".*":
        pattern = rf"^{re.escape(prefix)}\.(\d{{3}}|\d{{3}}\.\d{{3}})$"
        target_node_groups = [
            ng for ng in bpy.data.node_groups if re.match(pattern, ng.name)
        ]
    else:
        target_node_groups = [bpy.data.node_groups.get(target_node_group_name)]

    # Get the new node group
    new_node_group = bpy.data.node_groups.get(new_node_group_name)
    if not new_node_group:
        return 0  # New node group not found

    if len(target_node_groups) > 0:
        for t in target_node_groups:
            if t and t != new_node_group:
                # Replace the node group data
                t.user_remap(new_node_group)

                # Remove the old node group
                bpy.data.node_groups.remove(t)

        return len(target_node_groups)
    else:
        return -1


def to_hex(color):
    hexcol = ""
    for c in color[0:3]:
        if c < 0.0031308:
            srgb = 0.0 if c < 0.0 else c * 12.92
        else:
            srgb = 1.055 * math.pow(c, 1.0 / 2.4) - 0.055

        hexstr = hex(max(min(int(srgb * 255 + 0.5), 255), 0))
        if len(hexstr[2:]) == 1:
            hexcol += "0" + hexstr[2:]
        else:
            hexcol += hexstr[2:]
    return hexcol


# From OCC Extend
def list_of_shapes_to_compound(
    list_of_shapes: List[TopoDS_Shape],
) -> Tuple[TopoDS_Compound, bool]:
    """takes a list of shape in input, gather all shapes into one compound
    returns the compound and a boolean, True if all shapes were added to the compound,
    False otherwise
    """
    all_shapes_converted = True
    the_compound = TopoDS_Compound()
    the_builder = BRep_Builder()
    the_builder.MakeCompound(the_compound)
    for shp in list_of_shapes:
        # first ensure the shape is not Null
        if shp.IsNull():
            all_shapes_converted = False
            continue
        the_builder.Add(the_compound, shp)
    return the_compound, all_shapes_converted


def shape_list_to_compound(shape_list: list[TopoDS_Shape]) -> TopoDS_Compound:
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)

    for shape in shape_list:
        builder.Add(compound, shape)

    return compound


def shells_to_solids(topods_shape: TopoDS_Shape):
    separated_shapes_list = []

    # if compound, decompose
    if topods_shape.ShapeType() == TopAbs.TopAbs_COMPOUND:

        # shells to solids :
        iterator = TopoDS_Iterator(topods_shape)
        while iterator.More():
            sh = iterator.Value()

            # Shell
            if sh.ShapeType() == TopAbs.TopAbs_SHELL:
                make_solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(sh))
                analyzer = BRepCheck_Analyzer(make_solid.Shape())
                if make_solid.IsDone() and analyzer.IsValid():
                    separated_shapes_list.append(make_solid.Solid())
                else:
                    separated_shapes_list.append(sh)
                    print("None Manifold Shell")

            # Face or wire pass trough
            elif (
                sh.ShapeType() == TopAbs.TopAbs_FACE
                or sh.ShapeType() == TopAbs.TopAbs_WIRE
            ):
                separated_shapes_list.append(sh)

            # Other
            else:
                print(f"Unexpected shape of type {sh.ShapeType()}")
            iterator.Next()

    # Single shell
    elif topods_shape.ShapeType() == TopAbs.TopAbs_SHELL:
        make_solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(topods_shape))
        analyzer = BRepCheck_Analyzer(make_solid.Shape())
        if make_solid.IsDone() and analyzer.IsValid():
            separated_shapes_list.append(make_solid.Solid())
        else:
            separated_shapes_list.append(topods_shape)
            print("None Manifold Shell")
    # Face
    elif topods_shape.ShapeType() == TopAbs.TopAbs_FACE:
        separated_shapes_list.append(topods_shape)
    # other
    else:
        separated_shapes_list.append(topods_shape)
        print(f"Unexpected shape of type {topods_shape.ShapeType()}")

    return separated_shapes_list


def get_geom_adapt_curve_type(adaptor_curve: GeomAdaptor_Curve):
    try:
        curve_type = adaptor_curve.Curve().GetType()
    except AttributeError:
        curve_type = adaptor_curve.GetType()
    return curve_type


def curve_range_from_type(curve_type):
    match curve_type:
        case GeomAbs.GeomAbs_Line:
            min_u, max_u = 0, 1
        case GeomAbs.GeomAbs_BezierCurve:
            min_u, max_u = 0, 1
        case GeomAbs.GeomAbs_BSplineCurve:
            min_u, max_u = 0, 1
        case GeomAbs.GeomAbs_Circle:
            min_u, max_u = -math.pi, math.pi
        case GeomAbs.GeomAbs_Ellipse:
            min_u, max_u = -math.pi, math.pi

    return min_u, max_u
