import bpy
import numpy as np
from mathutils import Vector
from os.path import abspath, splitext, split, isfile
from .utils import *


# from OCP.Geom2dAdaptor import Geom2dAdaptor_Curve
# from OCP.GeomAbs import GeomAbs_Line, GeomAbs_BSplineCurve, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepAdaptor import BRepAdaptor_Surface #BRepAdaptor_Curve
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve, Geom_CylindricalSurface, Geom_Line
from OCP.GeomAbs import GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_Line, GeomAbs_Circle, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pnt, gp_Pnt2d
from OCP.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCP.IGESControl import IGESControl_Controller, IGESControl_Reader
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FORWARD, TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS, TopoDS_Wire, TopoDS_Edge, TopoDS_Face, TopoDS_Shape, TopoDS_Compound
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorTool


from .utils import list_of_shapes_to_compound



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
    def __init__(self, topods_edge : TopoDS_Edge, topods_face = None):
        if topods_edge!= None :
            self.verts = None
            self.degree = None
            self.type = None
            
            # Edge adaptor
            # 3D
            if topods_face is None:
                is2D=False
                edge_adaptor = BRepAdaptor_Curve(topods_edge)
                curve_type = edge_adaptor.Curve().GetType()
                # c = edge_adaptor.Curve()
                # curve_type = c.GetType()
                # curve = c.Curve()

                # curve_adaptor = GeomAdaptor_Curve(geom_curve)
            #2D
            else :
                is2D=True
                edge_adaptor = BRepAdaptor_Curve2d(topods_edge, topods_face)
                curve_type = edge_adaptor.GetType()
            
            if curve_type == GeomAbs_Line :
                self.line(edge_adaptor)
            elif curve_type == GeomAbs_BezierCurve :
                self.bezier(edge_adaptor)
            elif curve_type == GeomAbs_BSplineCurve :
                self.bspline(edge_adaptor, is2D)
            elif curve_type == GeomAbs_Circle :
                self.circle(edge_adaptor)
            else :
                print(f"Unsupported curve type: {curve_type}. Expect inaccurate results")
                start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
                end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
                gp_pnt_poles = [start_point, end_point]
                self.type = EDGES_TYPES['line']
                self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]

    def scale(self, scale_factor):
        self.verts = [v*scale_factor for v in self.verts]

    def line(self, edge_adaptor):
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        gp_pnt_poles = [start_point, end_point]
        self.type = EDGES_TYPES['line']
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]

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
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
        # TODO output weights

    def bspline(self, edge_adaptor, is2D):
        # if not is2D :
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
        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
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

        self.verts = [SP_Pole_import(g).vertex for g in gp_pnt_poles]
    


class SP_Wire_import :
    def __init__(self, topods_wire: TopoDS_Wire=None, scale=0.001, CP =[], topods_face = None, segs_p_counts=None, segs_degrees=None):
        self.CP = [] #Vectors, bmesh format
        # Import
        if topods_wire!=None:
            # vertex aligned attributes
            self.bmesh_edges = [] #int tuple
            self.endpoints_att = [] #float
            self.degree_att = [] #float
            # self.knot_att = [] #float
            # self.weight_att = cp_weight #float
            # self.mult_att = [] #float
            self.circle_att = []

            if topods_face == None :
                self.import_constructor_3d_space(topods_wire, scale)
            else :
                self.import_constructor_uv_space(topods_wire, topods_face)

    
    def import_constructor_3d_space(self, topods_wire: TopoDS_Wire, scale):
        topods_edges = get_edges_from_wire(topods_wire)
        wire_is_reversed = topods_wire.Orientation() == 1

        #Edges
        for e in topods_edges :
            sp_edge = SP_Edge_import(e)
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
            sp_edge = SP_Edge_import(e, topods_face)
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



class SP_Contour_import :
    def __init__(self, topodsface,  scale = None):
        self.wires = get_wires_from_face(topodsface)
        self.verts, self.edges, self.endpoints, self.degrees, self.circles = [], [], [], [], []

        for w in self.wires :
            if scale!=None:
                sp_wire = SP_Wire_import(topods_wire=w, scale = scale)
            else :
                sp_wire = SP_Wire_import(topods_wire=w, topods_face=topodsface)
                
            _, self.edges, _ = join_mesh_entities(self.verts, self.edges, [], sp_wire.CP, sp_wire.bmesh_edges, [])
            self.verts.extend(sp_wire.CP)
            self.endpoints.extend(sp_wire.endpoints_att)
            self.degrees.extend(sp_wire.degree_att)
            self.circles.extend(sp_wire.circle_att)
    
    # For square contour following the patch bounds
    def is_trivial(self):
        is_trivial_trim = False
        if len(self.verts) == 4 :

            print(self.verts)

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



