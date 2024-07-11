import bpy
import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve
from OCC.Core.GeomAbs import GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_Plane, GeomAbs_Torus, GeomAbs_Sphere, GeomAbs_Cone, GeomAbs_Cylinder
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve, GeomAdaptor_Surface
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Iterator
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import is_face, is_edge, is_compound, is_shell
from mathutils import Vector
from os.path import abspath, splitext, split
from utils import *




def build_SP_curve(brepEdge, collection, context) :
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
    
    
    status =""
    # edge, _, _ = BRep_Tool.Curve(brepEdge)
    # print(type(edge))

    # if isinstance(edge, Geom_BezierCurve):
    #     bezier_curve = Geom_BezierCurve.DownCast(edge)
    #     count = bezier_curve.NbPoles()
        
    #     vector_pts = np.zeros(count, dtype=Vector)
    #     for u in range(1, count + 1):
    #         pole = bezier_curve.Pole(u)
    #         vector_pts[u-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

    # elif isinstance(edge, Geom_BSplineCurve):
    #     bspline_curve = Geom_BSplineCurve.DownCast(edge)
    #     count = bspline_curve.NbPoles()

    #     knots = [bspline_curve.Knot(i+1) for i in range(bspline_curve.NbKnots())]
    #     if any(x not in [0.0, 1.0] for x in knots) :
    #         status = "Unsupported NURBS feature present, imported step will not be exact"

    #     vector_pts = np.zeros(count, dtype=Vector)
    #     for u in range(1, count + 1):
    #         pole = bspline_curve.Pole(u)
    #         vector_pts[u-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

    #         weight = bspline_curve.Weight(u)
    #         if weight!=1.0:
    #             status = "Weighted NURBS present, SP doesn't currently support them"
    # else:
    #     print("error on edge type")
    #     return False

    # create object
    mesh = bpy.data.meshes.new("Curve CP")
    vert = vector_pts
    edges = [(i,i+1) for i in range(len(vector_pts)-1)]
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP curve', mesh)

    # add_modifier(ob, "SP - Curve Meshing")
    collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob

    bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
                                        asset_library_identifier="SurfacePsycho",
                                        relative_asset_identifier="assets.blend\\NodeTree\\SP - Curve Through Points")
    bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
                                        asset_library_identifier="SurfacePsycho",
                                        relative_asset_identifier="assets.blend\\NodeTree\\SP - Curve Meshing")

    if status != "":
        print(status)
    return True




def build_SP_bezier_patch(brepFace, collection, context) :
    status =""
    face = BRep_Tool.Surface(brepFace)


    if face.DynamicType().Name() == "Geom_BezierSurface":
        bezier_surface = Geom_BezierSurface.DownCast(face)
        u_count, v_count = bezier_surface.NbUPoles(), bezier_surface.NbVPoles()
        
        vector_pts = np.zeros((u_count, v_count), dtype=Vector)
        for u in range(1, u_count + 1):
            for v in range(1, v_count + 1):
                pole = bezier_surface.Pole(u, v)
                vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

                weight = bezier_surface.Weight(u, v)
                if weight!=1.0:
                    status = "Weighted Bezier not unsupported"
    else:
        print("error on face type")
        return False

    # create object
    mesh = bpy.data.meshes.new("Patch CP")
    vert, edges, faces = create_grid(vector_pts)
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    
    # set smooth
    mesh = ob.data
    values = [True] * len(mesh.polygons)
    mesh.polygons.foreach_set("use_smooth", values)

    # add_modifier(ob, "SP - Any Order Patch Meshing")
    collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    
    bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
                                        asset_library_identifier="SurfacePsycho",
                                        relative_asset_identifier="assets.blend\\NodeTree\\SP - Any Order Patch Meshing")
    
    if status != "":
        print(status)
    return True





