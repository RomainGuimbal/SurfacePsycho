import bpy
# import bmesh
import numpy as np
from mathutils import Vector, Matrix
import math
from math import isclose

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.GCE2d import GCE2d_MakeSegment
from OCC.Core.Geom import Geom_BezierCurve, Geom_BSplineCurve
from OCC.Core.Geom2d import Geom2d_BezierCurve, Geom2d_BSplineCurve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_Line, GeomAbs_Circle, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface, GeomAdaptor_Curve
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.gp import gp_Pnt, gp_Pnt2d
from OCC.Core.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCC.Core.TopAbs import TopAbs_FORWARD, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_WIRE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Wire, TopoDS_Face, TopoDS_Edge, topods, TopoDS_Vertex
from OCC.Core.TopTools import TopTools_Array1OfShape
from OCC.Core.GeomConvert import geomconvert
from OCC.Core.Convert import Convert_TgtThetaOver2




# from multiprocessing import Process

from os.path import dirname, abspath, join

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"


TYPES_FROM_CP_ATTR = {        'CP_bezier_surf':'bicubic_surf',
                           'CP_any_order_surf':'bezier_surf',
                               'CP_NURBS_surf':'NURBS_surf',
                                   'CP_planar':'planar',
                          'CP_any_order_curve':'curve_any',
                                    'CP_curve':'curve',
                              'CP_NURBS_curve':'NURBS_curve',
                                 'CP_cylinder':'cylinder',
                                    'CP_torus':'torus',
                                   'CP_circle':'circle',
                                    'CP_conic':'conic',
                                  'CP_ellipse':'ellipse',
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



def normalize_array(array):
    mini = min(array)
    return ((np.array(array)-mini)/(max(array)-mini)).tolist()



def list_geometry_node_groups():
    geometry_node_groups = []
    
    for node_group in bpy.data.node_groups:
        if node_group.type == 'GEOMETRY':
            geometry_node_groups.append(node_group.name)
    return geometry_node_groups


def append_asset(asset_name, force=False):
    if force :
        asset_already = False
    else :
        groups_list = list_geometry_node_groups()
        asset_already = asset_name in groups_list
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


def append_multiple_node_groups(ng_names):
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

    return new_node_groups





def add_node_group_modifier_from_asset(obj, asset_name, settings_dict={}, pin = False):
    append_asset(asset_name)

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





# def get_edge_endpoints(topods_edge):
#     explorer = TopExp_Explorer(topods_edge, TopAbs_VERTEX)
#     vertices = []
#     while explorer.More():
#         vertex = explorer.Current()
#         vertices.append(TopoDS_Vertex(vertex))
#         explorer.Next()
    
#     if len(vertices)==2:
#         param1 = BRep_Tool.Parameter(vertices[0], topods_edge)
#         param2 = BRep_Tool.Parameter(vertices[1], topods_edge)
        
#         first_vertex = vertices[0] if param1 < param2 else vertices[1]
#         last_vertex = vertices[1] if param1 < param2 else vertices[0]

#     return BRep_Tool.Pnt(TopoDS_Vertex(first_vertex)), BRep_Tool.Pnt(TopoDS_Vertex(last_vertex))



def get_poles_from_curve(geom_curve, edge=None):
    curve_adaptor = GeomAdaptor_Curve(geom_curve)
    edge_adaptor = BRepAdaptor_Curve(edge)

    curve_type = curve_adaptor.GetType()
    
    degree = None

    if curve_type == GeomAbs_Line:
        if edge!=None :
            
            start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
            end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
            poles = [start_point, end_point]
        else:
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
        degree = bspline.Degree()
        # Should also output the degree, knot, multiplicities and weights


    
    else :
        if curve_type == GeomAbs_Circle:
            print("Unsupported curve type : GeomAbs_Circle. Expect inaccurate results")
        else :
            print("Unsupported curve type. Expect inaccurate results")
        # sampling approximation For other curve types, 
        num_points = 2
        params = [curve_adaptor.FirstParameter() + i * (curve_adaptor.LastParameter() - curve_adaptor.FirstParameter()) / (num_points - 1) for i in range(num_points)]
        poles = [curve_adaptor.Value(param) for param in params]
    
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
    return poles, degree



def get_poles_from_edge_2d(edge, face):
    edge_adaptor = BRepAdaptor_Curve2d(edge, face)
    curve_type = edge_adaptor.GetType()
    
    degree = None
    
    if curve_type == GeomAbs_Line:
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        poles = [start_point, end_point]

    elif curve_type == GeomAbs_BezierCurve:
        bezier = edge_adaptor.Bezier()
        poles = [bezier.Pole(i+1) for i in range(bezier.NbPoles())]

    elif curve_type == GeomAbs_BSplineCurve:
        bspline = edge_adaptor.BSpline()
        poles = [bspline.Pole(i+1) for i in range(bspline.NbPoles())]
        degree = bspline.Degree()

#TODO TEST
#TODO TEST
    elif curve_type == GeomAbs_Circle: 
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        center = edge_adaptor.Circle().Location()
        if start_point == end_point:
            print("GOT IT")
            poles = [start_point, center]
        poles = [start_point, center ,end_point]
#TODO TEST
#TODO TEST


    else:
        print(f"Unsupported curve type: {curve_type}. Expect inaccurate results")
        poles = []

    return poles, degree







# def get_poles_from_geom_curve_2d(curve_2d, edge=None):
#     curve_adaptor = BRepAdaptor_Curve2d(curve_2d)
#     curve_type = curve_adaptor.GetType()
#     degree = None
    
#     if curve_type == GeomAbs_Line:
#         if edge!=None :
#             start_point, end_point = get_edge_endpoints(edge)
#             poles = [start_point, end_point]
#         else:
#             start_point = curve_adaptor.Value(curve_adaptor.FirstParameter())
#             end_point = curve_adaptor.Value(curve_adaptor.LastParameter())
#             poles = [start_point, end_point]

#     elif curve_type == GeomAbs_BezierCurve:
#         bezier = curve_adaptor.Bezier()
#         poles = [bezier.Pole(i) for i in range(1, bezier.NbPoles() + 1)]
#         # Should also output weights

#     elif curve_type == GeomAbs_BSplineCurve:
#         bspline = curve_adaptor.BSpline()
#         poles = [bspline.Pole(i) for i in range(1, bspline.NbPoles() + 1)]
#         degree = bspline.Degree()
#         # Should also output the degree, knot, multiplicities and weights
    
#     else :
#         if curve_type == GeomAbs_Circle:
#             print("Unsupported curve type : GeomAbs_Circle. Expect inaccurate results")
#         else :
#             print("Unsupported curve type. Expect inaccurate results")
#         # sampling approximation For other curve types, 
#         num_points = 2
#         params = [curve_adaptor.FirstParameter() + i * (curve_adaptor.LastParameter() - curve_adaptor.FirstParameter()) / (num_points - 1) for i in range(num_points)]
#         poles = [curve_adaptor.Value(param) for param in params]
    
#     return poles, degree






def get_face_3D_contours(occface, scale = 1000):
    wires_verts, wires_edges, wires_endpoints, wires_degrees, wires_circles = [], [], [], [], []
    wires = get_wires_from_face(occface)

    # Wires
    for w in wires :
        sp_wire = SP_Wire(occ_wire=w, scale = scale)

        _, wires_edges, _ = join_mesh_entities(wires_verts, wires_edges, [], sp_wire.CP, sp_wire.bmesh_edges, [])
        wires_verts.extend(sp_wire.CP)
        wires_endpoints.extend(sp_wire.endpoints_att)
        wires_degrees.extend(sp_wire.degree_att)
        wires_circles.extend(sp_wire.circle_att)
        
    return wires_verts, wires_edges, wires_endpoints, wires_degrees, wires_circles



def get_face_uv_contours(face, uv_bounds=(0,1,0,1)):
    wires = get_wires_from_face(face)
    wires_verts, wires_edges, wires_endpoints  = [], [], []

    min_u, max_u, min_v, max_v = uv_bounds[0], uv_bounds[1], uv_bounds[2], uv_bounds[3]
    range_u, range_v = max_u - min_u, max_v - min_v

    # Wires
    for w in wires :
        edges = get_edges_from_wire(w)
        wire_degrees, endpoints, wire_verts, verts_of_edges, degree_att, knot_att, weights_att, mult_att = [], [], [], [], [], [], [], []
        
        wire_is_reversed = w.Orientation() == 1
        
        # Edges
        for e in edges :
            poles, edge_degree = get_poles_from_edge_2d(e, face)

            # Reverse
            if (e.Orientation() != TopAbs_FORWARD) != wire_is_reversed :
                poles.reverse()
            
            e_vert = []
            for p in poles :
                x=max(0, min(1, (p.X()-min_u)/range_u))
                y=max(0, min(1, (p.Y()-min_v)/range_v))
                e_vert.append(Vector((x, y, 0)))

            verts_of_edges.append(e_vert)
            wire_verts.extend(e_vert[:-1])
            endpoints.extend([1.0]+[0.0]*(len(e_vert)-2))
            if edge_degree!=None:
                degree_att.extend([edge_degree/10]+[0.0]*(len(e_vert)-2))
            else :
                degree_att.extend([0.0]*(len(e_vert)-1))
        

        wire_edges = [(i+len(wires_verts),((i+1)%len(wire_verts))+len(wires_verts)) for i in range(len(wire_verts))]
        wires_verts.extend(wire_verts)
        wires_edges.extend(wire_edges)
        wires_endpoints.extend(endpoints)
        wire_degrees.extend(degree_att)
        
    return wires_verts, wires_edges, wires_endpoints, wire_degrees






def auto_knot_and_mult(p_count, degree, isclamped = True, isperiodic = False):
    if isclamped :
        knot_length = p_count - degree + 1
        knot_att = [r/(knot_length-1) for r in range(knot_length)]
        mult_att = [degree+1] + [1]*(knot_length-2) + [degree+1]
    else :
        knot_length = p_count + degree + 1 + (degree*isperiodic)
        knot_att = [r/(knot_length-1) for r in range(knot_length)]
        mult_att = [1]*knot_length

    knot = TColStd_Array1OfReal(1, knot_length)
    mult = TColStd_Array1OfInteger(1, knot_length)
    for i in range(knot_length):
        knot.SetValue(i+1, knot_att[i])
        mult.SetValue(i+1, mult_att[i])
    return knot, mult




def create_wire_3d(vector_points, segs_p_counts, first_segment_p_id, segs_degrees, geom_plane=None, ob=None):
    total_p_count=len(vector_points)
    segment_count = len(segs_p_counts)

    # Create CP
    controlPoints = TColgp_Array1OfPnt(1, total_p_count)
    for i in range(total_p_count):
        pnt = gp_Pnt(vector_points[i][0], vector_points[i][1], vector_points[i][2])
        if geom_plane != None:
            pnt = GeomAPI_ProjectPointOnSurf(pnt, geom_plane).Point(1)
        controlPoints.SetValue(i+1, pnt)
    
    # Create segments
    edges_list = TopTools_Array1OfShape(1, segment_count)
    for i in range(segment_count):
        
        # Straight edge
        if segs_p_counts[i] == 2: 
            makesegment = GC_MakeSegment(controlPoints.Value((first_segment_p_id[i])%total_p_count +1), 
                                        controlPoints.Value((first_segment_p_id[i]+1)%total_p_count +1))
            segment = makesegment.Value()
        
        # Curved edge
        else:
            # CP
            segment_point_array = TColgp_Array1OfPnt(1, segs_p_counts[i])
            for j in range(segs_p_counts[i]):
                segment_point_array.SetValue(j+1, controlPoints.Value((first_segment_p_id[i]+j)%total_p_count +1))
            
            p_count = segs_p_counts[i]
            degree = segs_degrees[i]

            # weights
            try:
                weight_attr = get_attribute_by_name(ob, 'Weight', 'float', p_count)
                weights = TColStd_Array1OfReal(1, p_count)
                for j in range(p_count):
                    weights.SetValue(j+1, weight_attr[i])
            except Exception:
                weights = TColStd_Array1OfReal(1, p_count)
                for j in range(p_count):
                    weights.SetValue(j+1, 1)
            
            # Bezier
            if p_count-1==degree:
                segment = Geom_BezierCurve(segment_point_array)

            # Bspline
            else :
                # Mult and Knot
                try:
                    isclamped = get_attribute_by_name(ob, 'IsClamped', 'first_bool')
                    isperiodic = get_attribute_by_name(ob, 'IsPeriodic', 'first_bool')
                except Exception:
                    isclamped, isperiodic = True, False
                
                try :
                    if isclamped :
                        knot_length = p_count - degree + 1
                    else :
                        knot_length = p_count + degree

                    knot_attr = get_attribute_by_name(ob, 'Knot', 'float', knot_length)

                    # knot
                    knot = TColStd_Array1OfReal(1,knot_length)
                    for j in range(knot_length):
                        knot.SetValue(j+1, knot_attr[i])
                    
                    # Multiplicities
                    mult = TColStd_Array1OfInteger(1, knot_length)
                    for j in range(knot_length):
                        if isclamped and (j == 0 or j == knot_length-1):
                            mult.SetValue(j+1, degree+1)
                        else :
                            mult.SetValue(j+1, 1)
                except Exception:
                    knot, mult = auto_knot_and_mult(segs_p_counts[i], degree, isclamped, isperiodic)

                segment = Geom_BSplineCurve(segment_point_array, weights, knot, mult, degree, isperiodic)
        
        # append edge
        edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        edges_list.SetValue(i+1, edge)

    # Make contour
    makeWire = BRepBuilderAPI_MakeWire()
    for e in edges_list :
        makeWire.Add(e)
    wire = TopoDS_Wire()
    wire = makeWire.Wire()

    return wire





def create_wire_2d(pts_2d, segs_p_counts, first_segment_p_id, segs_degrees, geom_surf=None, ob = None):
    total_p_count = len(pts_2d)
    segment_count = len(segs_p_counts)

    # Create 2D points
    controlPoints = TColgp_Array1OfPnt2d(1, total_p_count)
    for i in range(total_p_count):
        pnt = gp_Pnt2d(pts_2d[i][1], pts_2d[i][0]) # INVERTED
        controlPoints.SetValue(i+1, pnt)

    # Create segments
    edges_list = TopTools_Array1OfShape(1, segment_count)
    for i in range(segment_count):
        
        # Straight edge
        if segs_p_counts[i] == 2: 
            makesegment = GCE2d_MakeSegment(controlPoints.Value((first_segment_p_id[i])%total_p_count+1), 
                                        controlPoints.Value((first_segment_p_id[i]+1)%total_p_count+1))
            segment = makesegment.Value()
        
        # Curved edge
        else :
            # CP
            segment_point_array = TColgp_Array1OfPnt2d(1, segs_p_counts[i])
            for j in range(segs_p_counts[i]):
                segment_point_array.SetValue(j+1, controlPoints.Value((first_segment_p_id[i]+j)%total_p_count+1))
            
            p_count = segs_p_counts[i]
            degree = segs_degrees[i]

            # weights
            try:
                weight_attr = get_attribute_by_name(ob, 'Weight', 'float', p_count)
                weights = TColStd_Array1OfReal(1, p_count)
                for j in range(p_count):
                    weights.SetValue(j+1, weight_attr[i])
            except Exception:
                weights = TColStd_Array1OfReal(1, p_count)
                for j in range(p_count):
                    weights.SetValue(j+1, 1)

            # Bezier
            if p_count-1==degree:
                segment = Geom2d_BezierCurve(segment_point_array)

            # Bspline
            else :
                # Mult and Knot
                try:
                    isclamped = get_attribute_by_name(ob, 'Clamped', 'first_bool')
                except Exception:
                    isclamped = True

                try :
                    knot_length = p_count - degree + 1
                    knot_attr = get_attribute_by_name(ob, 'Knot', 'float', knot_length)

                    # knot
                    knot = TColStd_Array1OfReal(1,knot_length)
                    for j in range(knot_length):
                        knot.SetValue(j+1, knot_attr[i])
                    
                    # Multiplicities
                    mult = TColStd_Array1OfInteger(1, knot_length)
                    for j in range(knot_length):
                        if j == 0 or j == knot_length-1:
                            mult.SetValue(j+1, degree+1)
                        else :
                            mult.SetValue(j+1, 1)
                except Exception:
                    knot, mult = auto_knot_and_mult(segs_p_counts[i], degree, isclamped)

                segment = Geom2d_BSplineCurve(segment_point_array, weights, knot, mult, degree, False)

        
        # make segment
        if geom_surf != None:
            adapt = GeomAdaptor_Surface(geom_surf)
            edge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface()).Edge()
        else :
            edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        
        # append edge
        edges_list.SetValue(i+1, edge)

    # Make contour
    makeWire = BRepBuilderAPI_MakeWire()
    for e in edges_list :
        makeWire.Add(e)
    wire = TopoDS_Wire()
    wire = makeWire.Wire()

    return wire










