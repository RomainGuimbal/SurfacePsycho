import bpy
import sys
import numpy as np
from mathutils import Vector
from os.path import dirname, abspath, isfile
from .utils import *
import copy

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)


from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCP.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCP.GCE2d import GCE2d_MakeSegment, GCE2d_MakeArcOfCircle
from OCP.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_Plane, Geom_BezierCurve, Geom_BSplineCurve
from OCP.Geom2d import Geom2d_BezierCurve, Geom2d_BSplineCurve
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Ax1, gp_Ax2, gp_Circ, gp_Ax2d, gp_Pnt2d, gp_Circ2d, gp_Dir2d, gp_Vec, gp_Vec2d
from OCP.IFSelect import IFSelect_RetDone
from OCP.IGESControl import IGESControl_Writer
from OCP.Interface import Interface_Static
from OCP.ShapeFix import ShapeFix_Face
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array2OfPnt
from OCP.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCP.TopoDS import TopoDS_Shape, TopoDS, TopoDS_Wire, TopoDS_Edge, TopoDS_Face, TopoDS_Shape, TopoDS_Compound
# from OCP.TopTools import TopTools_Array1OfShape



##############################
##    Converter classes     ##
##############################

class SP_Edge_export:
    def __init__(self, vec_cp : list[Vector], seg_attrs : dict[str:float],
                  cp_aligned_attrs : dict[str:list], is2D = False, geom_surf = None, 
                  flat_normal = None, single_seg = False):
        self.vec_cp = vec_cp
        self.gp_cp = []
        for v in vec_cp :
            if is2D:
                self.gp_cp.append(gp_Pnt2d(v[0], v[1]))
            else :
                self.gp_cp.append(gp_Pnt(v[0], v[1], v[2]))

        self.p_count = len(vec_cp)
        self.seg_attrs = seg_attrs
        self.cp_aligned_attrs = cp_aligned_attrs
        self.is2D = is2D
        self.flat_normal = flat_normal
        self.single_seg = single_seg
        
        type = self.get_type()
        match type :
            case 0 :
                self.line()
            case 1 :
                self.bezier()
            case 2 :
                self.bspline()
            case 3 :
                self.circle_arc()
            case 4 :
                self.circle()

        # make segment
        if geom_surf != None: #2D
            adapt = GeomAdaptor_Surface(geom_surf)
            self.topods_edge = BRepBuilderAPI_MakeEdge(self.geom, adapt.Surface()).Edge()
        else :
            self.topods_edge = BRepBuilderAPI_MakeEdge(self.geom).Edge()


    def get_type(self):
        circle_exists = 'circle' in self.seg_attrs.keys()
        if self.p_count < 2:
            print('Error : Invalid segment')
        elif self.p_count ==2 :
            if circle_exists and self.seg_attrs['circle'] > 0 and self.single_seg :
                return 4
            else:
                return 0
        elif circle_exists and self.p_count == 3 and self.seg_attrs['circle'] > 0.1:
            return 3
        elif self.seg_attrs['degree'] == None or self.p_count == self.seg_attrs['degree']+1 and not self.seg_attrs['isperiodic']:
            return 1
        else :
            return 2

    def line(self):
        if self.is2D:
            makesegment = GCE2d_MakeSegment(self.gp_cp[0], self.gp_cp[1])
        else:
            makesegment = GC_MakeSegment(self.gp_cp[0], self.gp_cp[1])
        self.geom = makesegment.Value()

    def circle_arc(self):
        if self.is2D:
            makesegment = GCE2d_MakeArcOfCircle(self.gp_cp[0], self.gp_cp[1], self.gp_cp[2]) 
        else :
            makesegment = GC_MakeArcOfCircle(self.gp_cp[0], self.gp_cp[1], self.gp_cp[2])
        self.geom = makesegment.Value() 

    def circle(self):
        radius = (self.vec_cp[0]-self.vec_cp[1]).length
        if self.is2D :
            p_center = gp_Pnt2d(self.vec_cp[0][0], self.vec_cp[0][1])
            circle = gp_Circ2d(gp_Ax2d(p_center, gp_Dir2d(self.vec_cp[1][0]-self.vec_cp[0][0], self.vec_cp[1][1]-self.vec_cp[0][1])), radius)
            self.geom = circle

        elif self.flat_normal is not None:
            p_center = gp_Pnt(self.vec_cp[0][0], self.vec_cp[0][1], self.vec_cp[0][2])
            dir1 = gp_Dir(self.vec_cp[1][0]-self.vec_cp[0][0],
                          self.vec_cp[1][1]-self.vec_cp[0][1],
                          self.vec_cp[1][2]-self.vec_cp[0][2])

            pl_normal_vec = [self.flat_normal.X(), self.flat_normal.Y(), self.flat_normal.Z()]

            dir2_vec = np.cross(pl_normal_vec, self.vec_cp[0]-self.vec_cp[1])
            dir2= gp_Dir(dir2_vec[0], dir2_vec[1], dir2_vec[2])

            circle = gp_Circ(gp_Ax2(p_center, dir1, dir2), radius)
            self.geom = circle
    
    def bezier(self):
        if self.is2D :
            segment_point_array = vec_list_to_gp_pnt2d(self.vec_cp)
            self.geom = Geom2d_BezierCurve(segment_point_array)
        else :
            segment_point_array = vec_list_to_gp_pnt(self.vec_cp)
            self.geom = Geom_BezierCurve(segment_point_array)

    def bspline(self):
        if self.is2D :
            segment_point_array = vec_list_to_gp_pnt2d(self.vec_cp)
        else :
            segment_point_array = vec_list_to_gp_pnt(self.vec_cp)

        isclamped = self.seg_attrs['isclamped'] if not None else True
        is_unclamped_periodic = (self.seg_attrs['isperiodic'] if not None else False) and not isclamped
        degree = self.seg_attrs['degree']
        
        tcol_weights = float_list_to_tcolstd(self.cp_aligned_attrs['weight'])
        
        # TODO custom knot/mult per edge, no design yet
        # try :
        #     if isclamped :
        #         knot_length = self.p_count - degree + 1
        #     else :
        #         knot_length = self.p_count + degree

        #     # knot
        #     knot = float_list_to_tcolstd(get_attribute_by_name(ob, 'Knot', 'float', knot_length))
            
        #     # Multiplicities
        #     mult = TColStd_Array1OfInteger(1, knot_length)
        #     for j in range(knot_length):
        #         if isclamped and (j == 0 or j == knot_length-1):
        #             mult.SetValue(j+1, degree+1)
        #         else :
        #             mult.SetValue(j+1, 1)
        # except Exception:
        #    knot, mult = self.auto_knot_and_mult(degree, isclamped, is_unclamped_periodic)

        knot, mult = auto_knot_and_mult(self.p_count, degree, isclamped, is_unclamped_periodic)
        if self.is2D :
            self.geom = Geom2d_BSplineCurve(segment_point_array, tcol_weights, knot, mult, degree, is_unclamped_periodic)
        else :
            self.geom = Geom_BSplineCurve(segment_point_array, tcol_weights, knot, mult, degree, is_unclamped_periodic)





