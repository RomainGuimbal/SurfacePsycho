import bpy
import numpy as np
from mathutils import Vector
from ..common.enums import SP_obj_type
from ..common.utils import to_hex, sp_type_of_object
import copy
from typing import List, Dict
from .export_shapes_final import SP_Contour_export


#####################################
#                                   #
#           SVG exporter            #
#                                   #
#####################################


def get_axis_ids_from_name(plane):
    match plane:
        case "XY":
            axis1 = 0
            axis2 = 1
            axis3 = 2

        case "YZ":
            axis1 = 1
            axis2 = 2
            axis3 = 0

        case "XZ":
            axis1 = 0
            axis2 = 2
            axis3 = 1

    return (axis1, axis2, axis3)


def svg_xy_string_from_CP(CP, plane="XY"):
    axis1, axis2, _ = get_axis_ids_from_name(plane)
    return f"{CP[axis1]} {-CP[axis2]} "


def svg_z_from_obj(o, plane="XY"):
    _, _, axis3 = get_axis_ids_from_name(plane)
    return o.location[axis3]


def mirror_wires_like_modifiers(o, wire_bundle: dict):
    # list of list of wires
    list_of_bundle_of_wires = [wire_bundle]
    self_matrix = o.matrix_world

    for m in o.modifiers:
        if m.type == "MIRROR" and m.show_viewport:
            if m.mirror_object != None:
                mirror_obj_mat = m.mirror_object.matrix_world
            else:
                mirror_obj_mat = None

            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            # copy bundles
            bundles_list = list_of_bundle_of_wires.copy()

            # mirror and append the copy to the original
            if x:
                for bundle in bundles_list.copy():
                    mir_wires = {}
                    for key, w in bundle.items():
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("X", self_matrix, mirror_obj_mat)
                        mir_wires[key] = wir
                    bundles_list.append(mir_wires)

            if y:
                for bundle in bundles_list.copy():
                    mir_wires = {}
                    for key, w in bundle.items():
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Y", self_matrix, mirror_obj_mat)
                        mir_wires[key] = wir
                    bundles_list.append(mir_wires)

            if z:
                for bundle in bundles_list.copy():
                    mir_wires = {}
                    for key, w in bundle.items():
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Z", self_matrix, mirror_obj_mat)
                        mir_wires[key] = wir
                    bundles_list.append(mir_wires)

            list_of_bundle_of_wires = bundles_list.copy()

    return list_of_bundle_of_wires


def svg_path_string_from_wires(wires, plane):
    # SVG path string
    d = ""
    for w in wires.values():
        d += "M "
        d += svg_xy_string_from_CP(w.CP[0], plane)
        i = 1
        seg_count = len(w.segs_p_counts)
        for j, p_count in enumerate(w.segs_p_counts):
            degree = p_count -1
            islast = j == seg_count - 1
            if degree == 1 or degree == 0:
                if not islast:
                    d += "L "
                    d += svg_xy_string_from_CP(w.CP[i], plane)
                else:
                    d += "Z "
                i += 1
            elif degree == 3:
                d += "C "
                d += svg_xy_string_from_CP(w.CP[i], plane)
                d += ","
                d += svg_xy_string_from_CP(w.CP[i + 1], plane)
                d += ","
                d += svg_xy_string_from_CP(w.CP[(i + 2) % (len(w.CP))], plane)
                i += 3
            else:
                print("Error, segment has degree not 1 or 3")
    return d


