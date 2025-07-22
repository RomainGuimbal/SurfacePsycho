from OCP.gp import (
    gp_Ax1,
    gp_Ax2,
    gp_Ax22d,
    gp_Dir,
    gp_Dir2d,
    gp_Elips,
    gp_Elips2d,
    gp_Pnt,
    gp_Pnt2d,
    gp_Vec,
    gp_Vec2d,
)

def a_transpose_mult_a_2x2(a, b, c, d):
    return (a**2 + c**2, a * b + c * d, b**2 + d**2)


def eigen_val_2x2(a, bc, d):
    half_trace = (a + d) / 2
    lambda1 = half_trace + (half_trace**2 - a * d + bc**2) ** 0.5
    lambda2 = half_trace - (half_trace**2 - a * d + bc**2) ** 0.5
    return lambda1, lambda2


def eigen_vec_2x2(lambda1, lambda2, a, b, c, d):
    b1 = b != 0.0 or lambda1 != a
    c2 = c != 0.0 or lambda2 != d
    x1 = b if b1 else 1.0
    y1 = lambda1 - a if b1 else 0.0
    x2 = lambda2 - d if c2 else 0.0
    y2 = c if c2 else 1.0

    return x1, y1, x2, y2


def ellipse_info(x1, y1, x2, y2):
    a, bc, d = a_transpose_mult_a_2x2(x1, y1, x2, y2)
    lambda1, lambda2 = eigen_val_2x2(a, bc, d)
    radiusa = lambda1**0.5
    radiusb = lambda2**0.5
    x1, y1, x2, y2 = eigen_vec_2x2(lambda1, lambda2, a, bc, bc, d)
    return radiusa, radiusb, x1, y1, x2, y2


def rotation_from_vectors(from_vector : gp_Vec, to_vector : gp_Vec):
    axis = from_vector.Crossed(to_vector)
    if axis.Magnitude() == 0.0 :
        axis = gp_Vec(0,0,1)
    angle = from_vector.Angle(to_vector)
    return gp_Ax1(gp_Pnt(0,0,0), gp_Dir(axis)), angle


def gp_Elips2d_from_3_points(center: gp_Pnt2d, p1: gp_Pnt2d, p2: gp_Pnt2d):
    center_vec = gp_Vec2d(center.X(), center.Y())
    p1_vec = gp_Vec2d(p1.X(), p1.Y())
    p2_vec = gp_Vec2d(p2.X(), p2.Y())

    vec1 = p1_vec - center_vec
    vec2 = p2_vec - center_vec

    radius_a, radius_b, x1, y1, x2, y2 = ellipse_info(
        vec1.X(), vec1.Y(), vec2.X(), vec2.Y()
    )

    basis = gp_Ax22d(center, gp_Dir2d(x1, y1), gp_Dir2d(x2, y2))

    return gp_Elips2d(basis, radius_a, radius_b)


def gp_Elips_from_3_points(center: gp_Pnt, p1: gp_Pnt, p2: gp_Pnt):
    center_vec = gp_Vec(center.X(), center.Y(), center.Z())
    p1_vec = gp_Vec(p1.X(), p1.Y(), p1.Z())
    p2_vec = gp_Vec(p2.X(), p2.Y(), p2.Z())

    vec1 = p1_vec - center_vec
    vec2 = p2_vec - center_vec

    # Transform to xy plane
    rotation = rotation_from_vectors(vec2.Crossed(vec1), gp_Vec(0,0,1))
    vec1_rotated = vec1.Rotated(*rotation)
    vec2_rotated = vec2.Rotated(*rotation)

    radius_a, radius_b, x1, y1, x2, y2 = ellipse_info(
        vec1_rotated.X(), vec1_rotated.Y(), vec2_rotated.X(), vec2_rotated.Y()
    )
    vec_a = gp_Vec(x1,y1,0)
    vec_b = gp_Vec(x2,y2,0)

    # Transform back
    inv_rotation = rotation_from_vectors(gp_Vec(0,0,1), vec2.Crossed(vec1))
    vec_a_inv_rotated = vec_a.Rotated(*inv_rotation)
    vec_b_inv_rotated = vec_b.Rotated(*inv_rotation)

    basis = gp_Ax2(center, gp_Dir(vec_b_inv_rotated.Crossed(vec_a_inv_rotated)), gp_Dir(vec_a_inv_rotated))

    return gp_Elips(basis, radius_a, radius_b)