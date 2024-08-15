import bpy
import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import breptools
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve
from OCC.Core.GeomAbs import GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_Plane, GeomAbs_Torus, GeomAbs_Sphere, GeomAbs_Cone, GeomAbs_Cylinder, GeomAbs_Line, GeomAbs_BSplineCurve
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve, GeomAdaptor_Surface
from OCC.Core.GeomConvert import geomconvert_CurveToBSplineCurve
from OCC.Core.TopoDS import topods
from OCC.Core.TopTools import TopTools_IndexedMapOfShape
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FORWARD, TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCC.Core.TopExp import TopExp_Explorer
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
    degree = curve_adaptator.GetType() #wrong but needs refactor anyway

    #retrieve CP
    ts = np.linspace(first, last, degree+1)
    vector_pts = []
    for t in ts :
        gp_pnt=curve_adaptator.Value(t)
        vector_pts+=[Vector((gp_pnt.X()/1000, gp_pnt.Y()/1000, gp_pnt.Z()/1000))]
    
    #poles = get_poles_from_geom_curve(curve_adaptator)
    
    
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

    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Curve Through Points")
    add_sp_modifier(ob, "SP - Curve Meshing")

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
                    status = "Weighted Bezier not supported"
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

    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Bezier Patch Meshing")
    
    if status != "":
        print(status)
    return True





def build_SP_NURBS_patch(brepFace, collection, context):
    status =""
    face = BRep_Tool.Surface(brepFace)

    if face.DynamicType().Name() == "Geom_BSplineSurface":
        bspline_surface = Geom_BSplineSurface.DownCast(face)
        u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()
        udeg = bspline_surface.UDegree()
        vdeg = bspline_surface.VDegree()
        uv_bounds = bspline_surface.Bounds()
        u_knots = normalize_array(bspline_surface.UKnots())
        v_knots = normalize_array(bspline_surface.VKnots())
        u_mult = bspline_surface.UMultiplicities()
        v_mult = bspline_surface.VMultiplicities()
        custom_knot = False
        if any(x not in [0.0, 1.0] for x in u_knots) or any(x not in [0.0, 1.0] for x in v_knots):
            custom_knot = True
            print(u_knots)
            print(v_knots)

        custom_weight = False
        vector_pts = np.zeros((u_count, v_count), dtype=Vector)
        weights = np.zeros((u_count, v_count), dtype=float)
        for u in range(1, u_count + 1):
            for v in range(1, v_count + 1):
                pole = bspline_surface.Pole(u, v)
                vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))
                
                weight = bspline_surface.Weight(u, v)
                weights[u-1, v-1] = weight
                if weight!=1.0 :
                    custom_weight = True
    else:
        print("error on face type")
        return False
    
    # control grid
    # vert, edges, faces = create_grid(vector_pts)
    CPvert, _, CPfaces = create_grid(vector_pts)

    # Add trim contour
    wires_verts, wires_edges, wires_endpoints = get_face_uv_contours(brepFace, uv_bounds)
    vert, edges, faces = join_mesh_entities(CPvert.tolist(), [], CPfaces, wires_verts, wires_edges, [])

    # Create object and add mesh
    mesh = bpy.data.meshes.new("Patch CP")

    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    
    # assign vertex groups
    add_vertex_group(ob, "Trim Contour", [0.0]*len(CPvert) + [1.0]*len(wires_verts))
    add_vertex_group(ob, "Endpoints", [0.0]*len(CPvert) + wires_endpoints)

    # set smooth
    mesh = ob.data
    values = [True] * len(mesh.polygons)
    mesh.polygons.foreach_set("use_smooth", values)

    # add_modifiers
    collection.objects.link(ob)
    # bpy.context.view_layer.objects.active = ob

    if custom_knot:
        add_vertex_group(ob, "Knot U", v_knots)# TO FIX U AND V INVERTED FOR DEBUG
        add_vertex_group(ob, "Knot V", u_knots)# TO FIX U AND V INVERTED FOR DEBUG
        add_vertex_group(ob, "Multiplicity U", np.array(v_mult)/10)# TO FIX U AND V INVERTED FOR DEBUG
        add_vertex_group(ob, "Multiplicity V", np.array(u_mult)/10)# TO FIX U AND V INVERTED FOR DEBUG

    if custom_weight:
        add_vertex_group(ob, "Weight", weights.flatten())
        print("weights are not fully supported yet")
        #add_sp_modifier(ob, "SP - NURBS Weighting")
        #TO NORMALIZE + factor

        # assign vertex group to modifier # change_node_socket_value
    
    # Meshing
    add_sp_modifier(ob, "SP - NURBS Patch Meshing", {"Order V": udeg, "Order U": vdeg, "Fit / UV": True})# TO FIX U AND V INVERTED FOR DEBUG

    if status != "":
        print(status)
    return True





