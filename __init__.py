# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Surface Psycho",
    "author": "Romain Guimbal",
    "version": (0, 4),
    "blender": (4, 1, 0),
    "description": "Surface design for the mechanical industry",
    "warning": "Alpha",
    "doc_url": "https://github.com/RomainGuimbal/SurfacePsycho/wiki",
    "category": "3D View",
    "location": "View3D > Add > Surface  |  View3D > N Panel > Edit"
}

import bpy
import sys
import numpy as np
from mathutils import Vector

from datetime import datetime
from os.path import dirname, abspath

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

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

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"

from macros import *






##############################
##         FUNCTIONS        ##
##############################

def append_object_by_name(obj_name, context):# for importing from the asset file
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name==obj_name]

    cursor_loc = context.scene.cursor.location

    for o in data_to.objects:
        if o is not None:
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            context.collection.objects.link(o)
            o.location = cursor_loc
            o.asset_clear()
            o.select_set(True)
            bpy.context.view_layer.objects.active = o


def get_attribute_by_name(ob_deps_graph, name, type='vec3', len_attr=None):
    ge = ob_deps_graph.data
    match type :
        case 'first_int':
            attribute = ge.attributes[name].data[0].value
        case 'second_int':
            attribute = ge.attributes[name].data[1].value
        case 'vec3':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.empty(3 * len_raw)
            ge.attributes[name].data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]
    return attribute









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
        points_occ = TColgp_Array1OfPnt2d(1, point_count)
        for i in range(point_count):
            pnt= gp_Pnt2d(trim_pts[i][1], trim_pts[i][0])
            points_occ.SetValue(i+1, pnt)

        #make edges
        if subtype :#polygon mode
            edges_list = TopTools_Array1OfShape(1, point_count)
            for i in range(point_count):
                makesegment = GCE2d_MakeSegment(points_occ[i], points_occ[(i+1)%point_count])
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
                bezier_segment_CP_array.SetValue(0, points_occ[i*3])
                bezier_segment_CP_array.SetValue(1, points_occ[(i*3+1)%point_count])
                bezier_segment_CP_array.SetValue(2, points_occ[(i*3+2)%point_count])
                bezier_segment_CP_array.SetValue(3, points_occ[(i*3+3)%point_count])
                
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
        points_occ = TColgp_Array1OfPnt2d(1, point_count)
        for i in range(point_count):
            pnt= gp_Pnt2d(trim_pts[i][1], trim_pts[i][0])
            points_occ.SetValue(i+1, pnt)

        #make edges
        if subtype :#polygon mode
            edges_list = TopTools_Array1OfShape(1, point_count)
            for i in range(point_count):
                makesegment = GCE2d_MakeSegment(points_occ[i], points_occ[(i+1)%point_count])
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
                bezier_segment_CP_array.SetValue(0, points_occ[i*3])
                bezier_segment_CP_array.SetValue(1, points_occ[(i*3+1)%point_count])
                bezier_segment_CP_array.SetValue(2, points_occ[(i*3+2)%point_count])
                bezier_segment_CP_array.SetValue(3, points_occ[(i*3+3)%point_count])
                
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


