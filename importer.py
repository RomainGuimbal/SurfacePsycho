import bpy
import numpy as np
from mathutils import Vector
from os.path import abspath, splitext, split, isfile
from .utils import *
# from .utils import list_of_shapes_to_compound
import unicodedata
from concurrent.futures import ThreadPoolExecutor
import typing

# from OCP.Geom2dAdaptor import Geom2dAdaptor_Curve
# from OCP.GeomAbs import GeomAbs_Line, GeomAbs_BSplineCurve, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface #BRepAdaptor_Curve
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
# from OCP.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve, Geom_CylindricalSurface, Geom_Line, Geom_ToroidalSurface
from OCP.GeomAbs import GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_Line, GeomAbs_Circle, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
# from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pnt, gp_Pnt2d
from OCP.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
# from OCP.IGESCAFControl import IGESCAFControl_Reader
from OCP.IGESControl import IGESControl_Controller, IGESControl_Reader
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB, Quantity_ColorRGBA
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FORWARD, TopAbs_REVERSED #, TopAbs_INTERNAL, TopAbs_EXTERNAL, TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS, TopoDS_Iterator, TopoDS_Wire, TopoDS_Edge, TopoDS_Face, TopoDS_Shape, TopoDS_Compound
# from OCP.TopTools import TopTools_IndexedMapOfShape
# from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorTool, XCAFDoc_ShapeTool, XCAFDoc_ColorCurv, XCAFDoc_ColorSurf, XCAFDoc_ColorGen 
import OCP.GeomAbs as GeomAbs
import OCP.TopAbs as TopAbs



##############################
##    Converter classes     ##
##############################

class SP_Pole_import :
    def __init__(self, gp_pole):
        if isinstance(gp_pole, gp_Pnt2d) : 
            self.vertex = Vector((gp_pole.X(), gp_pole.Y(), 0))
        else :
            self.vertex = Vector((gp_pole.X(), gp_pole.Y(), gp_pole.Z()))
    
        # self.weight ?


class SP_Edge_import :
    def __init__(self, topods_edge : TopoDS_Edge, topods_face = None, scale = None):
        self.verts = None
        self.degree = None
        self.degree_att = []
        self.type = None
        self.circle_att = []
        self.endpoints_att = []
        self.weight = []
        self.mult = []
        self.knot = []
        
        # Edge adaptor
        # 3D
        if topods_face is None:
            is2D=False
            edge_adaptor = BRepAdaptor_Curve(topods_edge)
            curve_type = edge_adaptor.Curve().GetType()
        #2D
        else :
            is2D=True
            edge_adaptor = BRepAdaptor_Curve2d(topods_edge, topods_face)
            curve_type = edge_adaptor.GetType()
        
        self.isclosed = edge_adaptor.IsClosed()

        if curve_type == GeomAbs_Line :
            self.line(edge_adaptor)
        elif curve_type == GeomAbs_BezierCurve :
            self.bezier(edge_adaptor)
        elif curve_type == GeomAbs_BSplineCurve :
            self.bspline(edge_adaptor)
        elif curve_type == GeomAbs_Circle :
            self.circle(edge_adaptor)
        else :
            print(f"Unsupported curve type: {curve_type}. Expect inaccurate results")
            start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
            end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
            gp_pnt_poles = [start_point, end_point]
            self.type = EDGES_TYPES['line']
            self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]

        # Reverse
        if topods_edge.Orientation() != TopAbs_FORWARD and self.type != EDGES_TYPES['circle']:
            self.verts.reverse()
            #circle, endpoints, degree are symmetric

        if scale!=None : 
            self.scale(scale)

    def scale(self, scale_factor):
        self.verts = [v*scale_factor for v in self.verts]

    def line(self, edge_adaptor):
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        gp_pnt_poles = [start_point, end_point]
        self.type = EDGES_TYPES['line']
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
        self.degree_att = [0.0,0.0]
        self.circle_att = [0.0,0.0]
        self.endpoints_att = [1.0,1.0]
        self.weight = [0.0,0.0]
        self.knot = [0.0,0.0]
        self.mult = [0,0]

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
        p_count = bezier.NbPoles()
        gp_pnt_poles = [bezier.Pole(i+1) for i in range(p_count)]
        self.type = EDGES_TYPES['bezier']
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
        self.degree_att = [0.0]*p_count
        self.circle_att = [0.0]*p_count
        self.endpoints_att = [1.0] + [0.0]*(p_count-2) + [1.0]
        self.weight = [bezier.Weight(i+1) for i in range(p_count)]
        self.knot = [0.0]*p_count
        self.mult = [0]*p_count

    def bspline(self, edge_adaptor):
        bspline = edge_adaptor.BSpline()
        p_count = bspline.NbPoles()
        gp_pnt_poles = [bspline.Pole(i+1) for i in range(p_count)]
        self.degree = bspline.Degree()
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
        self.type = EDGES_TYPES['nurbs']
        self.degree_att = [bspline.Degree()/10] + [0.0]*(p_count-2) + [bspline.Degree()/10]
        self.circle_att = [0.0]*p_count
        if edge_adaptor.BSpline().Multiplicity(1) == 1 : # unclamped periodic
            self.endpoints_att = [0.0]*p_count
        else :
            self.endpoints_att = [1.0] + [0.0]*(p_count-2) + [1.0]
        self.weight = [bspline.Weight(i+1) for i in range(p_count)]

        knot = normalize_array(tcolstd_array1_to_list(bspline.Knots()))
        mult = tcolstd_array1_to_list(bspline.Multiplicities())
        self.knot = knot + [0.0]*(p_count-len(knot))
        self.mult = mult + [0]*(p_count-len(mult))

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
            
            self.degree_att = [0.0,0.0,0.0]
            self.circle_att = [0.0,1.0,0.0]
            self.endpoints_att = [1.0,0.0,1.0]
            self.weight = [0.0,0.0,0.0]
            self.knot = [0.0,0.0,0.0]
            self.mult = [0,0,0]

        else:
            # arc from 3 pts
            min_t = edge_adaptor.FirstParameter()
            max_t = edge_adaptor.LastParameter()
            
            start_point = edge_adaptor.Value(min_t)
            end_point = edge_adaptor.Value(max_t)
            range_t = max_t - min_t

            # full circle
            if start_point == end_point or isclose(range_t, math.pi*2):
                center = edge_adaptor.Circle().Location()
                gp_pnt_poles = [center, start_point]
                self.type = EDGES_TYPES['circle']
                self.degree_att = [0.0,0.0]
                self.circle_att = [1.0,1.0]
                self.endpoints_att = [1.0,1.0]
                self.weight = [0.0,0.0]
                self.knot = [0.0,0.0]
                self.mult = [0,0,0]
            else: # arc
                mid_t = (max_t - min_t)/2 + min_t
                mid_point = edge_adaptor.Value(mid_t)
                gp_pnt_poles = [start_point, mid_point, end_point]
                self.type = EDGES_TYPES['circle_arc']
                # self.circle_arc_subtype = 1. # tree_points
                self.degree_att = [0.0,0.0,0.0]
                self.circle_att = [0.0,1.0,0.0]
                self.endpoints_att = [1.0,0.0,1.0]
                self.weight = [0.0,0.0,0.0]
                self.knot = [0.0,0.0,0.0]
                self.mult = [0,0,0]

        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]



