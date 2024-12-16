import bpy
# import bmesh
import numpy as np
from mathutils import Vector, Matrix
import math
from math import isclose
from typing import List, Tuple
from os.path import dirname, abspath, join

from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.TopAbs import TopAbs_FORWARD, TopAbs_EDGE, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Wire, TopoDS_Edge, TopoDS_Face, TopoDS_Shape, TopoDS_Compound



addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"


TYPES_FROM_CP_ATTR = {        'CP_bezier_surf':'bicubic_surf',
                           'CP_any_order_surf':'bezier_surf',
                               'CP_NURBS_surf':'NURBS_surf',
                                   'CP_planar':'planar',
                                    'CP_curve':'curve',
                              'CP_NURBS_curve':'NURBS_curve',
                                 'CP_cylinder':'cylinder',
                                    'CP_torus':'torus',
                                    'CP_conic':'conic',
                                   'CP_sphere':'sphere',
                               'CP_swept_surf':'swept_surf',
                          'CP_revolution_surf':'revolution_surf',}




def get_face_type_id(TopoDSface : TopoDS_Face):
    face_surface = BRepAdaptor_Surface(TopoDSface)
    return face_surface.GetType()

def get_face_type_name(TopoDSface : TopoDS_Face):
    surface_type = get_face_type_id(TopoDSface)
    type_names = {
        GeomAbs_Plane: "Plane", #0
        GeomAbs_Cylinder: "Cylinder", #1
        GeomAbs_Cone: "Cone", #2
        GeomAbs_Sphere: "Sphere", #3
        GeomAbs_Torus: "Torus", #4
        GeomAbs_BezierSurface: "Bezier Surface", #5
        GeomAbs_BSplineSurface: "BSpline Surface", #6
        GeomAbs_SurfaceOfRevolution: "Surface of Revolution", #7
        GeomAbs_SurfaceOfExtrusion: "Surface of Extrusion", #8
        GeomAbs_OffsetSurface: "Offset Surface", #9
        GeomAbs_OtherSurface: "Other Surface" #10
    }
    return type_names.get(surface_type, f"Unknown type: {surface_type}")




def geom_type_of_object(o, context):
    if o.type == 'EMPTY' and o.instance_collection != None :
        return 'collection_instance'
    else : 
        ob = o.evaluated_get(context.evaluated_depsgraph_get())
        if hasattr(ob.data, "attributes") :
            for k in ob.data.attributes.keys() :
                if k in TYPES_FROM_CP_ATTR.keys():
                    return TYPES_FROM_CP_ATTR[k]


def get_attribute_by_name(ob_deps_graph, name, type='vec3', len_attr=None):
    ge = ob_deps_graph.data
    match type :
        case 'first_bool':
            attribute = bool(ge.attributes[name].data[0].value)

        case 'first_int':
            attribute = int(ge.attributes[name].data[0].value)

        case 'second_int':
            attribute = int(ge.attributes[name].data[1].value)

        case 'bool':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            ge.attributes[name].data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = [bool(a) for a in attribute]


        case 'int':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            ge.attributes[name].data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            attribute = [int(a) for a in attribute]

        case 'float':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            ge.attributes[name].data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
            
        case 'vec3':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.empty(3 * len_raw)
            ge.attributes[name].data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]
            
    return attribute



def append_object_by_name(obj_name, context):# for importing from the asset file
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name==obj_name]

    cursor_loc = context.scene.cursor.location

    o = data_to.objects[0]
    if o is not None:
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        context.collection.objects.link(o)
        o.location = cursor_loc
        o.asset_clear()
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        # Iterate through all objects and their geometry node modifiers
        for mod in o.modifiers:
            if mod.type == 'NODES' and mod.node_group:
                mod.node_group.asset_clear()


def classify_strings_by_prefix(strings):
    import re
    strings.sort()
    object_dict = {}
    for string in strings:
        # Use regex to extract the common prefix
        match = re.match(r'(\D+)(\d*.*)', string)
        if match:
            prefix = match.group(1)
            if prefix not in object_dict:
                object_dict[prefix] = [string]
            else:
                object_dict[prefix].append(string)
    return object_dict


def highest_suffix_of_each_object_name(names):
    classified_objects=classify_strings_by_prefix(names)
    last_string = []
    for key, value in classified_objects.items():
        if value:
            last_string+= [value[-1]]
    return last_string


def create_grid(vertices):
    n,m = np.shape(vertices)
    vertices_flat = vertices.reshape(-1)
    return vertices_flat, [], [(i, i + 1, i + m + 1, i + m) for i in range((n - 1) * m) if (i + 1) % m != 0]



def change_node_socket_value(ob, value, potential_names, socket_type, context):
    for m in ob.modifiers :
        if m.type == "NODES" and m.node_group.name[:5]=='SP - ':
            for it in m.node_group.interface.items_tree :
                if it.name in potential_names and it.socket_type == socket_type:
                    input_id = it.identifier
                    m[input_id] = value
                    m.node_group.interface_update(context)

def change_GN_modifier_settings(modifier, settings_dict):
    for key, value in settings_dict.items():
        try :
            id = modifier.node_group.interface.items_tree[key].identifier
            modifier[id]=value
        except Exception:
            print("Modifier settings failed to apply")