def new_svg_fill(
    o, context, plane, origin=Vector((0, 0, 0)), scale=100, color_mode="material"
):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())

    # Wires
    wires_dict = SP_Contour_export(
        ob, "CP_planar", "CP_count", "IsClamped", "IsPeriodic"
    ).wires_dict

    # SVG path attributes
    if color_mode == "object":
        col_rgba = o.color
    elif color_mode == "material":
        if len(o.material_slots) > 0 :
            col_rgba = o.material_slots[0].material.diffuse_color
        else :
            col_rgba = o.color
    hex_col = to_hex(col_rgba)
    color = f"#{hex_col}"
    z = svg_z_from_obj(o, plane="XY")
    fills = []

    # mirror
    mirrored_wires = mirror_wires_like_modifiers(
        o, wires_dict
    )  # list of dictionaries of wires

    # transform
    for mw in mirrored_wires:
        for k, v in mw.items():
            v.offset(-origin)
            v.scale(scale)

    opacity = o.color[3] ** (1 / 2.2) if o.color[3] != 1.0 else 1.0

    for mw in mirrored_wires:
        d = svg_path_string_from_wires(mw, plane)
        fills.append({"d": d, "color": color, "opacity": opacity, "z": z})

    return fills


def prepare_svg(
    context,
    use_selection,
    plane="XY",
    origin_mode="auto",
    scale=100,
    color_mode="material",
):
    shapes = []
    SPobj_count = 0

    # Selection
    if use_selection:
        initial_selection = context.selected_objects
    else:
        initial_selection = context.visible_objects
    obj_list = initial_selection
    obj_to_del = []

    # Position
    if origin_mode == "auto":
        # Find bounds
        xmax, ymax, zmax = (
            -1.7976931348623157e308,
            -1.7976931348623157e308,
            -1.7976931348623157e308,
        )
        xmin, ymin, zmin = (
            1.7976931348623157e308,
            1.7976931348623157e308,
            1.7976931348623157e308,
        )

        for o in initial_selection:
            bbox_corners = [o.matrix_world @ Vector(corner) for corner in o.bound_box]
            oxmax, oymax, ozmax = np.array(bbox_corners).max(axis=0)
            xmax = oxmax if oxmax > xmax else xmax
            ymax = oymax if oymax > ymax else ymax
            zmax = ozmax if ozmax > zmax else zmax

            oxmin, oymin, ozmin = np.array(bbox_corners).min(axis=0)
            xmin = oxmin if oxmin < xmin else xmin
            ymin = oymin if oymin < ymin else ymin
            zmin = ozmin if ozmin < zmin else zmin

        # origin is in top-left corner
        axis1, axis2, _ = get_axis_ids_from_name(plane)
        ox = xmin  # if axis1==0 else 0
        oy = ymax if axis2 == 1 else ymin
        oz = zmax  # if axis2==2 else 0

        mx = xmax
        my = ymin if axis2 == 1 else ymax
        mz = zmin
        origin = Vector((ox, oy, oz))
        size3d = (Vector((mx, my, mz)) - origin) * scale

        canvas_size = (abs(size3d[axis1]), abs(size3d[axis2]))
    else:  # world
        origin = Vector((0, 0, 0))
        # considering there is high chance a fill is placed at less than 10 blender unit from the origin
        canvas_size = (10 * scale, 10 * scale)

    # Main entity loop
    while len(obj_list) > 0:  # itterates until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            type = sp_type_of_object(o)

            match type:
                case SP_obj_type.PLANE:
                    SPobj_count += 1
                    shapes.extend(
                        new_svg_fill(
                            o, context, plane, origin, scale, color_mode="material"
                        )
                    )

                # case "curve" :
                #     SPobj_count +=1
                #     cu = new_svg_curve(o, context)
                #     aSew.Add(mirror_brep(o, cu))

                # case "collection_instance":
                #     pass

        obj_list = []
        for onr in obj_newly_real:
            obj_list.append(onr)
            obj_to_del.append(onr)

    for o in obj_to_del:  # clear realized objects
        bpy.data.objects.remove(o, do_unlink=True)

    if SPobj_count > 0:
        shapes_sorted = list(sorted(shapes, key=lambda x: x["z"]))
        return shapes_sorted, canvas_size
    else:
        return None