#####################################
#                                   #
#        Converter Classes          #
#                                   #
#####################################

class SP_surface :
    # Importer class, to unify
    def __init__(self, brepFace, collection, trims_enabled, uv_bounds, CPvert, CPedges, CPfaces):
        self.trims_enabled = trims_enabled
        self.brepFace = brepFace
        self.uv_bounds = uv_bounds
        self.CPvert = CPvert
        self.CPedges = CPedges
        self.CPfaces = CPfaces
        self.vert, self.edges, self.faces = [],[],[]
        
        if trims_enabled :
            wires_verts, wires_edges, wires_endpoints, wire_degrees = get_face_uv_contours(self.brepFace, self.uv_bounds)
            self.vert, self.edges, self.faces = join_mesh_entities(CPvert, CPedges, CPfaces, wires_verts, wires_edges, [])
        else :
            self.vert, self.edges, self.faces = self.CPvert, self.CPedges, self.CPfaces

        mesh = bpy.data.meshes.new("Patch CP")
        mesh.from_pydata(self.vert, self.edges, self.faces)
        self.ob = bpy.data.objects.new('STEP Patch', mesh)
        
        if trims_enabled :
            self.assign_vertex_gr("Trim Contour", [0.0]*len(CPvert) + [1.0]*len(wires_verts))
            self.assign_vertex_gr("Endpoints", [0.0]*len(CPvert) + wires_endpoints)
            self.assign_vertex_gr("Degree", [0.0]*len(CPvert) + wire_degrees)

        self.set_smooth()

        collection.objects.link(self.ob)

    def set_smooth(self):
        mesh = self.ob.data
        values = [True] * len(mesh.polygons)
        mesh.polygons.foreach_set("use_smooth", values)

    def assign_vertex_gr(self, name, values):
        add_vertex_group(self.ob, name, values)
        
    def add_modifier(self, name, settings_dict = {}, pin=False):
        add_sp_modifier(self.ob, name, settings_dict, pin = pin)




