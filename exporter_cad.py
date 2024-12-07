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


from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform
from OCP.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_Plane #Geom_BezierCurve, Geom_TrimmedCurve, Geom_BSplineCurve
from OCP.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Ax1, gp_Ax2 #gp_Pnt2d #, gp_Vec
from OCP.TColgp import TColgp_Array2OfPnt
from OCP.TopoDS import TopoDS_Shape #TopoDS_Wire, TopoDS_Compound
from OCP.ShapeFix import ShapeFix_Face
from OCP.IGESControl import IGESControl_Writer
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.Interface import Interface_Static
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform




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






def new_brep_planar_face(o, context, scale=1000):
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
    points*=scale # Unit correction

    wires = split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_degrees)

    # Orient and place
    loc, rot, obj_scale = o.matrix_world.decompose()
    try :
        offset = get_attribute_by_name(ob, 'planar_offset', 'vec3', 1)[0]
        orient = get_attribute_by_name(ob, 'planar_orient', 'vec3', 1)[0]
    except KeyError :
        offset = [0,0,0]
        orient = [0,0,1]
    loc += rot@ Vector(offset)
    loc *= scale
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
                    pf = new_brep_planar_face(o, context, scale)
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