class SP_Wire_import :
    def __init__(self, topods_wire: TopoDS_Wire, scale=1, topods_face = None):
        self.CP = [] #Vectors, bmesh format
        # Import
        if topods_wire!=None:
            # vertex aligned attributes
            self.bmesh_edges = [] #int tuple
            self.endpoints_att = []
            self.degree_att = []
            self.circle_att = []
            self.weight_att = []
            self.knot_att = []
            self.mult_att = []

        topods_edges = get_edges_from_wire(topods_wire)
        is_wire_forward = topods_wire.Orientation() == TopAbs_FORWARD

        # iterate Edges
        for e in topods_edges :
            sp_edge = SP_Edge_import(e, topods_face, scale)
            e_vert = sp_edge.verts
            e_type = sp_edge.type

            if not is_wire_forward :
                e_vert.reverse()
                # other att are symmetric

            self.CP.extend(e_vert[:-1])
            self.endpoints_att.extend(sp_edge.endpoints_att[:-1])
            self.degree_att.extend(sp_edge.degree_att[:-1])
            self.circle_att.extend(sp_edge.circle_att[:-1])
            self.weight_att.extend(sp_edge.weight[:-1])
            self.knot_att.extend(sp_edge.knot[:-1])
            self.mult_att.extend(sp_edge.mult[:-1])
            
        # Add last point for single edge wire
        if len(topods_edges)==1 : # Skip circle (unclosed control mesh structure for single segment wire)
                                  # OR closed single wire
                                  # OR single segment curve
            # if sp_edge.isclosed :
            self.CP.append(e_vert[-1])
            self.endpoints_att.append(sp_edge.endpoints_att[-1])
            self.degree_att.append(sp_edge.degree_att[-1])
            self.circle_att.append(sp_edge.circle_att[-1])
            self.weight_att.append(sp_edge.weight[-1])
            self.knot_att.append(sp_edge.knot[-1])
            self.mult_att.append(sp_edge.mult[-1])

        # Open mesh structure
        if e_type == EDGES_TYPES['circle'] or not topods_wire.Closed(): 
            self.bmesh_edges = [(i, i+1) for i in range(len(self.CP)-1)]
        # Closed mesh structure
        else :
            self.bmesh_edges = [(i, ((i+1)%len(self.CP))) for i in range(len(self.CP))]




class SP_Contour_import :
    def __init__(self, topodsface,  scale = None):
        self.wires = get_wires_from_face(topodsface)
        self.verts, self.edges, self.endpoints, self.degrees, self.circles, self.weight, self.knot, self.mult = [], [], [], [], [], [], [], []
        
        for w in self.wires :
            if scale!=None:
                sp_wire = SP_Wire_import(w, scale = scale)
            else :
                sp_wire = SP_Wire_import(w, topods_face=topodsface)
                
            _, self.edges, _ = join_mesh_entities(self.verts, self.edges, [], sp_wire.CP, sp_wire.bmesh_edges, [])
            self.verts.extend(sp_wire.CP)
            self.endpoints.extend(sp_wire.endpoints_att)
            self.degrees.extend(sp_wire.degree_att)
            self.circles.extend(sp_wire.circle_att)
            self.weight.extend(sp_wire.weight_att)
            self.knot.extend(sp_wire.knot_att)
            self.mult.extend(sp_wire.mult_att)

    # For square contour following the patch bounds
    def is_trivial(self):
        is_trivial_trim = False
        if len(self.verts) == 4 :

            # print(self.verts)

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
            if range_u !=0.0 :
                x=max(0, min(1, (v[0]-min_u)/range_u))
            else :
                x = v[0]
            if range_v !=0.0 :
                y=max(0, min(1, (v[1]-min_v)/range_v))
            else :
                y = v[1]
            self.verts[i] = Vector((x, y, 0))
    
    def switch_u_and_v(self):
        self.verts = [Vector((v.y, v.x, v.z)) for v in self.verts]