def auto_knot_and_mult(p_count, degree, isclamped = True, isperiodic = False):
    if isclamped :
        knot_length = p_count - degree + 1
        knot_att = [r/(knot_length-1) for r in range(knot_length)]
        mult_att = [degree+1] + [1]*(knot_length-2) + [degree+1]
    elif isperiodic :
        knot_length = p_count + 1
        knot_att = list(range(-degree, p_count + 1 + degree))
        mult_att = [1]*knot_length
    else :
        knot_length = p_count + degree + 1
        knot_att = list(range(knot_length))#[r/(knot_length-1) for r in range(knot_length)]
        mult_att = [1]*knot_length
        
    knot = TColStd_Array1OfReal(1, knot_length)
    mult = TColStd_Array1OfInteger(1, knot_length)
    for i in range(knot_length):
        knot.SetValue(i+1, knot_att[i])
        mult.SetValue(i+1, mult_att[i])
    return knot, mult







class SP_Wire_export :
    def __init__(self, CP, segs_p_counts, segs_degrees=None):
        # Export
        self.segs_degrees = segs_degrees
        self.CP = [Vector(v) for v in CP]
        self.segs_p_counts = segs_p_counts
        self.isclosed = sum([s -1 for s in segs_p_counts]) == len(CP)

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


    def get_attr_per_edge(self, attr) -> list[list]:
        split_attr=[]
        inf = 0
        sup = self.segs_p_counts[0]
        seg_count = len(self.segs_p_counts)
        for i in range(seg_count) :
            if i==seg_count-1 and self.isclosed:
                split_attr.append(attr[inf:len(self.CP)]+[attr[0]])
            else :
                split_attr.append(attr[inf:sup])
                inf = sup - 1
                sup = inf + self.segs_p_counts[i+1]
        return split_attr
    

    def get_single_val_attr_per_edge(self, attr) -> list:
        split_attr=[]
        fp = self.seg_first_P_id
        for i in fp :
            split_attr.append(attr[i])
        return split_attr


    def get_topods_wire_3d(self, ob, geom_plane=None):
        wire_p_count=len(self.CP)
        segment_count = len(self.segs_p_counts)

        # Create CP 3D
        controlPoints = TColgp_Array1OfPnt(1, wire_p_count)
        for i in range(wire_p_count):
            pnt = gp_Pnt(self.CP[i][0], self.CP[i][1], self.CP[i][2])
            if geom_plane != None:
                pnt = GeomAPI_ProjectPointOnSurf(pnt, geom_plane).Point(1)
            controlPoints.SetValue(i+1, pnt)
        
        # Get attrs
        try :
            weight_attr = get_attribute_by_name(ob, 'Weight', 'float', wire_p_count)
        except KeyError:
            weight_attr = [1.0]*wire_p_count
        try :
            circle_att = get_attribute_by_name(ob, 'Circle', 'float', wire_p_count)
        except KeyError:
            circle_att = [0]*wire_p_count 
        try :
            isclamped = get_attribute_by_name(ob, 'IsClamped', 'first_bool')
        except KeyError:
            isclamped = True
        try :
            isperiodic = get_attribute_by_name(ob, 'IsPeriodic', 'first_bool')
        except KeyError:
            isperiodic = False

        # Split attrs per edge
        vec_cp_per_edge = self.get_attr_per_edge(self.CP)
        weight = self.get_attr_per_edge(weight_attr)
        edges_degrees = self.segs_degrees
        
        flat_normal = None
        if geom_plane is not None :
            flat_normal = geom_plane.Pln().Axis().Direction()

        # Make Edges
        edges_list = [SP_Edge_export(vec_cp_per_edge[i], {'degree':edges_degrees[i], 
                                                          'circle':circle_att[i],
                                                          'isclamped':isclamped,
                                                          'isperiodic':isperiodic,},
                                                          {'weight':weight[i],}, 
                                                           flat_normal=flat_normal, 
                                                           single_seg = segment_count == 1
                                                           ).topods_edge for i in range(segment_count)]

        # Make contour
        makeWire = BRepBuilderAPI_MakeWire()
        for e in edges_list :
            makeWire.Add(TopoDS.Edge_s(e))
        wire = makeWire.Wire()

        return wire

    

    def get_topods_wire_2d(self, ob, geom_surf=None):
        wire_p_count = len(self.CP)
        segment_count = len(self.segs_p_counts)

        # Create 2D points
        controlPoints = TColgp_Array1OfPnt2d(1, wire_p_count)
        for i in range(wire_p_count):
            pnt = gp_Pnt2d(self.CP[i][1], self.CP[i][0]) # INVERTED
            controlPoints.SetValue(i+1, pnt)

        # Get attrs
        try :
            weight_attr = get_attribute_by_name(ob, 'Weight', 'float', wire_p_count)
        except KeyError:
            weight_attr = [1.0]*wire_p_count
        try :
            circle_att = get_attribute_by_name(ob, 'Circle', 'float', wire_p_count)
        except KeyError:
            circle_att = [0]*wire_p_count 
        try :
            isclamped = get_attribute_by_name(ob, 'IsClamped', 'first_bool')
        except KeyError:
            isclamped = True
        try :
            isperiodic = get_attribute_by_name(ob, 'IsPeriodic', 'first_bool')
        except KeyError:
            isperiodic = False

        # Split attrs per edge
        vec_cp_per_edge = self.get_attr_per_edge(self.CP)
        weight = self.get_attr_per_edge(weight_attr)
        edges_degrees = self.segs_degrees
        
        # Make Edges
        edges_list = [SP_Edge_export(vec_cp_per_edge[i], {'degree':edges_degrees[i], 
                                                          'circle':circle_att[i],
                                                          'isclamped':isclamped,
                                                          'isperiodic':isperiodic,},
                                                          {'weight':weight[i],},
                                                            geom_surf=geom_surf,
                                                            single_seg = segment_count==1
                                                            ).topods_edge for i in range(segment_count)]

        # Make contour
        makeWire = BRepBuilderAPI_MakeWire()
        for e in edges_list :
            makeWire.Add(TopoDS.Edge_s(e))
        wire = makeWire.Wire()

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