class SP_Pole :
    def __init__(self, occ_pole : gp_Pnt):
        self.vertex = Vector((occ_pole.X(), occ_pole.Y(), occ_pole.Z()))
        # self.weight ?
        
        



EDGES_TYPES = {'line' : 0,
               'bezier' : 1,
               'nurbs' : 2,
               'circle_arc' : 3,
               'circle' : 4,
               }

class SP_Edge :
    # Importer for now
    def __init__(self, occ_edge : TopoDS_Edge = None):
        if occ_edge!= None :
            self.verts = None
            self.degree = None
            self.type = None
            self.init_attrs(occ_edge)

    def init_attrs(self, occ_edge : TopoDS_Edge):
        edge_adaptor = BRepAdaptor_Curve(occ_edge)

        c = edge_adaptor.Curve()
        curve_type = c.GetType()
        curve = c.Curve()
                
        if curve_type == GeomAbs_Line :
            start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
            end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
            gp_pnt_poles = [start_point, end_point]
            self.type = EDGES_TYPES['line']

        elif curve_type == GeomAbs_BezierCurve :
            bezier = Geom_BezierCurve.DownCast(curve)
            gp_pnt_poles = [bezier.Pole(i+1) for i in range(bezier.NbPoles())]
            self.type = EDGES_TYPES['bezier']
            # TODO output weights

        elif curve_type == GeomAbs_BSplineCurve :
            if not isinstance(curve, Geom_BSplineCurve):
                # first_param = edge_adaptor.FirstParameter()
                # last_param = edge_adaptor.LastParameter()
                bspline = geomconvert.CurveToBSplineCurve(curve, Convert_TgtThetaOver2)
            else:
                bspline = curve

            # bspline = Geom_BSplineCurve.DownCast(curve)
            gp_pnt_poles = [bspline.Pole(i+1) for i in range(bspline.NbPoles())]
            self.degree = bspline.Degree()
            self.type = EDGES_TYPES['nurbs']
            # TODO output the knot, multiplicities and weights

        elif curve_type == GeomAbs_Circle :
            arc_method = False
            if arc_method :
                # arc from center
                start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
                end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
                center = edge_adaptor.Circle().Location()
                if start_point == end_point:
                    gp_pnt_poles = [start_point, center]
                else:
                    gp_pnt_poles = [start_point, center, end_point]
            else:
                # arc from 3 pts (no need for invert but worse for tangency):
                min_t = edge_adaptor.FirstParameter()
                max_t = edge_adaptor.LastParameter()
                
                start_point = edge_adaptor.Value(min_t)
                end_point = edge_adaptor.Value(max_t)
                range_t = max_t - min_t

                if start_point == end_point or isclose(range_t, math.pi*2):
                    center = edge_adaptor.Circle().Location()
                    gp_pnt_poles = [start_point, center]
                    self.type = EDGES_TYPES['circle']
                else:
                    mid_t = (max_t - min_t)/2 + min_t
                    mid_point = edge_adaptor.Value(mid_t)
                    gp_pnt_poles = [start_point, mid_point, end_point]
                    self.type = EDGES_TYPES['circle_arc']
                    # self.circle_arc_subtype = 1. # tree_points
        else :
            print("Unsupported curve type. Expect wrong geometry")
            # # sampling approximation For other curve types, 
            # num_points = 2
            # params = [curve_adaptor.FirstParameter() + i * (curve_adaptor.LastParameter() - curve_adaptor.FirstParameter()) / (num_points - 1) for i in range(num_points)]
            # poles = [curve_adaptor.Value(param) for param in params]

        self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]

    def scale(self, scale_factor):
        self.verts = [v*scale_factor for v in self.verts]








