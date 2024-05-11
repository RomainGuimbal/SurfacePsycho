import bpy
import sys
import numpy as np
from mathutils import Vector
from datetime import datetime
from os.path import dirname, abspath

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"


import platform
os = platform.system()
if os=="Windows":
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge2d
    # from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
    from OCC.Core.GC import GC_MakeSegment
    from OCC.Core.GCE2d import GCE2d_MakeSegment
    from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_Plane, Geom_TrimmedCurve #, Geom_BSplineCurve
    from OCC.Core.Geom2d import Geom2d_BezierCurve
    from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
    from OCC.Core.GeomConvert import GeomConvert_CompBezierSurfacesToBSplineSurface
    from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Ax1, gp_Ax2, gp_Pnt2d #, gp_Vec
    from OCC.Core.TColGeom import TColGeom_Array2OfBezierSurface #, TColGeom_Array1OfBezierCurve
    from OCC.Core.TColgp import TColgp_Array2OfPnt, TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
    from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Wire #, TopoDS_Compound
    from OCC.Core.TopTools import TopTools_Array1OfShape
    from OCC.Extend.DataExchange import write_step_file, write_iges_file
    from OCC.Core.ShapeFix import ShapeFix_Face




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
        case 'vec3':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.empty(3 * len_raw)
            ge.attributes[name].data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]
    return attribute







##############################
##  Brep from SP entities   ##
##############################