class SP_Contour_export :
    def __init__(self, ob, cp_attr_name, p_count_attr_name, scale = 1):
        # Check if trimmed
        try :
            segs_p_counts = get_attribute_by_name(ob, p_count_attr_name, 'int')
            wire_index = get_attribute_by_name(ob, 'Wire', 'int')
            self.has_wire = True
        except Exception: # No trim
            self.has_wire = False

        if self.has_wire :
            # Get total_p_count
            total_p_count = 0
            for i,wi in enumerate(wire_index):
                if wi ==0:
                    break
                total_p_count+=1
        
            # crop wire_index
            wire_index = wire_index[:total_p_count]

            # Get segment count
            segment_count = 0
            for p in segs_p_counts:
                if p>0:
                    segment_count += 1
                else :
                    break
            
            #crop segs_p_counts
            segs_p_counts = segs_p_counts[:segment_count]
            
            # Get CP position attr
            points = get_attribute_by_name(ob, cp_attr_name, 'vec3', total_p_count)
            points*=scale

            # Get degree attr
            try :
                try :
                    try :
                        segs_degrees = get_attribute_by_name(ob, 'Contour Degree', 'int', len(segs_p_counts))
                    except KeyError :
                        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', len(segs_p_counts))
                except KeyError :
                    segs_degrees = get_attribute_by_name(ob, 'Contour Order', 'int', len(segs_p_counts))
            except KeyError :
                segs_degrees = None

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

            # iterate on cp and create wires
            for i, w_cur in enumerate(wire_index) :
                # wire first point
                if w_cur != w_prev :
                    wires_dict[w_prev] = SP_Wire_export(build_CP, build_segs_p_counts, build_segs_degrees)
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
            wires_dict[w_prev] = SP_Wire_export(build_CP, build_segs_p_counts, build_segs_degrees)
            self.wires_dict = wires_dict