def build_SP_flat(brepFace, collection, context):
    vector_pts = []
    # explorer = TopExp_Explorer(brepFace, TopAbs_VERTEX)
    # visited_vert = set()  

    # while explorer.More():
    #     vertex = explorer.Current()
    #     vert_hash = hash(vertex.__hash__())
    #     if vert_hash not in visited_vert:      
    #         visited_vert.add(vert_hash)
    #         pnt = BRep_Tool.Pnt(vertex)
    #         vector_pts.append(Vector((pnt.X()/1000, pnt.Y()/1000, pnt.Z()/1000)))
    #     explorer.Next()

    wire = breptools.OuterWire(brepFace)
    control_points = []
    endpoints = []
    explorer = TopExp_Explorer(wire, TopAbs_EDGE)
    
    while explorer.More():
        # Get the current edge
        edge = topods.Edge(explorer.Current())
        curve_adaptor = BRepAdaptor_Curve(edge)
        
        edge_control_points = get_poles_from_geom_curve(curve_adaptor)
        
        # Reverse the order if the edge orientation is reversed
        if edge.Orientation() != TopAbs_FORWARD:
            edge_control_points.reverse()
        control_points.extend(edge_control_points[:-1])
        endpoints.extend([1.0]+[0.0]*(len(edge_control_points)-2))
        explorer.Next()

    #prepare mesh
    for pnt in control_points :
        vector_pts.append(Vector((pnt.X()/1000, pnt.Y()/1000, pnt.Z()/1000)))
    vert = vector_pts
    edges = [(i,(i+1)%len(vector_pts)) for i in range(len(vector_pts))]
    
    # create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign endpoints
    add_vertex_group(ob, "Endpoints", endpoints)
    
    # add_modifier(ob, "SP - Any Order Patch Meshing")
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - FlatPatch Meshing", {'Orient': True})
    
    return True




# def recursive_SP_from_brep_shape(shape, collection, context, enabled_entities, visited_shapes=None, level=0, shape_lists=[]):
    
#     #Avoid duplicates
#     if visited_shapes is None:
#         visited_shapes = set()

#     shape_id = hash(shape.__hash__())
#     if shape_id in visited_shapes:
#         return
#     visited_shapes.add(shape_id)

#     # Types
#     tab = "  " * level
#     shape_type = shape.ShapeType()
#     if shape_type == TopAbs_COMPOUND:
#         print(f"{tab}Compound")
#         # MAKE COLLECTION
#     elif shape_type == TopAbs_COMPSOLID:
#         print(f"{tab}CompSolid")
#     elif shape_type == TopAbs_SOLID:
#         print(f"{tab}Solid")
#     elif shape_type == TopAbs_SHELL:
#         print(f"{tab}Shell")
    
#     elif shape_type == TopAbs_FACE:
#         print(f"{tab}Face")
#         if enabled_entities["faces"]:
#             ft= surface_type(shape)
#             if ft=="Bezier":
#                 build_SP_bezier_patch(shape, collection, context)
#             elif ft=="NURBS":
#                 build_SP_NURBS_patch(shape, collection, context)
#             elif ft=="Plane":
#                 build_SP_flat(shape, collection, context)
#             else :
#                 print("Unsupported Face Type")

#     elif shape_type == TopAbs_WIRE:
#         print(f"{tab}Wire")
    
#     elif shape_type == TopAbs_EDGE:
#         print(f"{tab}Edge")
#         if enabled_entities["curves"]:
#             try :
#                 build_SP_curve(shape, collection, context)
#             except Exception:
#                 pass
#     elif shape_type == TopAbs_VERTEX:
#         pass# print(f"{tab}Vertex")
#     else:
#         print(f"{tab}Unknown shape type")

#     explorer = TopoDS_Iterator(shape)
#     while explorer.More():
#         sub_shape = explorer.Value()
#         recursive_SP_from_brep_shape(sub_shape, collection, context, enabled_entities, visited_shapes, level + 1, shape_lists)
#         explorer.Next()






