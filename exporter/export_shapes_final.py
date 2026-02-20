import bpy
import numpy as np
import math
import warnings
from mathutils import Vector
from ..common.enums import SP_obj_type
from ..common.utils import (
    read_attribute_by_name,
    vec_grid_to_step_cartesian,
    float_list_to_tcolstd_H_2d,
    sp_type_of_object,
    split_by_index,
    blender_matrix_to_gp_trsf,
    shape_list_to_compound,
    shells_to_solids,
)
from ..common.compound_utils import (
    convert_compound_to_patches,
)
from OCP.TColgp import TColgp_Array2OfPnt
from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_GTransform,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Sewing,
    BRepBuilderAPI_Transform,
)
from OCP.Geom import (
    Geom_BezierSurface,
    Geom_Plane,
    Geom_ToroidalSurface,
    Geom_ConicalSurface,
    Geom_CylindricalSurface,
    Geom_SphericalSurface,
    Geom_SurfaceOfLinearExtrusion,
    Geom_SurfaceOfRevolution,
    Geom_TrimmedCurve,
)
from OCP.gp import (
    gp_Pnt,
    gp_Dir,
    gp_Pln,
    gp_Trsf,
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_GTrsf,
    gp_Mat,
)
from OCP.ShapeFix import ShapeFix_Face
from OCP.TColgp import TColgp_Array2OfPnt
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS_Compound
from OCP.StepGeom import (
    StepGeom_KnotType,
    StepGeom_BSplineSurfaceForm,
    StepGeom_BSplineSurfaceWithKnotsAndRationalBSplineSurface,
)
from OCP.StepData import StepData_Logical, StepData_Factors
from OCP.StepToGeom import StepToGeom
from OCP.TCollection import TCollection_HAsciiString

from .export_shapes_wire import (
    SP_Wire_export,
    SP_Edge_export,
    SP_Contour_export,
    knot_tcol_from_att,
)


def get_patch_knot_and_mult(
    ob, degree_u, degree_v, isclamped_u, isclamped_v, iscyclic_u, iscyclic_v
):
    # U
    umult_att = read_attribute_by_name(ob, "Multiplicity U")
    try:
        u_length = int(sum(np.asarray(umult_att) > 0))  # uncompatible with mirror
    except KeyError:  # weird
        u_length = int(sum(np.asarray(umult_att) > 0))
    uknots_att = list(read_attribute_by_name(ob, "Knot U", u_length))
    uknot, umult = knot_tcol_from_att(
        uknots_att, umult_att, degree_u, isclamped_u, iscyclic_u
    )

    # V
    vmult_att = read_attribute_by_name(ob, "Multiplicity V")
    try:
        v_length = int(sum(np.asarray(vmult_att) > 0))
    except Exception:
        v_length = int(sum(np.asarray(vmult_att) > 0))
    vknots_att = list(read_attribute_by_name(ob, "Knot V", v_length))
    vknot, vmult = knot_tcol_from_att(
        vknots_att, vmult_att, degree_v, isclamped_v, iscyclic_v
    )

    return uknot, vknot, umult, vmult


##############################
##  Brep from SP entities   ##
##############################


def geom_to_topods_face(geom_surf=None, outer_wire=None, inner_wires=[]):
    # Make face
    if geom_surf != None:
        if outer_wire == None:
            makeface = BRepBuilderAPI_MakeFace(geom_surf, 1e-6)
            return makeface.Face()
        else:
            makeface = BRepBuilderAPI_MakeFace(geom_surf, outer_wire, False)  # ,1e-6)
    else:  # Flat face
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


