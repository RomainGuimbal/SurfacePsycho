import bpy
import sys
import numpy as np
from mathutils import Vector
from os.path import dirname, abspath
from .utils import *
import copy

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
from typing import List, Dict




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
        segs_degrees = get_attribute_by_name(ob, 'Contour Degree', 'int', segment_count)
    except Exception :
        segs_degrees = None

    # Get CP position attr
    trim_pts = get_attribute_by_name(ob, 'CP_trim_contour_UV', 'vec3', total_p_count)

    wires = split_and_prepare_wires(ob, trim_pts, total_p_count, segs_p_counts, segs_degrees)

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
    bsurf = Geom_BSplineSurface(poles, uknots, vknots, umult, vmult, degree_u, degree_v, isperiodic_u, isperiodic_v)

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
        segs_degrees = get_attribute_by_name(ob, 'Contour Order', 'int', segment_count)
    except Exception :
        segs_degrees = None

    # Get CP position attr
    trim_pts = get_attribute_by_name(ob, 'CP_trim_contour_UV', 'vec3', total_p_count)
    
    wires = split_and_prepare_wires(ob, trim_pts, total_p_count, segs_p_counts, segs_degrees)

    # Get occ wires
    outer_wire = wires[-1].get_occ_wire_2d(bsurf)
    inner_wires=[]
    for k in wires.keys():
        if k!=-1:
            inner_wires.append(wires[k].get_occ_wire_2d(bsurf))

    face = create_face(bsurf, outer_wire, inner_wires)
    return face












def new_brep_curve(o, context, scale=1000):
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
        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', segment_count)
    except Exception :
        segs_degrees = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_curve', 'vec3', total_p_count)
    points*=scale # Unit correction

    wire = SP_Wire(CP = points, segs_p_counts= segs_p_counts, segs_degrees=segs_degrees)
    brep_wire = wire.get_occ_wire_3d(ob=ob)

    return brep_wire






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
        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', segment_count)
    except KeyError :
        segs_degrees = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', total_p_count)
    points*=1000 # Unit correction

    wires = split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_degrees)

    # Orient and place
    loc, rot, scale = o.matrix_world.decompose()
    try :
        offset = get_attribute_by_name(ob, 'planar_offset', 'vec3', 1)[0]
        orient = get_attribute_by_name(ob, 'planar_orient', 'vec3', 1)[0]
    except KeyError :
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

                case "curve" :
                    SPobj_count +=1
                    cu = new_brep_curve(o, context)
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















#####################################
#                                   #
#           SVG exporter            #
#                                   #
#####################################

def get_axis_ids_from_name(plane):
    match plane:
        case "XY":
            axis1 = 0
            axis2 = 1
            axis3 = 2

        case "YZ":
            axis1 = 1
            axis2 = 2
            axis3 = 0

        case "XZ":
            axis1 = 0
            axis2 = 2
            axis3 = 1

    return (axis1,axis2,axis3)

def svg_xy_string_from_CP(CP, plane="XY"):
    axis1, axis2, _ = get_axis_ids_from_name(plane)
    return f"{CP[axis1]} {-CP[axis2]} "

def svg_z_from_obj(o, plane="XY"):
    _, _, axis3 = get_axis_ids_from_name(plane)
    return o.location[axis3]




def mirror_wires_like_modifiers(o, wire_bundle : dict):
    # list of list of wires
    list_of_bundle_of_wires =[wire_bundle]
    self_matrix = o.matrix_world

    for m in o.modifiers :
        if m.type == 'MIRROR' and m.show_viewport :
            if m.mirror_object!=None:
                mirror_obj_mat = m.mirror_object.matrix_world
            else :
                mirror_obj_mat = None
            
            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            #copy bundles
            bundles_list = list_of_bundle_of_wires.copy()

            #mirror and append the copy to the original
            if x :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("X", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)
            
            if y :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Y", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)

            if z :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Z", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)
            
            list_of_bundle_of_wires = bundles_list.copy()

    return list_of_bundle_of_wires



def svg_path_string_from_wires(wires, plane):
    # SVG path string
    d =""
    for w in wires.values():
        d+="M "
        d+= svg_xy_string_from_CP(w.CP[0], plane)
        i=1
        seg_count = len(w.segs_degrees)
        for j,degree in enumerate(w.segs_degrees) :
            islast = j == seg_count-1
            if degree == 1:
                if not islast :
                    d+= "L "
                    d+= svg_xy_string_from_CP(w.CP[i], plane)
                else :
                    d+="Z "
                i+=1
            elif degree == 3:
                d+= "C "
                d+= svg_xy_string_from_CP(w.CP[i], plane)
                d+=","
                d+= svg_xy_string_from_CP(w.CP[i+1], plane)
                d+=","
                d+= svg_xy_string_from_CP(w.CP[(i+2)%(len(w.CP))], plane)
                i+=3
            else :
                print("Error, segment has degree not 1 or 3")
    return d




