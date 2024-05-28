import bpy
import numpy as np
from OCC.Extend.TopologyUtils import is_face, is_edge, is_compound, is_shell
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRep import BRep_Tool
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCC.Core.TopoDS import TopoDS_Iterator
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.Geom import Geom_BezierSurface
from mathutils import Vector
from os.path import abspath
from utils import *





def build_SP_curve(brepEdge, context) :
    # curve info
    curve_adaptator = BRepAdaptor_Curve(brepEdge)
    first = curve_adaptator.FirstParameter()
    last = curve_adaptator.LastParameter()
    degree = curve_adaptator.GetType()

    #retrieve CP
    ts = np.linspace(first, last, degree+1)
    vector_pts = []
    for t in ts :
        gp_pnt=curve_adaptator.Value(t)
        vector_pts+=[Vector((gp_pnt.X()/1000, gp_pnt.Y()/1000, gp_pnt.Z()/1000))]
    
    # create object
    mesh = bpy.data.meshes.new("Curve CP")
    vert = vector_pts
    edges = [(i,i+1) for i in range(len(vector_pts)-1)]
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP curve', mesh)
    context.scene.collection.objects.link(ob)
    return True


def build_SP_patch(brepFace, context) :
    # curve info
    surf_adaptator = BRepAdaptor_Surface(brepFace)
    firstU = surf_adaptator.FirstUParameter()
    lastU = surf_adaptator.LastUParameter()
    firstV = surf_adaptator.FirstVParameter()
    lastV = surf_adaptator.LastVParameter()
    degreeU = surf_adaptator.UDegree()
    degreeV = surf_adaptator.VDegree()
    
    # #### Retrieve poles ##### 
    # the surface adaptor seems to lose the poles :/

    # u_count, v_count = surf_adaptator.NbUPoles(), surf_adaptator.NbVPoles()
    # print("Poles of the Bézier surface:")
    # for u in range(1, u_count + 1):
    #     for v in range(1, v_count + 1):
    #         pole = surf_adaptator.Pole(u, v)
    #         print(f"Pole ({u}, {v}): ({pole.X()}, {pole.Y()}, {pole.Z()})")


    #retrieve CP
    us = np.linspace(firstU, lastU, degreeU+1)
    vs = np.linspace(firstV, lastV, degreeV+1)
    
    vector_pts = np.zeros((degreeU+1, degreeV+1), dtype=Vector)
    for i,u in enumerate(us):
        for j,v in enumerate(vs):
            gp_pnt=surf_adaptator.Value(u,v)
            vector_pts[i, j] = Vector((gp_pnt.X()/1000, gp_pnt.Y()/1000, gp_pnt.Z()/1000))

    # create object
    mesh = bpy.data.meshes.new("Patch CP")
    vert, edges, faces = create_grid(vector_pts)
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    context.scene.collection.objects.link(ob)
    return True


def recursive_SP_from_brep_shape(shape, context, level=0):
    tab = "  " * level
    shape_type = shape.ShapeType()
    if shape_type == TopAbs_COMPOUND:
        print(f"{tab}Compound")
        # MAKE COLLECTION
    elif shape_type == TopAbs_COMPSOLID:
        print(f"{tab}CompSolid")
    elif shape_type == TopAbs_SOLID:
        print(f"{tab}Solid")
    elif shape_type == TopAbs_SHELL:
        print(f"{tab}Shell")
    elif shape_type == TopAbs_FACE:
        print(f"{tab}Face")
        try :
            build_SP_patch(shape, context)
        except Exception:
            pass
    elif shape_type == TopAbs_WIRE:
        print(f"{tab}Wire")
    elif shape_type == TopAbs_EDGE:
        build_SP_curve(shape, context)
        print(f"{tab}Edge")
    elif shape_type == TopAbs_VERTEX:
        print(f"{tab}Vertex")
    else:
        print(f"{tab}Unknown shape type")

    explorer = TopoDS_Iterator(shape)
    while explorer.More():
        sub_shape = explorer.Value()
        recursive_SP_from_brep_shape(sub_shape, context, level + 1)
        explorer.Next()


def build_SP_from_brep(shape, context):
    #Add SP entities
    recursive_SP_from_brep_shape(shape, context)

    #TODO : Add brep relations (face connections...)

    return True


def import_step(filepath, context):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filepath)
    if status != IFSelect_RetDone:
        raise ValueError("Error reading STEP file")
    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    build_SP_from_brep(shape, context)
    