##############################
##  Brep from SP entities   ##
##############################

def geom_to_topods_face(geom_surf = None, outer_wire = None, inner_wires=[]):
    # Make face
    if geom_surf != None:
        if outer_wire == None :
            makeface = BRepBuilderAPI_MakeFace(geom_surf, 1e-6)
            return makeface.Face()
        else :
            makeface = BRepBuilderAPI_MakeFace(geom_surf, outer_wire, False)#,1e-6)
    else : # Flat face
        makeface = BRepBuilderAPI_MakeFace(outer_wire, True)

    # Add inner wires (holes)
    for inner_wire in inner_wires:
        makeface.Add(inner_wire)
    
    # Build the face
    makeface.Build()

    # makeface.Add(trim_wire)#.Reversed())
    face = makeface.Face()
    fix = ShapeFix_Face(face)
    fix.Perform()

    return fix.Face()






def new_brep_bezier_face(o, context, scale=1000):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
    points = get_attribute_by_name(ob, 'CP_any_order_surf', 'vec3', u_count*v_count)
    points *= scale #unit correction

    controlPoints = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id= u_count*i +j
            controlPoints.SetValue(j+1, i+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    geom_surf = Geom_BezierSurface(controlPoints)

    # Build trim contour
    contour = SP_Contour_export(ob, 'CP_trim_contour_UV', 'CP_count_trim_contour_UV')
    
    if not contour.has_wire :
        return geom_to_topods_face(geom_surf)
    else :
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire_2d(ob, geom_surf)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_topods_wire_2d(ob, geom_surf))

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face




