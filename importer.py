import bpy
import numpy as np
from mathutils import Vector
from os.path import abspath, splitext, split
from .utils import *

# from OCP.GeomAbs import GeomAbs_Line, GeomAbs_BSplineCurve, GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCP.BRep import BRep_Builder
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Surface #BRepAdaptor_Curve
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_BSplineCurve, Geom_CylindricalSurface, Geom_Line
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCP.IGESControl import IGESControl_Controller, IGESControl_Reader
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS_Compound, TopoDS_Face, TopoDS_Edge
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorTool

from .utils import list_of_shapes_to_compound










def build_SP_cylinder(brepFace, collection, trims_enabled) :
    # face = BRep_Tool.Surface_s(brepFace)
    # cylinder_surface = Geom_CylindricalSurface.DownCast(face)
    cylinder_surface = BRepAdaptor_Surface(brepFace).Surface().Cylinder()
    gp_cylinder = cylinder_surface.Cylinder()
    
    gpaxis= gp_cylinder.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_cylinder.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    face_adpator = BRepAdaptor_Surface(brepFace)
    

    aPnt1 = face_adpator.Value(face_adpator.FirstUParameter(), face_adpator.FirstVParameter())
    aPnt2 = face_adpator.Value(face_adpator.LastUParameter(), face_adpator.LastVParameter())

    aGeomAxis = Geom_Line(gpaxis)
    p1 = GeomAPI_ProjectPointOnCurve(aPnt1, aGeomAxis).Point(1)
    p2 = GeomAPI_ProjectPointOnCurve(aPnt2, aGeomAxis).Point(1)
    length = p1.Distance(p2)/1000


    location = gp_cylinder.Location()
    loc_vec = Vector((location.X()/1000,location.Y()/1000,location.Z()/1000)) - xaxis_vec*length/2
    radius = cylinder_surface.Radius()/1000


    false_uv_bounds = cylinder_surface.Bounds()
    uv_bounds = (false_uv_bounds[1], false_uv_bounds[0], -length/2, length/2) # -np.pi/2
    min_u, max_u, min_v, max_v = uv_bounds[0], uv_bounds[1], uv_bounds[2], uv_bounds[3]

    print(f"UV Bounds : {(min_u, max_u, min_v, max_v)}")

    raduis_vert = (zaxis_vec*radius)+loc_vec

    CPvert = [loc_vec, xaxis_vec*length + loc_vec, raduis_vert]
    CP_edges = [(0,1)]
    sp_surf = SP_surface(brepFace, collection, trims_enabled, uv_bounds, CPvert, CP_edges, [])
    sp_surf.add_modifier("SP - Cylindrical Meshing", {"Use Trim Contour":trims_enabled, "Scaling Method":1}, pin=True)
    return True




def build_SP_bezier_patch(brepFace, collection, trims_enabled):
    bezier_surface = BRepAdaptor_Surface(brepFace).Surface().Bezier()

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
    sp_surf.add_modifier("SP - Bezier Patch Meshing", {"Use Trim Contour":trims_enabled, "Scaling Method":1}, pin=True)
    return True





def build_SP_NURBS_patch(brepFace, collection, trims_enabled):
    #BRep_Tool.Surface_s(brepFace)
    # bspline_surface = Geom_BSplineSurface.DownCast(face)
    bspline_surface = BRepAdaptor_Surface(brepFace).Surface().BSpline()
    
    u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()
    udeg = bspline_surface.UDegree()
    vdeg = bspline_surface.VDegree()
    uv_bounds = bspline_surface.Bounds()
    u_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.UKnots()))
    v_knots = normalize_array(tcolstd_array1_to_list(bspline_surface.VKnots()))
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
    sp_surf.add_modifier("SP - NURBS Patch Meshing", {"Degree V": udeg, "Degree U": vdeg, "Use Trim Contour":False, "Scaling Method": 1}, pin=True)# TO FIX U AND V INVERTED
    return True