def write_svg_file(contours: List[Dict[str, str]], filepath: str, canvas_size):
    # Start SVG file structure
    svg_content = f"""<svg width="{canvas_size[0]}" height="{canvas_size[1]}" xmlns="http://www.w3.org/2000/svg">\n"""

    # Add each contour as a separate path with its own color
    for contour in contours:
        d = contour["d"]
        color = contour.get("color", "black")  # Default to black
        opacity = contour["opacity"]
        svg_content += f'    <path d="{d}" fill="{color}" fill-opacity="{opacity}" fill-rule="evenodd"/>\n'

    # Close SVG file structure
    svg_content += "</svg>"

    # Write the SVG content to file
    with open(filepath, "w") as svg_file:
        svg_file.write(svg_content)

    print("SVG Export succesful")


def export_svg(
    context,
    filepath,
    use_selection,
    plane="XY",
    origin_mode="auto",
    scale=100,
    color_mode="material",
):
    svg_shapes, canvas_size = prepare_svg(
        context, use_selection, plane, origin_mode, scale, color_mode
    )
    if svg_shapes is not None:
        write_svg_file(svg_shapes, filepath, canvas_size)
        return True
    else:
        return False


#######################################
#      OCC EXTENDS SVG EXPORTER !     #
#######################################

##############
# SVG export #
##############
# def edge_to_svg_polyline(topods_edge, tol=0.1, unit="mm"):
#     """Returns a svgwrite.Path for the edge, and the 2d bounding box"""
#     check_svgwrite_installed()

#     unit_factor = 1  # by default

#     if unit == "mm":
#         unit_factor = 1
#     elif unit == "m":
#         unit_factor = 1e3

#     points_3d = discretize_edge(topods_edge, tol)
#     points_2d = []
#     box2d = Bnd_Box2d()

#     for point in points_3d:
#         # we tak only the first 2 coordinates (x and y, leave z)
#         x_p = -point[0] * unit_factor
#         y_p = point[1] * unit_factor
#         box2d.Add(gp_Pnt2d(x_p, y_p))
#         points_2d.append((x_p, y_p))

#     return svgwrite.shapes.Polyline(points_2d, fill="none"), box2d


# Uses external package for the actuall export. (Should be quite easy to retro engineer)

# import os

# from OCC.Core.TopoDS import TopoDS_Shape
# from OCC.Core.TopAbs import TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND
# from OCC.Core.BRepTools import breptools
# from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
# from OCC.Core.StlAPI import stlapi, StlAPI_Writer
# from OCC.Core.BRep import BRep_Builder
# from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pnt2d
# from OCC.Core.Bnd import Bnd_Box2d
# from OCC.Core.TopoDS import TopoDS_Compound
# from OCC.Core.IGESControl import (
#     IGESControl_Controller,
#     IGESControl_Reader,
#     IGESControl_Writer,
# )
# from OCC.Core.STEPControl import (
#     STEPControl_Reader,
#     STEPControl_Writer,
#     STEPControl_AsIs,
# )
# from OCC.Core.Interface import Interface_Static
# from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
# from OCC.Core.TDocStd import TDocStd_Document
# from OCC.Core.XCAFDoc import (
#     XCAFDoc_DocumentTool,
#     XCAFDoc_ColorTool,
# )
# from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
# from OCC.Core.TDF import TDF_LabelSequence, TDF_Label
# from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
# from OCC.Core.TopLoc import TopLoc_Location
# from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
# from OCC.Core.TColStd import TColStd_IndexedDataMapOfStringString
# from OCC.Core.TCollection import TCollection_AsciiString
# from OCC.Core.RWPly import RWPly_CafWriter
# from OCC.Core.Message import Message_ProgressRange

# from OCC.Core.RWGltf import RWGltf_CafReader, RWGltf_CafWriter
# from OCC.Core.RWObj import RWObj_CafWriter, RWObj_CafReader
# from OCC.Core.RWMesh import (
#     RWMesh_CoordinateSystem_posYfwd_posZup,
#     RWMesh_CoordinateSystem_negZfwd_posYup,
# )
# from OCC.Core.UnitsMethods import unitsmethods