def bezier_face_to_topods(ob, scale=1000):
    u_count = int(ob.data.attributes["CP_count"].data[0].value)
    v_count = int(ob.data.attributes["CP_count"].data[1].value)
    points = read_attribute_by_name(ob, "CP_any_order_surf", u_count * v_count)
    points *= scale

    controlPoints = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id = u_count * i + j
            controlPoints.SetValue(
                j + 1, i + 1, gp_Pnt(points[id][0], points[id][1], points[id][2])
            )

    geom_surf = Geom_BezierSurface(controlPoints)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    if not contour.has_wire:
        return geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def NURBS_face_to_topods(ob, scale=1000):
    # Get attributes
    u_count, v_count = read_attribute_by_name(ob, "CP_count", 2)
    points = read_attribute_by_name(ob, "CP_NURBS_surf", u_count * v_count)
    points *= scale
    degree_u, degree_v = read_attribute_by_name(ob, "Degrees", 2)

    try:
        isclamped_u, isclamped_v = read_attribute_by_name(ob, "IsClamped", 2)
    except KeyError:
        isclamped_u, isclamped_v = True, True

    try:
        isperiodic_u, isperiodic_v = read_attribute_by_name(ob, "IsPeriodic", 2)
    except KeyError:
        isperiodic_u, isperiodic_v = False, False

    try:
        weigths_att = read_attribute_by_name(ob, "Weights", u_count * v_count)
    except KeyError:
        weigths_att = np.ones(u_count * v_count, dtype=float)

    points = points.reshape(v_count, u_count, 3).transpose(1, 0, 2)
    weigths_att = weigths_att.reshape(v_count, u_count).transpose()

    # Wrap control points
    if isperiodic_u:
        if isclamped_u:
            points = np.append(points, points[0:1, :, :], axis=0)
            weigths_att = np.append(weigths_att, weigths_att[0:1, :], axis=0)
            u_count += 1
        else:
            points = np.append(points, points[0:degree_u, :, :], axis=0)
            weigths_att = np.append(weigths_att, weigths_att[0:degree_u, :], axis=0)
            u_count += degree_u
    if isperiodic_v:
        if isclamped_v:
            points = np.append(points, points[:, 0:1, :], axis=1)
            weigths_att = np.append(weigths_att, weigths_att[:, 0:1], axis=1)
            v_count += 1
        else:
            points = np.append(points, points[:, 0:degree_v, :], axis=1)
            weigths_att = np.append(weigths_att, weigths_att[:, 0:degree_v], axis=1)
            v_count += degree_v

    # Knots and Multiplicities
    uknots, vknots, umult, vmult = get_patch_knot_and_mult(
        ob, degree_u, degree_v, isclamped_u, isclamped_v, isperiodic_u, isperiodic_v
    )

    # Poles grid
    poles = vec_grid_to_step_cartesian(list(points))

    # Weigths
    weigths = float_list_to_tcolstd_H_2d(list(weigths_att))

    # Create STEP B-spline surface
    name = TCollection_HAsciiString("bspline_surface")
    step_surf = StepGeom_BSplineSurfaceWithKnotsAndRationalBSplineSurface()
    step_surf.Init(
        name,
        degree_u,
        degree_v,
        poles,
        StepGeom_BSplineSurfaceForm(10),
        StepData_Logical(isperiodic_u),
        StepData_Logical(isperiodic_v),
        StepData_Logical(False),
        umult,
        vmult,
        uknots,
        vknots,
        StepGeom_KnotType(1),
        weigths,
    )

    geom_surf = StepToGeom.MakeBSplineSurface_s(step_surf, StepData_Factors())
    if geom_surf == None:
        raise ValueError("Failed to create BSpline surface geometry")

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def cone_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_cone", 3)
    semi_angle, radius = read_attribute_by_name(ob, "angle_radius", 2)
    radius *= scale
    origin *= scale

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*origin),
        gp_Dir(*dir1),
        gp_Dir(*dir2),
    )
    geom_surf = Geom_ConicalSurface(axis3, semi_angle, 0.0)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        scale=(1, 2),
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def sphere_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_sphere", 3)
    radius = float(ob.data.attributes["radius"].data[0].value)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*(origin * scale)),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
        gp_Dir(dir2[0], dir2[1], dir2[2]),
    )
    geom_surf = Geom_SphericalSurface(axis3, radius * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def torus_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_torus", 3)
    radius_major, radius_minor = read_attribute_by_name(ob, "radius", 2)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
        gp_Dir(dir2[0], dir2[1], dir2[2]),
    )
    geom_surf = Geom_ToroidalSurface(axis3, radius_major * scale, radius_minor * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def cylinder_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_cylinder", 3)
    radius, length = read_attribute_by_name(ob, "radius_length", 2)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*(origin * scale)),
        gp_Dir(*dir1),
        gp_Dir(*dir2),
    )
    geom_surf = Geom_CylindricalSurface(axis3, radius * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        scale=(1, length * scale),
    )

    # Create topods face
    if not contour.has_wire:
        face = BRepBuilderAPI_MakeFace(
            geom_surf, 0, 2 * math.pi, 0, length * scale, 1e-6
        ).Face()
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def revolution_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1 = read_attribute_by_name(ob, "axis1_revolution", 2)
    p_count = int(read_attribute_by_name(ob, "p_count_revolution", 1)[0])
    segment_CP = read_attribute_by_name(ob, "CP_revolution", p_count)
    segment_CP *= scale
    try:
        weight = read_attribute_by_name(ob, "weight_revolution", p_count)
    except KeyError:
        weight = [1.0] * p_count
    type = int(read_attribute_by_name(ob, "type_revolution", 1)[0])
    degree = int(read_attribute_by_name(ob, "degree_revolution", 1)[0])
    is_clamped, is_periodic = read_attribute_by_name(
        ob, "clamped_periodic_revolution", 2
    )

    # Get knot
    try:
        mult = read_attribute_by_name(ob, "Multiplicity")
        knot_length = int(sum(np.asarray(mult) > 0))
        knot = read_attribute_by_name(ob, "Knot", knot_length)
        mult = mult[:knot_length]
    except KeyError:
        knot = []
        mult = []

    # Create geom
    geom_segment = SP_Edge_export(
        {"CP": segment_CP, "weight": weight},
        {
            "degree": degree,
            "isclamped": [is_clamped],
            "isperiodic": [is_periodic],
            "type": type,
            "knot": knot,
            "mult": mult,
        },
        single_seg=True,
        is2D=False,
    ).geom

    # Create geom
    axis1 = gp_Ax1(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
    )
    geom_surf = Geom_SurfaceOfRevolution(geom_segment, axis1)

    # Get bounds
    v_min = 0.0
    v_max = 1.0
    if isinstance(geom_segment, Geom_TrimmedCurve):
        v_min = geom_segment.FirstParameter()
        v_max = geom_segment.LastParameter()

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        curr_bounds=(None, None, 0.0, 1.0),
        new_bounds=(None, None, v_min, v_max),
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def extrusion_face_to_topods(ob, scale=1000):
    # Get attr
    dir_att = read_attribute_by_name(ob, "dir_extrusion", 1)[0]
    p_count = int(read_attribute_by_name(ob, "p_count_extrusion", 1)[0])
    segment_CP = read_attribute_by_name(ob, "CP_extrusion", p_count)
    segment_CP *= scale
    weight = read_attribute_by_name(ob, "weight_extrusion", p_count)
    type = int(read_attribute_by_name(ob, "type_extrusion", 1)[0])
    degree = int(read_attribute_by_name(ob, "degree_extrusion", 1)[0])
    is_clamped, is_periodic = read_attribute_by_name(
        ob, "clamped_periodic_extrusion", 2
    )

    length = Vector(dir_att).length * scale

    try:
        # Get knot
        mult = read_attribute_by_name(ob, "Multiplicity")
        knot_length = int(sum(np.asarray(mult) > 0))
        knot = read_attribute_by_name(ob, "Knot", knot_length)
        mult = mult[:knot_length]
    except KeyError:
        knot = []
        mult = []

    geom_segment = SP_Edge_export(
        {"CP": segment_CP, "weight": weight},
        {
            "degree": degree,
            "isclamped": [is_clamped],
            "isperiodic": [is_periodic],
            "type": type,
            "knot": knot,
            "mult": mult,
        },
        single_seg=True,
        is2D=False,
    ).geom

    # Create geom
    dir = gp_Dir(*dir_att)
    geom_surf = Geom_SurfaceOfLinearExtrusion(geom_segment, dir)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        curr_bounds=(None, None, 0.0, 1.0),
        new_bounds=(None, None, 0.0, length),
    )

    # Create topods face
    if not contour.has_wire:
        u_min, u_max = geom_segment.FirstParameter(), geom_segment.LastParameter()
        v_min, v_max = 0.0, length  # Extrusion length
        face = BRepBuilderAPI_MakeFace(
            geom_surf, u_min, u_max, v_min, v_max, 1e-6
        ).Face()
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def curve_to_topods(ob, scale=1000):
    # Get point count attr
    segs_p_counts = read_attribute_by_name(ob, "CP_count")

    # get total_p_count and segment_count
    total_p_count, segment_count = 1, 0
    for p in segs_p_counts:
        if p > 1:
            total_p_count += p - 1
            segment_count += 1
        else:
            break
    # crop segs_p_counts
    segs_p_counts = segs_p_counts[:segment_count]

    # is closed
    is_closed = bool(read_attribute_by_name(ob, "closed", 1)[0])

    # One point less if closed
    total_p_count -= is_closed and segment_count > 1

    # is clamped
    is_clamped = bool(read_attribute_by_name(ob, "IsClamped", 1)[0])

    # is periodic
    is_periodic = bool(read_attribute_by_name(ob, "IsPeriodic", 1)[0])

    # Type
    try:
        type_att = read_attribute_by_name(ob, "Type", segment_count)
    except KeyError:
        type_att = [0] * segment_count

    # Degree
    try:
        segs_degrees = read_attribute_by_name(ob, "Degree", segment_count)
    except KeyError:
        segs_degrees = [0] * segment_count

    # Get CP position attr
    points = read_attribute_by_name(ob, "CP_curve", total_p_count)
    points *= scale

    # Weight
    try:
        weight_attr = read_attribute_by_name(ob, "Weight", total_p_count)
    except KeyError:
        weight_attr = [1.0] * total_p_count

    # Knots
    mult = read_attribute_by_name(ob, "Multiplicity")
    knot = read_attribute_by_name(ob, "Knot")
    knot_segment = list(read_attribute_by_name(ob, "knot_segment"))
    knot_per_seg = split_by_index(knot_segment, knot)
    mult_per_seg = split_by_index(knot_segment, mult)

    # Build wire
    wire = SP_Wire_export(
        {"CP": points, "weight": weight_attr},
        {
            "p_count": segs_p_counts,
            "degree": segs_degrees,
            "isperiodic": [is_periodic] * segment_count,
            "isclamped": [is_clamped] * segment_count,
            "type": type_att,
            "knot": knot_per_seg,
            "mult": mult_per_seg,
        },
        is2D=False,
    )
    topods_wire = wire.get_topods_wire()

    return topods_wire