class SP_Surface_import :
    def __init__(self, face : TopoDS_Face, collection, trims_enabled : bool, uv_bounds, CPvert, CPedges, CPfaces, ob_name = "STEP Patch", scale=0.001):
        self.trims_enabled = trims_enabled
        self.face = face
        self.uv_bounds = uv_bounds
        self.CPvert = CPvert
        self.CPedges = CPedges
        self.CPfaces = CPfaces
        self.vert, self.edges, self.faces = [],[],[]
        
        if trims_enabled :
            contour = SP_Contour_import(face)
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









def build_SP_cylinder(brepFace : TopoDS_Face, collection, trims_enabled, scale = 0.001) :
    face_adpator = BRepAdaptor_Surface(brepFace)
    gp_cylinder = face_adpator.Surface().Cylinder()
    geom_cylinder = Geom_CylindricalSurface(gp_cylinder)
    
    gpaxis= gp_cylinder.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_cylinder.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    aPnt1 = face_adpator.Value(face_adpator.FirstUParameter(), face_adpator.FirstVParameter())
    aPnt2 = face_adpator.Value(face_adpator.LastUParameter(), face_adpator.LastVParameter())

    aGeomAxis = Geom_Line(gpaxis)
    p1 = GeomAPI_ProjectPointOnCurve(aPnt1, aGeomAxis).Point(1)
    p2 = GeomAPI_ProjectPointOnCurve(aPnt2, aGeomAxis).Point(1)
    length = p1.Distance(p2)*scale

    location = gp_cylinder.Location()
    loc_vec = Vector((location.X()*scale, location.Y()*scale, location.Z()*scale)) - xaxis_vec*length/2
    radius = gp_cylinder.Radius()*scale


    fake_uv_bounds = geom_cylinder.Bounds()
    uv_bounds = (fake_uv_bounds[1], fake_uv_bounds[0], -length/2, length/2) # -np.pi/2
    min_u, max_u, min_v, max_v = uv_bounds[0], uv_bounds[1], uv_bounds[2], uv_bounds[3]

    print(f"Cylinder UV bounds : {(min_u, max_u, min_v, max_v)}")

    raduis_vert = Vector((zaxis_vec*radius) + loc_vec)

    CPvert = [loc_vec, xaxis_vec*length + loc_vec, raduis_vert]
    CP_edges = [(0,1)]
    sp_surf = SP_Surface_import(brepFace, collection, trims_enabled, uv_bounds, CPvert, CP_edges, [], ob_name= "STEP Cylinder")
    sp_surf.add_modifier("SP - Cylindrical Meshing", {"Use Trim Contour":trims_enabled, "Scaling Method":1}, pin=True)
    return True




def build_SP_bezier_patch(brepFace, collection, trims_enabled):
    bezier_surface = BRepAdaptor_Surface(brepFace).Surface().Bezier()

    u_count, v_count = bezier_surface.NbUPoles(), bezier_surface.NbVPoles()
    uv_bounds = bezier_surface.Bounds()
    vector_pts = np.zeros((u_count, v_count), dtype=Vector)
    for u in range(1, u_count + 1):
        for v in range(1, v_count + 1):
            pole = bezier_surface.Pole(u, v)
            vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

            weight = bezier_surface.Weight(u, v)
            if weight!=1.0:
                print("Weighted Bezier not supported")

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)

    sp_surf = SP_Surface_import(brepFace, collection, trims_enabled, uv_bounds, CPvert.tolist(), [], CPfaces)
    sp_surf.add_modifier("SP - Bezier Patch Meshing", {"Use Trim Contour":trims_enabled, "Scaling Method":1}, pin=True)
    return True