def new_brep_bezier_face(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())

    # Control Polygon
    points = get_attribute_by_name(ob, 'CP_bezier_surf', 'vec3', 16)
    points *= 1000 #unit correction
    controlPoints = TColgp_Array2OfPnt(1, 4, 1, 4)
    for i in range(4):
        for j in range(4):
            id= 4*i+j
            controlPoints.SetValue(i+1, j+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    #Bezier surface
    geom_surf = Geom_BezierSurface(controlPoints)
    bezierarray = TColGeom_Array2OfBezierSurface(1, 1, 1, 1)
    bezierarray.SetValue(1, 1, geom_surf)
    
    bspline_param = GeomConvert_CompBezierSurfacesToBSplineSurface(bezierarray)
    if bspline_param.IsDone():
        poles = bspline_param.Poles().Array2()
        uknots = bspline_param.UKnots().Array1()
        vknots = bspline_param.VKnots().Array1()
        umult = bspline_param.UMultiplicities().Array1()
        vmult = bspline_param.VMultiplicities().Array1()
        udeg = bspline_param.UDegree()
        vdeg = bspline_param.VDegree()

        bsurf = Geom_BSplineSurface( poles, uknots, vknots, umult, vmult, udeg, vdeg, False, False )
    
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

        #make edges
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
        
        makeface = BRepBuilderAPI_MakeFace(bsurf, trim_wire, False)#,1e-6)#, trim_wire)
        # makeface.Add(trim_wire)#.Reversed())
        face = makeface.Face()
        fix = ShapeFix_Face(face)
        fix.Perform()
        face= fix.Face()
    return face



def new_brep_any_order_face(o, context):
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

    geom_surf = Geom_BezierSurface(controlPoints)
    bezierarray = TColGeom_Array2OfBezierSurface(1, 1, 1, 1)
    bezierarray.SetValue(1, 1, geom_surf)
    
    bspline_param = GeomConvert_CompBezierSurfacesToBSplineSurface(bezierarray)
    if bspline_param.IsDone():
        poles = bspline_param.Poles().Array2()
        uknots = bspline_param.UKnots().Array1()
        vknots = bspline_param.VKnots().Array1()
        umult = bspline_param.UMultiplicities().Array1()
        vmult = bspline_param.VMultiplicities().Array1()
        udeg = bspline_param.UDegree()
        vdeg = bspline_param.VDegree()

        bsurf = Geom_BSplineSurface( poles, uknots, vknots, umult, vmult, udeg, vdeg, False, False )
    
    # Check if trimmed
    try: # Old
        point_count = get_attribute_by_name(ob, 'P_count', 'first_int')
        trimmed = True
        old_version = True
    except Exception:
        try : # New
            point_count = get_attribute_by_name(ob, 'CP_count_trim_contour_UV', 'int')
            point_count = [int(p) for p in point_count]
            trimmed = True
            old_version = False
            
        except Exception: # No trim
            point_count=None
            trimmed = False
            face = BRepBuilderAPI_MakeFace(bsurf, 1e-6).Face()

    # old behaviour
    try :
        subtype = get_attribute_by_name(ob, 'subtype', 'first_int')
    except Exception:
        pass
    else :
        if subtype :
            point_count = [2]*point_count
        elif not subtype :
            point_count = [4]*(point_count//3)
        else :
            raise Exception("Invalid subtype attribute")


    # Build trim contour
    if trimmed:
        total_p_count = 0
        segment_count = 0
        p_count_accumulate = point_count[:]
        for i, p in enumerate(point_count):
            if p>0:
                total_p_count += p-1
                segment_count += 1
            if p==0 :
                break
            if i>0:
                p_count_accumulate[i] += p_count_accumulate[i-1]-1

        first_segment_p_id = [0] + [p-1 for p in p_count_accumulate[:segment_count-1]]


        if old_version :
            subtype = get_attribute_by_name(ob, 'subtype', 'first_int')
            trim_pts = get_attribute_by_name(ob, 'Trim_contour', 'vec3', point_count)
        else :
            trim_pts = get_attribute_by_name(ob, 'CP_trim_contour_UV', 'vec3', total_p_count)

        # Create 2D points
        controlPoints = TColgp_Array1OfPnt2d(1, total_p_count)
        for i in range(total_p_count):
            pnt= gp_Pnt2d(trim_pts[i][1], trim_pts[i][0])
            controlPoints.SetValue(i+1, pnt)

        # Create edge list
        edges_list = TopTools_Array1OfShape(1, segment_count)
        for i in range(segment_count):
            segment_point_array = TColgp_Array1OfPnt2d(1, point_count[i])
            for j in range(point_count[i]):
                segment_point_array.SetValue(j+1, controlPoints.Value((first_segment_p_id[i]+j)%total_p_count+1))
            segment = Geom2d_BezierCurve(segment_point_array)

            # make curve 3D
            adapt = GeomAdaptor_Surface(bsurf)
            makeEdge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface())#.Surface()
            edge = makeEdge.Edge()
            edges_list.SetValue(i+1, edge)

    #     # make edges
    #     if subtype : # polygon mode
    #         edges_list = TopTools_Array1OfShape(1, point_count)
    #         for i in range(point_count):
    #             makesegment = GCE2d_MakeSegment(controlPoints[i], controlPoints[(i+1)%point_count])
    #             segment = makesegment.Value()
                
    #             # make 3D curves
    #             adapt = GeomAdaptor_Surface(bsurf)
    #             makeEdge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface())#.Surface()
    #             edge = makeEdge.Edge()
    #             edges_list.SetValue(i+1, edge)

    #     else : # bezier mode
    #         edges_list = TopTools_Array1OfShape(1, point_count//3)
    #         for i in range(point_count//3):
    #             bezier_segment_CP_array = TColgp_Array1OfPnt2d(0,3)
    #             bezier_segment_CP_array.SetValue(0, controlPoints[i*3])
    #             bezier_segment_CP_array.SetValue(1, controlPoints[(i*3+1)%point_count])
    #             bezier_segment_CP_array.SetValue(2, controlPoints[(i*3+2)%point_count])
    #             bezier_segment_CP_array.SetValue(3, controlPoints[(i*3+3)%point_count])
                
    #             segment = Geom2d_BezierCurve(bezier_segment_CP_array)
                
    #             # make 3D curves
    #             adapt = GeomAdaptor_Surface(bsurf)
    #             makeEdge = BRepBuilderAPI_MakeEdge(segment, adapt.Surface())#.Surface()
    #             edge = makeEdge.Edge()
    #             edges_list.SetValue(i+1, edge)

        makeWire = BRepBuilderAPI_MakeWire()
        for e in edges_list :
            makeWire.Add(e)
        trim_wire = TopoDS_Wire()
        trim_wire = makeWire.Wire()
        
        makeface = BRepBuilderAPI_MakeFace(bsurf, trim_wire, False)#,1e-6)#, trim_wire)
        # makeface.Add(trim_wire)#.Reversed())
        face = makeface.Face()
        fix = ShapeFix_Face(face)
        fix.Perform()
        face= fix.Face()

    return face










































def new_brep_any_order_curve(o, context):
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



def new_brep_cubic_bezier_chain(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    point_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
    points = get_attribute_by_name(ob, 'CP_bezier_chain', 'vec3', point_count)
    points *= 1000 #unit correction

    # Create CP
    controlPoints = TColgp_Array1OfPnt(1, point_count)
    for i in range(point_count):
        pnt= gp_Pnt(points[i][0], points[i][1], points[i][2])
        controlPoints.SetValue(i+1, pnt)

    ms = BRepBuilderAPI_Sewing(1e-1)
    ms.SetNonManifoldMode(True)
    
    for i in range(point_count//3):
        bezier_segment_CP_array = TColgp_Array1OfPnt(0,3)
        bezier_segment_CP_array.SetValue(0, controlPoints[i*3])
        bezier_segment_CP_array.SetValue(1, controlPoints[(i*3+1)%point_count])
        bezier_segment_CP_array.SetValue(2, controlPoints[(i*3+2)%point_count])
        bezier_segment_CP_array.SetValue(3, controlPoints[(i*3+3)%point_count])
        
        segment = Geom_BezierCurve(bezier_segment_CP_array)
        edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        ms.Add(edge)

    ms.Perform()
    chain = ms.SewedShape()
    return chain



def new_brep_curve(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    point_count = get_attribute_by_name(ob, 'CP_count', 'int')
    point_count = [int(p) for p in point_count]
    total_p_count = 1
    segment_count = 0
    p_count_accumulate = point_count
    for i, p in enumerate(point_count):
        if p>0:
            total_p_count += p-1
            segment_count += 1
        if p==0:
            break
        if i>0:
            p_count_accumulate[i] += p_count_accumulate[i-1]-1

    first_segment_p_id = [0] + [p-1 for p in p_count_accumulate[:segment_count]]
    points = get_attribute_by_name(ob, 'CP_curve', 'vec3', total_p_count)
    points *= 1000 #unit correction

    # Create CP
    controlPoints = TColgp_Array1OfPnt(1, total_p_count)
    for i in range(total_p_count):
        controlPoints.SetValue(i+1, gp_Pnt(points[i][0], points[i][1], points[i][2]))

    #init sewing
    ms = BRepBuilderAPI_Sewing(1e-7)
    ms.SetNonManifoldMode(True)

    #create segments
    for i in range(segment_count):
        segment_point_array = TColgp_Array1OfPnt(first_segment_p_id[i], first_segment_p_id[i+1])
        for j in range(first_segment_p_id[i], first_segment_p_id[i+1]+1):
            segment_point_array.SetValue(j, controlPoints.Value(j+1))
            
        segment = Geom_BezierCurve(segment_point_array)
        edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        ms.Add(edge)

    #sew segments
    ms.Perform()
    curve = ms.SewedShape()
    return curve



def new_brep_planar_face(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    try:
        point_count = get_attribute_by_name(ob, 'CP_count', 'int')
    except Exception:
        point_count = get_attribute_by_name(ob, 'P_count', 'int')
        
    point_count = [int(p) for p in point_count]
    
    # Old behaviour
    try :
        subtype = get_attribute_by_name(ob, 'subtype', 'first_int')
    except Exception:
        pass
    else :
        if subtype :
            point_count = [2]*point_count[0]
        else :
            point_count = [4]*(point_count[0]//3)

    total_p_count = 0
    segment_count = 0
    p_count_accumulate = point_count[:]
    for i, p in enumerate(point_count):
        if p>0:
            total_p_count += p-1
            segment_count += 1
        if p==0:
            break
        if i>0:
            p_count_accumulate[i] += p_count_accumulate[i-1]-1

    first_segment_p_id = [0] + [p-1 for p in p_count_accumulate[:segment_count-1]]
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', total_p_count)
    points*=1000 # Unit correction

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
    pl = gp_Pln(gp_Pnt(loc.x,loc.y,loc.z),gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z))
    geom_pl = Geom_Plane(pl)

    # Create CP
    controlPoints = TColgp_Array1OfPnt(1, total_p_count)
    for i in range(total_p_count):
        pnt = gp_Pnt(points[i][0], points[i][1], points[i][2])
        pnt = GeomAPI_ProjectPointOnSurf(pnt, geom_pl).Point(1)
        controlPoints.SetValue(i+1, pnt)
    
    # Create segments
    edges_list = TopTools_Array1OfShape(1, segment_count)
    for i in range(segment_count):
        if point_count[i] == 2: # straight edges
            makesegment = GC_MakeSegment(controlPoints.Value((first_segment_p_id[i])%total_p_count+1), 
                                         controlPoints.Value((first_segment_p_id[i]+1)%total_p_count+1))
            segment = makesegment.Value()
        else:
            segment_point_array = TColgp_Array1OfPnt(1, point_count[i])

            for j in range(point_count[i]):
                segment_point_array.SetValue(j+1, controlPoints.Value((first_segment_p_id[i]+j)%total_p_count+1))
            segment = Geom_BezierCurve(segment_point_array)

        edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        edges_list.SetValue(i+1, edge)

    # Make contour
    makeWire = BRepBuilderAPI_MakeWire()
    for e in edges_list :
        makeWire.Add(e)
    w = TopoDS_Wire()
    w = makeWire.Wire()

    aface = BRepBuilderAPI_MakeFace(w, True).Face()
    return aface










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
                        type = 'bezier_surf'
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
                    case 'CP_bezier_chain':
                        type = 'bezier_chain'
                        break
                    case 'CP_curve':
                        type = 'curve'
                        break
    return type



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
                    ms.Add(mshape)
            
            ms.Perform()
            shape = ms.SewedShape()
            
    # ms.Perform()
    shape = ms.SewedShape()
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
    
    while(len(obj_list)>0): # itterates until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            gto = geom_type_of_object(o, context)

            match gto :
                case "bezier_surf" :
                    SPobj_count +=1
                    bf = new_brep_bezier_face(o, context)
                    aSew.Add(mirror_brep(o, bf))

                case "surf_any" :
                    SPobj_count +=1
                    af = new_brep_any_order_face(o, context)
                    aSew.Add(mirror_brep(o, af))

                case "planar" :
                    SPobj_count +=1
                    pf = new_brep_planar_face(o, context)
                    aSew.Add(mirror_brep(o, pf))
                
                case "curve_any" :
                    SPobj_count +=1
                    ce = new_brep_any_order_curve(o, context)
                    aSew.Add(mirror_brep(o, ce))
                
                case "bezier_chain" :
                    SPobj_count +=1
                    bc = new_brep_cubic_bezier_chain(o, context)
                    aSew.Add(mirror_brep(o, bc))

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