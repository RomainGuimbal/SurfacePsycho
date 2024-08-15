import bpy
import bmesh
import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopoDS import topods_Edge
from OCC.Core.Geom2d import Geom2d_BSplineCurve, Geom2d_Line
# from multiprocessing import Process
import sys
from os.path import dirname, abspath, join
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"



def geom_type_of_object(o, context):
    type = None
    if o.type == 'EMPTY' and o.instance_collection != None :
        type = 'collection_instance'
    else : 
        ob = o.evaluated_get(context.evaluated_depsgraph_get())
        if hasattr(ob.data, "attributes") :

            for k in ob.data.attributes.keys() :
                match k:
                    case 'CP_bezier_surf' :
                        type = 'bicubic_surf'
                        break
                    case 'CP_any_order_surf' :
                        type = 'surf_any'
                        break
                    case 'CP_planar' :
                        type = 'planar'
                        break
                    case 'CP_any_order_curve':
                        type = 'curve_any'
                        break
                    case 'CP_curve':
                        type = 'curve'
                        break
                    case 'CP_NURBS_curve' :
                        type = 'NURBS_curve'
                        break
    return type


def get_attribute_by_name(ob_deps_graph, name, type='vec3', len_attr=None):
    ge = ob_deps_graph.data
    match type :
        case 'first_int':
            attribute = ge.attributes[name].data[0].value

        case 'second_int':
            attribute = ge.attributes[name].data[1].value

        case 'int':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            ge.attributes[name].data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]

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


# def modifier_exists_in_file(modifier_name):
#     for mod in bpy.data.modifiers:
#         if mod.name == modifier_name:
#             return True
#     return False


# def add_modifier(object, modifier_name):
#     if not modifier_exists_in_file(modifier_name):
#         append_modifier_from_sp_lib(modifier_name)

#     for mod in bpy.data.modifiers:
#         if mod.name == modifier_name:
#             appended_modifier = mod
#             break

#     object.modifiers.new(name=modifier_name, type=appended_modifier.type)


# def append_modifier_from_sp_lib(modifier_name):
#     with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
#         if modifier_name in data_from.modifiers:
#             data_to.modifiers.append(modifier_name)

# def progress_bar(self, context):
#     row = self.layout.row()
#     row.progress(
#         factor=context.window_manager.progress,
#         type="BAR",
#         text="Import in progress..." if context.window_manager.progress < 1 else "Import Successful"
#     )
#     row.scale_x = 1


# def runInParallel(fns):
#   proc = []
#   for fn in fns:
#     p = Process(target=fn)
#     p.start()
#     proc.append(p)
#   for p in proc:
#     p.join()

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
        print(len(object.data.vertices))
        print(values)
        return False

    for i,v in enumerate(values):
        if v>1. :
            v=1
            print("vertex group value clamped to 1")
        object.data.vertices
        if v!=0.0 :
            vg.add([i], v, 'ADD')
    
    return True



def normalize_array(array):
    mini = min(array)
    return ((np.array(array)-mini)/(max(array)-mini)).tolist()


APPENDED_ASSETS = []
# TODO
# To not lose the list at each close>open fill APPENDED_ASSETS with a list of all modifiers of the file ?
# Alternatively : store properly in the blend file (need a way to be reset)

def append_asset(asset_name, library_name = "SurfacePsycho"):
    if asset_name not in APPENDED_ASSETS :
        APPENDED_ASSETS.append(asset_name)

        # Get the asset library
        library = bpy.context.preferences.filepaths.asset_libraries.get(library_name)
        if not library:
            print(f"Asset library '{library_name}' not found")
            return

        # Construct the full path to the asset file
        asset_file = join(library.path, "assets.blend")

        # Load the asset file
        with bpy.data.libraries.load(asset_file, link=False) as (data_from, data_to):
            # Find the node group in the file
            if asset_name in data_from.node_groups:
                data_to.node_groups = [asset_name]
            else:
                print(f"Asset '{asset_name}' not found in library '{library_name}'")
                return

def add_node_group_modifier_from_asset(obj, asset_name, library_name = "SurfacePsycho", settings_dict={}, append_to_list=True):
    if append_to_list:
        append_asset(asset_name, library_name)

    # Create the modifier and assign the loaded node group
    modifier = obj.modifiers.new(name=asset_name, type='NODES')
    modifier.node_group = bpy.data.node_groups.get(asset_name)
    
    #Change settings
    change_GN_modifier_settings(modifier, settings_dict)


def add_sp_modifier(ob, name, settings_dict={}, append_to_list=True):
    add_node_group_modifier_from_asset(ob, name, "SurfacePsycho", settings_dict, append_to_list)
    # try :
        # bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
        #                                     asset_library_identifier="SurfacePsycho",
        #                                     relative_asset_identifier="assets.blend\\NodeTree\\"+name)
    #     return True
    # except Exception:
    #     return False




