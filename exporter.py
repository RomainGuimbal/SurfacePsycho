import bpy
import sys
import numpy as np
from mathutils import Vector
from os.path import dirname, abspath
from .utils import *

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)



from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge2d
# from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.GCE2d import GCE2d_MakeSegment
from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_Plane, Geom_TrimmedCurve, Geom_BSplineCurve
from OCC.Core.Geom2d import Geom2d_BezierCurve
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.GeomConvert import GeomConvert_CompBezierSurfacesToBSplineSurface
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Ax1, gp_Ax2, gp_Pnt2d #, gp_Vec
from OCC.Core.TColGeom import TColGeom_Array2OfSurface #, TColGeom_Array1OfBezierCurve
from OCC.Core.TColgp import TColgp_Array2OfPnt, TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Wire #, TopoDS_Compound
from OCC.Core.TopTools import TopTools_Array1OfShape
from OCC.Extend.DataExchange import write_step_file, write_iges_file
from OCC.Core.ShapeFix import ShapeFix_Face






##############################
##  Brep from SP entities   ##
##############################

def create_face(geom_surf = None, outer_wire = None, inner_wires=[]):
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








def new_brep_bicubic_face(o, context): # DEPRECATED
    ob = o.evaluated_get(context.evaluated_depsgraph_get())

    # Control Polygon
    points = get_attribute_by_name(ob, 'CP_bezier_surf', 'vec3', 16)
    points *= 1000 #unit correction
    controlPoints = TColgp_Array2OfPnt(1, 4, 1, 4)
    for i in range(4):
        for j in range(4):
            id= 4*i+j
            controlPoints.SetValue(i+1, j+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    # Bezier surface
    bsurf = Geom_BezierSurface(controlPoints)
    
    # Trimming wire
    try:
        point_count = get_attribute_by_name(ob, 'P_count', 'first_int')
        trimmed = True
    except Exception:
        point_count=None
        trimmed = False
        face = BRepBuilderAPI_MakeFace(bsurf, 1e-6).Face()
    
    if trimmed:
        subtype = get_attribute_by_name(ob, 'subtype', 'first_int')
        trim_pts = get_attribute_by_name(ob, 'Trim_contour', 'vec3', point_count)

        # Create points
        controlPoints = TColgp_Array1OfPnt2d(1, point_count)
        for i in range(point_count):
            pnt= gp_Pnt2d(trim_pts[i][1], trim_pts[i][0])
            controlPoints.SetValue(i+1, pnt)

        # Make edges
        if subtype :#polygon mode
            edges_list = TopTools_Array1OfShape(1, point_count)
            for i in range(point_count):
                makesegment = GCE2d_MakeSegment(controlPoints[i], controlPoints[(i+1)%point_count])
                segment = makesegment.Value()
                
                #make 3D curves
                adapt = GeomAdaptor_Surface(bsurf)
                makeEdge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface())#.Surface()
                edge = makeEdge.Edge()
                edges_list.SetValue(i+1, edge)

        else :#bezier mode
            edges_list = TopTools_Array1OfShape(1, point_count//3)
            for i in range(point_count//3):
                bezier_segment_CP_array = TColgp_Array1OfPnt2d(0,3)
                bezier_segment_CP_array.SetValue(0, controlPoints[i*3])
                bezier_segment_CP_array.SetValue(1, controlPoints[(i*3+1)%point_count])
                bezier_segment_CP_array.SetValue(2, controlPoints[(i*3+2)%point_count])
                bezier_segment_CP_array.SetValue(3, controlPoints[(i*3+3)%point_count])
                
                segment = Geom2d_BezierCurve(bezier_segment_CP_array)
                
                #make 3D curves
                adapt = GeomAdaptor_Surface(bsurf)
                makeEdge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface())#.Surface()
                edge = makeEdge.Edge()
                edges_list.SetValue(i+1, edge)

        makeWire = BRepBuilderAPI_MakeWire()
        for e in edges_list :
            makeWire.Add(e)
        trim_wire = TopoDS_Wire()
        trim_wire = makeWire.Wire()
        
        face = create_face(bsurf, trim_wire)
    return face




def new_brep_bezier_face(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
    points = get_attribute_by_name(ob, 'CP_any_order_surf', 'vec3', u_count*v_count)
    points *= 1000 #unit correction

    controlPoints = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id= u_count*i +j
            controlPoints.SetValue(j+1, i+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    bsurf = Geom_BezierSurface(controlPoints)

    # Check if trimmed
    try :
        segs_p_counts = get_attribute_by_name(ob, 'CP_count_trim_contour_UV', 'int')
    except Exception: # No trim
        segs_p_counts=None
        face = create_face(bsurf)
        return face

    # Build trim contour

    # get total_p_count
    total_p_count=0
    segment_count=0
    for p in segs_p_counts:
        if p>0:
            total_p_count += p-1
            segment_count += 1
        else :
            break
    segs_p_counts=segs_p_counts[:segment_count]

    try :
        segs_orders = get_attribute_by_name(ob, 'Contour Order', 'int', segment_count)
    except Exception :
        segs_orders = None

    # Get CP position attr
    trim_pts = get_attribute_by_name(ob, 'CP_trim_contour_UV', 'vec3', total_p_count)

    wires = split_and_prepare_wires(ob, trim_pts, total_p_count, segs_p_counts, segs_orders)

    # Get occ wires
    outer_wire = wires[-1].get_occ_wire_2d(bsurf)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_occ_wire_2d(bsurf))

    face = create_face(bsurf, outer_wire, inner_wires)
    return face




def new_brep_NURBS_face(o, context):
    # Get attributes
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
    points = get_attribute_by_name(ob, 'CP_NURBS_surf', 'vec3', u_count*v_count)
    points *= 1000 #unit correction
    order_u, order_v = get_attribute_by_name(ob, 'Orders', 'int', 2)

    # Knots and Multiplicities
    try : 
        knot_u = get_attribute_by_name(ob, 'Knot U', 'int')
        knot_v = get_attribute_by_name(ob, 'Knot V', 'int')
        mult_u = get_attribute_by_name(ob, 'Multiplicity U', 'int')
        mult_v = get_attribute_by_name(ob, 'Multiplicity V', 'int')

        # TODO (not auto)
        uknots, umult = auto_knot_and_mult(u_count, order_u) # TODO 
        vknots, vmult = auto_knot_and_mult(v_count, order_v) # TODO
    except Exception: # No trim
        uknots, umult = auto_knot_and_mult(u_count, order_u)
        vknots, vmult = auto_knot_and_mult(v_count, order_v)

    # Poles grid
    poles = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id= u_count*i +j
            poles.SetValue(j+1, i+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    # Compose Geom
    bsurf = Geom_BSplineSurface(poles, uknots, vknots, umult, vmult, order_u, order_v, False, False)

    # Check if trimmed
    try :
        segs_p_counts = get_attribute_by_name(ob, 'CP_count_trim_contour_UV', 'int')
    except Exception: # No trim
        segs_p_counts=None
        face = create_face(bsurf)
        return face

    # Build trim contour

    # get total_p_count
    total_p_count=0
    segment_count=0
    for p in segs_p_counts:
        if p>0:
            total_p_count += p-1
            segment_count += 1
        else :
            break
    segs_p_counts=segs_p_counts[:segment_count]

    try :
        segs_orders = get_attribute_by_name(ob, 'Contour Order', 'int', segment_count)
    except Exception :
        segs_orders = None

    # Get CP position attr
    trim_pts = get_attribute_by_name(ob, 'CP_trim_contour_UV', 'vec3', total_p_count)
    
    wires = split_and_prepare_wires(ob, trim_pts, total_p_count, segs_p_counts, segs_orders)

    # Get occ wires
    outer_wire = wires[-1].get_occ_wire_2d(bsurf)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_occ_wire_2d(bsurf))

    face = create_face(bsurf, outer_wire, inner_wires)
    return face












def new_brep_any_order_curve(o, context): # LEGACY
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    point_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    points = get_attribute_by_name(ob, 'CP_any_order_curve', 'vec3', point_count)
    points *= 1000 #unit correction

    controlPoints = TColgp_Array1OfPnt(1, point_count)
    for i in range(point_count):
        controlPoints.SetValue(i+1, gp_Pnt(points[i][0], points[i][1], points[i][2]))

    geom_curve = Geom_BezierCurve(controlPoints)
    curve = BRepBuilderAPI_MakeEdge(geom_curve).Edge()
    return curve




def new_brep_curve(o, context):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    segs_p_counts = get_attribute_by_name(ob, 'CP_count', 'int')

    
    # get total_p_count
    total_p_count, segment_count= 1, 0
    for p in segs_p_counts:
        if p>0:
            total_p_count += p-1
            segment_count += 1
    
    segs_p_counts = segs_p_counts[:segment_count]

    try :
        segs_orders = get_attribute_by_name(ob, 'Order', 'int', segment_count)
    except Exception :
        segs_orders = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_curve', 'vec3', total_p_count)
    points*=1000 # Unit correction

    wire = Wire(points, segs_p_counts, segs_orders)
    brep_wire = wire.get_occ_wire_3d(ob=ob)

    return brep_wire # single wire support for now




def new_brep_NURBS_curve(o, context): # TO DELETE
    # get attributes
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    point_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    order = get_attribute_by_name(ob, 'Order', 'first_int')
    points = get_attribute_by_name(ob, 'CP_NURBS_curve', 'vec3', point_count)
    knot_length = order+point_count+1 - order*2
    knot_attr = get_attribute_by_name(ob, 'Knot', 'float', knot_length)
    weight_attr = get_attribute_by_name(ob, 'Weight', 'float', point_count)
    points *= 1000 #unit correction

    # poles
    controlPoints = TColgp_Array1OfPnt(1, point_count)
    for i in range(point_count):
        controlPoints.SetValue(i+1, gp_Pnt(points[i][0], points[i][1], points[i][2]))

    # weights
    weights = TColStd_Array1OfReal(1, point_count)
    for i in range(point_count):
        weights.SetValue(i+1, weight_attr[i])

    # knots
    knots = TColStd_Array1OfReal(1,knot_length)
    for i in range(knot_length):
        knots.SetValue(i+1, knot_attr[i])
    
    # Multiplicities
    mult = TColStd_Array1OfInteger(1, knot_length)
    for i in range(knot_length):
        if i == 0 or i == knot_length-1:
            mult.SetValue(i+1, order+1)
        else :
            mult.SetValue(i+1, 1)

    #create curve
    geom_curve = Geom_BSplineCurve(controlPoints, weights, knots, mult, order)
    curve = BRepBuilderAPI_MakeEdge(geom_curve).Edge()
    return curve




def new_brep_planar_face(o, context):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    try :
        segs_p_counts = get_attribute_by_name(ob, 'CP_count', 'int')
    except Exception :
        segs_p_counts = get_attribute_by_name(ob, 'P_count', 'int')
    
    # get total_p_count
    total_p_count, segment_count= 0, 0
    for p in segs_p_counts:
        if p>0:
            total_p_count += p-1
            segment_count += 1
        if p==0:
            break
    
    segs_p_counts = segs_p_counts[:segment_count]

    try :
        segs_orders = get_attribute_by_name(ob, 'Order', 'int', segment_count)
    except Exception :
        segs_orders = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', total_p_count)
    points*=1000 # Unit correction

    wires = split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_orders)

    # Orient and place
    loc, rot, scale = o.matrix_world.decompose()
    try :
        offset = get_attribute_by_name(ob, 'planar_offset', 'vec3', 1)[0]
        orient = get_attribute_by_name(ob, 'planar_orient', 'vec3', 1)[0]
    except Exception:
        offset = [0,0,0]
        orient = [0,0,1]
    loc += rot@ Vector(offset)
    loc *= 1000
    pl_normal = rot@ Vector(orient)
    pl = gp_Pln(gp_Pnt(loc.x,loc.y,loc.z), gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z))
    geom_pl = Geom_Plane(pl)

    # Get occ wires
    outer_wire = wires[-1].get_occ_wire_3d(geom_pl)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_occ_wire_3d(geom_pl))

    face = create_face(None, outer_wire, inner_wires)
    return face