def flat_patch_to_topods(ob, scale=1000):
    # Get point count attr
    # Orient and offset
    loc, rot, _ = ob.matrix_world.decompose()
    try:
        offset = read_attribute_by_name(ob, "planar_offset", 1)[0]
        orient = read_attribute_by_name(ob, "planar_orient", 1)[0]
    except KeyError:
        offset = [0, 0, 0]
        orient = [0, 0, 1]
    loc += rot @ Vector(offset)
    loc *= scale
    pl_normal = rot @ Vector(orient)
    pl_normal_dir = gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z)
    pl = gp_Pln(gp_Pnt(loc.x, loc.y, loc.z), pl_normal_dir)
    geom_pl = Geom_Plane(pl)

    # Build Contour
    contour = SP_Contour_export(
        ob,
        "CP_planar",
        "CP_count",
        "IsClamped",
        "IsPeriodic",
        scale,
        geom_plane=geom_pl,
        is2D=False,
    )

    # Get occ wires
    outer_wire, inner_wires = contour.get_topods_wires()

    face = geom_to_topods_face(None, outer_wire, inner_wires)
    return face


def empty_to_topods(o, scale=1000):
    # Orient and offset
    gp_trsf = blender_matrix_to_gp_trsf(o.matrix_world, scale)
    gp_pln = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)).Transformed(gp_trsf)
    # gp_pnt = TopoDS_Vertex(gp_Pnt(0,0,0).Transformed(gp_trsf)) vertices cannot be exported :c
    topods_plane = geom_to_topods_face(Geom_Plane(gp_pln))
    return topods_plane


