import bpy
import numpy as np
from mathutils import Vector
from os.path import abspath, splitext, split, isfile
from ..utils import *

from OCP.BRepAdaptor import (
    BRepAdaptor_Curve,
    BRepAdaptor_Curve2d,
    BRepAdaptor_Surface,
)
# from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Pnt, gp_Pnt2d
from OCP.TopAbs import (
    TopAbs_FORWARD,
    TopAbs_REVERSED,
)
from OCP.TopoDS import (
    TopoDS,
    TopoDS_Iterator,
    TopoDS_Wire,
    TopoDS_Edge,
    TopoDS_Face,
    # TopoDS_Shape,
    # TopoDS_Compound,
)
import OCP.GeomAbs as GeomAbs
import OCP.TopAbs as TopAbs


##############################
##    Converter classes     ##
##############################

class SP_Curve_no_edge_import:
    def __init__(self, adaptor_curve, scale=None):
        self.verts = None
        self.degree = 0
        self.degree_att = []
        self.type = 0
        self.type_att = []
        self.endpoints_att = []
        self.weight = []
        self.mult = []
        self.knot = []

        curve_type = get_geom_adapt_curve_type(adaptor_curve)
        self.isclosed = adaptor_curve.IsClosed()

        match curve_type:
            case GeomAbs.GeomAbs_Line:
                self.line(adaptor_curve)
            case GeomAbs.GeomAbs_BezierCurve:
                self.bezier(adaptor_curve)
            case GeomAbs.GeomAbs_BSplineCurve:
                self.bspline(adaptor_curve)
            case GeomAbs.GeomAbs_Circle:
                self.circle(adaptor_curve)
            case GeomAbs.GeomAbs_Ellipse:
                self.ellipse(adaptor_curve)
            case _:
                print(
                    f"Unsupported curve type: {curve_type}. Expect inaccurate results"
                )
                start_point = adaptor_curve.Value(adaptor_curve.FirstParameter())
                end_point = adaptor_curve.Value(adaptor_curve.LastParameter())
                gp_pnt_poles = [start_point, end_point]
                self.type_att = [EDGES_TYPES["line"]] * 2
                if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
                    self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
                else :
                    self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)
                self.degree_att = [0, 0]
                self.endpoints_att = [True] * 2
                self.weight = [0.0, 0.0]
                self.knot = [0.0, 0.0]
                self.mult = [0, 0]

        if scale != None:
            self.scale(scale)

    def scale(self, scale_factor):
        self.verts = [v * scale_factor for v in self.verts]

    def line(self, edge_adaptor):
        start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        gp_pnt_poles = [start_point, end_point]
        self.type = EDGES_TYPES["line"]
        self.type_att = [EDGES_TYPES["line"]] * 2
        if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
            self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
        else :
            self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)
        self.degree_att = [0, 0]
        self.endpoints_att = [True] * 2
        self.weight = [0.0, 0.0]
        self.knot = [0.0, 0.0]
        self.mult = [0, 0]

        # if edge!=None :
        #     start_point = edge_adaptor.Value(edge_adaptor.FirstParameter())
        #     end_point = edge_adaptor.Value(edge_adaptor.LastParameter())
        #     poles = [start_point, end_point]
        # else:
        #     start_point = curve_adaptor.Value(curve_adaptor.FirstParameter())
        #     end_point = curve_adaptor.Value(curve_adaptor.LastParameter())
        #     poles = [start_point, end_point]

    def bezier(self, edge_adaptor):
        # Get geom curve
        bezier = edge_adaptor.Bezier()

        # Trim for poles matching param range
        first = edge_adaptor.FirstParameter()
        last = edge_adaptor.LastParameter()
        bezier.Segment(first, last)
        
        # Get poles
        p_count = bezier.NbPoles()
        gp_pnt_poles = [bezier.Pole(i + 1) for i in range(p_count)]

        # Set attributes
        self.type = EDGES_TYPES["bezier"]
        self.type_att = [EDGES_TYPES["bezier"]] * p_count
        if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
            self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
        else :
            self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)
        self.degree_att = [0] * p_count
        self.endpoints_att = [True] + [False] * (p_count - 2) + [True]
        self.weight = [bezier.Weight(i + 1) for i in range(p_count)]
        self.knot = [0.0] * p_count
        self.mult = [0] * p_count

    def bspline(self, edge_adaptor):
        # Get geom curve
        bspline = edge_adaptor.BSpline()

        # Trim for poles matching param range
        first = edge_adaptor.FirstParameter()
        last = edge_adaptor.LastParameter()
        bspline.Segment(first, last)
        
        # Get poles
        p_count = bspline.NbPoles()
        gp_pnt_poles = [bspline.Pole(i + 1) for i in range(p_count)]
        
        # Set attributes
        self.degree = bspline.Degree()
        if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
            self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
        else :
            self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)
        self.type = EDGES_TYPES["nurbs"]
        self.type_att = [EDGES_TYPES["nurbs"]] * p_count
        self.degree_att = [bspline.Degree()] + [0] * (p_count - 2) + [bspline.Degree()]
        if edge_adaptor.BSpline().Multiplicity(1) == 1:  # unclamped periodic
            self.endpoints_att = [False] * p_count
        else:
            self.endpoints_att = [True] + [False] * (p_count - 2) + [True]
        self.weight = [bspline.Weight(i + 1) for i in range(p_count)]

        knot = normalize_array(haarray1_of_real_to_list(bspline.Knots()))
        mult = haarray1_of_int_to_list(bspline.Multiplicities())
        self.knot = knot + [0.0] * (p_count - len(knot))
        self.mult = mult + [0] * (p_count - len(mult))

    def circle(self, edge_adaptor):
        min_t = edge_adaptor.FirstParameter()
        max_t = edge_adaptor.LastParameter()

        start_point = edge_adaptor.Value(min_t)
        end_point = edge_adaptor.Value(max_t)
        range_t = max_t - min_t

        # full circle
        if start_point == end_point or isclose(range_t, math.pi * 2):
            end_point = edge_adaptor.Value(min_t + math.pi / 2)
            center = edge_adaptor.Circle().Location()
            gp_pnt_poles = [
                end_point,
                center,
                start_point,
            ]  # Invert because of parametrisation
            self.type = EDGES_TYPES["circle"]
            self.type_att = [EDGES_TYPES["circle"]] * 3

        # arc
        else:
            mid_t = (max_t + min_t) / 2
            mid_point = edge_adaptor.Value(mid_t)
            gp_pnt_poles = [start_point, mid_point, end_point]
            self.type = EDGES_TYPES["circle_arc"]
            self.type_att = [EDGES_TYPES["circle_arc"]] * 3

        self.degree_att = [0] * 3
        self.endpoints_att = [True, False, True]
        self.weight = [0.0] * 3
        self.knot = [0.0] * 3
        self.mult = [0] * 3
        if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
            self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
        else :
            self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)

    def ellipse(self, edge_adaptor):
        # arc from 3 pts
        min_t = edge_adaptor.FirstParameter()
        max_t = edge_adaptor.LastParameter()

        start_point = edge_adaptor.Value(min_t)
        end_point = edge_adaptor.Value(max_t)
        range_t = max_t - min_t

        axis_point_1 = edge_adaptor.Value(0)
        axis_point_2 = edge_adaptor.Value(math.pi / 2)
        center = edge_adaptor.Ellipse().Location()

        # full ellipse
        if start_point == end_point or isclose(range_t, math.pi * 2):
            gp_pnt_poles = [axis_point_1, center, axis_point_2]
            self.type = EDGES_TYPES["ellipse"]
            self.type_att = [EDGES_TYPES["ellipse"]] * 3
            self.degree_att = [0] * 3
            self.endpoints_att = [True, False, True]
            self.weight = [0.0, 0.0, 0.0]
            self.knot = [0.0, 0.0, 0.0]
            self.mult = [0, 0, 0]
        # arc
        else:
            gp_pnt_poles = [start_point, axis_point_1, center, axis_point_2, end_point]
            self.type = EDGES_TYPES["ellipse_arc"]
            self.type_att = [EDGES_TYPES["ellipse_arc"]] * 5
            self.degree_att = [0] * 5
            self.endpoints_att = [True] + [False] * 3 + [True]
            self.weight = [0.0, 0.0, 0.0, 0.0, 0.0]
            self.knot = [0.0, 0.0, 0.0, 0.0, 0.0]
            self.mult = [0, 0, 0, 0, 0]

        if isinstance(gp_pnt_poles[0], gp_Pnt2d ):       
            self.verts = gp_pnt_to_blender_vec_list_2d(gp_pnt_poles)
        else :
            self.verts = gp_pnt_to_blender_vec_list(gp_pnt_poles)