def generic_import_surface(face : TopoDS_Face, doc, collection, trims_enabled : bool, 
                            CPvert, CPedges, CPfaces, modifier, attrs={}, ob_name = "STEP Patch",
                            scale=0.001, uv_bounds=None, weight=None):
    if weight == None :
        weight = [1.]*len(CPvert)

    transform = get_shape_transform(face, scale)
    
    if trims_enabled :
        contour = SP_Contour_import(face)
        if uv_bounds!=None :
            contour.rebound(uv_bounds)

        contour.switch_u_and_v()
        istrivial = contour.is_trivial()
        
        if istrivial : 
            del contour
    
    if trims_enabled and not istrivial :
        mesh_data = join_mesh_entities(CPvert, CPedges, CPfaces, contour.verts, contour.edges, [])           
        attrs = attrs | {'Weight' : weight + contour.weight,
                'Knot' : [0.0]*len(CPvert) + contour.knot,
                'Multiplicity': [0.0]*len(CPvert) + contour.mult,
                'Trim Contour' : [0.0]*len(CPvert) + [1.0]*len(contour.verts),
                'Endpoints' : [0.0]*len(CPvert) + contour.endpoints,
                'Degree': [0.0]*len(CPvert) + contour.degrees,
                'Circle': [0.0]*len(CPvert) + contour.circles,
                }
    else :
        mesh_data = (CPvert, CPedges, CPfaces)
        attrs = attrs | {'Weight' : weight}

    name, color = get_shape_name_and_color(face, doc)
    if name == None:
        name = ob_name

    if len(color)==3:
        color = list(color) + [1.]
        
    object_data = {
        'mesh_data': mesh_data,
        'name': name,
        'collection' : collection,
        'scale': scale,
        'color': color,
        'attrs' : attrs,
        'modifier': modifier,
        'transform': transform,
    }

    return object_data










def build_SP_cylinder(topods_face : TopoDS_Face, doc, collection, trims_enabled, scale = 0.001) :
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_cylinder = face_adpator.Surface().Cylinder()
    
    gpaxis= gp_cylinder.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_cylinder.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_cylinder.Location()
    loc_vec = Vector((location.X()*scale, location.Y()*scale, location.Z()*scale))
    radius = gp_cylinder.Radius()*scale

    raduis_vert = Vector((zaxis_vec*radius) + loc_vec)

    CPvert = [loc_vec, xaxis_vec*scale + loc_vec, raduis_vert]
    CP_edges = [(0,1)]
    
    modifier = ("SP - Cylindrical Meshing", 
                    {"Use Trim Contour":trims_enabled, 
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED, 
                    "Scaling Method":1,},
                True)

    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, 
                                         CPvert, CP_edges, [], modifier, ob_name= "STEP Cylinder")
    
    return object_data




def build_SP_torus(topods_face : TopoDS_Face, doc, collection, trims_enabled, scale = 0.001) :
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_torus = face_adpator.Surface().Torus()
    
    gpaxis= gp_torus.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_torus.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_torus.Location()
    origin_vec = Vector((location.X()*scale, location.Y()*scale, location.Z()*scale))
    major_radius = gp_torus.MajorRadius()*scale

    minor_radius =  gp_torus.MinorRadius()*scale
    raduis_vert = Vector((zaxis_vec*major_radius) + origin_vec)
    
    CPvert = [origin_vec, raduis_vert, -xaxis_vec*minor_radius + raduis_vert]
    CP_edges = [(0,1),(1,2)]

    modifier = ("SP - Toroidal Meshing",
                {"Use Trim Contour":trims_enabled,
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED,
                    "Scaling Method" : 1,
                    "Resolution U" : 16,
                    "Resolution V" : 32}, 
                True)
    
    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, CPvert, CP_edges, [], modifier, ob_name= "STEP Torus")

    return object_data



def build_SP_sphere(topods_face : TopoDS_Face, doc, collection, trims_enabled, scale = 0.001) :
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_sphere = face_adpator.Surface().Sphere()
    
    gpaxis= gp_sphere.XAxis()
    xaxis = gpaxis.Direction()
    yaxis = gp_sphere.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = Vector(np.cross(yaxis_vec, xaxis_vec))

    location = gp_sphere.Location()
    loc_vec = Vector((location.X()*scale, location.Y()*scale, location.Z()*scale))
    radius = gp_sphere.Radius()*scale

    CPvert = [loc_vec - zaxis_vec*radius, loc_vec + zaxis_vec*radius, yaxis_vec*radius + loc_vec]
    CP_edges = [(0,1)]

    modifier = ("SP - Spherical Meshing",
                    {"Use Trim Contour":trims_enabled,
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED,
                    "Scaling Method":1,}, 
                True)
    
    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, CPvert, CP_edges, [], modifier, ob_name= "STEP Sphere")
    return object_data


