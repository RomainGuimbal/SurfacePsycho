import bpy
import numpy as np
from OCC.Extend.TopologyUtils import is_face, is_edge, is_compound, is_shell
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_COMPOUND, TopAbs_EDGE, TopAbs_FACE, TopAbs_SHELL, TopAbs_UNKNOWN, TopAbs_SHAPE
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
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

    #retrieve CP
    us = np.linspace(firstU, lastU, degreeU+1)
    vs = np.linspace(firstV, lastV, degreeV+1)
    
    vector_pts = np.zeros((degreeU+1, degreeV+1), dtype=Vector)
    for u in us:
        for v in vs:
            gp_pnt=surf_adaptator.Value(u,v)
            vector_pts[u.index, v.index] = [Vector((gp_pnt.X()/1000, gp_pnt.Y()/1000, gp_pnt.Z()/1000))]
    
    # create object
    mesh = bpy.data.meshes.new("Patch CP")
    vert, edges, faces = create_grid(vector_pts)
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    context.scene.collection.objects.link(ob)
    return True




def build_SP_from_brep(list_of_shapes, context):
    # single entity case
    if type(list_of_shapes) != 'list' :
        list_of_shapes = [list_of_shapes]
        print("single shape")

    for shape in list_of_shapes:
        recursive_SP_from_brep_shape(shape, context)

    return True


def recursive_SP_from_brep_shape(shape, context, visited_shapes=None):
    if visited_shapes is None:
        visited_shapes = set()



    print(is_compound(shape))
    print(is_shell(shape))
    print(is_edge(shape))
    print(is_face(shape))
    # print(type(shape))

    # if is_compound(shape):
    #     exp = TopExp_Explorer(shape, TopAbs_SHAPE)
    #     while exp.More() :
    #         print("recurse")
    #         print(type(exp.Current()))
    #         recursive_SP_from_brep_shape(exp.Current(), context)
    #         exp.Next()
    
    
    if is_shell(shape):
        exp_shell = TopExp_Explorer(shape, TopAbs_SHAPE)
        while exp_shell.More :
            
            # Add the current shape to the set of visited shapes
            shape_hash = hash(shape.__hash__())
            if shape_hash in visited_shapes:
                break
            print(type(exp_shell.Current()))
            visited_shapes.add(shape_hash)

            
            recursive_SP_from_brep_shape(exp_shell.Current(), context, visited_shapes)
            exp_shell.Next()

    elif is_edge(shape):
        build_SP_curve(shape, context)

    elif is_face(shape):
        # if geom=='bezier':
        build_SP_patch(shape, context)
        # elif :
        #     build_SP_flatpatch(shape, context)
        
    return True
        



def import_step(filepath, context):
    shape_list = read_step_file(filepath, False)
    return build_SP_from_brep(shape_list, context)

class SP_OT_import_step_file(bpy.types.Operator):
    bl_idname = "sp.import_step_file"
    bl_label = "Import STEP File"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import_step(abspath("C:/Users/romai/Documents/Projets/Bezier-quest/FreeCad Test Surface.step"), context)
        return {'FINISHED'}