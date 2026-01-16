import bmesh
import bpy
import numpy as np
from mathutils import Vector, Matrix, Quaternion
import math
from typing import List, Tuple
from os.path import dirname, abspath
import re

from .enums import SP_obj_type, MESHER_NAMES, geom_to_sp_type
from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAdaptor import GeomAdaptor_Curve
from OCP.TopAbs import TopAbs_EDGE, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import (
    TopoDS,
    TopoDS_Wire,
    TopoDS_Edge,
    TopoDS_Face,
    TopoDS_Shape,
    TopoDS_Compound,
    TopoDS_Iterator,
)
from OCP.gp import (
    gp_Pnt,
    gp_Quaternion,
    gp_Trsf,
    gp_Pnt2d,
    gp_Trsf,
    gp_Vec,
)
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array2OfPnt
from OCP.TColStd import (
    TColStd_Array1OfInteger,
    TColStd_Array1OfReal,
    TColStd_HArray1OfReal,
    TColStd_HArray1OfInteger,
    TColStd_HArray2OfReal,
)
from OCP.TCollection import TCollection_HAsciiString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorGen
from OCP.Quantity import Quantity_Color
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.StepGeom import (
    StepGeom_CartesianPoint,
    StepGeom_HArray1OfCartesianPoint,
    StepGeom_HArray2OfCartesianPoint,
)
import OCP.TopAbs as TopAbs
import OCP.GeomAbs as GeomAbs

addonpath = dirname(dirname(abspath(__file__)))  # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"


def get_face_sp_type(TopoDSface: TopoDS_Face):
    adapt_surf = BRepAdaptor_Surface(TopoDSface)
    surface_type = adapt_surf.GetType()
    return geom_to_sp_type.get(surface_type, f"Unknown type: {surface_type}")


def sp_type_of_object(o: bpy.types.Object) -> SP_obj_type:
    # Instance or Empty
    if o.type == "EMPTY":
        if o.instance_collection != None:
            return SP_obj_type.INSTANCE
        else:
            return SP_obj_type.EMPTY

    # Standard
    for m in reversed(o.modifiers):
        if m.type == "NODES" and m.node_group:
            for k, v in MESHER_NAMES.items():
                if v == m.node_group.name[:-4] or v == m.node_group.name:
                    return k

    # Non SP
    return None


def read_attribute_by_name(object, name, len_attr=None) -> np.array:
    att = object.data.attributes[name]
    type = att.data_type
    len_raw = len(att.data)
    if len_attr is None:
        len_attr = len_raw
    match type:
        case "BOOLEAN":
            attribute = np.zeros(len_raw, dtype=bool)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = np.array([bool(a) for a in attribute])

        case "INT":
            attribute = np.zeros(len_raw)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = np.array([int(a) for a in attribute])

        case "FLOAT":
            attribute = np.zeros(len_raw, dtype=float)
            att.data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]

        case "FLOAT_VECTOR":
            attribute = np.empty(3 * len_raw, dtype=float)
            att.data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]

        case "FLOAT2":
            attribute = np.empty(2 * len_raw, dtype=float)
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
                remove_preview_image(mod.node_group)
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
        if m.type == "NODES" and m.node_group and m.node_group.name.startswith("SP - "):
            # Collect items first to avoid modifying during iteration
            items_to_process = []

            for it in list(m.node_group.interface.items_tree):  # Create a copy
                if (
                    it.item_type == "SOCKET"
                    and it.socket_type == socket_type
                    and it.name in potential_names
                ):
                    items_to_process.append(it)

            # Process collected items
            modifier_updated = False
            for it in items_to_process:
                input_id = it.identifier
                # if input_id in m:  # Check existence before access
                m[input_id] = value
                modifier_updated = True

            # Single interface update after all changes
            if modifier_updated:
                m.node_group.interface_update(context)


def flip_node_socket_bool(ob: bpy.types.Object, potential_names, context):
    for m in ob.modifiers:
        if m.type == "NODES" and m.node_group and m.node_group.name.startswith("SP - "):
            # Collect items first to avoid modifying during iteration
            items_to_process = []

            for it in list(m.node_group.interface.items_tree):  # Create a copy
                if (
                    it.item_type == "SOCKET"
                    and it.socket_type == "NodeSocketBool"
                    and it.name in potential_names
                ):
                    items_to_process.append(it)

            # Process collected items
            modifier_updated = False
            for it in items_to_process:
                input_id = it.identifier
                # if input_id in m:  # Check existence before access
                m[input_id] = not m[input_id]
                modifier_updated = True

            # Single interface update after all changes
            if modifier_updated:
                m.node_group.interface_update(context)