class ShapeHierarchy:
    def __init__(self):
        self.faces = {}
        self.edges = {}
        self.hierarchy = {}

    # def add_face(self, face):
    #     if face not in self.faces :
    #         face_id = f"Face_{id(face)}"
    #         self.faces[face_id] = face
    #         return face_id

    # def add_edge(self, edge):
    #     if edge not in self.edges :
    #         edge_id = f"Edge_{id(edge)}"
    #         self.edges[edge_id] = edge
    #         return edge_id

    def add_face(self, face):
        face_id = hash(face.__hash__())
        if face_id not in self.faces:
            self.faces[face_id] = face
        return f"Face_{face_id}"

    def add_edge(self, edge):
        edge_id = hash(edge.__hash__())
        if edge_id not in self.edges:
            self.edges[edge_id] = edge
        return f"Edge_{edge_id}"

    def create_shape_hierarchy(self, shape):
        hierarchy = {}
        
        if shape.ShapeType() == TopAbs_COMPOUND:
            hierarchy['Compound'] = []
            for subshape_type in [TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_FACE, TopAbs_EDGE]:
                exp = TopExp_Explorer(shape, subshape_type)
                while exp.More():
                    hierarchy['Compound'].append(self.create_shape_hierarchy(exp.Current()))
                    exp.Next()
        
        elif shape.ShapeType() == TopAbs_COMPSOLID:
            hierarchy['CompSolid'] = []
            exp = TopExp_Explorer(shape, TopAbs_SOLID)
            while exp.More():
                hierarchy['CompSolid'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_SOLID:
            hierarchy['Solid'] = []
            exp = TopExp_Explorer(shape, TopAbs_SHELL)
            while exp.More():
                hierarchy['Solid'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_SHELL:
            hierarchy['Shell'] = []
            exp = TopExp_Explorer(shape, TopAbs_FACE)
            while exp.More():
                hierarchy['Shell'].append(self.create_shape_hierarchy(exp.Current()))
                exp.Next()
        
        elif shape.ShapeType() == TopAbs_FACE:
            face = topods.Face(shape)
            hierarchy['Face'] = self.add_face(face)
        
        elif shape.ShapeType() == TopAbs_EDGE:
            edge = topods.Edge(shape)
            hierarchy['Edge'] = self.add_edge(edge)
        
        return hierarchy

    def find_free_edges(self, shape):
        edge_map = TopTools_IndexedMapOfShape()
        face_map = TopTools_IndexedMapOfShape()
        
        exp = TopExp_Explorer(shape, TopAbs_EDGE)
        while exp.More():
            edge_map.Add(exp.Current())
            exp.Next()
        
        exp = TopExp_Explorer(shape, TopAbs_FACE)
        while exp.More():
            face = topods.Face(exp.Current())
            face_exp = TopExp_Explorer(face, TopAbs_EDGE)
            while face_exp.More():
                face_map.Add(face_exp.Current())
                face_exp.Next()
            exp.Next()
        
        free_edges = []
        for i in range(1, edge_map.Size() + 1):
            if not face_map.Contains(edge_map.FindKey(i)):
                free_edges.append(edge_map.FindKey(i))
        
        return free_edges

    def process_shape(self, shape):
        self.hierarchy = self.create_shape_hierarchy(shape)
        free_edges = self.find_free_edges(shape)
        if free_edges:
            self.hierarchy['FreeEdges'] = [self.create_shape_hierarchy(edge) for edge in free_edges]

    def print_hierarchy(self, node=None, level=0):
        if node is None:
            node = self.hierarchy

        indent = "  " * level
        for key, value in node.items():
            if isinstance(value, list):
                print(f"{indent}{key}:")
                for i, item in enumerate(value):
                    print(f"{indent}  {key}_{i+1}:")
                    self.print_hierarchy(item, level + 2)
            else:
                print(f"{indent}{key}: {value}")



def build_SP_from_brep(shape, collection, context, enabled_entities):
    # Create the hierarchy
    shape_hierarchy = ShapeHierarchy()
    shape_hierarchy.process_shape(shape)

    # shape_hierarchy.print_hierarchy()
    
    #Create SP faces
    if enabled_entities["faces"]:
        for face_id, face in shape_hierarchy.faces.items():
            ft= surface_type(face)
            if ft=="Bezier":
                build_SP_bezier_patch(face, collection, context)
            elif ft=="NURBS":
                build_SP_NURBS_patch(face, collection, context)
            elif ft=="Plane":
                build_SP_flat(face, collection, context)
            else :
                print("Unsupported Face Type : " + ft)

    #recursive_SP_from_brep_shape(shape, collection, context, enabled_entities)
    #TODO : Add brep relations (face connections...)

    return True



def surface_type(face):
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
        return str(surface_type)





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


    # import cProfile
    # profiler = cProfile.Profile()
    # profiler.enable()
    build_SP_from_brep(shape, new_collection, context, enabled_entities)
    # profiler.disable()
    # profiler.print_stats()