def mirror_brep(o, shape):
    ms = BRepBuilderAPI_Sewing(1e-1)
    ms.SetNonManifoldMode(True)
    ms.Add(shape)
    mshape = TopoDS_Shape()

    ms.Perform()
    shape = ms.SewedShape()
    loc, rot, scale = o.matrix_world.decompose()

    for m in o.modifiers :
        if m.type == 'MIRROR' and m.show_viewport :
            if m.mirror_object==None:
                mirror_offset = loc*1000
            else :
                loc, rot, scale = m.mirror_object.matrix_world.decompose()
                mirror_offset = loc*1000
            
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



def prepare_brep(context, use_selection, axis_up, axis_forward):
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
                case "bicubic_surf" :
                    SPobj_count +=1
                    bf = new_brep_bicubic_face(o, context)
                    aSew.Add(mirror_brep(o, bf))

                case "bezier_surf" :
                    SPobj_count +=1
                    af = new_brep_bezier_face(o, context)
                    aSew.Add(mirror_brep(o, af))

                case "NURBS_surf" :
                    SPobj_count +=1
                    nf = new_brep_NURBS_face(o, context)
                    aSew.Add(mirror_brep(o, nf))

                case "planar" :
                    SPobj_count +=1
                    pf = new_brep_planar_face(o, context)
                    aSew.Add(mirror_brep(o, pf))
                
                case "curve_any" : # LEGACY
                    SPobj_count +=1
                    ce = new_brep_any_order_curve(o, context)
                    aSew.Add(mirror_brep(o, ce))

                case "curve" :
                    SPobj_count +=1
                    cu = new_brep_curve(o, context)
                    aSew.Add(mirror_brep(o, cu))

                case "NURBS_curve" :
                    SPobj_count +=1
                    cu = new_brep_NURBS_curve(o, context)
                    aSew.Add(mirror_brep(o, cu))

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



def export_step(context, filepath, use_selection, axis_up='Z', axis_forward='Y'):
    brep_shapes = prepare_brep(context, use_selection, axis_up, axis_forward)
    if brep_shapes is not None :
        write_step_file(brep_shapes, filepath, application_protocol="AP203")
        return True
    else:
        return False

def export_iges(context, filepath, use_selection, axis_up='Z', axis_forward='Y'):
    brep_shapes = prepare_brep(context, use_selection, axis_up, axis_forward)
    if brep_shapes is not None :
        write_iges_file(brep_shapes, filepath)
        return True
    else:
        return False