class SP_Wire :
    def __init__(self, occ_wire: TopoDS_Wire=None, scale=1000, CP =[], segs_p_counts=None, segs_degrees=None):
        self.CP = [] #Vectors, bmesh format
        if occ_wire!=None:
            # vertex aligned attributes
            self.bmesh_edges = [] #int tuple
            self.endpoints_att = [] #float
            self.degree_att = [] #float
            # self.knot_att = [] #float
            # self.weights_att = [] #float
            # self.mult_att = [] #float
            self.circle_att = []
            self.import_constructor(occ_wire, scale)
        else :
            self.segs_degrees = segs_degrees
            self.CP = [Vector(v) for v in CP]
            self.segs_p_counts = segs_p_counts
            self.export_constructor()

    
    def import_constructor(self, occ_wire: TopoDS_Wire, scale=1000):
            # verts_of_edges = []
            topods_edges = get_edges_from_wire(occ_wire)
            wire_is_reversed = occ_wire.Orientation() == 1

            #Edges
            for e in topods_edges :
                sp_edge = SP_Edge(e)
                sp_edge.scale(1/scale)
                e_vert = sp_edge.verts
                e_degree = sp_edge.degree
                e_type = sp_edge.type
                
                # Reverse
                if (e.Orientation() != TopAbs_FORWARD) != wire_is_reversed :
                    e_vert.reverse()

                self.CP.extend(e_vert[:-1])

                self.endpoints_att.extend([1.0]+[0.0]*(len(e_vert)-2))
                if e_degree!=None:
                    self.degree_att.extend([e_degree/10]+[0.0]*(len(e_vert)-2))
                else :
                    self.degree_att.extend([0.0]*(len(e_vert)-1))
                
                # is arc :
                if e_type == EDGES_TYPES['circle_arc'] or e_type == EDGES_TYPES['circle']:
                    self.circle_att.extend([0.0, 1.0])
                else :
                    self.circle_att.extend([0.0]*(len(e_vert)-1))
                

            # if len(topods_edges)==1: # Unclosed wire (for now just for the circle case)
            #     self.bmesh_edges = [(i + len(self.CP), i+1 + len(self.CP)) for i in range(len(self.CP)-1)]
            # else :
            #     self.bmesh_edges = [(i + len(self.CP), ((i+1)%len(self.CP)) + len(self.CP)) for i in range(len(self.CP))]
            if len(topods_edges)==1: # Unclosed mesh wire (for now just for the circle case)
                self.CP.append(e_vert[-1])
                self.degree_att.append(0.0)
                self.endpoints_att.append(0.0)
                self.bmesh_edges = [(i, i+1) for i in range(len(self.CP)-1)]
                
                if e_type == EDGES_TYPES['circle']:
                    self.CP.reverse()
                    self.circle_att.reverse()

            else : # Closed
                self.bmesh_edges = [(i, ((i+1)%len(self.CP))) for i in range(len(self.CP))]


    # Exporter constructor
    def export_constructor(self):
        # Bezier if no degree
        if self.segs_degrees==None:
            self.segs_degrees = [c-1 for c in self.segs_p_counts]

        p_count = 0 #(total)
        p_count_accumulate = self.segs_p_counts[:]
        for i, p in enumerate(self.segs_p_counts):
            if p>0:
                p_count += p-1
            elif p==0:
                break
            if i>0:
                p_count_accumulate[i] += p_count_accumulate[i-1]-1
        
        self.seg_first_P_id = [0] + [p-1 for p in p_count_accumulate[:len(self.segs_p_counts)-1]]


    def get_occ_wire_3d(self, geom_plane=None, ob=None):
        wire = create_wire_3d(self.CP, self.segs_p_counts, self.seg_first_P_id, self.segs_degrees, geom_plane, ob)
        return wire
    

    def get_occ_wire_2d(self, geom_surf=None, ob=None):
        wire = create_wire_2d(self.CP, self.segs_p_counts, self.seg_first_P_id, self.segs_degrees, geom_surf, ob)
        return wire
    

    def mirror_CP(self, axis, object_matrix, mirror_obj_matrix=None):
        if mirror_obj_matrix==None :
            mirror_obj_matrix = object_matrix
        # Example :
        # w_M_o @ p_o = p_w : matrix transform of p in object coords to p in world coords (w)
        match axis :
            # the initial mirror matrix is either expressed in object coords (o) or in mirror object coords (t)
                case "X":
                    m_M_o_or_t = Matrix(((-1,0,0,0),
                                (0,1,0,0),
                                (0,0,1,0),
                                (0,0,0,1)))
                case "Y":
                    m_M_o_or_t = Matrix(((1,0,0,0),
                                (0,-1,0,0),
                                (0,0,1,0),
                                (0,0,0,1)))
                case "Z":
                    m_M_o_or_t = Matrix(((1,0,0,0),
                                (0,1,0,0),
                                (0,0,-1,0),
                                (0,0,0,1)))

        o_or_t_M_w = mirror_obj_matrix.inverted() #t_M_w or o_M_w
        m_M_w = m_M_o_or_t @ o_or_t_M_w

        self.CP = [ o_or_t_M_w.inverted() @ (m_M_w @ pw) for pw in self.CP]

    def scale(self, scale_factor):
        self.CP = [v*scale_factor for v in self.CP]
    
    def offset(self, offset : Vector):
        self.CP = [v+offset for v in self.CP]