def build_SP_curve(topodsEdge, collection, scale = 1000) :
    sp_edge = SP_Edge(topodsEdge)
    sp_edge.scale(1/scale)
    verts = sp_edge.verts
    edge_degree = sp_edge.degree

    endpoints = [1.0] + [0.0]*(len(verts)-2) + [1.0]
    if edge_degree!=None:
        degree_att=[edge_degree/10]+[0.0]*(len(verts)-1)
    else :
        degree_att=[0.0]*(len(verts))

    edges = [(i,i+1) for i in range(len(verts)-1)]

    # create object
    mesh = bpy.data.meshes.new("Curve CP")
    mesh.from_pydata(verts, edges, [])
    ob = bpy.data.objects.new('STEP curve', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", endpoints)
    add_vertex_group(ob, "Degree", degree_att)

    # add modifier
    collection.objects.link(ob)
    add_sp_modifier(ob, "SP - Curve Meshing", pin=True)

    return True






def build_SP_flat(topodsFace, collection):
    wires_verts, wires_edges, wires_endpoints, degree_att, circle_att = get_face_3D_contours(topodsFace)

    # create object
    mesh = bpy.data.meshes.new("FlatPatch CP")
    mesh.from_pydata(wires_verts, wires_edges, [])
    ob = bpy.data.objects.new('STEP FlatPatch', mesh)

    # Assign vertex groups
    add_vertex_group(ob, "Endpoints", wires_endpoints)
    add_vertex_group(ob, "Degree", degree_att)
    add_vertex_group(ob, "Circle", circle_att)
    
    # add modifier
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
            face = TopoDS.Face_s(shape)
            hierarchy['Face'] = self.add_face(face)
        
        elif shape.ShapeType() == TopAbs_EDGE:
            edge = TopoDS.Edge_s(shape)
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
            face = TopoDS.Face_s(exp.Current())
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



def build_SP_from_brep(shape, collection, enabled_entities, scale = 1000):
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
            build_SP_curve(edge, collection, scale)

    # TODO : Add brep relations (face connections...)
    
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
    build_SP_from_brep(shape, new_collection, enabled_entities)
    # profiler.disable()
    # profiler.print_stats()













###########################
# Step import OCC Extends #
###########################
def read_step_file(filename, as_compound=True, verbosity=True):
    """read the STEP file and returns a compound
    filename: the file path
    verbosity: optional, False by default.
    as_compound: True by default. If there are more than one shape at root,
    gather all shapes into one compound. Otherwise returns a list of shapes.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Error: can't read file.")
    if verbosity:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    transfer_result = step_reader.TransferRoots()
    if not transfer_result:
        raise AssertionError("Transfer failed.")
    _nbs = step_reader.NbShapes()
    if _nbs == 0:
        raise AssertionError("No shape to transfer.")
    if _nbs == 1:  # most cases
        return step_reader.Shape(1)
    if _nbs > 1:
        print("Number of shapes:", _nbs)
        shps = []
        # loop over root shapes
        for k in range(1, _nbs + 1):
            new_shp = step_reader.Shape(k)
            if not new_shp.IsNull():
                shps.append(new_shp)
        if as_compound:
            compound, result = list_of_shapes_to_compound(shps)
            if not result:
                print("Warning: all shapes were not added to the compound")
            return compound
        print("Warning, returns a list of shapes.")
        return shps
    return None



def read_step_file_with_names_colors(filename):
    """Returns list of tuples (topods_shape, label, color)
    Use OCAF.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")
    # the list:
    output_shapes = {}

    # create an handle to a document
    doc = TDocStd_Document("pythonocc-doc-step-import")

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool(doc.Main())
    # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    step_reader = STEPCAFControl_Reader()
    step_reader.SetColorMode(True)
    step_reader.SetLayerMode(True)
    step_reader.SetNameMode(True)
    step_reader.SetMatMode(True)
    step_reader.SetGDTMode(True)

    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        step_reader.Transfer(doc)

    locs = []

    def _get_sub_shapes(lab, loc):
        # global cnt, lvl
        # cnt += 1
        # print("\n[%d] level %d, handling LABEL %s\n" % (cnt, lvl, _get_label_name(lab)))
        # print()
        # print(lab.DumpToString())
        # print()
        # print("Is Assembly    :", shape_tool.IsAssembly(lab))
        # print("Is Free        :", shape_tool.IsFree(lab))
        # print("Is Shape       :", shape_tool.IsShape(lab))
        # print("Is Compound    :", shape_tool.IsCompound(lab))
        # print("Is Component   :", shape_tool.IsComponent(lab))
        # print("Is SimpleShape :", shape_tool.IsSimpleShape(lab))
        # print("Is Reference   :", shape_tool.IsReference(lab))

        # users = TDF_LabelSequence()
        # users_cnt = shape_tool.GetUsers(lab, users)
        # print("Nr Users       :", users_cnt)

        l_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes(lab, l_subss)
        # print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents(lab, l_comps)
        # print("Nb components  :", l_comps.Length())
        # print()
        name = lab.GetLabelName()
        print("Name :", name)

        if shape_tool.IsAssembly(lab):
            l_c = TDF_LabelSequence()
            shape_tool.GetComponents(lab, l_c)
            for i in range(l_c.Length()):
                label = l_c.Value(i + 1)
                if shape_tool.IsReference(label):
                    # print("\n########  reference label :", label)
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(label, label_reference)
                    loc = shape_tool.GetLocation(label)
                    # print("    loc          :", loc)
                    # trans = loc.Transformation()
                    # print("    tran form    :", trans.Form())
                    # rot = trans.GetRotation()
                    # print("    rotation     :", rot)
                    # print("    X            :", rot.X())
                    # print("    Y            :", rot.Y())
                    # print("    Z            :", rot.Z())
                    # print("    W            :", rot.W())
                    # tran = trans.TranslationPart()
                    # print("    translation  :", tran)
                    # print("    X            :", tran.X())
                    # print("    Y            :", tran.Y())
                    # print("    Z            :", tran.Z())

                    locs.append(loc)
                    # print(">>>>")
                    # lvl += 1
                    _get_sub_shapes(label_reference, loc)
                    # lvl -= 1
                    # print("<<<<")
                    locs.pop()

        elif shape_tool.IsSimpleShape(lab):
            # print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape(lab)
            # print("    all ass locs   :", locs)

            loc = TopLoc_Location()
            for l in locs:
                # print("    take loc       :", l)
                loc = loc.Multiplied(l)

            # trans = loc.Transformation()
            # print("    FINAL loc    :")
            # print("    tran form    :", trans.Form())
            # rot = trans.GetRotation()
            # print("    rotation     :", rot)
            # print("    X            :", rot.X())
            # print("    Y            :", rot.Y())
            # print("    Z            :", rot.Z())
            # print("    W            :", rot.W())
            # tran = trans.TranslationPart()
            # print("    translation  :", tran)
            # print("    X            :", tran.X())
            # print("    Y            :", tran.Y())
            # print("    Z            :", tran.Z())
            c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
            color_set = False
            if (
                color_tool.GetInstanceColor(shape, 0, c)
                or color_tool.GetInstanceColor(shape, 1, c)
                or color_tool.GetInstanceColor(shape, 2, c)
            ):
                color_tool.SetInstanceColor(shape, 0, c)
                color_tool.SetInstanceColor(shape, 1, c)
                color_tool.SetInstanceColor(shape, 2, c)
                color_set = True
                n = c.Name(c.Red(), c.Green(), c.Blue())
                print(
                    "    instance color Name & RGB: ",
                    c,
                    n,
                    c.Red(),
                    c.Green(),
                    c.Blue(),
                )

            if not color_set:
                if (
                    XCAFDoc_ColorTool.GetColor(lab, 0, c)
                    or XCAFDoc_ColorTool.GetColor(lab, 1, c)
                    or XCAFDoc_ColorTool.GetColor(lab, 2, c)
                ):
                    color_tool.SetInstanceColor(shape, 0, c)
                    color_tool.SetInstanceColor(shape, 1, c)
                    color_tool.SetInstanceColor(shape, 2, c)

                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    shape color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

            shape_disp = BRepBuilderAPI_Transform(shape, loc.Transformation()).Shape()
            if shape_disp not in output_shapes:
                output_shapes[shape_disp] = [lab.GetLabelName(), c]
            for i in range(l_subss.Length()):
                lab_subs = l_subss.Value(i + 1)
                # print("\n########  simpleshape subshape label :", lab)
                shape_sub = shape_tool.GetShape(lab_subs)

                c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
                color_set = False
                if (
                    color_tool.GetInstanceColor(shape_sub, 0, c)
                    or color_tool.GetInstanceColor(shape_sub, 1, c)
                    or color_tool.GetInstanceColor(shape_sub, 2, c)
                ):
                    color_tool.SetInstanceColor(shape_sub, 0, c)
                    color_tool.SetInstanceColor(shape_sub, 1, c)
                    color_tool.SetInstanceColor(shape_sub, 2, c)
                    color_set = True
                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    instance color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

                if not color_set:
                    if (
                        XCAFDoc_ColorTool.GetColor(lab_subs, 0, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, 1, c)
                        or XCAFDoc_ColorTool.GetColor(lab_subs, 2, c)
                    ):
                        color_tool.SetInstanceColor(shape, 0, c)
                        color_tool.SetInstanceColor(shape, 1, c)
                        color_tool.SetInstanceColor(shape, 2, c)

                        n = c.Name(c.Red(), c.Green(), c.Blue())
                        print(
                            "    shape color Name & RGB: ",
                            c,
                            n,
                            c.Red(),
                            c.Green(),
                            c.Blue(),
                        )
                shape_to_disp = BRepBuilderAPI_Transform(
                    shape_sub, loc.Transformation()
                ).Shape()
                # position the subshape to display
                if shape_to_disp not in output_shapes:
                    output_shapes[shape_to_disp] = [lab_subs.GetLabelName(), c]

    def _get_shapes():
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels)
        # global cnt
        # cnt += 1

        print()
        print("Number of shapes at root :", labels.Length())
        print()
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return output_shapes







###########################
# IGES import OCC Extends #
###########################
def read_iges_file(
    filename, return_as_shapes=False, verbosity=False, visible_only=False
):
    """read the IGES file and returns a compound
    filename: the file path
    return_as_shapes: optional, False by default. If True returns a list of shapes,
                      else returns a single compound
    verbosity: optionl, False by default.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    IGESControl_Controller.Init()

    iges_reader = IGESControl_Reader()
    iges_reader.SetReadVisible(visible_only)
    status = iges_reader.ReadFile(filename)

    if status != IFSelect_RetDone:  # check status
        raise IOError("Cannot read IGES file")

    if verbosity:
        failsonly = False
        iges_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        iges_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    iges_reader.ClearShapes()
    iges_reader.TransferRoots()
    nbr = iges_reader.NbShapes()

    _shapes = []
    for i in range(1, nbr + 1):
        a_shp = iges_reader.Shape(i)
        if not a_shp.IsNull():
            _shapes.append(a_shp)

    # create a compound and store all shapes
    if not return_as_shapes:
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)
        for s in _shapes:
            builder.Add(compound, s)
        return [compound]

    return _shapes