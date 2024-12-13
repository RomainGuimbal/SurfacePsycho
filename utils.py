import bpy
# import bmesh
import numpy as np
from mathutils import Vector, Matrix
import math
from math import isclose
from typing import List, Tuple
from os.path import dirname, abspath, join

# from OCP.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCP.Convert import Convert_TgtThetaOver2
from OCP.GC import GC_MakeSegment
from OCP.GCE2d import GCE2d_MakeSegment
from OCP.Geom import Geom_BezierCurve, Geom_BSplineCurve
from OCP.Geom2d import Geom2d_BezierCurve, Geom2d_BSplineCurve
from OCP.GeomAbs import GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_Line, GeomAbs_Circle, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.GeomAdaptor import GeomAdaptor_Surface, GeomAdaptor_Curve
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.GeomConvert import GeomConvert
from OCP.gp import gp_Pnt, gp_Pnt2d
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCP.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCP.TopAbs import TopAbs_FORWARD, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Wire, TopoDS_Edge, TopoDS_Face, TopoDS_Shape, TopoDS_Compound
from OCP.TopTools import TopTools_Array1OfShape



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



# exporter
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
        makeWire.Add(TopoDS.Edge_s(e))
    wire = TopoDS_Wire()
    wire = makeWire.Wire()

    return wire





#exporter
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
        makeWire.Add(TopoDS.Edge_s(e))
    wire = TopoDS_Wire()
    wire = makeWire.Wire()

    return wire










#####################################
#                                   #
#        Converter Classes          #
#                                   #
#####################################
class SP_Pole :
    def __init__(self, occ_pole):
        if isinstance(occ_pole, gp_Pnt2d) : 
            self.vertex = Vector((occ_pole.X(), occ_pole.Y(), 0))
        else :
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
    def __init__(self, topods_edge : TopoDS_Edge, topods_face = None):
        if topods_edge!= None :
            self.verts = None
            self.degree = None
            self.type = None
            
            # Edge adaptor
            # 3D
            if topods_face is None:
                twoD=False
                edge_adaptor = BRepAdaptor_Curve(topods_edge)
                curve_type = edge_adaptor.Curve().GetType()
                # c = edge_adaptor.Curve()
                # curve_type = c.GetType()
                # curve = c.Curve()

                # curve_adaptor = GeomAdaptor_Curve(geom_curve)
            #2D
            else :
                twoD=True
                edge_adaptor = BRepAdaptor_Curve2d(topods_edge, topods_face)
                curve_type = edge_adaptor.GetType()
            
            if curve_type == GeomAbs_Line :
                self.line(edge_adaptor)
            elif curve_type == GeomAbs_BezierCurve :
                self.bezier(edge_adaptor)
            elif curve_type == GeomAbs_BSplineCurve :
                self.bspline(edge_adaptor, twoD)
            elif curve_type == GeomAbs_Circle :
                self.circle(edge_adaptor)
            else :
                print(f"Unsupported curve type: {curve_type}. Expect inaccurate results")
                start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
                end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
                gp_pnt_poles = [start_point, end_point]
                self.type = EDGES_TYPES['line']
                self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]

    def scale(self, scale_factor):
        self.verts = [v*scale_factor for v in self.verts]

    def line(self, edge_adaptor):
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        gp_pnt_poles = [start_point, end_point]
        self.type = EDGES_TYPES['line']
        self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]

        # if edge!=None :
        #     start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        #     end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        #     poles = [start_point, end_point]
        # else:
        #     start_point = curve_adaptor.Value(curve_adaptor.FirstParameter())
        #     end_point = curve_adaptor.Value(curve_adaptor.LastParameter())
        #     poles = [start_point, end_point]


    def bezier(self, edge_adaptor):
        bezier = edge_adaptor.Bezier()
        gp_pnt_poles = [bezier.Pole(i+1) for i in range(bezier.NbPoles())]
        self.type = EDGES_TYPES['bezier']
        self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]
        # TODO output weights

    def bspline(self, edge_adaptor, twoD):
        # if not twoD :
        #     curve = edge_adaptor.Curve()
        #     if not isinstance(curve, Geom_BSplineCurve):
        #         # first_param = edge_adaptor.FirstParameter()
        #         # last_param = edge_adaptor.LastParameter()
        #         bspline = GeomConvert.CurveToBSplineCurve(curve, Convert_TgtThetaOver2)
        #     else:
        #         bspline = curve

        # else :
        #     # 2D version
        #     bspline = edge_adaptor.BSpline()
        bspline = edge_adaptor.BSpline()
        
        gp_pnt_poles = [bspline.Pole(i+1) for i in range(bspline.NbPoles())]
        self.degree = bspline.Degree()
        self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]
        self.type = EDGES_TYPES['nurbs']
        # TODO output the knot, multiplicities and weights  

    def circle(self, edge_adaptor):
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

        self.verts = [SP_Pole(g).vertex for g in gp_pnt_poles]
    