def join_mesh_entities(verts1, edges1, faces1, verts2, edges2, faces2):
    len1 = len(verts1)
    verts1.extend(verts2)
    edges1.extend([(e[0]+len1, e[1]+len1) for e in edges2])
    faces1.extend([[i+len1 for i in f] for f in faces2])
    
    return verts1, edges1, faces1



def flatten_list_of_lists(list_of_lists):
    flat_list = []
    for row in list_of_lists:
        flat_list.extend(row)
    return flat_list












from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_WIRE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FORWARD, TopAbs_EDGE
from OCC.Core.GeomAbs import GeomAbs_CurveType, GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_Line
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.TopoDS import topods
from mathutils import Vector


def get_wires_from_face(face):
    # face type = TopoDS_Face
    wires = []
    explorer = TopExp_Explorer(face, TopAbs_WIRE)

    while explorer.More():
        wire = explorer.Current()
        if wire.ShapeType() == TopAbs_WIRE and wire.Closed():
            wires.append(topods.Wire(wire))
        explorer.Next()

    return wires



def get_edges_from_wire(wire):
    edges = []
    explorer = TopExp_Explorer(wire, TopAbs_EDGE)

    while explorer.More():
        edge = explorer.Current()
        if edge.ShapeType() == TopAbs_EDGE:
            edges.append(topods.Edge(edge))
        explorer.Next()

    return edges



def get_poles_from_geom_curve(curve_adaptor: BRepAdaptor_Curve):
    curve_type = curve_adaptor.GetType()
            
    if curve_type == GeomAbs_Line:
        start_point = curve_adaptor.Value(curve_adaptor.FirstParameter())
        end_point = curve_adaptor.Value(curve_adaptor.LastParameter())
        poles = [start_point, end_point]

    elif curve_type == GeomAbs_BezierCurve:
        bezier = curve_adaptor.Bezier()
        poles = [bezier.Pole(i) for i in range(1, bezier.NbPoles() + 1)]
        # Should also output weights

    elif curve_type == GeomAbs_BSplineCurve:
        bspline = curve_adaptor.BSpline()
        poles = [bspline.Pole(i) for i in range(1, bspline.NbPoles() + 1)]
        print(bspline.Degree())
        # Should also output the order, knot, multiplicities and weights
    
    else :
        print("Unsupported curve type. Expect inaccurate results")
        poles = []
        # # For other curve types, we'll use a sampling approximation
        # num_points = 5
        # params = [curve_adaptor.FirstParameter() + i * (curve_adaptor.LastParameter() - curve_adaptor.FirstParameter()) / (num_points - 1) for i in range(num_points)]
        # poles = [curve_adaptor.Value(param) for param in params]
    
    # elif curve_type == GeomAbs_Circle:
    #     # center = curve_adaptor.Circle().Location()
    #     # radius = curve_adaptor.Circle().Radius()
    #     # start_angle = curve_adaptor.FirstParameter()
    #     # end_angle = curve_adaptor.LastParameter()
    #     # mid_angle = (start_angle + end_angle) / 2
    #     # start_point = curve_adaptor.Value(start_angle)
    #     # mid_point = curve_adaptor.Value(mid_angle)
    #     # end_point = curve_adaptor.Value(end_angle)
    #     # control_points = [start_point, mid_point, end_point]
    return poles




def get_face_uv_contours(face, bounds=(0,1,0,1)):
    wires = get_wires_from_face(face)
    wires_verts, wires_edges, wires_endpoints  = [], [], []

    min_u, max_u, min_v, max_v = bounds[0], bounds[1], bounds[2], bounds[3]
    range_u, range_v = max_u - min_u, max_v - min_v

    for w in wires :
        edges = get_edges_from_wire(w)
        wire_poles, endpoints, wire_vert = [], [], []

        for e in edges :
            # Get the 2D curve on the surface
            curve2d, u0, u1 = BRep_Tool.CurveOnSurface(e, face)
            adaptor = Geom2dAdaptor_Curve(curve2d)
            curve_type = adaptor.GetType()

            poles = get_poles_from_geom_curve(adaptor)

            # Reverse the order if the edge orientation is reversed
            if e.Orientation() != TopAbs_FORWARD:
                poles.reverse()
            
            wire_poles.extend(poles[:-1])
            endpoints.extend([1.0]+[0.0]*(len(poles)-2))

        for p in wire_poles :
            x=(p.X()-min_u)/range_u
            y=(p.Y()-min_v)/range_v
            wire_vert.append(Vector((x, y, 0)))

        wire_edge = [(i,(i+1)%len(wire_vert)) for i in range(len(wire_vert))]
    
        wires_verts.extend(wire_vert)
        wires_edges.extend(wire_edge)
        wires_endpoints.extend(endpoints)
        
    return wires_verts, wires_edges, wires_endpoints




