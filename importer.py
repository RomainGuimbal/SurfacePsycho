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
from .utils import *








def build_SP_bezier_patch(brepFace, collection, trims_enabled) :
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

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)
    
    if trims_enabled :
        # Add trim contour
        wires_verts, wires_edges, wires_endpoints, wire_orders = get_face_uv_contours(brepFace, uv_bounds)
        vert, edges, faces = join_mesh_entities(CPvert.tolist(), [], CPfaces, wires_verts, wires_edges, [])
    else :
        vert, edges, faces = CPvert, [], CPfaces


    # create object
    mesh = bpy.data.meshes.new("Patch CP")
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)

    if trims_enabled :
        # assign vertex groups
        add_vertex_group(ob, "Trim Contour", [0.0]*len(CPvert) + [1.0]*len(wires_verts))
        add_vertex_group(ob, "Endpoints", [0.0]*len(CPvert) + wires_endpoints)
        add_vertex_group(ob, "Order", [0.0]*len(CPvert) + wire_orders)
    
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





def build_SP_NURBS_patch(brepFace, collection, trims_enabled):
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
    CPvert, _, CPfaces = create_grid(vector_pts)
    
    if trims_enabled :
        # Add trim contour
        wires_verts, wires_edges, wires_endpoints, wire_orders = get_face_uv_contours(brepFace, uv_bounds)
        vert, edges, faces = join_mesh_entities(CPvert.tolist(), [], CPfaces, wires_verts, wires_edges, [])
    else :
        vert, edges, faces = CPvert, [], CPfaces

    # Create object and add mesh
    mesh = bpy.data.meshes.new("Patch CP")
    mesh.from_pydata(vert, edges, faces)
    ob = bpy.data.objects.new('STEP Patch', mesh)
    
    if trims_enabled :
        # assign vertex groups
        add_vertex_group(ob, "Trim Contour", [0.0]*len(CPvert) + [1.0]*len(wires_verts))
        add_vertex_group(ob, "Endpoints", [0.0]*len(CPvert) + wires_endpoints)
        add_vertex_group(ob, "Order", [0.0]*len(CPvert) + wire_orders)

    # set smooth
    mesh = ob.data
    values = [True] * len(mesh.polygons)
    mesh.polygons.foreach_set("use_smooth", values)

    # add_modifiers
    collection.objects.link(ob)

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

    return True






def build_SP_curve(brepEdge, collection, context) :
    vector_pts = []
    curve_adaptor = BRepAdaptor_Curve(brepEdge)

    edge_poles, edge_order = get_poles_from_geom_curve(curve_adaptor, brepEdge)
    endpoints=[1.0] + [0.0]*(len(edge_poles)-2) + [1.0]
    if edge_order!=None:
        order_att=[edge_order/10]+[0.0]*(len(edge_poles)-1)
    else :
        order_att=[0.0]*(len(edge_poles))

    # prepare mesh
    for pnt in edge_poles :
        vector_pts.append(Vector((pnt.X()/1000, pnt.Y()/1000, pnt.Z()/1000)))
    vert = vector_pts
    edges = [(i,i+1) for i in range(len(vector_pts)-1)]

    # create object
    mesh = bpy.data.meshes.new("Curve CP")
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP curve', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Order", order_att)

    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Curve Meshing")

    return True






def build_SP_flat(brepFace, collection, context):
    vector_pts, poles, endpoints, order_att = [], [], [], []
    wire = breptools.OuterWire(brepFace)
    explorer = TopExp_Explorer(wire, TopAbs_EDGE)
    
    while explorer.More():
        # Get the current edge
        edge = topods.Edge(explorer.Current())
        curve_adaptor = BRepAdaptor_Curve(edge)
        edge_poles, edge_order = get_poles_from_geom_curve(curve_adaptor, edge)
        
        # Reverse
        if edge.Orientation() != TopAbs_FORWARD:
            edge_poles.reverse()

        poles.extend(edge_poles[:-1])
        endpoints.extend([1.0]+[0.0]*(len(edge_poles)-2))
        if edge_order!=None:
            order_att.extend([edge_order/10]+[0.0]*(len(edge_poles)-2))
        else :
            order_att.extend([0.0]*(len(edge_poles)-1))

        explorer.Next()

    # prepare mesh
    for pnt in poles :
        vector_pts.append(Vector((pnt.X()/1000, pnt.Y()/1000, pnt.Z()/1000)))
    vert = vector_pts
    edges = [(i,(i+1)%len(vector_pts)) for i in range(len(vector_pts))]
    
    # create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    mesh.from_pydata(vert, edges, [])
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Order", order_att)
    
    # add_modifier(ob, "SP - Any Order Patch Meshing")
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - FlatPatch Meshing", {'Orient': True})
    
    return True









class ShapeHierarchy:
    def __init__(self):
        self.faces = {}
        self.edges = {}
        self.hierarchy = {}

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
    
    def get_face_count(self) :
        return len(self.faces)



def build_SP_from_brep(shape, collection, context, enabled_entities):
    # Create the hierarchy
    shape_hierarchy = ShapeHierarchy()
    shape_hierarchy.process_shape(shape)
        
    # progress cursor
    wm = bpy.context.window_manager
    face_count = shape_hierarchy.get_face_count()
    wm.progress_begin(0, face_count)
    progress = 0

    trims_enabled = enabled_entities["trim_contours"]

    #Create SP faces
    if enabled_entities["faces"]:
        for face_id, face in shape_hierarchy.faces.items():

            ft= surface_type(face)
            if ft=="Bezier":
                build_SP_bezier_patch(face, collection, trims_enabled)
            elif ft=="NURBS":
                build_SP_NURBS_patch(face, collection, trims_enabled)
            elif ft=="Plane":
                build_SP_flat(face, collection, context)
            else :
                print("Unsupported Face Type : " + ft)
            progress+=1
            wm.progress_update(progress)

    #Create SP free edges
    if enabled_entities["curves"]:
        for egde_id, edge in shape_hierarchy.edges.items():
            build_SP_curve(edge, collection, context)

    #recursive_SP_from_brep_shape(shape, collection, context, enabled_entities)
    #TODO : Add brep relations (face connections...)
    
    wm.progress_end()
    return True



def surface_type(face):
    surface_adaptor = GeomAdaptor_Surface(BRep_Tool.Surface(face))
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_Plane :
        return "Plane"
    elif surface_type == GeomAbs_Cylinder :
        return "Cylindrical"
    elif surface_type == GeomAbs_Cone :
        return "Conical"
    elif surface_type == GeomAbs_Sphere :
        return "Spherical"
    elif surface_type == GeomAbs_Torus :
        return "Toroidal"
    elif surface_type == GeomAbs_BezierSurface :
        return "Bezier"
    elif surface_type == GeomAbs_BSplineSurface :
        return "NURBS"
    else :
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