def change_GN_modifier_settings(modifier, settings_dict):
    tree = modifier.node_group.interface.items_tree
    for i, k in enumerate(tree.keys()):
        if k in settings_dict.keys():
            item = tree[i]
            if isinstance(item, bpy.types.NodeTreeInterfaceSocket):
                id = item.identifier
            # elif isinstance(item, bpy.types.NodeTreeInterfacePanel):
            #     for it in tree:
            #         if it.name == k and isinstance(
            #             item, bpy.types.NodeTreeInterfaceSocket
            #         ):
            #             id = item.identifier
            #             break

            modifier[id] = settings_dict[k]


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
    bpy.ops.object.mode_set(mode="OBJECT")
    for o in objs:
        # Switch to object mode

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
    # Must be in object mode
    # Get attribute
    att = o.data.attributes[att_name]
    if att.data_type != "BOOLEAN":
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
    return True


def toggle_pseudo_bool_attribute(o, att_name):
    # Must be in object mode
    # Get attribute
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
        return [array(i) for i in range(array.Lower(), array.Upper() + 1)]
    else:
        return [array(i) for i in range(array.Lower(), array.Upper() + 1)]


def harray1_of_real_to_list(harray):
    return [harray(i) for i in range(harray.Lower(), harray.Upper() + 1)]


def harray1_of_int_to_list(harray):
    return [harray(i) for i in range(harray.Lower(), harray.Upper() + 1)]


def gp_list_to_arrayofpnt(array: list):
    tcol = TColgp_Array1OfPnt(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, gp_Pnt(array[i].X(), array[i].Y(), array[i].Z()))
    return tcol


def float_list_to_tcolstd(array: list[float]):
    tcol = TColStd_Array1OfReal(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, array[i])
    return tcol


def int_list_to_tcolstd(array: list[int]):
    tcol = TColStd_Array1OfInteger(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, array[i])
    return tcol


def float_list_to_tcolstd_H(array: list[float]):
    tcol = TColStd_HArray1OfReal(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, array[i])
    return tcol


def int_list_to_tcolstd_H(array: list[int]):
    tcol = TColStd_HArray1OfInteger(1, len(array))
    for i in range(len(array)):
        tcol.SetValue(i + 1, array[i])
    return tcol


def float_list_to_tcolstd_H_2d(array: list[list[float]]):
    rows = len(array)
    cols = len(array[0]) if rows > 0 else 0
    tcol = TColStd_HArray2OfReal(1, rows, 1, cols)
    for i in range(rows):
        for j in range(cols):
            tcol.SetValue(i + 1, j + 1, array[i][j])
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


def vec_list_to_step_cartesian2d(array: list):
    step_array = StepGeom_HArray1OfCartesianPoint(1, len(array))
    for i in range(len(array)):
        p = StepGeom_CartesianPoint()
        p.Init2D(TCollection_HAsciiString("cp"), array[i][0], array[i][1])
        step_array.SetValue(i + 1, p)
    return step_array


def vec_list_to_step_cartesian(array: list):
    step_array = StepGeom_HArray1OfCartesianPoint(1, len(array))
    for i in range(len(array)):
        p = StepGeom_CartesianPoint()
        p.Init3D(TCollection_HAsciiString("cp"), *(array[i]))
        step_array.SetValue(i + 1, p)
    return step_array


def vec_grid_to_step_cartesian(array: list):
    rows = len(array)
    cols = len(array[0]) if rows > 0 else 0
    step_array = StepGeom_HArray2OfCartesianPoint(1, rows, 1, cols)
    for i in range(rows):
        for j in range(cols):
            p = StepGeom_CartesianPoint()
            p.Init3D(TCollection_HAsciiString("cp"), *(array[i][j]))
            step_array.SetValue(i + 1, j + 1, p)
    return step_array


def blender_to_gp_vec(vec: Vector):
    return gp_Vec(*vec)


def gp_pnt_to_blender_vec(vec: gp_Pnt):
    return Vector((vec.X(), vec.Y(), vec.Z()))


def gp_pnt2d_to_blender_vec(vec: gp_Pnt2d):
    return Vector((vec.X(), vec.Y(), 0.0))


def gp_pnt_to_blender_vec_list(vecs: list[gp_Pnt]) -> list[Vector]:
    return [Vector((vec.X(), vec.Y(), vec.Z())) for vec in vecs]


def gp_pnt_to_blender_vec_list_2d(vecs: list[gp_Pnt2d]) -> list[Vector]:
    return [Vector((vec.X(), vec.Y(), 0.0)) for vec in vecs]


# def gp_pnt2d_to_blender_vec_list(vecs: list):
#     return [Vector((vec.X(), vec.Y(), 0.0)) for vec in vecs]


def normalize_array(array):
    mini = min(array)
    return ((np.array(array) - mini) / (max(array) - mini)).tolist()