def new_brep_planar_face(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    point_count = get_attribute_by_name(ob, 'P_count', 'first_int')
    subtype = get_attribute_by_name(ob, 'subtype', 'first_int')
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', point_count)
    points*=1000 #unit correction

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
    points_occ = TColgp_Array1OfPnt(1, point_count)
    for i in range(point_count):
        pnt= gp_Pnt(points[i][0], points[i][1], points[i][2])
        pnt= GeomAPI_ProjectPointOnSurf(pnt, geom_pl).Point(1)
        points_occ.SetValue(i+1, pnt)

    # Make contour
    if subtype :#polygon mode
        edges_list = TopTools_Array1OfShape(1, point_count)
        for i in range(point_count):
            makesegment = GC_MakeSegment(points_occ[i], points_occ[(i+1)%point_count])
            segment = makesegment.Value()
            edge = BRepBuilderAPI_MakeEdge(segment).Edge()
            edges_list.SetValue(i+1, edge)

    else :#bezier mode
        edges_list = TopTools_Array1OfShape(1, point_count//3)
        for i in range(point_count//3):
            bezier_segment_CP_array = TColgp_Array1OfPnt(0,3)
            bezier_segment_CP_array.SetValue(0, points_occ[i*3])
            bezier_segment_CP_array.SetValue(1, points_occ[(i*3+1)%point_count])
            bezier_segment_CP_array.SetValue(2, points_occ[(i*3+2)%point_count])
            bezier_segment_CP_array.SetValue(3, points_occ[(i*3+3)%point_count])
            
            segment = Geom_BezierCurve(bezier_segment_CP_array)
            edge = BRepBuilderAPI_MakeEdge(segment).Edge()
            edges_list.SetValue(i+1, edge)

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
    return type


def mirrors(o, shape):
    ms = BRepBuilderAPI_Sewing(1e-1)
    ms.SetNonManifoldMode(True)
    ms.Add(shape)
    mshape = TopoDS_Shape()

    ms.Perform()
    shape = ms.SewedShape()
    loc, rot, scale = o.matrix_world.decompose()

    for m in o.modifiers :
        if m.type == 'MIRROR':
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
    
    while(len(obj_list)>0): # itterate until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            gto = geom_type_of_object(o, context)

            match gto :
                case "bezier_surf" :
                    SPobj_count +=1
                    bf = new_brep_bezier_face(o, context)
                    aSew.Add(mirrors(o, bf))

                case "surf_any" :
                    SPobj_count +=1
                    af = new_brep_any_order_face(o, context)
                    aSew.Add(mirrors(o, af))

                case "planar" :
                    SPobj_count +=1
                    pf = new_brep_planar_face(o, context)
                    aSew.Add(mirrors(o, pf))
                
                case "curve_any" :
                    SPobj_count +=1
                    ce = new_brep_any_order_curve(o, context)
                    aSew.Add(mirrors(o, ce))
                
                case "bezier_chain" :
                    SPobj_count +=1
                    bc = new_brep_cubic_bezier_chain(o, context)
                    aSew.Add(mirrors(o, bc))

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














##############################
##       OPERTATORS         ##
##############################
    
class SP_OT_quick_export(bpy.types.Operator):
    bl_idname = "sp.quick_export"
    bl_label = "SP - Quick export"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        blenddir = bpy.path.abspath("//")
        if blenddir !="":#avoids exporting to root
            dir =  blenddir
        else :
            dir = context.preferences.filepaths.temporary_directory
        pathstr = dir + str(datetime.today())[:-7].replace('-','').replace(' ','-').replace(':','')

        export_isdone = export_step(context, f"{pathstr}.step", True)
        if export_isdone:
            self.report({'INFO'}, f"Step file exported as {pathstr}.step")
        else :
            self.report({'INFO'}, 'No SurfacePsycho Objects selected')
        return {'FINISHED'}

class SP_OT_add_bicubic_patch(bpy.types.Operator):
    bl_idname = "sp.add_bicubic_patch"
    bl_label = "Add Bicubic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoPatch", context)
        return {'FINISHED'}
    
class SP_OT_add_biquadratic_patch(bpy.types.Operator):
    bl_idname = "sp.add_biquadratic_patch"
    bl_label = "Add Biquadratic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoPatch Quadratic", context)
        return {'FINISHED'}
    
class SP_OT_add_aop(bpy.types.Operator):
    bl_idname = "sp.add_aop"
    bl_label = "Add Any Order PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoPatch Any Order", context)
        return {'FINISHED'}
    
class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "sp.add_flat_patch"
    bl_label = "Add flat PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("FlatPatch", context)
        return {'FINISHED'}

class SP_OT_add_cubic_bezier_chain(bpy.types.Operator):
    bl_idname = "sp.add_cubic_bezier_chain"
    bl_label = "Add Cubic Bezier Chain"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("Psycho Cubic Chain", context)
        return {'FINISHED'}
    