def build_SP_cone(topods_face : TopoDS_Face, doc, collection, trims_enabled, scale = 0.001) :
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_cone = face_adpator.Surface().Cone()
    
    gpaxis= gp_cone.Axis()
    axis = gpaxis.Direction()
    yaxis = gp_cone.YAxis().Direction()
    axis_vec = Vector([axis.X(), axis.Y(), axis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    # zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_cone.Location()
    loc_vec = Vector((location.X()*scale, location.Y()*scale, location.Z()*scale))
    radius = gp_cone.RefRadius()
    
    CPvert = [loc_vec, loc_vec + yaxis_vec*radius*scale, axis_vec*math.cos(gp_cone.SemiAngle())*scale + loc_vec + yaxis_vec*(math.sin(gp_cone.SemiAngle())+radius)*scale,  axis_vec*math.cos(gp_cone.SemiAngle())*scale + loc_vec]
    CP_edges = [(0,1),(1,2),(2,3)]

    modifier = ("SP - Conical Meshing", 
                    {"Use Trim Contour":trims_enabled, 
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED,
                    "Scaling Method":1,},
                True)
    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, CPvert, CP_edges, [], modifier, ob_name= "STEP Cone")
    
    return object_data





def build_SP_bezier_patch(topods_face, doc, collection, trims_enabled, scale = 0.001, resolution = 16):
    bezier_surface = BRepAdaptor_Surface(topods_face).Surface().Bezier()

    u_count, v_count = bezier_surface.NbUPoles(), bezier_surface.NbVPoles()
    uv_bounds = bezier_surface.Bounds()
    vector_pts = np.zeros((u_count, v_count), dtype=Vector)
    weight = np.ones((v_count, u_count), dtype=float)
    for u in range(1, u_count + 1):
        for v in range(1, v_count + 1):
            pole = bezier_surface.Pole(u, v)
            vector_pts[u-1, v-1] = Vector((pole.X(), pole.Y(), pole.Z()))*scale

            weight[u,v] = bezier_surface.Weight(u, v)
    
    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)
   
    modifier = ("SP - Bezier Patch Meshing", 
                    {"Use Trim Contour":trims_enabled,
                    "Resolution U": resolution,
                    "Resolution V": resolution,
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED,
                    "Scaling Method":1}, 
                True)

    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, CPvert.tolist(), 
                                [], CPfaces, modifier, uv_bounds = uv_bounds,
                                 weight = weight.flatten().tolist())
    return object_data



    
def build_SP_NURBS_patch(topods_face, doc, collection, trims_enabled, scale = 0.001, resolution = 16):
    # Patch attributes
    bspline_surface = BRepAdaptor_Surface(topods_face).Surface().BSpline()
    u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()
    udeg = bspline_surface.UDegree()
    vdeg = bspline_surface.VDegree()
    u_closed = bspline_surface.IsUClosed()
    v_closed = bspline_surface.IsVClosed()
    u_periodic = bspline_surface.IsUPeriodic()
    v_periodic = bspline_surface.IsVPeriodic()
    uv_bounds = bspline_surface.Bounds()
    u_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.UKnots()))
    v_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.VKnots()))
    u_mult = tcolstd_array1_to_list(bspline_surface.UMultiplicities())
    v_mult = tcolstd_array1_to_list(bspline_surface.VMultiplicities())
    
    # Custom knot
    custom_knot = False
    # not custom if sequence a...a,b...b (bezier)
    if any(x not in [min(u_knots), max(u_knots)] for x in u_knots) or any(x not in [min(v_knots), max(v_knots)] for x in v_knots):
        custom_knot = True
    # TODO
    # else :
    #    Convert to bezier then
    #    build_SP_BezierPatch(...)

    # Vertex aligned attributes

    # CP Grid
    vector_pts = np.zeros((v_count + v_closed, u_count + u_closed), dtype=Vector)
    weight = np.ones((v_count + v_closed, u_count + u_closed), dtype=float)
    for u in range(u_count):
        for v in range(v_count):
            pole = bspline_surface.Pole(u+1, v+1)
            vector_pts[v, u] = Vector((pole.X(), pole.Y(), pole.Z()))*scale
            
            w = bspline_surface.Weight(u+1, v+1)
            weight[v, u] = w

    if u_closed :
        vector_pts[:,u_count] = vector_pts[:,0]
        weight[:,u_count] = weight[:,0]
    if v_closed :
        vector_pts[v_count,:] = vector_pts[0,:]
        weight[v_count,:] = weight[0,:]

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)

    attrs = {}
    if custom_knot: # must be attr and not vertex groups to avoid collisions at export
        attrs = {"Knot U" : u_knots,
                 "Knot V": v_knots,
                 "Multiplicity U": u_mult,
                 "Multiplicity V": v_mult
                }
    
    # If 1 mult not 1 or no custom knot -> clamp
    u_clamped = any(m!=1 for m in u_mult) or not custom_knot
    v_clamped = any(m!=1 for m in v_mult) or not custom_knot

    # Meshing
    modifier = ("SP - NURBS Patch Meshing",
                    {"Degree U": udeg,
                     "Degree V": vdeg,
                    "Resolution U": resolution,
                    "Resolution V": resolution, 
                    "Flip Normals" : topods_face.Orientation()!=TopAbs_REVERSED,
                    "Use Trim Contour":trims_enabled, "Scaling Method": 1,
                    "Endpoint U" : u_clamped, "Endpoint V" : v_clamped,
                    "Cyclic U": u_periodic,  "Cyclic V": v_periodic}, 
                True)
    
    

    object_data = generic_import_surface(topods_face, doc, collection, trims_enabled, 
                                         CPvert.tolist(), [], CPfaces, modifier, attrs, uv_bounds = uv_bounds, 
                                         weight = weight.flatten().tolist())
    return object_data