def build_SP_NURBS_patch(brepFace, collection, context):
    status =""
    face = BRep_Tool.Surface(brepFace)

    if face.DynamicType().Name() == "Geom_BSplineSurface":
        bspline_surface = Geom_BSplineSurface.DownCast(face)
        u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()

        custom_knot = False
        u_knots = [bspline_surface.UKnot(i+1) for i in range(bspline_surface.NbUKnots())]
        v_knots = [bspline_surface.VKnot(i+1) for i in range(bspline_surface.NbVKnots())]
        if any(x not in [0.0, 1.0] for x in u_knots) or any(x not in [0.0, 1.0] for x in v_knots):
            custom_knot = True

        custom_weight = False
        vector_pts = np.zeros((u_count, v_count), dtype=Vector)
        for u in range(1, u_count + 1):
            for v in range(1, v_count + 1):
                pole = bspline_surface.Pole(u, v)
                vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

                weight = bspline_surface.Weight(u, v)
                if weight!=1.0:
                    custom_weight = True
    else:
        print("error on face type")
        return False

    # create object
    mesh = bpy.data.meshes.new("Patch CP")
    vert, edges, faces = create_grid(vector_pts)
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    
    # set smooth
    mesh = ob.data
    values = [True] * len(mesh.polygons)
    mesh.polygons.foreach_set("use_smooth", values)

    # add_modifier(ob, "SP - NURBS Patch Meshing")
    collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob

    # TODO
    # if custom_knot:
        # Add vertex groups
        # add modifier
        # assign vertex groups to modifier

    # if custom_weight:
        # Add vertex group
        # add modifier
        # assign vertex group to modifier
    
    bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
                                        asset_library_identifier="SurfacePsycho",
                                        relative_asset_identifier="assets.blend\\NodeTree\\SP - NURBS Patch Meshing")
    
    if status != "":
        print(status)
    return True





def build_SP_flat(brepFace, collection, context):
    vector_pts = []

    explorer = TopExp_Explorer(brepFace, TopAbs_VERTEX)
    visited_vert = set()  

    while explorer.More():
        vertex = explorer.Current()
        vert_hash = hash(vertex.__hash__())
        if vert_hash not in visited_vert:      
            visited_vert.add(vert_hash)
            pnt = BRep_Tool.Pnt(vertex)
            vector_pts.append(Vector((pnt.X()/1000, pnt.Y()/1000, pnt.Z()/1000)))
        explorer.Next()

    # create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    vert = vector_pts
    edges = [(i,(i+1)%len(vector_pts)) for i in range(len(vector_pts))]
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign endpoints
    if "Endpoints" not in ob.vertex_groups:
        ob.vertex_groups.new(name="Endpoints")
    vg = ob.vertex_groups["Endpoints"]

    for v in ob.data.vertices:
        if True : # Mask to implement
            vg.add([v.index], 1.0, 'ADD')
    
    # add_modifier(ob, "SP - Any Order Patch Meshing")
    collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    
    bpy.ops.object.modifier_add_node_group(asset_library_type='CUSTOM',
                                        asset_library_identifier="SurfacePsycho",
                                        relative_asset_identifier="assets.blend\\NodeTree\\SP - FlatPatch Meshing")
    # Enable Orient option
    change_node_socket_value(ob, True, ['Orient'], 'NodeSocketBool', context)

    return True





def recursive_SP_from_brep_shape(shape, collection, context, enabled_entities, visited_shapes=None, level=0):
    if visited_shapes is None:
        visited_shapes = set()

    shape_id = hash(shape.__hash__())
    if shape_id in visited_shapes:
        return
    visited_shapes.add(shape_id)

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
        if enabled_entities["faces"]:
            ft= face_type(shape)
            if ft=="Bezier":
                build_SP_bezier_patch(shape, collection, context)
            elif ft=="NURBS":
                build_SP_NURBS_patch(shape, collection, context)
            elif ft=="Plane":
                build_SP_flat(shape, collection, context)
            else :
                print("Unsupported Face Type")

    elif shape_type == TopAbs_WIRE:
        print(f"{tab}Wire")
    
    elif shape_type == TopAbs_EDGE:
        print(f"{tab}Edge")
        if enabled_entities["curves"]:
            try :
                build_SP_curve(shape, collection, context)
            except Exception:
                pass
    elif shape_type == TopAbs_VERTEX:
        pass# print(f"{tab}Vertex")
    else:
        print(f"{tab}Unknown shape type")

    explorer = TopoDS_Iterator(shape)
    while explorer.More():
        sub_shape = explorer.Value()
        recursive_SP_from_brep_shape(sub_shape, collection, context, enabled_entities, visited_shapes, level + 1)
        explorer.Next()


def build_SP_from_brep(shape, collection, context, enabled_entities):
    #Add SP entities
    recursive_SP_from_brep_shape(shape, collection, context, enabled_entities)

    #TODO : Add brep relations (face connections...)

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

    build_SP_from_brep(shape, new_collection, context, enabled_entities)


def face_type(face):
    surface_adaptor = GeomAdaptor_Surface(BRep_Tool.Surface(face))
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_Plane:
        return "Plane"
    elif surface_type == GeomAbs_Cylinder:
        return "Cylindrical"
    elif surface_type == GeomAbs_Cone:
        return "Conical"
    elif surface_type == GeomAbs_Sphere:
        return "Spherical"
    elif surface_type == GeomAbs_Torus:
        return "Toroidal"
    elif surface_type == GeomAbs_BezierSurface:
        return "Bezier"
    elif surface_type == GeomAbs_BSplineSurface:
        return "NURBS"
    else:
        return "Other"