# from OCC.Extend.TopologyUtils import (
#     discretize_edge,
#     get_sorted_hlr_edges,
#     list_of_shapes_to_compound,
# )

# try:
#     import svgwrite

#     HAVE_SVGWRITE = True
# except ImportError:
#     HAVE_SVGWRITE = False


# def check_svgwrite_installed():
#     if not HAVE_SVGWRITE:
#         raise IOError(
#             "svg exporter not available because the svgwrite package is not installed. use $pip install svgwrite'"
#         )


# def export_shape_to_svg(
#     shape,
#     filename=None,
#     width=800,
#     height=600,
#     margin_left=10,
#     margin_top=30,
#     export_hidden_edges=True,
#     location=gp_Pnt(0, 0, 0),
#     direction=gp_Dir(1, 1, 1),
#     color="black",
#     line_width="1px",
#     unit="mm",
# ):
#     """export a single shape to an svg file and/or string.
#     shape: the TopoDS_Shape to export
#     filename (optional): if provided, save to an svg file
#     width, height (optional): integers, specify the canva size in pixels
#     margin_left, margin_top (optional): integers, in pixel
#     export_hidden_edges (optional): whether or not draw hidden edges using a dashed line
#     location (optional): a gp_Pnt, the lookat
#     direction (optional): to set up the projector direction
#     color (optional), "default to "black".
#     line_width (optional, default to 1): an integer
#     """
#     check_svgwrite_installed()

#     if shape.IsNull():
#         raise AssertionError("shape is Null")

#     # find all edges
#     visible_edges, hidden_edges = get_sorted_hlr_edges(
#         shape,
#         position=location,
#         direction=direction,
#         export_hidden_edges=export_hidden_edges,
#     )

#     # compute polylines for all edges
#     # we compute a global 2d bounding box as well, to be able to compute
#     # the scale factor and translation vector to apply to all 2d edges so that
#     # they fit the svg canva
#     global_2d_bounding_box = Bnd_Box2d()

#     polylines = []
#     for visible_edge in visible_edges:
#         visible_svg_line, visible_edge_box2d = edge_to_svg_polyline(
#             visible_edge, 0.1, unit
#         )
#         polylines.append(visible_svg_line)
#         global_2d_bounding_box.Add(visible_edge_box2d)
#     if export_hidden_edges:
#         for hidden_edge in hidden_edges:
#             hidden_svg_line, hidden_edge_box2d = edge_to_svg_polyline(
#                 hidden_edge, 0.1, unit
#             )
#             # hidden lines are dashed style
#             hidden_svg_line.dasharray([5, 5])
#             polylines.append(hidden_svg_line)
#             global_2d_bounding_box.Add(hidden_edge_box2d)

#     # translate and scale polylines

#     # first compute shape translation and scale according to size/margins
#     x_min, y_min, x_max, y_max = global_2d_bounding_box.Get()
#     bb2d_width = x_max - x_min
#     bb2d_height = y_max - y_min

#     # build the svg drawing
#     dwg = svgwrite.Drawing(filename, (width, height), debug=True)
#     # adjust the view box so that the lines fit then svg canvas
#     dwg.viewbox(
#         x_min - margin_left,
#         y_min - margin_top,
#         bb2d_width + 2 * margin_left,
#         bb2d_height + 2 * margin_top,
#     )

#     for polyline in polylines:
#         # apply color and style
#         polyline.stroke(color, width=line_width, linecap="round")
#         # then adds the polyline to the svg canva
#         dwg.add(polyline)

#     # export to string or file according to the user choice
#     if filename is not None:
#         dwg.save()
#         if not os.path.isfile(filename):
#             raise AssertionError("svg export failed")
#         print(f"Shape successfully exported to {filename}")
#         return True
#     return dwg.tostring()