def new_svg_fill(o, context, plane, origin=Vector((0,0,0)), scale=100, color_mode="material"):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    segs_p_counts = get_attribute_by_name(ob, 'CP_count', 'int')

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
        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', segment_count)
    except KeyError :
        segs_degrees = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', total_p_count)
    

    # Wires
    wires_dict = split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_degrees)
    
    
    # SVG path attributes
    if color_mode == "object":
        col_rgba = o.color
    elif color_mode == "material":
        col_rgba = o.material_slots[0].material.diffuse_color
    hex_col = to_hex(col_rgba)
    color = f"#{hex_col}"
    z = svg_z_from_obj(o, plane="XY")
    fills = []

    # mirror
    mirrored_wires = mirror_wires_like_modifiers(o, wires_dict) # list of dictionaries of wires
    
    # transform
    for mw in mirrored_wires :
        for k, v in mw.items():
            v.offset(-origin)
            v.scale(scale)
    
    opacity = o.color[3]**(1/2.2) if o.color[3]!=1.0 else 1.0

    for mw in mirrored_wires :
        d = svg_path_string_from_wires(mw, plane)
        fills.append({"d": d, "color": color, "opacity": opacity, "z": z})
    
    return fills



def prepare_svg(context, use_selection, plane="XY",  origin_mode="auto", scale=100, color_mode="material"):
    shapes = []
    SPobj_count=0

    # Selection
    if use_selection:
        initial_selection = context.selected_objects
    else :
        initial_selection = context.visible_objects
    obj_list = initial_selection
    obj_to_del = []

    # Position
    if origin_mode=="auto":
        # Find bounds
        xmax, ymax, zmax = -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
        xmin, ymin, zmin = 1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308
        
        for o in initial_selection :
            bbox_corners = [o.matrix_world @ Vector(corner) for corner in o.bound_box]
            oxmax, oymax, ozmax = np.array(bbox_corners).max(axis=0)
            xmax = oxmax if oxmax > xmax else xmax
            ymax = oymax if oymax > ymax else ymax
            zmax = ozmax if ozmax > zmax else zmax
            
            oxmin, oymin, ozmin = np.array(bbox_corners).min(axis=0)
            xmin = oxmin if oxmin < xmin else xmin
            ymin = oymin if oymin < ymin else ymin
            zmin = ozmin if ozmin < zmin else zmin

        

        #origin is in top-left corner
        axis1, axis2, _ = get_axis_ids_from_name(plane)
        ox = xmin #if axis1==0 else 0
        oy = ymax if axis2==1 else ymin
        oz = zmax #if axis2==2 else 0

        mx = xmax
        my = ymin if axis2==1 else ymax
        mz = zmin
        origin = Vector((ox, oy, oz))
        size3d = (Vector((mx,my,mz))-origin)*scale

        canvas_size = (abs(size3d[axis1]), abs(size3d[axis2]))
    else : #world
        origin = Vector((0,0,0))
        #considering there is high chance a fill is placed at less than 10 blender unit from the origin
        canvas_size = (10*scale,10*scale)

    # Main entity loop
    while(len(obj_list)>0): # itterates until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            gto = geom_type_of_object(o, context)

            match gto :
                case "planar" :
                    SPobj_count +=1
                    shapes.extend(new_svg_fill(o, context, plane, origin, scale, color_mode="material"))

                # case "curve" :
                #     SPobj_count +=1
                #     cu = new_svg_curve(o, context)
                #     aSew.Add(mirror_brep(o, cu))

                # case "collection_instance":
                #     pass

        obj_list=[]
        for onr in obj_newly_real:
            obj_list.append(onr)
            obj_to_del.append(onr)

    for o in obj_to_del : # clear realized objects
        bpy.data.objects.remove(o, do_unlink=True)
    
    if SPobj_count>0 :
        shapes_sorted = list(sorted(shapes, key=lambda x: x["z"]))
        return shapes_sorted, canvas_size
    else :
        return None




def write_svg_file(contours: List[Dict[str, str]], filepath: str, canvas_size):
    # Start SVG file structure
    svg_content = f'''<svg width="{canvas_size[0]}" height="{canvas_size[1]}" xmlns="http://www.w3.org/2000/svg">\n'''
    
    # Add each contour as a separate path with its own color
    for contour in contours:
        d = contour["d"]
        color = contour.get("color", "black")  # Default to black if color not provided
        opacity = contour["opacity"]
        svg_content += f'    <path d="{d}" fill="{color}" fill-opacity="{opacity}" fill-rule="evenodd"/>\n'
    
    # Close SVG file structure
    svg_content += "</svg>"
    
    # Write the SVG content to file
    with open(filepath, "w") as svg_file:
        svg_file.write(svg_content)

    print("SVG Export succesful")



def export_svg(context, filepath, use_selection, plane="XY", origin_mode="auto", scale=100, color_mode="material"):
    svg_shapes, canvas_size = prepare_svg(context, use_selection, plane,  origin_mode, scale, color_mode)
    if svg_shapes is not None :
        write_svg_file(svg_shapes, filepath, canvas_size)
        return True
    else:
        return False