class SP_Edge_import:
    def __init__(self, topods_edge: TopoDS_Edge, topods_face=None, scale=None):
        # Edge adaptor
        # 3D


        if topods_face is None:
            edge_adaptor = BRepAdaptor_Curve(topods_edge)
        # 2D
        else:
            edge_adaptor = BRepAdaptor_Curve2d(topods_edge, topods_face)

        sp_curve_no_edge = SP_Curve_no_edge_import(edge_adaptor, scale)

        self.verts = sp_curve_no_edge.verts
        self.degree = sp_curve_no_edge.degree
        self.degree_att = sp_curve_no_edge.degree_att
        self.type_att = sp_curve_no_edge.type_att
        self.endpoints_att = sp_curve_no_edge.endpoints_att
        self.weight = sp_curve_no_edge.weight
        self.mult = sp_curve_no_edge.mult
        self.knot = sp_curve_no_edge.knot

        # Reverse
        if (
            topods_edge.Orientation() != TopAbs_FORWARD
            and self.type_att[0] != EDGES_TYPES["circle"]
        ):
            self.verts.reverse()
            self.weight.reverse()
            # type, endpoints, degree are symmetric

        self.isclosed = sp_curve_no_edge.isclosed


class SP_Wire_import:
    def __init__(self, topods_wire: TopoDS_Wire, scale=1, topods_face=None):
        self.CP = []  # Vectors, bmesh format
        # Import
        if topods_wire != None:
            # vertex aligned attributes
            self.bmesh_edges = []  # int tuple
            self.endpoints_att = []
            self.degree_att = []
            self.weight_att = []
            self.knot_att = []
            self.mult_att = []
            self.type_att = []

        topods_edges = get_edges_from_wire(topods_wire)
        is_wire_forward = topods_wire.Orientation() == TopAbs_FORWARD

        # iterate Edges
        for e in topods_edges:
            sp_edge = SP_Edge_import(e, topods_face, scale)
            e_vert = sp_edge.verts

            if not is_wire_forward:
                e_vert.reverse()
                # other att are symmetric

            self.CP.extend(e_vert[:-1])
            self.endpoints_att.extend(sp_edge.endpoints_att[:-1])
            self.degree_att.extend(sp_edge.degree_att[:-1])
            self.type_att.extend(sp_edge.type_att[:-1])
            self.weight_att.extend(sp_edge.weight[:-1])
            self.knot_att.extend(sp_edge.knot[:-1])
            self.mult_att.extend(sp_edge.mult[:-1])

        # Add last point for single edge wire
        if (
            len(topods_edges) == 1
        ):  # Skip circle (unclosed control mesh structure for single segment wire)
            # OR closed single wire
            # OR single segment curve
            # if sp_edge.isclosed :
            self.CP.append(e_vert[-1])
            self.endpoints_att.append(sp_edge.endpoints_att[-1])
            self.degree_att.append(sp_edge.degree_att[-1])
            self.type_att.append(sp_edge.type_att[-1])
            self.weight_att.append(sp_edge.weight[-1])
            self.knot_att.append(sp_edge.knot[-1])
            self.mult_att.append(sp_edge.mult[-1])

        # Open control mesh structure
        if (
            self.type_att[-1] == EDGES_TYPES["circle"]
            or self.type_att[-1] == EDGES_TYPES["ellipse"]
            or not topods_wire.Closed()
        ):
            self.bmesh_edges = [(i, i + 1) for i in range(len(self.CP) - 1)]
        # Closed control mesh structure
        else:
            self.bmesh_edges = [
                (i, ((i + 1) % len(self.CP))) for i in range(len(self.CP))
            ]