def build_SP_curve(shape, doc, collection, scale = 0.001, resolution = 16) :
    if shape.ShapeType() == TopAbs.TopAbs_WIRE:
        sp_wire = SP_Wire_import(shape, scale=scale)
        verts = sp_wire.CP
        edges = sp_wire.bmesh_edges
        endpoints = sp_wire.endpoints_att
        degree_att = sp_wire.degree_att
        circle_att = sp_wire.circle_att
        weight_att = sp_wire.weight_att
        knot_att = sp_wire.knot_att
        mult_att = sp_wire.mult_att
    else :
        sp_edge = SP_Edge_import(shape)
        sp_edge.scale(scale)
        verts = sp_edge.verts
        edge_degree = sp_edge.degree
        weight_att = sp_edge.weight
        knot_att = sp_edge.knot
        mult_att = sp_edge.mult

        endpoints = [1.0] + [0.0]*(len(verts)-2) + [1.0]
        if edge_degree!=None:
            degree_att=[edge_degree/10]+[0.0]*(len(verts)-1)
        else :
            degree_att=[0.0]*(len(verts))

        if sp_edge.type == EDGES_TYPES['circle']:
            circle_att = [0.0, 1.0, 0.0]
        else :
            circle_att = [0.0]*(len(verts))

        edges = [(i,i+1) for i in range(len(verts)-1)]

    # create object
    name, color = get_shape_name_and_color(shape, doc)
    if name == None:
        name = "STEP Curve"
    mesh = bpy.data.meshes.new("Curve CP")
    mesh.from_pydata(verts, edges, [], False)
    ob = bpy.data.objects.new(name, mesh)
    ob.matrix_world = get_shape_transform(shape, scale)
    
    if len(color)==3:
        ob.color = list(color) + [1.]
    elif len(color)==4 :
        ob.color = color

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Degree", degree_att)
    add_vertex_group(ob, "Circle", circle_att)
    add_vertex_group(ob, "Weight", weight_att)
    add_float_attribute(ob, "Knot", knot_att)
    add_int_attribute(ob, "Multiplicity", mult_att)


    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Curve Meshing",
                    {"Resolution": resolution}, pin=True)

    return True






def build_SP_flat(topods_face, doc, collection, scale = 0.001):
    # Get contour
    contour = SP_Contour_import(topods_face, scale)
    verts = contour.verts
    edges = contour.edges
    endpoints = contour.endpoints
    degree_att = contour.degrees
    circle_att = contour.circles
    weight_att = contour.weight
    knot_att = contour.knot
    mult_att = contour.mult

    name, color = get_shape_name_and_color(topods_face, doc)
    if name == None:
        name = "STEP FlatPatch"

    if len(color)==3:
        color = list(color) + [1.]

    modifier = ("SP - FlatPatch Meshing", 
                {'Orient': True,
                "Flip Normal" : topods_face.Orientation()!=TopAbs_REVERSED,}, True)
    
    attrs = {'Weight' : weight_att,
            'Knot' : knot_att,
            'Multiplicity': mult_att,
            'Endpoints' : endpoints,
            'Degree': degree_att,
            'Circle': circle_att,
            }
    
    object_data = {
        'mesh_data': (verts, edges, []),
        'name': name,
        'collection' : collection,
        'scale': scale,
        'color': color,
        'attrs' : attrs,
        'modifier': modifier,
        'transform': Matrix(),
    }

    return object_data