class SP_Wire :
    def __init__(self, topods_wire: TopoDS_Wire=None, scale=0.001, CP =[], topods_face = None, segs_p_counts=None, segs_degrees=None):
        self.CP = [] #Vectors, bmesh format
        
        # Import
        if topods_wire!=None:
            # vertex aligned attributes
            self.bmesh_edges = [] #int tuple
            self.endpoints_att = [] #float
            self.degree_att = [] #float
            # self.knot_att = [] #float
            # self.weights_att = [] #float
            # self.mult_att = [] #float
            self.circle_att = []

            if topods_face == None :
                self.import_constructor_3d_space(topods_wire, scale)
            else :
                self.import_constructor_uv_space(topods_wire, topods_face)
        
        # Export
        else :
            self.segs_degrees = segs_degrees
            self.CP = [Vector(v) for v in CP]
            self.segs_p_counts = segs_p_counts
            self.export_constructor()

    
    def import_constructor_3d_space(self, topods_wire: TopoDS_Wire, scale):
        topods_edges = get_edges_from_wire(topods_wire)
        wire_is_reversed = topods_wire.Orientation() == 1

        #Edges
        for e in topods_edges :
            sp_edge = SP_Edge(e)
            sp_edge.scale(scale)
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


    def import_constructor_uv_space(self, topods_wire, topods_face):
        
        topods_edges = get_edges_from_wire(topods_wire)
        wire_is_reversed = topods_wire.Orientation() == 1

        #Edges
        for e in topods_edges :
            sp_edge = SP_Edge(e, topods_face)
            e_vert = sp_edge.verts
            e_degree = sp_edge.degree
            e_type = sp_edge.type
            
            # Reverse
            if (e.Orientation() != TopAbs_FORWARD) != wire_is_reversed :
                e_vert.reverse()
            
            # verts_of_edges.append(e_vert)
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





# for export
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