class SP_Contour_import:
    def __init__(self, topodsface, scale=None):
        self.wires = get_wires_from_face(topodsface)
        (
            self.verts,
            self.edges,
            self.endpoints,
            self.degrees,
            self.type_att,
            self.weight,
            self.knot,
            self.mult,
        ) = ([], [], [], [], [], [], [], [])

        for w in self.wires:
            if scale != None:
                sp_wire = SP_Wire_import(w, scale=scale)
            else:
                sp_wire = SP_Wire_import(w, topods_face=topodsface)

            _, self.edges, _ = join_mesh_entities(
                self.verts, self.edges, [], sp_wire.CP, sp_wire.bmesh_edges, []
            )
            self.verts.extend(sp_wire.CP)
            self.endpoints.extend(sp_wire.endpoints_att)
            self.degrees.extend(sp_wire.degree_att)
            self.type_att.extend(sp_wire.type_att)
            self.weight.extend(sp_wire.weight_att)
            self.knot.extend(sp_wire.knot_att)
            self.mult.extend(sp_wire.mult_att)

    # For square contour following the patch bounds
    def is_trivial(self):
        is_trivial_trim = False
        if len(self.verts) == 4:

            # print(self.verts)

            t1 = self.verts == [
                Vector((0.0, 0.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
            ]
            t2 = self.verts == [
                Vector((0.0, 1.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
            ]
            t3 = self.verts == [
                Vector((1.0, 1.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
            ]
            t4 = self.verts == [
                Vector((1.0, 0.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
            ]

            t5 = self.verts == [
                Vector((1.0, 0.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
            ]
            t6 = self.verts == [
                Vector((1.0, 1.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
            ]
            t7 = self.verts == [
                Vector((0.0, 1.0, 0.0)),
                Vector((0.0, 0.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
            ]
            t8 = self.verts == [
                Vector((0.0, 0.0, 0.0)),
                Vector((1.0, 0.0, 0.0)),
                Vector((1.0, 1.0, 0.0)),
                Vector((0.0, 1.0, 0.0)),
            ]

            t9 = set(self.edges) == {(0, 1), (1, 2), (2, 3), (3, 0)}

            is_trivial_trim = (t1 or t2 or t3 or t4 or t5 or t6 or t7 or t8) and t9

        return is_trivial_trim

    def rebound(self, curr_bounds, new_bounds):
        curr_min_u, curr_max_u, curr_min_v, curr_max_v = (
            curr_bounds[0] if curr_bounds[0] != None else 0.0,
            curr_bounds[1] if curr_bounds[1] != None else 0.0,
            curr_bounds[2] if curr_bounds[2] != None else 0.0,
            curr_bounds[3] if curr_bounds[3] != None else 0.0,
        )

        new_min_u, new_max_u, new_min_v, new_max_v = (
            new_bounds[0] if new_bounds[0] != None else 0.0,
            new_bounds[1] if new_bounds[1] != None else 0.0,
            new_bounds[2] if new_bounds[2] != None else 0.0,
            new_bounds[3] if new_bounds[3] != None else 0.0,
        )

        curr_range_u, curr_range_v = curr_max_u - curr_min_u, curr_max_v - curr_min_v
        new_range_u, new_range_v = new_max_u - new_min_u, new_max_v - new_min_v

        for i, v in enumerate(self.verts):
            if curr_range_u != 0.0:
                v.x = ((v.x - curr_min_u) / curr_range_u) * new_range_u + new_min_u
            if curr_range_v != 0.0:
                v.y = ((v.y - curr_min_v) / curr_range_v) * new_range_v + new_min_v

    def switch_u_and_v(self):
        self.verts = [Vector((v.y, v.x, v.z)) for v in self.verts]


def generic_import_surface(
    face: TopoDS_Face,
    doc,
    collection,
    trims_enabled: bool,
    CPvert,
    CPedges,
    CPfaces,
    modifier,
    attrs={},
    ob_name="STEP Patch",
    scale=0.001,
    curr_uv_bounds=None,
    new_uv_bounds=(0.0, 1.0, 0.0, 1.0),
    weight=None,
):
    if weight == None:
        weight = [1.0] * len(CPvert)

    transform = get_shape_transform(face, scale)

    if trims_enabled:
        contour = SP_Contour_import(face)
        if curr_uv_bounds != None:
            contour.rebound(curr_uv_bounds, new_uv_bounds)

        contour.switch_u_and_v()
        istrivial = contour.is_trivial()

        if istrivial:
            del contour

    if trims_enabled and not istrivial:
        mesh_data = join_mesh_entities(
            CPvert, CPedges, CPfaces, contour.verts, contour.edges, []
        )
        attrs = attrs | {
            "Weight": weight + contour.weight,
            "Knot": [0.0] * len(CPvert) + contour.knot,
            "Multiplicity": [0] * len(CPvert) + contour.mult,
            "Trim Contour": [False] * len(CPvert) + [True] * len(contour.verts),
            "Endpoints": [False] * len(CPvert) + contour.endpoints,
            "Degree": [0] * len(CPvert) + contour.degrees,
            "Type": [0] * len(CPvert) + contour.type_att,
        }
    else:
        mesh_data = (CPvert, CPedges, CPfaces)
        attrs = attrs | {"Weight": weight}

    name, color = get_shape_name_and_color(face, doc)
    if name == None:
        name = ob_name

    if len(color) == 3:
        color = list(color) + [1.0]

    object_data = {
        "mesh_data": mesh_data,
        "name": name,
        "collection": collection,
        "scale": scale,
        "color": color,
        "attrs": attrs,
        "modifier": modifier,
        "transform": transform,
    }

    return object_data


def build_SP_cylinder(
    topods_face: TopoDS_Face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_cylinder = face_adpator.Surface().Cylinder()

    gpaxis = gp_cylinder.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_cylinder.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_cylinder.Location()
    loc_vec = Vector((location.X() * scale, location.Y() * scale, location.Z() * scale))
    radius = gp_cylinder.Radius() * scale

    raduis_vert = Vector((zaxis_vec * radius) + loc_vec)

    CPvert = [loc_vec, xaxis_vec * scale + loc_vec, raduis_vert]
    CP_edges = [(0, 1)]

    modifier = (
        "SP - Cylindrical Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution * 2,
        },
        True,
    )

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CP_edges,
        [],
        modifier,
        ob_name="STEP Cylinder",
    )

    return object_data


def build_SP_torus(
    topods_face: TopoDS_Face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_torus = face_adpator.Surface().Torus()

    gpaxis = gp_torus.Axis()
    xaxis = gpaxis.Direction()
    yaxis = gp_torus.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_torus.Location()
    origin_vec = Vector(
        (location.X() * scale, location.Y() * scale, location.Z() * scale)
    )
    major_radius = gp_torus.MajorRadius() * scale

    minor_radius = gp_torus.MinorRadius() * scale
    raduis_vert = Vector((zaxis_vec * major_radius) + origin_vec)

    CPvert = [origin_vec, raduis_vert, -xaxis_vec * minor_radius + raduis_vert]
    CP_edges = [(0, 1), (1, 2)]

    modifier = (
        "SP - Toroidal Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution * 2,
        },
        True,
    )

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CP_edges,
        [],
        modifier,
        ob_name="STEP Torus",
    )

    return object_data


def build_SP_sphere(
    topods_face: TopoDS_Face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_sphere = face_adpator.Surface().Sphere()

    gpaxis = gp_sphere.XAxis()
    xaxis = gpaxis.Direction()
    yaxis = gp_sphere.YAxis().Direction()
    xaxis_vec = Vector([xaxis.X(), xaxis.Y(), xaxis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    zaxis_vec = Vector(np.cross(yaxis_vec, xaxis_vec))

    location = gp_sphere.Location()
    loc_vec = Vector((location.X() * scale, location.Y() * scale, location.Z() * scale))
    radius = gp_sphere.Radius() * scale

    CPvert = [
        loc_vec - zaxis_vec * radius,
        loc_vec + zaxis_vec * radius,
        yaxis_vec * radius + loc_vec,
    ]
    CP_edges = [(0, 1)]

    modifier = (
        "SP - Spherical Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution * 2,
        },
        True,
    )

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CP_edges,
        [],
        modifier,
        ob_name="STEP Sphere",
    )
    return object_data


def build_SP_cone(
    topods_face: TopoDS_Face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    face_adpator = BRepAdaptor_Surface(topods_face)
    gp_cone = face_adpator.Surface().Cone()

    gpaxis = gp_cone.Axis()
    axis = gpaxis.Direction()
    yaxis = gp_cone.YAxis().Direction()
    axis_vec = Vector([axis.X(), axis.Y(), axis.Z()])
    yaxis_vec = Vector([yaxis.X(), yaxis.Y(), yaxis.Z()])
    # zaxis_vec = np.cross(yaxis_vec, xaxis_vec)

    location = gp_cone.Location()
    loc_vec = Vector((location.X() * scale, location.Y() * scale, location.Z() * scale))
    radius = gp_cone.RefRadius()

    CPvert = [
        loc_vec,
        loc_vec + yaxis_vec * radius * scale,
        axis_vec * math.cos(gp_cone.SemiAngle()) * scale
        + loc_vec
        + yaxis_vec * (math.sin(gp_cone.SemiAngle()) + radius) * scale,
        axis_vec * math.cos(gp_cone.SemiAngle()) * scale + loc_vec,
    ]
    CP_edges = [(0, 1), (1, 2), (2, 3)]

    modifier = (
        "SP - Conical Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution * 2,
        },
        True,
    )
    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CP_edges,
        [],
        modifier,
        ob_name="STEP Cone",
    )

    return object_data


def build_SP_bezier_patch(
    topods_face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    bezier_surface = BRepAdaptor_Surface(topods_face).Surface().Bezier()

    u_count, v_count = bezier_surface.NbUPoles(), bezier_surface.NbVPoles()
    uv_bounds = bezier_surface.Bounds()
    vector_pts = np.zeros((u_count, v_count), dtype=Vector)
    weight = np.ones((v_count, u_count), dtype=float)
    for u in range(1, u_count + 1):
        for v in range(1, v_count + 1):
            pole = bezier_surface.Pole(u, v)
            vector_pts[u - 1, v - 1] = Vector((pole.X(), pole.Y(), pole.Z())) * scale

            weight[u, v] = bezier_surface.Weight(u, v)

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)

    modifier = (
        "SP - Bezier Patch Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Resolution U": resolution,
            "Resolution V": resolution,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
        },
        True,
    )

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert.tolist(),
        [],
        CPfaces,
        modifier,
        curr_uv_bounds=uv_bounds,
        weight=weight.flatten().tolist(),
    )
    return object_data


def build_SP_NURBS_patch(
    topods_face, doc, collection, trims_enabled, scale=0.001, resolution=16
):
    # Patch attributes
    bspline_surface = BRepAdaptor_Surface(topods_face).Surface().BSpline()
    u_count, v_count = bspline_surface.NbUPoles(), bspline_surface.NbVPoles()
    udeg = bspline_surface.UDegree()
    vdeg = bspline_surface.VDegree()
    u_closed = bspline_surface.IsUClosed()
    v_closed = bspline_surface.IsVClosed()
    u_periodic = bspline_surface.IsUPeriodic()
    v_periodic = bspline_surface.IsVPeriodic()
    uv_bounds = bspline_surface.Bounds()
    u_knots = normalize_array(haarray1_of_real_to_list(bspline_surface.UKnots()))
    v_knots = normalize_array(haarray1_of_real_to_list(bspline_surface.VKnots()))
    u_mult = haarray1_of_int_to_list(bspline_surface.UMultiplicities())
    v_mult = haarray1_of_int_to_list(bspline_surface.VMultiplicities())

    # Custom knot
    custom_knot = False
    # not custom if sequence a...a,b...b (bezier)
    if any(x not in [min(u_knots), max(u_knots)] for x in u_knots) or any(
        x not in [min(v_knots), max(v_knots)] for x in v_knots
    ):
        custom_knot = True
    # TODO
    # else :
    #    Convert to bezier then
    #    build_SP_BezierPatch(...)

    # Vertex aligned attributes

    # CP Grid
    vector_pts = np.zeros((v_count + v_closed, u_count + u_closed), dtype=Vector)
    weight = np.ones((v_count + v_closed, u_count + u_closed), dtype=float)
    for u in range(u_count):
        for v in range(v_count):
            pole = bspline_surface.Pole(u + 1, v + 1)
            vector_pts[v, u] = Vector((pole.X(), pole.Y(), pole.Z())) * scale

            w = bspline_surface.Weight(u + 1, v + 1)
            weight[v, u] = w

    if u_closed:
        vector_pts[:, u_count] = vector_pts[:, 0]
        weight[:, u_count] = weight[:, 0]
    if v_closed:
        vector_pts[v_count, :] = vector_pts[0, :]
        weight[v_count, :] = weight[0, :]

    # control grid
    CPvert, _, CPfaces = create_grid(vector_pts)

    attrs = {}
    if custom_knot:  # must be attr and not vertex groups to avoid collisions at export
        attrs = {
            "Knot U": u_knots,
            "Knot V": v_knots,
            "Multiplicity U": u_mult,
            "Multiplicity V": v_mult,
        }

    # If 1 mult not 1 or no custom knot -> clamp
    u_clamped = any(m != 1 for m in u_mult) or not custom_knot
    v_clamped = any(m != 1 for m in v_mult) or not custom_knot

    # Meshing
    modifier = (
        "SP - NURBS Patch Meshing",
        {
            "Degree U": udeg,
            "Degree V": vdeg,
            "Resolution U": resolution,
            "Resolution V": resolution,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Use Trim Contour": trims_enabled,
            "Scaling Method": 1,
            "Endpoint U": u_clamped,
            "Endpoint V": v_clamped,
            "Cyclic U": u_periodic,
            "Cyclic V": v_periodic,
        },
        True,
    )

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert.tolist(),
        [],
        CPfaces,
        modifier,
        attrs,
        curr_uv_bounds=uv_bounds,
        weight=weight.flatten().tolist(),
    )
    return object_data


def build_SP_curve(shape, doc, collection, scale=0.001, resolution=16):
    if shape.ShapeType() == TopAbs.TopAbs_WIRE:
        sp_wire = SP_Wire_import(shape, scale=scale)
        verts = sp_wire.CP
        edges = sp_wire.bmesh_edges
        endpoints = sp_wire.endpoints_att
        degree_att = sp_wire.degree_att
        type_att = sp_wire.type_att
        weight_att = sp_wire.weight_att
        knot_att = sp_wire.knot_att
        mult_att = sp_wire.mult_att
    else:
        sp_edge = SP_Edge_import(shape, scale=scale)
        verts = sp_edge.verts
        edge_degree = sp_edge.degree
        weight_att = sp_edge.weight
        type_att = sp_edge.type_att
        knot_att = sp_edge.knot
        mult_att = sp_edge.mult

        endpoints = [True] + [False] * (len(verts) - 2) + [True]
        if edge_degree != None:
            degree_att = [edge_degree] + [0] * (len(verts) - 1)
        else:
            degree_att = [0] * (len(verts))

        edges = [(i, i + 1) for i in range(len(verts) - 1)]

    # create object
    name, color = get_shape_name_and_color(shape, doc)
    if name == None:
        name = "STEP Curve"

    if len(color) == 3:
        color = list(color) + [1.0]

    modifier = ("SP - Curve Meshing", {"Resolution": resolution}, True)

    attrs = {
        "Weight": weight_att,
        "Knot": knot_att,
        "Multiplicity": mult_att,
        "Endpoints": endpoints,
        "Degree": degree_att,
        "Type": type_att,
    }

    object_data = {
        "mesh_data": (verts, edges, []),
        "name": name,
        "collection": collection,
        "scale": scale,
        "color": color,
        "attrs": attrs,
        "modifier": modifier,
        "transform": Matrix(),
    }

    return object_data


def build_SP_flat(topods_face, doc, collection, scale=0.001, resolution=16):
    # Get contour
    contour = SP_Contour_import(topods_face, scale)
    verts = contour.verts
    edges = contour.edges
    endpoints = contour.endpoints
    degree_att = contour.degrees
    type_att = contour.type_att
    weight_att = contour.weight
    knot_att = contour.knot
    mult_att = contour.mult

    name, color = get_shape_name_and_color(topods_face, doc)
    if name == None:
        name = "STEP FlatPatch"

    if len(color) == 3:
        color = list(color) + [1.0]

    modifier = (
        "SP - FlatPatch Meshing",
        {
            "Orient": True,
            "Flip Normal": topods_face.Orientation() != TopAbs_REVERSED,
            "Resolution": resolution * 2,
        },
        True,
    )

    attrs = {
        "Weight": weight_att,
        "Knot": knot_att,
        "Multiplicity": mult_att,
        "Endpoints": endpoints,
        "Degree": degree_att,
        "Type": type_att,
    }

    object_data = {
        "mesh_data": (verts, edges, []),
        "name": name,
        "collection": collection,
        "scale": scale,
        "color": color,
        "attrs": attrs,
        "modifier": modifier,
        "transform": Matrix(),
    }

    return object_data


def build_SP_extrusion(topods_face, doc, collection, trims_enabled, scale, resolution):
    adapt_surf = BRepAdaptor_Surface(topods_face).Surface()
    adapt_curve = adapt_surf.BasisCurve()
    geom_surf = adapt_surf.Surface()

    curve_no_edge = SP_Curve_no_edge_import(adapt_curve, scale)

    gpdir = geom_surf.Direction()
    CPvert = curve_no_edge.verts
    CPvert.insert(0, CPvert[0] + (Vector((gpdir.X(), gpdir.Y(), gpdir.Z())) * scale))
    CPedges = [(i, i + 1) for i in range(len(CPvert) - 1)]

    modifier = (
        "SP - Surface of Extrusion Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() != TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution,
        },
        True,
    )

    # needed rebound
    curve_type = get_geom_adapt_curve_type(adapt_curve)
    min_u, max_u = curve_range_from_type(curve_type)

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CPedges,
        [],
        modifier,
        ob_name="STEP Extrusion",
        curr_uv_bounds=(
            adapt_curve.FirstParameter(),
            adapt_curve.LastParameter(),
            None,
            None,
        ),
        new_uv_bounds=(min_u, max_u, None, None),
    )

    # Add curve attributes
        # Ideally should be an input of generic_import_surface which merges it
    curve_p_count = len(curve_no_edge.verts)
    object_data["attrs"]["Degree"][1] = curve_no_edge.degree
    object_data["attrs"]["Type"][1] = curve_no_edge.type
    object_data["attrs"]["Knot"][1 : 1 + curve_p_count] = curve_no_edge.knot
    object_data["attrs"]["Multiplicity"][1 : 1 + curve_p_count] = curve_no_edge.mult

    # Cyclic todo (both cyclic CP and cyclic eval)

    return object_data


def build_SP_revolution(topods_face, doc, collection, trims_enabled, scale, resolution):
    adapt_surf = BRepAdaptor_Surface(topods_face).Surface()
    adapt_curve = adapt_surf.BasisCurve()
    geom_surf = adapt_surf.Surface()

    curve_no_edge = SP_Curve_no_edge_import(adapt_curve, scale)

    gpdir = geom_surf.Direction()
    gploc = geom_surf.Location()
    CPvert = curve_no_edge.verts
    p1 = Vector((gploc.X(), gploc.Y(), gploc.Z())) * scale
    p2 = (
        p1 + Vector((gpdir.X(), gpdir.Y(), gpdir.Z())) * scale
    )  # ideally max of CPvert projected instead
    CPvert = [p1, p2] + CPvert
    CPedges = [(0, 1)] + [(i, i + 1) for i in range(2, len(CPvert) - 1)]

    modifier = (
        "SP - Surface of Revolution Meshing",
        {
            "Use Trim Contour": trims_enabled,
            "Flip Normals": topods_face.Orientation() == TopAbs_REVERSED,
            "Scaling Method": 1,
            "Resolution U": resolution,
            "Resolution V": resolution,
        },
        True,
    )

    # needed rebound
    curve_type = get_geom_adapt_curve_type(adapt_curve)
    min_u, max_u = curve_range_from_type(curve_type)

    object_data = generic_import_surface(
        topods_face,
        doc,
        collection,
        trims_enabled,
        CPvert,
        CPedges,
        [],
        modifier,
        ob_name="STEP Revolution",
        curr_uv_bounds=(
            None,
            None,
            adapt_curve.FirstParameter(),
            adapt_curve.LastParameter(),
        ),
        new_uv_bounds=(None, None, min_u, max_u),
    )

    # Add curve attributes
        # Ideally should be an input of generic_import_surface which merges it
    curve_p_count = len(curve_no_edge.verts)
    object_data["attrs"]["Degree"][2] = curve_no_edge.degree
    object_data["attrs"]["Type"][2] = curve_no_edge.type
    object_data["attrs"]["Knot"][2 : 2 + curve_p_count] = curve_no_edge.knot
    object_data["attrs"]["Multiplicity"][2 : 2 + curve_p_count] = curve_no_edge.mult

    # Cyclic todo (both cyclic CP and cyclic eval)

    return object_data


class ShapeHierarchy:
    def __init__(self, shape, container_name):
        self.faces = []  # tuples (face, collection)
        self.edges = []  # tuples (edges, collection)
        self.hierarchy = {}
        container_collection = self.create_collection(container_name)
        self.hierarchy[container_collection] = []
        iterator = TopoDS_Iterator(shape)
        while iterator.More():
            self.hierarchy[container_collection].append(
                self.create_shape_hierarchy(iterator.Value(), container_collection)
            )
            iterator.Next()

    def create_collection(self, name, parent=None):
        new_collection = bpy.data.collections.new(name)

        # If no parent, link to scene collection
        if parent is None:
            bpy.context.scene.collection.children.link(new_collection)
        else:
            parent.children.link(new_collection)

        return new_collection

    def create_shape_hierarchy(self, shape, parent_col):
        hierarchy = {}

        match shape.ShapeType():
            case TopAbs.TopAbs_COMPOUND:
                hierarchy[parent_col] = []
                new_collection = self.create_collection("Compound", parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(
                        self.create_shape_hierarchy(iterator.Value(), new_collection)
                    )
                    iterator.Next()

            case TopAbs.TopAbs_COMPSOLID:
                hierarchy[parent_col] = []
                new_collection = self.create_collection("CompSolid", parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(
                        self.create_shape_hierarchy(iterator.Value(), new_collection)
                    )
                    iterator.Next()

            case TopAbs.TopAbs_SOLID:
                hierarchy[parent_col] = []
                new_collection = self.create_collection("Solid", parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(
                        self.create_shape_hierarchy(iterator.Value(), new_collection)
                    )
                    iterator.Next()

            case TopAbs.TopAbs_SHELL:
                hierarchy[parent_col] = []
                new_collection = self.create_collection("Shell", parent_col)
                iterator = TopoDS_Iterator(shape)
                while iterator.More():
                    hierarchy[parent_col].append(
                        self.create_shape_hierarchy(iterator.Value(), new_collection)
                    )
                    iterator.Next()

            case TopAbs.TopAbs_FACE:  # must be before wire and edge
                face = TopoDS.Face_s(shape)
                hierarchy["Face"] = face
                self.faces.append((face, parent_col))

            case TopAbs.TopAbs_WIRE:  # must be before edge
                wire = TopoDS.Wire_s(shape)
                hierarchy["Wire"] = wire
                self.edges.append((wire, parent_col))

            case TopAbs.TopAbs_EDGE:
                edge = TopoDS.Edge_s(shape)
                hierarchy["Edge"] = edge
                self.edges.append((edge, parent_col))

        return hierarchy


def import_face_nodegroups(shape_hierarchy):
    to_import_ng_names = []
    face_encountered = set()

    for face, _ in shape_hierarchy.faces:
        adapt_surf = BRepAdaptor_Surface(face)
        ft = adapt_surf.GetType()
        if ft not in face_encountered:
            face_encountered.add(ft)
            match ft:
                case GeomAbs.GeomAbs_Plane:
                    to_import_ng_names.append("SP - FlatPatch Meshing")
                case GeomAbs.GeomAbs_Cylinder:
                    to_import_ng_names.append("SP - Cylindrical Meshing")
                case GeomAbs.GeomAbs_Cone:
                    to_import_ng_names.append("SP - Conical Meshing")
                case GeomAbs.GeomAbs_Sphere:
                    to_import_ng_names.append("SP - Spherical Meshing")
                case GeomAbs.GeomAbs_Torus:
                    to_import_ng_names.append("SP - Toroidal Meshing")
                case GeomAbs.GeomAbs_BezierSurface:
                    to_import_ng_names.append("SP - Bezier Patch Meshing")
                case GeomAbs.GeomAbs_BSplineSurface:
                    to_import_ng_names.append("SP - NURBS Patch Meshing")
                case GeomAbs.GeomAbs_SurfaceOfRevolution:
                    to_import_ng_names.append("SP - Surface of Revolution Meshing")
                case GeomAbs.GeomAbs_SurfaceOfExtrusion:
                    to_import_ng_names.append("SP - Surface of Extrusion Meshing")

    append_multiple_node_groups(to_import_ng_names)


def process_object_data_of_shape(
    topods_shape, doc, collection, trims_enabled, scale, resolution: int, iscurve: bool
):
    if iscurve:
        return build_SP_curve(topods_shape, doc, collection, scale, resolution)

    ft = get_face_sp_type(topods_shape)
    match ft:
        case SP_obj_type.PLANE:
            object_data = build_SP_flat(
                topods_shape, doc, collection, scale, resolution
            )
        case SP_obj_type.CYLINDER:
            object_data = build_SP_cylinder(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.CONE:
            object_data = build_SP_cone(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.SPHERE:
            object_data = build_SP_sphere(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.TORUS:
            object_data = build_SP_torus(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.BEZIER_SURFACE:
            object_data = build_SP_bezier_patch(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.BSPLINE_SURFACE:
            object_data = build_SP_NURBS_patch(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.SURFACE_OF_REVOLUTION:
            object_data = build_SP_revolution(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case SP_obj_type.SURFACE_OF_EXTRUSION:
            object_data = build_SP_extrusion(
                topods_shape, doc, collection, trims_enabled, scale, resolution
            )
        case _:
            print(f"Unsupported Face Type : {ft}")
            return {}
    return object_data


def create_blender_object(object_data):
    if object_data == {}:
        return False

    mesh = bpy.data.meshes.new(object_data["name"])
    mesh.from_pydata(*object_data["mesh_data"], False)
    ob = bpy.data.objects.new(object_data["name"], mesh)
    ob.matrix_world = object_data["transform"]
    ob.color = object_data["color"]

    for name, att in object_data["attrs"].items():
        match att[0]:
            case _ if isinstance(att[0], bool):
                add_bool_attribute(ob, name, att)
            case _ if isinstance(att[0], int):
                add_int_attribute(ob, name, att)
            case _ if isinstance(att[0], float):
                add_float_attribute(ob, name, att)
            case _:
                raise Exception("Attribute type issue")

    name, param, pin = object_data["modifier"]
    add_sp_modifier(ob, name, param, pin)

    object_data["collection"].objects.link(ob)
    return True