def list_geometry_node_groups():
    geometry_node_groups = []

    for node_group in bpy.data.node_groups:
        if node_group.type == "GEOMETRY":
            geometry_node_groups.append(node_group.name)
    return geometry_node_groups


def append_node_group(asset_name, force=False, remove_asset_data=True):
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
            if asset_name not in data_from.node_groups:
                print(f"Asset '{asset_name}' not found")
                return False
            else:
                data_to.node_groups = [asset_name]
        if remove_asset_data:
            for ng in data_to.node_groups:
                remove_preview_image(ng)
                ng.asset_clear()
        return True


def append_multiple_node_groups(ng_names: set, remove_asset_data=True):
    # Get the current node group names
    existing_node_groups = set(bpy.data.node_groups.keys())

    # Append the new node groups
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        # Filter the node groups that exist in the asset file
        valid_node_groups = [name for name in ng_names if name in data_from.node_groups]

        # Append the valid node groups
        data_to.node_groups = valid_node_groups

    if remove_asset_data:
        for ng in data_to.node_groups:
            remove_preview_image(ng)
            ng.asset_clear()

    # Find the newly added node groups
    # new_node_groups = []
    # new_node_groups_keys = set(bpy.data.node_groups.keys()) - existing_node_groups
    # for k in new_node_groups_keys:
    #     new_node_groups.append(bpy.data.node_groups[k])

    # return new_node_groups


def add_sp_modifier(
    obj,
    asset_name: str,
    settings_dict={},
    pin=False,
    append=False,
    render=True,
    force_last=False,
):
    if append:
        append_node_group(asset_name)

    if force_last:
        # Unpin modifiers
        pinned_mods = []
        for m in obj.modifiers:
            if m.use_pin_to_last:
                m.use_pin_to_last = False
                pinned_mods.append(m)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=asset_name, type="NODES")
    modifier.node_group = bpy.data.node_groups.get(asset_name)
    modifier.use_pin_to_last = pin
    modifier.show_render = render

    if force_last:
        # Re-pin modifiers
        for m in pinned_mods:
            m.use_pin_to_last = True

    if modifier.node_group == None:
        raise ValueError(f"Node group '{asset_name}' not found")

    # Change settings
    change_GN_modifier_settings(modifier, settings_dict)


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
                    # print("None Manifold Shell")

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
            min_u, max_u = 0.0, 1.0
        case GeomAbs.GeomAbs_BezierCurve:
            min_u, max_u = 0.0, 1.0
        case GeomAbs.GeomAbs_BSplineCurve:
            min_u, max_u = 0.0, 1.0
        case GeomAbs.GeomAbs_Circle:
            min_u, max_u = 0.0, 2 * math.pi
        case GeomAbs.GeomAbs_Ellipse:
            min_u, max_u = 0.0, 2 * math.pi

    return min_u, max_u


def select_by_attriute(att_name, objects):
    for o in objects:
        # Attribute
        if att_name in o.data.attributes:
            att_type = o.data.attributes[att_name].data_type
            if att_type == "FLOAT":
                weights = read_attribute_by_name(o, att_name)
                for v in o.data.vertices:
                    weight = weights[v.index]
                    v.select = weight > 0.6
            elif att_type == "BOOLEAN":
                weights = read_attribute_by_name(o, att_name)
                for v in o.data.vertices:
                    v.select = weights[v.index]

        # Vertex group
        elif att_name in o.vertex_groups:
            vertex_group = o.vertex_groups[att_name]
            for v in o.data.vertices:
                try:
                    weight = vertex_group.weight(v.index)
                    v.select = weight > 0.6
                except RuntimeError:
                    # Vertex is not in the group, skip it
                    pass


def override_attribute_dictionary(dict1, dict2):
    res = dict1.copy()
    for key, value in dict2.items():
        if key in res:
            for i in range(len(value)):
                res[key][i] = value[i]
        else:
            res[key] = value
    return res


def create_grid_mesh(vertex_count_u, vertex_count_v, smooth=True):

    # bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1)

    mesh = bpy.data.meshes.new(name="Grid")
    bm = bmesh.new()

    # divide grid
    step_x = 2 / (vertex_count_v - 1)
    step_y = 2 / (vertex_count_u - 1)

    # Create vertices
    for i in range(vertex_count_u):
        for j in range(vertex_count_v):
            x = j * step_x - 1.0  # Subtract 1 to center
            y = i * step_y - 1.0  # Subtract 1 to center
            bm.verts.new((x, y, 0))

    bm.verts.ensure_lookup_table()

    # Create faces
    for i in range(vertex_count_u - 1):
        for j in range(vertex_count_v - 1):
            v1 = bm.verts[i * vertex_count_v + j]
            v2 = bm.verts[i * vertex_count_v + j + 1]
            v3 = bm.verts[(i + 1) * vertex_count_v + j + 1]
            v4 = bm.verts[(i + 1) * vertex_count_v + j]
            bm.faces.new((v1, v2, v3, v4))

    # Update bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Set smooth
    if smooth:
        values = [True] * len(mesh.polygons)
        mesh.polygons.foreach_set("use_smooth", values)
        mesh.update()

    return mesh