def mirror_topods_shape(o, shape, scale=1000):
    shape_list = [shape]

    loc, rot, _ = o.matrix_world.decompose()

    for m in o.modifiers:
        if m.type == "MIRROR" and m.show_viewport:

            # Get mirror offset
            if m.mirror_object == None:
                mirror_offset = loc * scale
            else:
                loc, rot, _ = m.mirror_object.matrix_world.decompose()
                mirror_offset = loc * scale

            # Fill configurations array
            configurations = [False] * 7

            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            configurations[0] = x
            configurations[1] = y
            configurations[2] = z
            configurations[3] = x and y and z
            configurations[4] = y and z
            configurations[5] = x and z
            configurations[6] = x and y

            xscales = [1, 0, 0, 1, 0, 1, 1]
            yscales = [0, 1, 0, 1, 1, 0, 1]
            zscales = [0, 0, 1, 1, 1, 1, 0]
            symtype = [x + y + z for x, y, z in zip(xscales, yscales, zscales)]

            # Loop through configurations
            for i in range(7):  # 7 = 8 mirror configs -1 original config
                if configurations[i]:
                    # Create transforms

                    # planar symmetry
                    if symtype[i] == 1:
                        base = rot @ (Vector([xscales[i], yscales[i], zscales[i]]))
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Ax2(
                                gp_Pnt(
                                    mirror_offset[0], mirror_offset[1], mirror_offset[2]
                                ),
                                gp_Dir(base.x, base.y, base.z),
                            )
                        )
                    # axis symmetry
                    elif symtype[i] == 2:
                        base = rot @ (
                            Vector(
                                [
                                    xscales[i] - 1,
                                    abs(yscales[i] - 1),
                                    abs(zscales[i] - 1),
                                ]
                            )
                        )
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Ax1(
                                gp_Pnt(
                                    mirror_offset[0], mirror_offset[1], mirror_offset[2]
                                ),
                                gp_Dir(base.x, base.y, base.z),
                            )
                        )

                    # centric symmetry
                    else:
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2])
                        )

                    for s in range(len(shape_list)):
                        sh = BRepBuilderAPI_Transform(shape_list[s], atrsf).Shape()
                        shape_list.append(sh)

    return shape_list