class ShapeHierarchy:
    def __init__(self, shape, container_name):
        self.faces = [] # tuples (face, collection)
        self.edges = [] # tuples (edges, collection)
        self.hierarchy = {}
        container_collection = self.create_collection(container_name)
        self.hierarchy[container_collection] = []
        iterator = TopoDS_Iterator(shape)
        while iterator.More():
            self.hierarchy[container_collection].append(self.create_shape_hierarchy(iterator.Value(), container_collection))
            iterator.Next()

    def create_collection(self, name, parent=None):
        new_collection = bpy.data.collections.new(name)

        # If no parent, link to scene collection
        if parent is None :
            bpy.context.scene.collection.children.link(new_collection)
        else:
            parent.children.link(new_collection)

        return new_collection

    def create_shape_hierarchy(self, shape, parent_col):
        hierarchy = {}
        
        match shape.ShapeType():
            case TopAbs.TopAbs_COMPOUND :
                hierarchy[parent_col] = []
                new_collection = self.create_collection('Compound', parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(self.create_shape_hierarchy(iterator.Value(), new_collection))
                    iterator.Next()

            case TopAbs.TopAbs_COMPSOLID :
                hierarchy[parent_col] = []
                new_collection = self.create_collection('CompSolid', parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(self.create_shape_hierarchy(iterator.Value(), new_collection))
                    iterator.Next()
        
            case TopAbs.TopAbs_SOLID:
                hierarchy[parent_col] = []
                new_collection = self.create_collection('Solid', parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(self.create_shape_hierarchy(iterator.Value(), new_collection))
                    iterator.Next()
        
            case TopAbs.TopAbs_SHELL:
                hierarchy[parent_col] = []
                new_collection = self.create_collection('Shell', parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(self.create_shape_hierarchy(iterator.Value(), new_collection))
                    iterator.Next()
        
            case TopAbs.TopAbs_FACE: # must be before wire and edge
                face = TopoDS.Face_s(shape)
                hierarchy['Face'] = face
                self.faces.append((face, parent_col))

            case TopAbs.TopAbs_WIRE:
                wire = TopoDS.Wire_s(shape)
                hierarchy['Wire'] = wire
                self.edges.append((wire, parent_col))
        
            case TopAbs.TopAbs_EDGE:
                edge = TopoDS.Edge_s(shape)
                hierarchy['Edge'] = edge
                self.edges.append((edge, parent_col))
                
        return hierarchy



def import_face_nodegroups(shape_hierarchy):
    to_import_ng_names = set()
    face_encountered = set()

    for face, _ in shape_hierarchy.faces: 
        ft= get_face_type_id(face)
        face_encountered.add(ft)
        match ft:
            case GeomAbs.GeomAbs_Plane:
                to_import_ng_names.add("SP - FlatPatch Meshing")
            case GeomAbs.GeomAbs_Cylinder:
                to_import_ng_names.add("SP - Cylindrical Meshing")
            case GeomAbs.GeomAbs_BezierSurface:
                to_import_ng_names.add("SP - Bezier Patch Meshing")
            case GeomAbs.GeomAbs_BSplineSurface:
                to_import_ng_names.add("SP - NURBS Patch Meshing")
            case GeomAbs.GeomAbs_Torus:
                to_import_ng_names.add("SP - Toroidal Meshing")
            case GeomAbs.GeomAbs_Sphere:
                to_import_ng_names.add("SP - Spherical Meshing")
            case GeomAbs.GeomAbs_Cone:
                to_import_ng_names.add("SP - Conical Meshing")
    
    append_multiple_node_groups(to_import_ng_names)



def process_topods_face(topods_face, doc, collection, trims_enabled, scale, resolution):
    ft= get_face_type_id(topods_face)
    match ft:
        case GeomAbs.GeomAbs_Plane:
            object_data = build_SP_flat(topods_face, doc, collection, scale)
        case GeomAbs.GeomAbs_Cylinder:
            object_data = build_SP_cylinder(topods_face, doc, collection, trims_enabled, scale )
        case GeomAbs.GeomAbs_BezierSurface:
            object_data = build_SP_bezier_patch(topods_face, doc, collection, trims_enabled, scale, resolution)
        case GeomAbs.GeomAbs_BSplineSurface:
            object_data = build_SP_NURBS_patch(topods_face, doc, collection, trims_enabled, scale, resolution)
        case GeomAbs.GeomAbs_Torus:
            object_data = build_SP_torus(topods_face, doc, collection, trims_enabled, scale )
        case GeomAbs.GeomAbs_Sphere:
            object_data = build_SP_sphere(topods_face, doc, collection, trims_enabled, scale ) 
        case GeomAbs.GeomAbs_Cone:
            object_data = build_SP_cone(topods_face, doc, collection, trims_enabled, scale )
        case _ :
            print("Unsupported Face Type : " + get_face_type_name(topods_face))
            return {}
    return object_data



def create_blender_object(object_data):
    if object_data == {}:
        return False
    
    mesh = bpy.data.meshes.new(object_data['name'])
    vert, edges, faces = object_data['mesh_data']
    mesh.from_pydata(vert, edges, faces, False)   
    ob = bpy.data.objects.new(object_data['name'], mesh)
    ob.matrix_world = object_data['transform']
    ob.color = object_data['color']

    for name, att in object_data['attrs'].items() :
        match att[0] :
            case float() :
                add_float_attribute(ob, name, att)
            case int() :
                add_int_attribute(ob, name, att)

    name, param, pin = object_data['modifier']
    add_sp_modifier(ob, name, param, pin)

    object_data['collection'].objects.link(ob)
    return True



def prepare_import(filepath):
    # Create document
    doc = None

    # STEP
    if splitext(split(filepath)[1])[1].lower() in ['.step', '.stp']:
        shape = read_step_file(filepath)
        if shape == None :
            return False
        # _toplevel_shapes, doc = read_step_file_with_names_colors(filepath)
        # #(topods_shape, label, color)
        # shape = list(_toplevel_shapes.items())[0][0]
        # print(len(list(_toplevel_shapes.items())))

    # IGES
    elif splitext(split(filepath)[1])[1] in ['.igs','.iges','.IGES', '.IGS']:
        iges_reader = IGESControl_Reader()
        status = iges_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading IGES file")
        iges_reader.TransferRoots()
        shape = iges_reader.OneShape()
        # shape = read_iges_file(filepath)
    
    container_name = splitext(split(filepath)[1])[0]

    return shape, doc, container_name










#######################################
# Step import adapted from Build 123d #
#######################################

# def import_step(filepath):

#     def get_name(label: TDF_Label) -> str:
#         """Extract name and format"""
#         name = ""
#         std_name = TDataStd_Name()
#         if label.FindAttribute(TDataStd_Name.GetID_s(), std_name):
#             name = TCollection_AsciiString(std_name.Get()).ToCString()
#         # Remove characters that cause ocp_vscode to fail
#         clean_name = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
#         return clean_name.translate(str.maketrans(" .()", "____"))

#     def get_color(shape: TopoDS_Shape) -> Quantity_ColorRGBA:
#         """Get the color - take that of the largest Face if multiple"""

#         def get_col(obj: TopoDS_Shape) -> Quantity_ColorRGBA:
#             col = Quantity_ColorRGBA()
#             if (
#                 color_tool.GetColor(obj, XCAFDoc_ColorCurv, col)
#                 or color_tool.GetColor(obj, XCAFDoc_ColorGen, col)
#                 or color_tool.GetColor(obj, XCAFDoc_ColorSurf, col)
#             ):
#                 return col

#         shape_color = get_col(shape)

#         colors = {}
#         face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
#         while face_explorer.More():
#             current_face = face_explorer.Current()
#             properties = GProp_GProps()
#             BRepGProp.SurfaceProperties_s(current_face, properties)
#             area = properties.Mass()
#             color = get_col(current_face)
#             if color is not None:
#                 colors[area] = color
#             face_explorer.Next()

#         # If there are multiple colors, return the one from the largest face
#         if colors:
#             shape_color = sorted(colors.items())[-1][1]

#         return shape_color

#     def build_assembly(parent_tdf_label: TDF_Label | None = None) -> list[TopoDS_Shape]:
#         """Recursively extract object into an assembly"""
#         sub_tdf_labels = TDF_LabelSequence()
#         if parent_tdf_label is None:
#             shape_tool.GetFreeShapes(sub_tdf_labels)
#         else:
#             shape_tool.GetComponents_s(parent_tdf_label, sub_tdf_labels)

#         sub_shapes: list[TopoDS_Shape] = []
#         for i in range(sub_tdf_labels.Length()):
#             sub_tdf_label = sub_tdf_labels.Value(i + 1)
#             if shape_tool.IsReference_s(sub_tdf_label):
#                 ref_tdf_label = TDF_Label()
#                 shape_tool.GetReferredShape_s(sub_tdf_label, ref_tdf_label)
#             else:
#                 ref_tdf_label = sub_tdf_label

#             sub_topo_shape = downcast(shape_tool.GetShape_s(ref_tdf_label))
#             if shape_tool.IsAssembly_s(ref_tdf_label):
#                 sub_shape = TopoDS_Compound()
#                 sub_shape.children = build_assembly(ref_tdf_label)
#             else:
#                 sub_shape = topods_lut[type(sub_topo_shape)](sub_topo_shape)

#             sub_shape.color = get_color(sub_topo_shape)
#             sub_shape.label = get_name(ref_tdf_label)
#             sub_shape.move(shape_tool.GetLocation_s(sub_tdf_label))

#             sub_shapes.append(sub_shape)
#         return sub_shapes

#     fmt = TCollection_ExtendedString("XCAF")
#     doc = TDocStd_Document(fmt)
#     shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
#     color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
#     reader = STEPCAFControl_Reader()
#     reader.SetNameMode(True)
#     reader.SetColorMode(True)
#     reader.SetLayerMode(True)
#     reader.ReadFile(filepath)
#     reader.Transfer(doc)

#     root = TopoDS_Compound()
#     root.children = build_assembly()
#     # Remove empty Compound wrapper if single free object
#     if len(root.children) == 1:
#         root = root.children[0]

#     return root, doc






########################################
# Step import adapted from OCC Extends #
########################################

def read_step_file(filename, as_compound=True, verbosity=True):
    """read the STEP file and returns a compound
    filename: the file path
    verbosity: optional, False by default.
    as_compound: True by default. If there are more than one shape at root,
    gather all shapes into one compound. Otherwise returns a list of shapes.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Error: can't read file.")
    if verbosity:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    transfer_result = step_reader.TransferRoots()
    if not transfer_result:
        raise AssertionError("Transfer failed.")
    _nbs = step_reader.NbShapes()
    if _nbs == 0:
        raise AssertionError("No shape to transfer.")
    if _nbs == 1:  # most cases
        return step_reader.Shape(1)
    if _nbs > 1:
        print("Number of shapes:", _nbs)
        shps = []
        # loop over root shapes
        for k in range(1, _nbs + 1):
            new_shp = step_reader.Shape(k)
            if not new_shp.IsNull():
                shps.append(new_shp)
        if as_compound:
            compound, result = list_of_shapes_to_compound(shps)
            if not result:
                print("Warning: all shapes were not added to the compound")
            return compound
        print("Warning, returns a list of shapes.")
        return shps
    return None




def read_step_file_with_names_colors(filename):
    """Returns list of tuples (topods_shape, label, color)
    Use OCAF.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")
    # the list:
    output_shapes = {}

    # create an handle to a document
    doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc-step-import"))

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    step_reader = STEPCAFControl_Reader()
    step_reader.SetColorMode(True)
    step_reader.SetLayerMode(True)
    step_reader.SetNameMode(True)
    step_reader.SetMatMode(True)
    step_reader.SetGDTMode(True)

    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        step_reader.Transfer(doc)

    locs = []

    def get_name(label: TDF_Label) -> str:
        """Extract name and format"""
        name = ""
        std_name = TDataStd_Name()
        if label.FindAttribute(TDataStd_Name.GetID_s(), std_name):
            name = TCollection_AsciiString(std_name.Get()).ToCString()
        # Remove characters that cause ocp_vscode to fail
        clean_name = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
        return clean_name.translate(str.maketrans(" .()", "____"))

    def _get_sub_shapes(lab, loc):
        # global cnt, lvl
        # cnt += 1
        # print("\n[%d] level %d, handling LABEL %s\n" % (cnt, lvl, _get_label_name(lab)))
        # print()
        # print(lab.DumpToString())
        # print()
        # print("Is Assembly    :", shape_tool.IsAssembly(lab))
        # print("Is Free        :", shape_tool.IsFree(lab))
        # print("Is Shape       :", shape_tool.IsShape(lab))
        # print("Is Compound    :", shape_tool.IsCompound(lab))
        # print("Is Component   :", shape_tool.IsComponent(lab))
        # print("Is SimpleShape :", shape_tool.IsSimpleShape(lab))
        # print("Is Reference   :", shape_tool.IsReference(lab))

        # users = TDF_LabelSequence()
        # users_cnt = shape_tool.GetUsers(lab, users)
        # print("Nr Users       :", users_cnt)

        l_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes_s(lab, l_subss)
        # print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents_s(lab, l_comps)
        # print("Nb components  :", l_comps.Length())
        # print()
        name = get_name(lab)
        print("Name :", name)

        if shape_tool.IsAssembly_s(lab):
            l_c = TDF_LabelSequence()
            shape_tool.GetComponents_s(lab, l_c)
            for i in range(l_c.Length()):
                label = l_c.Value(i + 1)
                if shape_tool.IsReference(label):
                    # print("\n########  reference label :", label)
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(label, label_reference)
                    loc = shape_tool.GetLocation_s(label)
                    # print("    loc          :", loc)
                    # trans = loc.Transformation()
                    # print("    tran form    :", trans.Form())
                    # rot = trans.GetRotation()
                    # print("    rotation     :", rot)
                    # print("    X            :", rot.X())
                    # print("    Y            :", rot.Y())
                    # print("    Z            :", rot.Z())
                    # print("    W            :", rot.W())
                    # tran = trans.TranslationPart()
                    # print("    translation  :", tran)
                    # print("    X            :", tran.X())
                    # print("    Y            :", tran.Y())
                    # print("    Z            :", tran.Z())

                    locs.append(loc)
                    # print(">>>>")
                    # lvl += 1
                    _get_sub_shapes(label_reference, loc)
                    # lvl -= 1
                    # print("<<<<")
                    locs.pop()

        elif shape_tool.IsSimpleShape_s(lab):
            # print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape_s(lab)
            # print("    all ass locs   :", locs)

            loc = TopLoc_Location()
            for l in locs:
                # print("    take loc       :", l)
                loc = loc.Multiplied(l)

            # trans = loc.Transformation()
            # print("    FINAL loc    :")
            # print("    tran form    :", trans.Form())
            # rot = trans.GetRotation()
            # print("    rotation     :", rot)
            # print("    X            :", rot.X())
            # print("    Y            :", rot.Y())
            # print("    Z            :", rot.Z())
            # print("    W            :", rot.W())
            # tran = trans.TranslationPart()
            # print("    translation  :", tran)
            # print("    X            :", tran.X())
            # print("    Y            :", tran.Y())
            # print("    Z            :", tran.Z())
            c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
            color_set = False
            if (
                color_tool.GetInstanceColor(shape, XCAFDoc_ColorGen, c)
                or color_tool.GetInstanceColor(shape, XCAFDoc_ColorSurf, c)
                or color_tool.GetInstanceColor(shape, XCAFDoc_ColorCurv , c)
            ):
                color_tool.SetInstanceColor(shape, 0, c)
                color_tool.SetInstanceColor(shape, 1, c)
                color_tool.SetInstanceColor(shape, 2, c)
                color_set = True
                n = c.Name(c.Red(), c.Green(), c.Blue())
                print(
                    "    instance color Name & RGB: ",
                    c,
                    n,
                    c.Red(),
                    c.Green(),
                    c.Blue(),
                )

            if not color_set:
                if (
                    color_tool.GetColor(shape, XCAFDoc_ColorGen, c)
                    or color_tool.GetColor(shape, XCAFDoc_ColorSurf, c)
                    or color_tool.GetColor(shape, XCAFDoc_ColorCurv, c)
                ):
                    color_tool.SetInstanceColor(shape, 0, c)
                    color_tool.SetInstanceColor(shape, 1, c)
                    color_tool.SetInstanceColor(shape, 2, c)

                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    shape color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

            shape_disp = BRepBuilderAPI_Transform(shape, loc.Transformation()).Shape()
            if shape_disp not in output_shapes:
                output_shapes[shape_disp] = [get_name(lab), c]
            for i in range(l_subss.Length()):
                lab_subs = l_subss.Value(i + 1)
                # print("\n########  simpleshape subshape label :", lab)
                shape_sub = shape_tool.GetShape_s(lab_subs)

                c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
                color_set = False
                if (
                    color_tool.GetInstanceColor(shape_sub, 0, c)
                    or color_tool.GetInstanceColor(shape_sub, 1, c)
                    or color_tool.GetInstanceColor(shape_sub, 2, c)
                ):
                    color_tool.SetInstanceColor(shape_sub, 0, c)
                    color_tool.SetInstanceColor(shape_sub, 1, c)
                    color_tool.SetInstanceColor(shape_sub, 2, c)
                    color_set = True
                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    instance color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

                if not color_set:
                    if (
                        XCAFDoc_ColorTool.GetColor(lab_subs, XCAFDoc_ColorGen, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, XCAFDoc_ColorSurf, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, XCAFDoc_ColorCurv, c)
                    ):
                        color_tool.SetInstanceColor(shape, 0, c)
                        color_tool.SetInstanceColor(shape, 1, c)
                        color_tool.SetInstanceColor(shape, 2, c)

                        n = c.Name(c.Red(), c.Green(), c.Blue())
                        print(
                            "    shape color Name & RGB: ",
                            c,
                            n,
                            c.Red(),
                            c.Green(),
                            c.Blue(),
                        )
                shape_to_disp = BRepBuilderAPI_Transform(
                    shape_sub, loc.Transformation()
                ).Shape()
                # position the subshape to display
                if shape_to_disp not in output_shapes:
                    output_shapes[shape_to_disp] = [get_name(lab_subs), c]

    def _get_shapes():
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels)
        # global cnt
        # cnt += 1

        print()
        print("Number of shapes at root :", labels.Length())
        print()
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return output_shapes, doc







###########################
# IGES import OCC Extends #
###########################
def read_iges_file(
    filename, return_as_shapes=False, verbosity=False, visible_only=False
):
    """read the IGES file and returns a compound
    filename: the file path
    return_as_shapes: optional, False by default. If True returns a list of shapes,
                      else returns a single compound
    verbosity: optionl, False by default.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    IGESControl_Controller.Init_s()

    iges_reader = IGESControl_Reader()
    iges_reader.SetReadVisible(visible_only)
    status = iges_reader.ReadFile(filename)

    if status != IFSelect_RetDone:  # check status
        raise IOError("Cannot read IGES file")

    if verbosity:
        failsonly = False
        iges_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        iges_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    iges_reader.ClearShapes()
    iges_reader.TransferRoots()
    nbr = iges_reader.NbShapes()

    _shapes = []
    for i in range(1, nbr + 1):
        a_shp = iges_reader.Shape(i)
        if not a_shp.IsNull():
            _shapes.append(a_shp)

    # create a compound and store all shapes
    if not return_as_shapes:
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)
        for s in _shapes:
            builder.Add(compound, s)
        return [compound]

    return _shapes