def build_SP_NURBS_patch(topods_face, collection, trims_enabled):
    # Patch attributes
    bspline_surface = BRepAdaptor_Surface(topods_face).Surface().BSpline()
    u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()
    udeg = bspline_surface.UDegree()
    vdeg = bspline_surface.VDegree()
    uv_bounds = bspline_surface.Bounds()
    u_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.UKnots()))
    v_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.VKnots()))
    u_mult = tcolstd_array1_to_list(bspline_surface.UMultiplicities())
    v_mult = tcolstd_array1_to_list(bspline_surface.VMultiplicities())
    
    # Custom knot
    custom_knot = False
    if any(x not in [min(u_knots), max(u_knots)] for x in u_knots) or any(x not in [min(v_knots), max(v_knots)] for x in v_knots):
        custom_knot = True
        print(u_knots)
        print(v_knots)
    # TODO
    # else :
    #    Convert to bezier then
    #    build_SP_BezierPatch(...)

    # vertex aligned attributes

    # CP Grid
    custom_weight = False
    vector_pts = np.zeros((u_count, v_count), dtype=Vector)
    weights = np.zeros((u_count, v_count), dtype=float)
    for u in range(1, u_count + 1):
        for v in range(1, v_count + 1):
            pole = bspline_surface.Pole(u, v)
            vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))
            
            weight = bspline_surface.Weight(u, v)
            weights[u-1, v-1] = weight
            
            # Custom weight flag, true if 1 weight is not 1.0
            custom_weight = custom_weight or weight!=1.0

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)
    
    sp_surf = SP_Surface_import(topods_face, collection, trims_enabled, uv_bounds, CPvert.tolist(), [], CPfaces)
    
    if custom_knot:
        sp_surf.assign_vertex_gr("Knot U", v_knots)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Knot V", u_knots)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Multiplicity U", np.array(v_mult)/10)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Multiplicity V", np.array(u_mult)/10)# TO FIX U AND V INVERTED

    if custom_weight:
        # Since Nurbs trim contour uses "weight" attr too, set all trim contour weights to 1.0. To improve later
        weights = weights.flatten().tolist()
        weights.extend([1.0]*(len(sp_surf.ob.data.vertices)-len(weights)))
        sp_surf.assign_vertex_gr("Weight", weights)
        print("Weights are not fully supported yet")
        # sp_surf.add_modifier(ob, "SP - NURBS Weighting")
        # TO NORMALIZE + factor
        # assign vertex group to modifier # change_node_socket_value
    
    u_clamped = any(m!=1 for m in u_mult) or not custom_knot
    v_clamped = any(m!=1 for m in v_mult) or not custom_knot

    # Meshing
    sp_surf.add_modifier("SP - NURBS Patch Meshing", {"Degree V": udeg, "Degree U": vdeg, "Use Trim Contour":trims_enabled, "Scaling Method": 1, "Endpoint U" : v_clamped, "Endpoint V" : u_clamped }, pin=True)# TO FIX U AND V INVERTED
    return True