# not a true hierarchy. too complex for now
class ShapeHierarchy_export:
    def __init__(self, context, use_selection, scale, sew, sew_tolerance):
        self.context = context
        self.use_selection = use_selection
        self.scale = scale
        self.sew = sew
        self.sew_tolerance = sew_tolerance
        self.depsgraph = context.evaluated_depsgraph_get()

        objs, shapes, empties, instances, compounds = self.create_shape_hierarchy(
            context.scene.collection
        )
        self.shapes = shapes
        self.instances = instances
        self.empties = empties
        self.compounds = compounds

        # objs is used only for instancing
        self.obj_shapes = {}  # {obj: shape}
        for i, o in enumerate(objs):
            self.obj_shapes[o] = shapes[i]

    def create_shape_hierarchy(self, parent):
        objs, shapes, empties, instances, compounds = [], [], [], [], []

        for child in parent.children:
            o, s, e, i, c = self.create_shape_hierarchy(child)
            objs.extend(o)
            shapes.extend(s)
            empties.extend(e)
            instances.extend(i)
            compounds.extend(c)

        for o in parent.objects:
            if ((not self.use_selection) or (o in self.context.selected_objects)) and (
                not o.hide_viewport
            ):
                sp_type = sp_type_of_object(o)
                match sp_type:
                    case None:
                        pass
                    case SP_obj_type.INSTANCE:
                        instances.append(o)
                    case SP_obj_type.EMPTY:
                        empties.append(o)
                        # treat empties later as they should not be sew (and are instances of the same compound)

                    # empty_to_topods(object, context, scale)
                    case SP_obj_type.COMPOUND:
                        new_objects = convert_compound_to_patches(
                            o, self.context, objects_suffix="_export", resolution=1
                        )
                        comp_shapes = []

                        # from line_profiler import LineProfiler
                        # lp = LineProfiler()
                        # lp.add_function(SP_Contour_export.__init__)
                        # lp.enable()

                        for o_new in new_objects:
                            # Temporarily link
                            self.context.view_layer.active_layer_collection.collection.objects.link(
                                o_new
                            )

                        # bpy.context.view_layer.update()
                        depsgraph = self.context.evaluated_depsgraph_get()

                        for o_new in new_objects:
                            type = sp_type_of_object(o_new)

                            sh = blender_object_to_topods_shapes(
                                depsgraph,
                                o_new,
                                type,
                                scale=self.scale,
                                sew=self.sew,
                            )
                            comp_shapes.append(sh)

                            # Unlink
                            bpy.context.collection.objects.unlink(o_new)

                        new_objects.clear()
                        del new_objects[:]
                        shapes.append(shape_list_to_compound(comp_shapes))
                        objs.append(o)

                        # lp.disable()
                        # lp.print_stats()

                    # Standard shape
                    case _:

                        s = blender_object_to_topods_shapes(
                            self.depsgraph,
                            o,
                            sp_type,
                            self.scale,
                            self.sew,
                            self.sew_tolerance,
                        )
                        objs.append(o)
                        shapes.append(s)

        return objs, shapes, empties, instances, compounds