class SP_Contour :
    def __init__(self, topodsface,  scale = None):
        self.wires = get_wires_from_face(topodsface)
        self.verts, self.edges, self.endpoints, self.degrees, self.circles = [], [], [], [], []

        for w in self.wires :
            if scale!=None:
                sp_wire = SP_Wire(topods_wire=w, scale = scale)
            else :
                sp_wire = SP_Wire(topods_wire=w, topods_face=topodsface)
                
            _, self.edges, _ = join_mesh_entities(self.verts, self.edges, [], sp_wire.CP, sp_wire.bmesh_edges, [])
            self.verts.extend(sp_wire.CP)
            self.endpoints.extend(sp_wire.endpoints_att)
            self.degrees.extend(sp_wire.degree_att)
            self.circles.extend(sp_wire.circle_att)
    
    # For square contour following the patch bounds
    def is_trivial(self):
        is_trivial_trim = False
        if len(self.verts) == 4 :
            t1 = self.verts == [Vector((0.0,0.0,0.0)), Vector((0.0,1.0,0.0)), Vector((1.0,1.0,0.0)), Vector((1.0,0.0,0.0)),]
            t2 = self.verts == [Vector((0.0,1.0,0.0)), Vector((1.0,1.0,0.0)), Vector((1.0,0.0,0.0)), Vector((0.0,0.0,0.0)),]
            t3 = self.verts == [Vector((1.0,1.0,0.0)), Vector((1.0,0.0,0.0)), Vector((0.0,0.0,0.0)), Vector((0.0,1.0,0.0)),]
            t4 = self.verts == [Vector((1.0,0.0,0.0)), Vector((0.0,0.0,0.0)), Vector((0.0,1.0,0.0)), Vector((1.0,1.0,0.0)),]

            t5 = self.verts == [Vector((1.0,0.0,0.0)), Vector((1.0,1.0,0.0)), Vector((0.0,1.0,0.0)), Vector((0.0,0.0,0.0)),]
            t6 = self.verts == [Vector((1.0,1.0,0.0)), Vector((0.0,1.0,0.0)), Vector((0.0,0.0,0.0)), Vector((1.0,0.0,0.0)),]
            t7 = self.verts == [Vector((0.0,1.0,0.0)), Vector((0.0,0.0,0.0)), Vector((1.0,0.0,0.0)), Vector((1.0,1.0,0.0)),]
            t8 = self.verts == [Vector((0.0,0.0,0.0)), Vector((1.0,0.0,0.0)), Vector((1.0,1.0,0.0)), Vector((0.0,1.0,0.0)),]
            
            t9 = set(self.edges) == {(0,1), (1,2), (2,3), (3,0)}
            
            is_trivial_trim = (t1 or t2 or t3 or t4 or t5 or t6 or t7 or t8) and t9

        return is_trivial_trim

    def rebound(self, uv_bounds):
        min_u, max_u, min_v, max_v = uv_bounds[0], uv_bounds[1], uv_bounds[2], uv_bounds[3]
        range_u, range_v = max_u - min_u, max_v - min_v

        for i,v in enumerate(self.verts) :
            x=max(0, min(1, (v[0]-min_u)/range_u))
            y=max(0, min(1, (v[1]-min_v)/range_v))
            self.verts[i] = Vector((x, y, 0))





class SP_surface :
    # Importer class, to unify
    def __init__(self, face : TopoDS_Face, collection, trims_enabled : bool, uv_bounds, CPvert, CPedges, CPfaces, ob_name = "STEP Patch", scale=0.001):
        self.trims_enabled = trims_enabled
        self.face = face
        self.uv_bounds = uv_bounds
        self.CPvert = CPvert
        self.CPedges = CPedges
        self.CPfaces = CPfaces
        self.vert, self.edges, self.faces = [],[],[]
        
        if trims_enabled :
            contour = SP_Contour(face)
            contour.rebound(uv_bounds)
            istrivial = contour.is_trivial()
            if istrivial :
                print("Trivial contour skipped")
                self.vert, self.edges, self.faces = self.CPvert, self.CPedges, self.CPfaces
                del contour
            else :
                self.vert, self.edges, self.faces = join_mesh_entities(CPvert, CPedges, CPfaces, contour.verts, contour.edges, [])           
        else :
            self.vert, self.edges, self.faces = self.CPvert, self.CPedges, self.CPfaces

        mesh = bpy.data.meshes.new("Patch CP")
        mesh.from_pydata(self.vert, self.edges, self.faces, False)
        self.ob = bpy.data.objects.new(ob_name, mesh)
        
        if trims_enabled and not istrivial :
            self.assign_vertex_gr("Trim Contour", [0.0]*len(CPvert) + [1.0]*len(contour.verts))
            self.assign_vertex_gr("Endpoints", [0.0]*len(CPvert) + contour.endpoints)
            self.assign_vertex_gr("Degree", [0.0]*len(CPvert) + contour.degrees)

        collection.objects.link(self.ob)

    def assign_vertex_gr(self, name, values):
        add_vertex_group(self.ob, name, values)
        
    def add_modifier(self, name, settings_dict = {}, pin=False):
        add_sp_modifier(self.ob, name, settings_dict, pin = pin)




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