def split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_degrees=None):
    # wire index attr
    try :
        wire_index = get_attribute_by_name(ob, 'Wire', 'int', total_p_count)
        wire_index = [int(w) for w in wire_index]
    except Exception :
        wire_index = [-1]*total_p_count

    # Bezier if no degree
    if segs_degrees == None:
        segs_degrees = [c-1 for c in segs_p_counts]
    
    # Make wires
    # Init
    wires_dict = {}
    w_prev = wire_index[0]
    build_CP, build_segs_p_counts, build_segs_degrees = [], [], []
    seg_p_added = 0
    seg_curr_id = 0
    seg_p_count_curr = segs_p_counts[0]
    segs_degrees_curr = segs_degrees[0]

    for i, w_cur in enumerate(wire_index) :
        # wire first point
        if w_cur != w_prev :
            wires_dict[w_prev] = SP_Wire(CP = build_CP, segs_p_counts= build_segs_p_counts, segs_degrees= build_segs_degrees)
            build_CP, build_segs_p_counts, build_segs_degrees = [], [], []

        # Add point
        build_CP.append(points[i])
        seg_p_added += 1
        
        # Segment last point
        if seg_p_added == seg_p_count_curr-1 :
            build_segs_p_counts.append(seg_p_count_curr)
            build_segs_degrees.append(segs_degrees_curr)
            seg_curr_id+=1
            if i<len(wire_index)-1:
                seg_p_count_curr = segs_p_counts[seg_curr_id]
                segs_degrees_curr = segs_degrees[seg_curr_id]
            seg_p_added = 0

        w_prev = w_cur
    # Build last wire
    wires_dict[w_prev] = SP_Wire(CP = build_CP, segs_p_counts= build_segs_p_counts, segs_degrees= build_segs_degrees)

    return wires_dict # dictionary of SP_Wires





# from OCC.Core.TopoDS import TopoDS_Face
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopAbs import TopAbs_WIRE
# from OCC.Core.TopoDS import topods_Wire
# from OCC.Core.BRepCheck import BRepCheck_Wire, BRepCheck_NoError

# def check_trim_wires_for_face(face: TopoDS_Face):
#     if not isinstance(face, TopoDS_Face):
#         raise TypeError("Input must be a TopoDS_Face")

#     issues_found = False
#     wire_explorer = TopExp_Explorer(face, TopAbs_WIRE)

#     while wire_explorer.More():
#         wire = topods_Wire(wire_explorer.Current())
#         wire_checker = BRepCheck_Wire(wire)
        
#         # Check if the wire is valid on the face
#         if wire_checker.InContext(face) != BRepCheck_NoError:
#             print(f"Wire is invalid on the given face")
#             issues_found = True
        
#         # Check wire closure
#         if wire_checker.Closed() != BRepCheck_NoError:
#             print(f"Wire is not closed on the given face")
#             issues_found = True
        
#         wire_explorer.Next()

#     if not issues_found:
#         print("All trim wires on the face are valid")




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