def blender_object_to_topods_shapes(
    depsgraph, object, sp_type, scale=1000, sew=True, sew_tolerance=1e-1
):
    ob = object.evaluated_get(depsgraph)

    match sp_type:
        case SP_obj_type.CONE:
            shape = cone_face_to_topods(ob, scale)

        case SP_obj_type.SPHERE:
            shape = sphere_face_to_topods(ob, scale)

        case SP_obj_type.CYLINDER:
            shape = cylinder_face_to_topods(ob, scale)

        case SP_obj_type.TORUS:
            shape = torus_face_to_topods(ob, scale)

        case SP_obj_type.BEZIER_SURFACE:
            shape = bezier_face_to_topods(ob, scale)

        case SP_obj_type.BSPLINE_SURFACE:
            shape = NURBS_face_to_topods(ob, scale)

        case SP_obj_type.PLANE:
            shape = flat_patch_to_topods(ob, scale)

        case SP_obj_type.CURVE:
            shape = curve_to_topods(ob, scale)

        case SP_obj_type.SURFACE_OF_REVOLUTION:
            shape = revolution_face_to_topods(ob, scale)

        case SP_obj_type.SURFACE_OF_EXTRUSION:
            shape = extrusion_face_to_topods(ob, scale)

        case _:
            raise Exception(f"Invalid shape of type {sp_type}")

    # Mirror
    shape_list_mirrored = mirror_topods_shape(object, shape, scale)

    # Sew
    if sew:
        compound = sew_shapes(shape_list_mirrored, sew_tolerance)
    else:
        compound = shape_list_to_compound(shape_list_mirrored)

    return compound


def blender_instances_to_topods_instances(
    context, hierarchy, scale=1000, sew_tolerance=1e-1
):
    sewed_shapes_list = []
    depsgraph = context.evaluated_depsgraph_get()

    for ins in hierarchy.instances:
        if ins.scale.x < 0 or ins.scale.y < 0 or ins.scale.z < 0:
            warnings.warn("Negative instance scale not supported")

        swd = blender_instance_to_topods_instance(
            ins, depsgraph, hierarchy, scale, sew_tolerance
        )
        sewed_shapes_list.append(swd)

    return sewed_shapes_list