def build_SP_curve(topodsEdge, collection, scale = 0.001) :
    sp_edge = SP_Edge_import(topodsEdge)
    sp_edge.scale(scale)
    verts = sp_edge.verts
    edge_degree = sp_edge.degree

    endpoints = [1.0] + [0.0]*(len(verts)-2) + [1.0]
    if edge_degree!=None:
        degree_att=[edge_degree/10]+[0.0]*(len(verts)-1)
    else :
        degree_att=[0.0]*(len(verts))

    edges = [(i,i+1) for i in range(len(verts)-1)]

    # create object
    mesh = bpy.data.meshes.new("Curve CP")
    mesh.from_pydata(verts, edges, [], False)
    ob = bpy.data.objects.new('STEP curve', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Degree", degree_att)

    if sp_edge.type == EDGES_TYPES['circle']:
        add_vertex_group(ob, "Circle", [0.0, 1.0, 0.0])

    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Curve Meshing", pin=True)

    return True






def build_SP_flat(topodsFace, collection, scale = 0.001):
    # Get contour
    contour = SP_Contour_import(topodsFace, scale)
    verts = contour.verts
    edges = contour.edges
    endpoints = contour.endpoints
    degree_att = contour.degrees
    circle_att = contour.circles

    # Create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    mesh.from_pydata(verts, edges, [], False)
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Degree", degree_att)
    add_vertex_group(ob, "Circle", circle_att)
    
    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - FlatPatch Meshing", {'Orient': True}, pin=True)
    
    return True









class ShapeHierarchy:
    def __init__(self):
        self.faces = {}
        self.edges = {}
        self.hierarchy = {}

    def add_face(self, face):
        face_id = hash(face.__hash__())
        if face_id not in self.faces:
            self.faces[face_id] = face
        return f"Face_{face_id}"

    def add_edge(self, edge):
        edge_id = hash(edge.__hash__())
        if edge_id not in self.edges:
            self.edges[edge_id] = edge
        return f"Edge_{edge_id}"

    def create_shape_hierarchy(self, shape):
        hierarchy = {}
        
        if shape.ShapeType() == TopAbs_COMPOUND:
            hierarchy['Compound'] = []
            for subshape_type in [TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_FACE, TopAbs_EDGE]:
                exp = TopExp_Explorer(shape, subshape_type)
                while exp.More():
                    hierarchy['Compound'].append(self.create_shape_hierarchy(exp.Current()))
                    exp.Next()
        
        elif shape.ShapeType() == TopAbs_COMPSOLID:
            hierarchy['CompSolid'] = []
            exp = TopExp_Explorer(shape, TopAbs_SOLID)
            while exp.More():
                hierarchy['CompSolid'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_SOLID:
            hierarchy['Solid'] = []
            exp = TopExp_Explorer(shape, TopAbs_SHELL)
            while exp.More():
                hierarchy['Solid'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_SHELL:
            hierarchy['Shell'] = []
            exp = TopExp_Explorer(shape, TopAbs_FACE)
            while exp.More():
                hierarchy['Shell'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_FACE:
            face = TopoDS.Face_s(shape)
            hierarchy['Face'] = self.add_face(face)
        
        elif shape.ShapeType() == TopAbs_EDGE:
            edge = TopoDS.Edge_s(shape)
            hierarchy['Edge'] = self.add_edge(edge)
        
        return hierarchy

    def find_free_edges(self, shape):
        edge_map = TopTools_IndexedMapOfShape()
        face_map = TopTools_IndexedMapOfShape()
        
        exp = TopExp_Explorer(shape, TopAbs_EDGE)
        while exp.More():
            edge_map.Add(exp.Current())
            exp.Next()
        
        exp = TopExp_Explorer(shape, TopAbs_FACE)
        while exp.More():
            face = TopoDS.Face_s(exp.Current())
            face_exp = TopExp_Explorer(face, TopAbs_EDGE)
            while face_exp.More():
                face_map.Add(face_exp.Current())
                face_exp.Next()
            exp.Next()
        
        free_edges = []
        for i in range(1, edge_map.Size() + 1):
            if not face_map.Contains(edge_map.FindKey(i)):
                free_edges.append(edge_map.FindKey(i))
        
        return free_edges

    def process_shape(self, shape):
        self.hierarchy = self.create_shape_hierarchy(shape)
        free_edges = self.find_free_edges(shape)
        if free_edges:
            self.hierarchy['FreeEdges'] = [self.create_shape_hierarchy(edge) for edge in free_edges]

    def print_hierarchy(self, node=None, level=0):
        if node is None:
            node = self.hierarchy

        indent = "  " * level
        for key, value in node.items():
            if isinstance(value, list):
                print(f"{indent}{key}:")
                for i, item in enumerate(value):
                    print(f"{indent}  {key}_{i+1}:")
                    self.print_hierarchy(item, level + 2)
            else:
                print(f"{indent}{key}: {value}")
    
    def get_face_count(self) :
        return len(self.faces)







def import_face_nodegroups(shape_hierarchy):
    to_import_ng_names = set()
    face_encountered = set()

    for _, face in shape_hierarchy.faces.items(): 
        ft= get_face_type_id(face)
        if ft not in face_encountered :
            face_encountered.add(ft)
            match ft:
                case 0:
                    to_import_ng_names.add("SP - FlatPatch Meshing")
                case 1:
                    to_import_ng_names.add("SP - Cylindrical Meshing")
                case 5:
                    to_import_ng_names.add("SP - Bezier Patch Meshing")
                case 6:
                    to_import_ng_names.add("SP - NURBS Patch Meshing")
    
    append_multiple_node_groups(to_import_ng_names)


def process_topods_face(face, collection, trims_enabled):
    ft= get_face_type_id(face)
    match ft:
        case 0:
            build_SP_flat(face, collection)
        case 1:
            build_SP_cylinder(face, collection, trims_enabled)
        case 5:
            build_SP_bezier_patch(face, collection, trims_enabled)
        case 6:
            build_SP_NURBS_patch(face, collection, trims_enabled)
        case _ :
            print("Unsupported Face Type : " + get_face_type_name(face))
    return True

def build_SP_from_brep(shape, collection, enabled_entities, scale = 1000):
    # Create the hierarchy
    shape_hierarchy = ShapeHierarchy()
    shape_hierarchy.process_shape(shape)
        
    # progress cursor
    wm = bpy.context.window_manager
    face_count = shape_hierarchy.get_face_count()
    wm.progress_begin(0, face_count)
    progress = 0

    trims_enabled = enabled_entities["trim_contours"]

    # Create SP faces
    if enabled_entities["faces"]:
        import_face_nodegroups(shape_hierarchy)

        for _, face in shape_hierarchy.faces.items():# TODO ThreadPool
            process_topods_face(face, collection, trims_enabled)
            progress+=1
            wm.progress_update(progress)

    # Create SP free edges (bug, processes all edges)
    if enabled_entities["curves"]:
        for _, edge in shape_hierarchy.edges.items():
            build_SP_curve(edge, collection, scale)

    # TODO : Add brep relations (face connections...)
    
    wm.progress_end()
    return True








def import_cad(filepath, context, enabled_entities):
    if splitext(split(filepath)[1])[1] in ['.step','.stp','.STEP', '.STP']:
        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading STEP file")
        step_reader.TransferRoots()
        shape = step_reader.OneShape()

    elif splitext(split(filepath)[1])[1] in ['.igs','.iges','.IGES', '.IGS']:
        iges_reader = IGESControl_Reader()
        status = iges_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading IGES file")
        iges_reader.TransferRoots()
        shape = iges_reader.OneShape()
    
    # Create container collection
    collection_name = splitext(split(filepath)[1])[0]
    new_collection = bpy.data.collections.new(collection_name)
    context.scene.collection.children.link(new_collection)
    context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[collection_name]

    # import cProfile
    # profiler = cProfile.Profile()
    # profiler.enable()
    build_SP_from_brep(shape, new_collection, enabled_entities)
    # profiler.disable()
    # profiler.print_stats()













###########################
# Step import OCC Extends #
###########################

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
    doc = TDocStd_Document("pythonocc-doc-step-import")

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool(doc.Main())
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
        shape_tool.GetSubShapes(lab, l_subss)
        # print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents(lab, l_comps)
        # print("Nb components  :", l_comps.Length())
        # print()
        name = lab.GetLabelName()
        print("Name :", name)

        if shape_tool.IsAssembly(lab):
            l_c = TDF_LabelSequence()
            shape_tool.GetComponents(lab, l_c)
            for i in range(l_c.Length()):
                label = l_c.Value(i + 1)
                if shape_tool.IsReference(label):
                    # print("\n########  reference label :", label)
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(label, label_reference)
                    loc = shape_tool.GetLocation(label)
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

        elif shape_tool.IsSimpleShape(lab):
            # print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape(lab)
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
                color_tool.GetInstanceColor(shape, 0, c)
                or color_tool.GetInstanceColor(shape, 1, c)
                or color_tool.GetInstanceColor(shape, 2, c)
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
                    XCAFDoc_ColorTool.GetColor(lab, 0, c)
                    or XCAFDoc_ColorTool.GetColor(lab, 1, c)
                    or XCAFDoc_ColorTool.GetColor(lab, 2, c)
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
                output_shapes[shape_disp] = [lab.GetLabelName(), c]
            for i in range(l_subss.Length()):
                lab_subs = l_subss.Value(i + 1)
                # print("\n########  simpleshape subshape label :", lab)
                shape_sub = shape_tool.GetShape(lab_subs)

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
                        XCAFDoc_ColorTool.GetColor(lab_subs, 0, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, 1, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, 2, c)
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
                    output_shapes[shape_to_disp] = [lab_subs.GetLabelName(), c]

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
    return output_shapes







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

    IGESControl_Controller.Init()

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