def new_brep_NURBS_face(o, context, scale=1000):
    # Get attributes
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
    points = get_attribute_by_name(ob, 'CP_NURBS_surf', 'vec3', u_count*v_count)
    points *= scale #unit correction
    degree_u, degree_v = get_attribute_by_name(ob, 'Degrees', 'int', 2)
    try:
        isclamped_u, isclamped_v = get_attribute_by_name(ob, 'IsClamped', 'bool', 2)
        isperiodic_u, isperiodic_v = get_attribute_by_name(ob, 'IsPeriodic', 'bool', 2)
    except KeyError:
        isclamped_u, isclamped_v, isperiodic_u, isperiodic_v = True, True, False, False

    # Knots and Multiplicities
    try : 
        knot_u = get_attribute_by_name(ob, 'Knot U', 'int')
        knot_v = get_attribute_by_name(ob, 'Knot V', 'int')
        mult_u = get_attribute_by_name(ob, 'Multiplicity U', 'int')
        mult_v = get_attribute_by_name(ob, 'Multiplicity V', 'int')

        # TODO (not auto)
        uknots, umult = auto_knot_and_mult(u_count, degree_u, isclamped_u, isperiodic_u) # TODO 
        vknots, vmult = auto_knot_and_mult(v_count, degree_v, isclamped_v, isperiodic_v) # TODO
    except KeyError: # No custom knot
        uknots, umult = auto_knot_and_mult(u_count, degree_u, isclamped_u, isperiodic_u) 
        vknots, vmult = auto_knot_and_mult(v_count, degree_v, isclamped_v, isperiodic_v)

    # Poles grid
    poles = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id= u_count*i +j
            poles.SetValue(j+1, i+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    # Compose Geom
    geom_surf = Geom_BSplineSurface(poles, uknots, vknots, umult, vmult, degree_u, degree_v, isperiodic_u, isperiodic_v)

    # Build trim contour
    contour = SP_Contour_export(ob, 'CP_trim_contour_UV', 'CP_count_trim_contour_UV')
    if not contour.has_wire :
        return geom_to_topods_face(geom_surf)
    else :
        wires = contour.wires_dict

        # Get topods wires
        outer_wire = wires[-1].get_topods_wire_2d(ob, geom_surf)
        inner_wires=[]
        for k in wires.keys():
            if k!=-1:
                inner_wires.append(wires[k].get_topods_wire_2d(ob, geom_surf))

        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
        return face










# class SP_Curve_obj_export :?
def new_brep_curve(o, context, scale=1000):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    segs_p_counts = get_attribute_by_name(ob, 'CP_count', 'int')
    
    # get total_p_count and segment_count
    total_p_count, segment_count= 1, 0
    for p in segs_p_counts:
        if p>1:
            total_p_count += p-1
            segment_count += 1
        else :
            break
    #crop segs_p_counts
    segs_p_counts = segs_p_counts[:segment_count]
    
    # 1 point less if closed
    is_closed = get_attribute_by_name(ob, 'IsPeriodic', 'first_int')
    total_p_count -= is_closed

    try :
        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', segment_count)
    except Exception :
        segs_degrees = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_curve', 'vec3', total_p_count)
    points*=scale # Unit correction

    wire = SP_Wire_export(points, segs_p_counts, segs_degrees)
    brep_wire = wire.get_topods_wire_3d(ob)

    return brep_wire






def new_brep_flat_face(o, context, scale=1000):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    
    # Build Contour
    wires = SP_Contour_export(ob, 'CP_planar', 'CP_count', scale).wires_dict

    # Orient and offset
    loc, rot, _ = o.matrix_world.decompose()
    try :
        offset = get_attribute_by_name(ob, 'planar_offset', 'vec3', 1)[0]
        orient = get_attribute_by_name(ob, 'planar_orient', 'vec3', 1)[0]
    except KeyError :
        offset = [0,0,0]
        orient = [0,0,1]
    loc += rot@ Vector(offset)
    loc *= scale
    pl_normal = rot@ Vector(orient)
    pl_normal_dir = gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z)
    pl = gp_Pln(gp_Pnt(loc.x,loc.y,loc.z), pl_normal_dir)
    geom_pl = Geom_Plane(pl)

    # Get occ wires
    outer_wire = wires[-1].get_topods_wire_3d(ob, geom_pl)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_topods_wire_3d(ob, geom_pl))

    face = geom_to_topods_face(None, outer_wire, inner_wires)
    return face