class SP_OT_add_any_order_curve(bpy.types.Operator):
    bl_idname = "sp.add_any_order_curve"
    bl_label = "Add Any Order PsychoCurve"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("PsychoCurve Any Order", context)
        return {'FINISHED'}

class SP_OT_add_curvatures_probe(bpy.types.Operator):
    bl_idname = "sp.add_curvatures_probe"
    bl_label = "Add Curvatures Probe"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        append_object_by_name("SP - Curvatures Probe", context)
        return {'FINISHED'}

class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "sp.add_library"
    bl_label = "Add Library"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        asset_lib_path = dirname(abspath(__file__))
        paths = [a.path for a in bpy.context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths :
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)
        return {'FINISHED'}

class SP_OT_psychopatch_to_bl_nurbs(bpy.types.Operator):
    bl_idname = "sp.psychopatch_to_bl_nurbs"
    bl_label = "Convert Psychopatches to internal NURBS"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        i=-1
        for o in context.selected_objects :
            type = geom_type_of_object(o, context)
            ob = o.evaluated_get(context.evaluated_depsgraph_get())
            match type :
                case "bezier_surf":
                    cp=get_attribute_by_name(ob, 'CP_bezier_surf', 'vec3', 16)
                    bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                    i+=1
                    spline=context.active_object.data.splines[i]
                    spline.use_endpoint_u = True
                    spline.use_endpoint_v = True
                    spline.order_u = 4
                    spline.order_v = 4
                    
                    # set CP of spline
                    for j,p in enumerate(spline.points): 
                        p.co = (cp[j][0], cp[j][1], cp[j][2], 1)
                    
                case "surf_any":
                    u_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
                    v_count = get_attribute_by_name(ob, 'CP_count', 'second_int')
                    cp=get_attribute_by_name(ob, 'CP_any_order_surf', 'vec3', u_count*v_count)
                    if i == -1 :
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.ops.curve.delete(type='VERT')
                    i+=1
                    splines = context.active_object.data.splines
                    for v in range(v_count):
                        spline = splines.new('NURBS')
                        spline.points.add(u_count-1)
                        spline.use_endpoint_u = True
                        spline.use_endpoint_v = True
                        spline.use_bezier_u = True
                        spline.use_bezier_v = True
                        # set CP of spline
                        for j,p in enumerate(spline.points): 
                            p.co = (cp[j+v*u_count][0], cp[j+v*u_count][1], cp[j+v*u_count][2], 1)

                    for s in splines[i:i+v_count]:
                        for p in s.points:
                            p.select = True
                    bpy.ops.object.mode_set(mode = 'EDIT') 
                    bpy.ops.curve.make_segment()
                    splines[i].order_u =min(v_count,6)
                    splines[i].order_v =min(u_count,6)
                
                case "curve_any":
                    cp_count = get_attribute_by_name(ob, 'CP_count', 'first_int')
                    cp=get_attribute_by_name(ob, 'CP_any_order_curve', 'vec3', cp_count)
                    if i == -1 :
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        bpy.ops.curve.delete(type='VERT')
                    i+=1
                    spline = context.active_object.data.splines.new('NURBS')
                    spline.points.add(cp_count-1)
                    spline.use_endpoint_u = True
                    spline.use_endpoint_v = True
                    spline.use_bezier_u = True
                    spline.use_bezier_v = True
                    spline.order_u =min(cp_count,6)
                    spline.order_v =min(cp_count,6)

                    # set CP of spline
                    for j,p in enumerate(spline.points): 
                        p.co = (cp[j][0], cp[j][1], cp[j][2], 1)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class SP_OT_bl_nurbs_to_psychopatch(bpy.types.Operator):
    bl_idname = "sp.bl_nurbs_to_psychopatch"
    bl_label = "Convert internal NURBS to Psychopatches"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj_to_convert = context.selected_objects
        first_patch_flag=True

        for o in obj_to_convert:
            if o.type == 'SURFACE':
                for s in o.data.splines:
                    if first_patch_flag :
                        append_object_by_name("PsychoPatch Any Order", context)
                        first_sp_patch = context.selected_objects[0]
                        first_sp_patch.location = o.location
                        sp_patch = first_sp_patch
                        first_patch_flag = False
                    else :
                        sp_patch = first_sp_patch.copy()
                        sp_patch.animation_data_clear()
                        sp_patch.matrix_world = o.matrix_world
                        bpy.context.collection.objects.link(sp_patch)

                    spline_cp = [Vector(p.co[0:3]) for p in s.points]
                    
                    #create mesh grid
                    u_count = s.order_u
                    v_count = s.order_v
                    
                    faces = [(v*u_count + u, (v + 1)*u_count + u, (v + 1)*u_count + 1 + u, v*u_count + 1 + u) for v in range(v_count-1) for u in range(u_count-1)]
                    mesh = bpy.data.meshes.new("Grid") 
                    mesh.from_pydata(spline_cp, [], faces)
                    sp_patch.data=mesh
                    bpy.ops.object.shade_smooth()
        return {'FINISHED'}




