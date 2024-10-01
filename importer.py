import bpy
import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import breptools
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve, Geom_CylindricalSurface
from OCC.Core.GeomAbs import GeomAbs_Line, GeomAbs_BSplineCurve, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
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



class SP_surface :
    def __init__(self, brepFace, collection, trims_enabled, uv_bounds, CPvert, CPedges, CPfaces):
        self.trims_enabled = trims_enabled
        self.brepFace = brepFace
        self.uv_bounds = uv_bounds
        self.CPvert = CPvert
        self.CPedges = CPedges
        self.CPfaces = CPfaces
        self.vert, self.edges, self.faces = [],[],[]
        
        if trims_enabled :
            wires_verts, wires_edges, wires_endpoints, wire_orders = get_face_uv_contours(self.brepFace, self.uv_bounds)
            self.vert, self.edges, self.faces = join_mesh_entities(CPvert, CPedges, CPfaces, wires_verts, wires_edges, [])
        else :
            self.vert, self.edges, self.faces = self.CPvert, self.CP_edges, self.CPfaces

        mesh = bpy.data.meshes.new("Patch CP")
        mesh.from_pydata(self.vert, self.edges, self.faces)
        self.ob = bpy.data.objects.new('STEP Patch', mesh)
        
        if trims_enabled :
            print(f"biiiizard : CP : {len(CPvert)} wire: {len(wires_verts)}")
            print(len(self.vert))

            self.assign_vertex_gr("Trim Contour", [0.0]*len(CPvert) + [1.0]*len(wires_verts))
            self.assign_vertex_gr("Endpoints", [0.0]*len(CPvert) + wires_endpoints)
            self.assign_vertex_gr("Order", [0.0]*len(CPvert) + wire_orders)

        self.set_smooth()

        collection.objects.link(self.ob)

    def set_smooth(self):
        mesh = self.ob.data
        values = [True] * len(mesh.polygons)
        mesh.polygons.foreach_set("use_smooth", values)

    def assign_vertex_gr(self, name, values):
        add_vertex_group(self.ob, name, values)
        
    def add_modifier(self, name, settings_dict = {}, pin=False):
        add_sp_modifier(self.ob, name, settings_dict, pin = pin)




def build_SP_cylinder(brepFace, collection, trims_enabled) :
    face = BRep_Tool.Surface(brepFace)
    cylinder_surface = Geom_CylindricalSurface.DownCast(face)
    radius = cylinder_surface.Radius()/1000
    uv_bounds = cylinder_surface.Bounds()

    CPvert = [Vector((0,0,0)), Vector((0,0,1)), Vector((0,radius,.5))]
    CP_edges = [(0,1)]
    sp_surf = SP_surface(brepFace, collection, trims_enabled, uv_bounds, CPvert, CP_edges, [])
    sp_surf.add_modifier("SP - Cylindrical Meshing", pin=True)
    del sp_surf
    return True




def build_SP_bezier_patch(brepFace, collection, trims_enabled) :
    face = BRep_Tool.Surface(brepFace)
    bezier_surface = Geom_BezierSurface.DownCast(face)
    u_count, v_count = bezier_surface.NbUPoles(), bezier_surface.NbVPoles()
    uv_bounds = bezier_surface.Bounds()
    vector_pts = np.zeros((u_count, v_count), dtype=Vector)
    for u in range(1, u_count + 1):
        for v in range(1, v_count + 1):
            pole = bezier_surface.Pole(u, v)
            vector_pts[u-1, v-1] = Vector((pole.X()/1000, pole.Y()/1000, pole.Z()/1000))

            weight = bezier_surface.Weight(u, v)
            if weight!=1.0:
                print("Weighted Bezier not supported")

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)

    sp_surf = SP_surface(brepFace, collection, trims_enabled, uv_bounds, CPvert.tolist(), [], CPfaces)
    sp_surf.add_modifier("SP - Bezier Patch Meshing", pin=True)
    del sp_surf
    return True





def build_SP_NURBS_patch(brepFace, collection, trims_enabled):
    face = BRep_Tool.Surface(brepFace)
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
    
    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)
    
    sp_surf = SP_surface(brepFace, collection, trims_enabled, uv_bounds, CPvert.tolist(), [], CPfaces)
    
    if custom_knot:
        sp_surf.assign_vertex_gr("Knot U", v_knots)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Knot V", u_knots)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Multiplicity U", np.array(v_mult)/10)# TO FIX U AND V INVERTED
        sp_surf.assign_vertex_gr("Multiplicity V", np.array(u_mult)/10)# TO FIX U AND V INVERTED

    if custom_weight:
        sp_surf.assign_vertex_gr("Weight", weights.flatten())
        print("Weights are not fully supported yet")
        #add_sp_modifier(ob, "SP - NURBS Weighting")
        #TO NORMALIZE + factor
        # assign vertex group to modifier # change_node_socket_value
    
    # Meshing
    sp_surf.add_modifier("SP - NURBS Patch Meshing", {"Order V": udeg, "Order U": vdeg, "Fit / UV": True}, pin=True)# TO FIX U AND V INVERTED
    del sp_surf
    return True






def build_SP_curve(brepEdge, collection) :
    vector_pts = []
    
    edge_poles, edge_order = get_poles_from_edge(brepEdge)
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
    add_sp_modifier(ob, "SP - Curve Meshing", pin=True)

    return True






def build_SP_flat(brepFace, collection):
    wires_verts, wires_edges, wires_endpoints, order_att = get_face_3D_contours(brepFace)

    # create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    mesh.from_pydata(wires_verts, wires_edges, [])
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", wires_endpoints)
    add_vertex_group(ob, "Order", order_att)
    
    # add_modifier(ob, "SP - Any Order Patch Meshing")
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - FlatPatch Meshing", {'Orient': True}, pin=True)
    
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

            ft= get_face_type_id(face)
            match ft:
                case 0:
                    build_SP_flat(face, collection)
                case 1:
                    build_SP_cylinder(face, collection, trims_enabled)
                case 5:
                    build_SP_bezier_patch(face, collection, trims_enabled)
                case 6:
                    build_SP_NURBS_patch(face, collection, trims_enabled)
                case _ :
                    print("Unsupported Face Type : " + get_face_type_name(face))
            progress+=1
            wm.progress_update(progress)

    #Create SP free edges
    if enabled_entities["curves"]:
        for egde_id, edge in shape_hierarchy.edges.items():
            build_SP_curve(edge, collection)

    #recursive_SP_from_brep_shape(shape, collection, context, enabled_entities)
    #TODO : Add brep relations (face connections...)
    
    wm.progress_end()
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

    # import cProfile
    # profiler = cProfile.Profile()
    # profiler.enable()
    build_SP_from_brep(shape, new_collection, context, enabled_entities)
    # profiler.disable()
    # profiler.print_stats()