def mirror_brep(o, shape, scale=1000):
    ms = BRepBuilderAPI_Sewing(1e-1)
    ms.SetNonManifoldMode(True)
    ms.Add(shape)
    mshape = TopoDS_Shape()

    ms.Perform()
    shape = ms.SewedShape()
    loc, rot, _ = o.matrix_world.decompose()

    for m in o.modifiers :
        if m.type == 'MIRROR' and m.show_viewport :
            if m.mirror_object==None:
                mirror_offset = loc*scale
            else :
                loc, rot, _ = m.mirror_object.matrix_world.decompose()
                mirror_offset = loc*scale
            
            #Fill configurations array
            configurations = [False]*7

            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            configurations[0]= x
            configurations[1]= y
            configurations[2]= z
            configurations[3]= x and y and z
            configurations[4]= y and z
            configurations[5]= x and z
            configurations[6]= x and y

            xscales = [ 1, 0, 0, 1, 0, 1, 1]
            yscales = [ 0, 1, 0, 1, 1, 0, 1]
            zscales = [ 0, 0, 1, 1, 1, 1, 0]
            symtype = [x+y+z for x,y,z in zip(xscales,yscales,zscales)]


            ms2 = BRepBuilderAPI_Sewing(1e-1)
            ms2.SetNonManifoldMode(True)


            for i in range(7): # 7 = 8 mirror configs -1 original config
                if configurations[i]:
                    if symtype[i]==1:#sym planaire
                        base = rot@(Vector([xscales[i],yscales[i],zscales[i]]))
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Ax2(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]), gp_Dir(base.x, base.y, base.z)))
                    
                    elif symtype[i]==2 :#sym axiale
                        base = rot@(Vector([xscales[i]-1,abs(yscales[i]-1),abs(zscales[i]-1)])) 
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Ax1(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]), gp_Dir(base.x, base.y, base.z)))
                    
                    else :#sym centrale
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]))
                    
                    mshape = BRepBuilderAPI_Transform(shape, atrsf).Shape()
                    ms2.Add(shape)
                    ms2.Add(mshape)
                    # mshape = BRepBuilderAPI_Transform(shape, atrsf).Shape()
                    # ms.Add(mshape)

            ms2.Perform()
            shape = ms2.SewedShape()
            # ms.Perform()
            # shape = ms.SewedShape()
            
    # ms.Perform()
    # shape = ms.SewedShape()
    return shape