def blender_instance_to_topods_instance(
    ins, depsgraph, hierarchy, scale=1000, sew=True, sew_tolerance=1e-1
):
    if ins.scale != Vector((1.0, 1.0, 1.0)):
        print(f"Scale not 1, instance is realized (Scale = {ins.scale})")

    to_sew_shape_list = []
    ins_obj = list(ins.instance_collection.objects)

    # # create compound
    # builder = BRep_Builder()
    # comp = TopoDS_Compound()
    # builder.MakeCompound(comp)
    # is_nested = False

    # add obj of child collections (doesn't support nested instances)
    for col in ins.instance_collection.children_recursive:
        for o in col.objects:
            ins_obj.append(o)

    for o in ins_obj:
        sp_type = sp_type_of_object(o)
        if sp_type not in (None, SP_obj_type.EMPTY, SP_obj_type.INSTANCE):
            if o in hierarchy.obj_shapes.keys():
                shape = hierarchy.obj_shapes[o]
            elif not o.hide_viewport:
                shape = blender_object_to_topods_shapes(
                    depsgraph, o, sp_type, scale, sew, sew_tolerance
                )

            if ins.scale == Vector((1.0, 1.0, 1.0)):
                trsf = blender_matrix_to_gp_trsf(ins.matrix_world, scale)
                trsf.SetScaleFactor(1)
                location = TopLoc_Location(trsf)
                instance = shape.Located(location)
                to_sew_shape_list.append(instance)
            else:
                trsf = blender_matrix_to_gp_trsf(ins.matrix_world, scale)
                trsf.SetScaleFactor(1)
                scalingMatrix = gp_Mat()
                scalingMatrix.SetDiagonal(ins.scale.x, ins.scale.y, ins.scale.z)
                gtrsf = gp_GTrsf()
                gtrsf.SetVectorialPart(scalingMatrix)
                shape = BRepBuilderAPI_GTransform(shape, gtrsf, True).Shape()
                shape = BRepBuilderAPI_Transform(shape, trsf, False).Shape()
                to_sew_shape_list.append(shape)

        # elif sp_type == SP_obj_type.INSTANCE:
        #     warnings.warn("Nested instances not supported yet")
        # #     # nested instance HARD, need to call an instance already built somewhere
        # #     #
        # #     # swd_nested = blender_instance_to_topods_instance(ins, context, hierarchy, scale, sew_tolerance)
        # #     builder.Add(comp, swd_nested)
        # #     is_nested=True

    # each collection instance is sewed separately
    swd = sew_shapes(to_sew_shape_list, sew_tolerance)

    # if is_nested:
    #     builder.Add(comp, swd)
    #     return comp
    # else :
    return swd


def sew_shapes(shape_list, tolerance=1e-1):
    aSew = BRepBuilderAPI_Sewing(tolerance)
    for shape in shape_list:
        aSew.Add(shape)

    # Sew
    aSew.SetNonManifoldMode(True)

    # try :
    aSew.Perform()
    return aSew.SewedShape()


def gather_export_shapes(
    context, use_selection: bool, scale=1000, sew: bool = True, sew_tolerance=1e-1
) -> TopoDS_Compound:

    separated_shapes_list = []
    hierarchy = ShapeHierarchy_export(context, use_selection, scale, sew, sew_tolerance)

    # prepare shapes
    if len(hierarchy.shapes) > 0:
        if sew:
            sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
            separated_shapes_list.extend(shells_to_solids(sewed))
        else:
            separated_shapes_list.extend(hierarchy.shapes)

    # TODO prepare sp compound objects
    # if len(hierarchy.compounds) > 0:
    #     pass
    #     sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
    #     separated_shapes_list.extend(shells_to_solids(sewed))

    # prepare instances
    if len(hierarchy.instances) > 0:
        sewed_instances_list = blender_instances_to_topods_instances(
            context, hierarchy, scale
        )

        for s in sewed_instances_list:
            separated_shapes_list.extend(shells_to_solids(s))

    if len(separated_shapes_list) > 0:
        root_compound = shape_list_to_compound(separated_shapes_list)
    else:
        return None

    return root_compound