def split_by_index(index: list[int], attribute: list) -> list[list]:
    # KNOWN TO FAIL ON SEVERAL CASES
    # treat 0 case
    last_zero = 0
    try:
        last_zero = index.index(1)
    except ValueError:
        # All zeros
        pass

    split_attr = []
    start = 0
    end = 0
    for i in list(dict.fromkeys(index)):
        if i == 0 and last_zero != 0:
            end = last_zero
        else:
            end += index.count(i)
        split_attr.append(attribute[start:end])
        start = end
    return split_attr


def split_by_index_dict(index: list[int], attribute: list) -> dict[list]:
    # KNOWN TO FAIL ON SEVERAL CASES
    # treat 0 case
    last_zero = 0
    try:
        last_zero = index.index(1)
    except ValueError:
        # All zeros
        pass

    split_attr = {}
    start = 0
    end = 0
    for i in list(dict.fromkeys(index)):
        if i == 0 and last_zero != 0:
            end = last_zero
        else:
            end += index.count(i)
        split_attr[i] = attribute[start:end]
        start = end
    return split_attr


def dict_to_list_missing_index_filled(dict: dict) -> list:
    min_index = min(dict.keys())
    max_index = max(dict.keys())
    list_attr = []
    for i in range(min_index, max_index + 1):
        if i in dict:
            list_attr.append(dict[i])
        else:
            list_attr.append([])
    return list_attr


def remove_preview_image(ng: bpy.types.GeometryNodeTree):
    # Somhow broken D:

    override = bpy.context.copy()
    override["id"] = ng

    # Call the remove preview operator with the override
    with bpy.context.temp_override(**override):
        if bpy.ops.ed.lib_id_remove_preview.poll():
            bpy.ops.ed.lib_id_remove_preview()
            return True
    return False


def rebound_UV(verts, curr_bounds, new_bounds):
    curr_min_u, curr_max_u, curr_min_v, curr_max_v = (
        curr_bounds[0] if curr_bounds[0] != None else 0.0,
        curr_bounds[1] if curr_bounds[1] != None else 0.0,
        curr_bounds[2] if curr_bounds[2] != None else 0.0,
        curr_bounds[3] if curr_bounds[3] != None else 0.0,
    )
    # Zero and not 1, because 0 range is ignored (as intended)

    new_min_u, new_max_u, new_min_v, new_max_v = (
        new_bounds[0] if new_bounds[0] != None else 0.0,
        new_bounds[1] if new_bounds[1] != None else 1.0,
        new_bounds[2] if new_bounds[2] != None else 0.0,
        new_bounds[3] if new_bounds[3] != None else 1.0,
    )

    curr_range_u = curr_max_u - curr_min_u
    curr_range_v = curr_max_v - curr_min_v

    new_range_u = new_max_u - new_min_u
    new_range_v = new_max_v - new_min_v

    for v in verts:
        if curr_range_u != 0.0:
            v[0] = ((v[0] - curr_min_u) / curr_range_u) * new_range_u + new_min_u
        if curr_range_v != 0.0:
            v[1] = ((v[1] - curr_min_v) / curr_range_v) * new_range_v + new_min_v

    return verts


def is_natural_bounds(verts, edges):
    is_natural_bounds_trim = False
    if len(verts) == 4:

        t1 = verts == [
            Vector((0.0, 0.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
        ]
        t2 = verts == [
            Vector((0.0, 1.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
        ]
        t3 = verts == [
            Vector((1.0, 1.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
        ]
        t4 = verts == [
            Vector((1.0, 0.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
        ]

        t5 = verts == [
            Vector((1.0, 0.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
        ]
        t6 = verts == [
            Vector((1.0, 1.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
        ]
        t7 = verts == [
            Vector((0.0, 1.0, 0.0)),
            Vector((0.0, 0.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
        ]
        t8 = verts == [
            Vector((0.0, 0.0, 0.0)),
            Vector((1.0, 0.0, 0.0)),
            Vector((1.0, 1.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
        ]

        t9 = set(edges) == {(0, 1), (1, 2), (2, 3), (3, 0)}

        is_natural_bounds_trim = (t1 or t2 or t3 or t4 or t5 or t6 or t7 or t8) and t9

    return is_natural_bounds_trim