def prepare_brep(context, use_selection, axis_up, axis_forward, scale = 1000):
    aShape = TopoDS_Shape()
    aSew = BRepBuilderAPI_Sewing(1e-1)
    SPobj_count=0

    if use_selection:
        initial_selection = context.selected_objects
    else :
        initial_selection = context.visible_objects
    obj_list = initial_selection
    obj_to_del = []

    #TODO replace with recursive version

    while(len(obj_list)>0): # itterates until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            gto = geom_type_of_object(o, context)

            match gto :
                case "bezier_surf" :
                    SPobj_count +=1
                    af = new_brep_bezier_face(o, context, scale)
                    aSew.Add(mirror_brep(o, af, scale))

                case "NURBS_surf" :
                    SPobj_count +=1
                    nf = new_brep_NURBS_face(o, context, scale)
                    aSew.Add(mirror_brep(o, nf, scale))

                case "planar" :
                    SPobj_count +=1
                    pf = new_brep_flat_face(o, context, scale)
                    aSew.Add(mirror_brep(o, pf, scale))

                case "curve" :
                    SPobj_count +=1
                    cu = new_brep_curve(o, context, scale)
                    aSew.Add(mirror_brep(o, cu, scale))

                # case "collection_instance":
                #     pass
                    # self.report({'INFO'}, 'Collection instances will not export')
                    # empty_mw = o.matrix_world
                    # for co in o.instance_collection.all_objects : #select all object of collection linked to o
                    #     dupli = co.copy()
                    #     dupli.data = co.data.copy()
                    #     dupli.matrix_world = empty_mw @ dupli.matrix_world # not recursive compliant? :/
                    #     obj_newly_real.append(dupli) #flag the new objects
                    #     context.scene.collection.objects.link(dupli)

        obj_list=[]
        for onr in obj_newly_real:
            obj_list.append(onr)
            obj_to_del.append(onr)

    for o in obj_to_del : # clear realized objects
        bpy.data.objects.remove(o, do_unlink=True)

    aSew.SetNonManifoldMode(True)
    aSew.Perform()
    aShape = aSew.SewedShape()
    
    if SPobj_count>0 :
        return aShape
    else :
        return None



def export_step(context, filepath, use_selection, axis_up='Z', axis_forward='Y', scale =1000):
    brep_shapes = prepare_brep(context, use_selection, axis_up, axis_forward, scale)
    if brep_shapes is not None :
        write_step_file(brep_shapes, filepath, application_protocol="AP203")
        return True
    else:
        return False

def export_iges(context, filepath, use_selection, axis_up='Z', axis_forward='Y', scale =1000):
    brep_shapes = prepare_brep(context, use_selection, axis_up, axis_forward, scale)
    if brep_shapes is not None :
        write_iges_file(brep_shapes, filepath)
        return True
    else:
        return False
    









###########################
# Step export OCC Extends #
###########################

def write_step_file(a_shape, filename, application_protocol="AP203"):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214IS" or "AP242DIS"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError(f"Shape {a_shape} is null.")
    if application_protocol not in ["AP203", "AP214IS", "AP242DIS"]:
        raise AssertionError(
            f"application_protocol must be either AP203 or AP214IS. You passed {application_protocol}."
        )
    if isfile(filename):
        print(f"Warning: {filename} file already exists and will be replaced")
    # creates and initialise the step exporter
    step_writer = STEPControl_Writer()
    Interface_Static.SetCVal_s("write.step.schema", application_protocol)

    # transfer shapes and write file
    step_writer.Transfer(a_shape, STEPControl_AsIs)
    status = step_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise IOError("Error while writing shape to STEP file.")
    if not isfile(filename):
        raise IOError(f"{filename} not saved to filesystem.")
    





###########################
# IGES export OCC Extends #
###########################

def write_iges_file(a_shape, filename):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError("Shape is null.")
    if isfile(filename):
        print(f"Warning: {filename} already exists and will be replaced")
    # creates and initialise the step exporter
    iges_writer = IGESControl_Writer()
    iges_writer.AddShape(a_shape)
    status = iges_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Not done.")
    if not isfile(filename):
        raise IOError("File not written to disk.")