from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import (
    ExportHelper,
    orientation_helper,
    axis_conversion,
)

@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.step_export"
    bl_label = "Export STEP"

    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    axis_up: EnumProperty(default='Z')
    axis_forward: EnumProperty(default='Y')

    def execute(self, context):
        export_step(context, self.filepath, self.use_selection, self.axis_up, self.axis_forward)
        return {'FINISHED'}


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.iges_export"
    bl_label = "Export IGES"

    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    axis_up: EnumProperty(default='Z')
    axis_forward: EnumProperty(default='Y')

    def execute(self, context):
        export_iges(context, self.filepath, self.use_selection,self.axis_up, self.axis_forward)
        return {'FINISHED'}




















##############################
##          MENUES          ##
##############################

class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            if os == "Windows" :
                row = self.layout.row()
                row.scale_y = 2.0
                row.operator("sp.quick_export", text="Quick export as .STEP", icon="EXPORT")
            row = self.layout.row()
            row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR")
            row = self.layout.row()
            row.operator("sp.toogle_control_geom", text="Toogle Control Geometry", icon="OUTLINER_DATA_LATTICE")
            
            self.layout.label(text="Select Entities")
            row = self.layout.row()
            row.operator("sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE")
            row = self.layout.row()
            row.operator("sp.select_visible_surfaces", text="Surfaces", icon="OUTLINER_OB_SURFACE")
            


class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("sp.add_library", text="Add Assets Path")

def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_aop", text="Any Order PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_bicubic_patch", text="Bicubic PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_biquadratic_patch", text="Biquadratic PsychoPatch", icon="SURFACE_NSURFACE") #almost deprecated
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_cubic_bezier_chain", text="Cubic Bezier Chain", icon="CURVE_BEZCURVE")
        self.layout.operator("sp.add_any_order_curve", text="Any Order PsychoCurve", icon="CURVE_NCURVE")


def menu_convert(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.bl_nurbs_to_psychopatch", text="Internal NURBS to PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.psychopatch_to_bl_nurbs", text="PsychoPatch to internal NURBS", icon="SURFACE_NSURFACE")


def menu_export_step(self, context):
    self.layout.operator("sp.step_export", text="SurfacePsycho CAD (.step)")

def menu_export_iges(self, context):
    self.layout.operator("sp.iges_export", text="SurfacePsycho CAD (.iges)")




##############################
##         REGISTER         ##
##############################

classes = (
    SP_AddonPreferences,
    SP_OT_add_any_order_curve,
    SP_OT_add_aop,
    SP_OT_add_bicubic_patch,
    SP_OT_add_biquadratic_patch,
    SP_OT_add_cubic_bezier_chain,
    SP_OT_add_curvatures_probe,
    SP_OT_add_flat_patch,
    SP_OT_add_library,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_quick_export,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_toogle_control_geom,
    SP_PT_MainPanel,
    SP_OT_ExportStep,
    SP_OT_ExportIges,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_class(SP_OT_add_library)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)

    
    

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)

if __name__ == "__main__":
    register()