def add_vertex_group(object, name, values):
    if name not in object.vertex_groups:
        object.vertex_groups.new(name=name)
    vg = object.vertex_groups[name]

    if len(object.data.vertices) < len(values):
        print(f"Error : {len(values)} values on {len(object.data.vertices)} vertices")
        return False

    for i,v in enumerate(values):
        if v>1. :
            v=1
            print("Warning : vertex group value clamped to 1")
        object.data.vertices
        if v!=0.0 :
            vg.add([i], v, 'ADD')
    
    return True


# Done but I am not convinced
# def add_multiple_vertex_group(object, vert_groups_dict : dict[str:list[float]]):
#     # vert_groups_dict as {"mygroup": [values],...}
    
#     # Add if don't exist
#     for name in vert_groups_dict.keys():
#         if name not in object.vertex_groups:
#             object.vertex_groups.new(name=name)
    
#     # Actual vertex groups
#     vgs = {k:object.vertex_groups[k] for k in vert_groups_dict.keys()}

#     for v in vert_groups_dict.values():
#         if len(object.data.vertices) < len(v):
#             print(f"Error : {len(v)} values on {len(object.data.vertices)} vertices")
#             return False

#     for i in range(len(object.data.vertices)):
#         for k,vg_dict in vert_groups_dict.items() :
#             v = vg_dict.values[i] if i < len(vg_dict.values()) else 0.0
#             vg = vgs[k]
#             if v>1. :
#                 v=1
#                 print("Warning : vertex group value clamped to 1")
#             object.data.vertices
#             if v!=0.0 :
#                 vg.add([i], v, 'ADD')
#     return True




def tcolstd_array1_to_list(array):
    return [array.Value(i) for i in range(array.Lower(), array.Upper() + 1)]


def normalize_array(array):
    mini = min(array)
    return ((np.array(array)-mini)/(max(array)-mini)).tolist()


def list_geometry_node_groups():
    geometry_node_groups = []
    
    for node_group in bpy.data.node_groups:
        if node_group.type == 'GEOMETRY':
            geometry_node_groups.append(node_group.name)
    return geometry_node_groups



def append_node_group(asset_name, force=False):
    # check if asset is already imported
    if force :
        asset_already = False
    else :
        groups_list = list_geometry_node_groups()
        asset_already = asset_name in groups_list
    
    # if not, import
    if not asset_already :
         # Load the asset file
        with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
            # Find the node group in the file
            if asset_name in data_from.node_groups:
                data_to.node_groups = [asset_name]
                return True
            else:
                print(f"Asset '{asset_name}' not found")
                return False



def append_multiple_node_groups(ng_names : set):
    # Get the current node group names
    existing_node_groups = set(bpy.data.node_groups.keys())

    # Append the new node groups
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        # Filter the node groups that exist in the asset file
        valid_node_groups = [name for name in ng_names if name in data_from.node_groups]

        # Append the valid node groups
        data_to.node_groups = valid_node_groups

    # Find the newly added node groups
    new_node_groups=[]
    new_node_groups_keys = set(bpy.data.node_groups.keys()) - existing_node_groups
    for k in new_node_groups_keys:
        new_node_groups.append(bpy.data.node_groups[k])

    # return new_node_groups




def add_node_group_modifier_from_asset(obj, asset_name, settings_dict={}, pin = False):
    # append_node_group(asset_name)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=asset_name, type='NODES')
    modifier.node_group = bpy.data.node_groups.get(asset_name)
    modifier.use_pin_to_last = pin

    #Change settings
    change_GN_modifier_settings(modifier, settings_dict)



def add_sp_modifier(ob, name : str, settings_dict={}, pin=False):
    add_node_group_modifier_from_asset(ob, name, settings_dict, pin = pin)



def join_mesh_entities(verts1, edges1, faces1, verts2, edges2, faces2):
    len1 = len(verts1)
    verts3=verts1.copy()
    verts3.extend(verts2)
    edges3=edges1.copy()
    edges3.extend([(e[0]+len1, e[1]+len1) for e in edges2])
    faces3=faces1.copy()
    faces3.extend([[i+len1 for i in f] for f in faces2])
    
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



def get_edges_from_wire(wire : TopoDS_Wire) -> List[TopoDS_Edge]:
    edges = []
    explorer = TopExp_Explorer(wire, TopAbs_EDGE)

    while explorer.More():
        edge = explorer.Current()
        if edge.ShapeType() == TopAbs_EDGE:
            edges.append(TopoDS.Edge_s(edge))
        explorer.Next()

    return edges




EDGES_TYPES = {'line' : 0,
               'bezier' : 1,
               'nurbs' : 2,
               'circle_arc' : 3,
               'circle' : 4,
               }




def replace_all_instances_of_node_group(old_name, new_name):
    target_node_group_name = old_name
    new_node_group_name = new_name

    # Get the target node group
    target_node_group = bpy.data.node_groups.get(target_node_group_name)

    if target_node_group:
        # Get the new node group
        new_node_group = bpy.data.node_groups.get(new_node_group_name)
        
        if new_node_group:
            # Replace the node group data
            target_node_group.user_remap(new_node_group)
            
            # Remove the old node group
            bpy.data.node_groups.remove(target_node_group)
            
            return 1
        else:
            return 0
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
        if len(hexstr[2:])==1:
            hexcol+= "0" + hexstr[2:]
        else :
            hexcol+= hexstr[2:]
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