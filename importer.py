import bpy
import numpy as np
from OCC.Extend.TopologyUtils import is_face, is_edge, is_compound
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_COMPOUND, TopAbs_EDGE 
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from mathutils import Vector
from os.path import abspath

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



def build_SP_from_brep(list_of_shapes, context):
    if type(list_of_shapes) != 'list' :
        list_of_shapes = [list_of_shapes]
    comp_mask = [is_compound(s) for s in list_of_shapes]
    ed_mask = [is_edge(s) for s in list_of_shapes]
    fa_mask = [is_face(s) for s in list_of_shapes]

    for i,s in enumerate(list_of_shapes):
        if comp_mask[i]:
            exp = TopExp_Explorer(s, TopAbs_EDGE)
            while True :
                if is_edge(exp.Current()):
                    build_SP_curve(exp.Current(), context)
                if not exp.More():
                    break
                exp.Next()
            #...
            
        if ed_mask[i]:
            build_SP_curve(s)
        #...

    return True



def import_step(filepath, context):
    shape_list = read_step_file(filepath, False)
    return build_SP_from_brep(shape_list, context)

class SP_OT_import_step_file(bpy.types.Operator):
    bl_idname = "sp.import_step_file"
    bl_label = "Import STEP File"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        import_step(abspath("C:/Users/romai/Documents/Lonely files/CAD, 3D Printing/SP edge for import test.step"), context)
        return {'FINISHED'}