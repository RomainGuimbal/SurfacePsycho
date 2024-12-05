import bpy
import numpy as np
from mathutils import Vector
from os.path import dirname, abspath
from .utils import *
import copy
from typing import List, Dict


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

    return (axis1,axis2,axis3)

def svg_xy_string_from_CP(CP, plane="XY"):
    axis1, axis2, _ = get_axis_ids_from_name(plane)
    return f"{CP[axis1]} {-CP[axis2]} "

def svg_z_from_obj(o, plane="XY"):
    _, _, axis3 = get_axis_ids_from_name(plane)
    return o.location[axis3]




def mirror_wires_like_modifiers(o, wire_bundle : dict):
    # list of list of wires
    list_of_bundle_of_wires =[wire_bundle]
    self_matrix = o.matrix_world

    for m in o.modifiers :
        if m.type == 'MIRROR' and m.show_viewport :
            if m.mirror_object!=None:
                mirror_obj_mat = m.mirror_object.matrix_world
            else :
                mirror_obj_mat = None
            
            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            #copy bundles
            bundles_list = list_of_bundle_of_wires.copy()

            #mirror and append the copy to the original
            if x :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("X", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)
            
            if y :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Y", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)

            if z :
                for bundle in bundles_list.copy() :
                    mir_wires = {}
                    for key, w in bundle.items() :
                        wir = copy.deepcopy(w)
                        wir.mirror_CP("Z", self_matrix, mirror_obj_mat)
                        mir_wires[key]= wir
                    bundles_list.append(mir_wires)
            
            list_of_bundle_of_wires = bundles_list.copy()

    return list_of_bundle_of_wires



def svg_path_string_from_wires(wires, plane):
    # SVG path string
    d =""
    for w in wires.values():
        d+="M "
        d+= svg_xy_string_from_CP(w.CP[0], plane)
        i=1
        seg_count = len(w.segs_degrees)
        for j,degree in enumerate(w.segs_degrees) :
            islast = j == seg_count-1
            if degree == 1:
                if not islast :
                    d+= "L "
                    d+= svg_xy_string_from_CP(w.CP[i], plane)
                else :
                    d+="Z "
                i+=1
            elif degree == 3:
                d+= "C "
                d+= svg_xy_string_from_CP(w.CP[i], plane)
                d+=","
                d+= svg_xy_string_from_CP(w.CP[i+1], plane)
                d+=","
                d+= svg_xy_string_from_CP(w.CP[(i+2)%(len(w.CP))], plane)
                i+=3
            else :
                print("Error, segment has degree not 1 or 3")
    return d




def new_svg_fill(o, context, plane, origin=Vector((0,0,0)), scale=100, color_mode="material"):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    segs_p_counts = get_attribute_by_name(ob, 'CP_count', 'int')

    # get total_p_count
    total_p_count, segment_count= 0, 0
    for p in segs_p_counts:
        if p>0:
            total_p_count += p-1
            segment_count += 1
        if p==0:
            break
    
    segs_p_counts = segs_p_counts[:segment_count]

    try :
        segs_degrees = get_attribute_by_name(ob, 'Degree', 'int', segment_count)
    except KeyError :
        segs_degrees = None

    # Get CP position attr
    points = get_attribute_by_name(ob, 'CP_planar', 'vec3', total_p_count)
    

    # Wires
    wires_dict = split_and_prepare_wires(ob, points, total_p_count, segs_p_counts, segs_degrees)
    
    
    # SVG path attributes
    if color_mode == "object":
        col_rgba = o.color
    elif color_mode == "material":
        col_rgba = o.material_slots[0].material.diffuse_color
    hex_col = to_hex(col_rgba)
    color = f"#{hex_col}"
    z = svg_z_from_obj(o, plane="XY")
    fills = []

    # mirror
    mirrored_wires = mirror_wires_like_modifiers(o, wires_dict) # list of dictionaries of wires
    
    # transform
    for mw in mirrored_wires :
        for k, v in mw.items():
            v.offset(-origin)
            v.scale(scale)
    
    opacity = o.color[3]**(1/2.2) if o.color[3]!=1.0 else 1.0

    for mw in mirrored_wires :
        d = svg_path_string_from_wires(mw, plane)
        fills.append({"d": d, "color": color, "opacity": opacity, "z": z})
    
    return fills



def prepare_svg(context, use_selection, plane="XY",  origin_mode="auto", scale=100, color_mode="material"):
    shapes = []
    SPobj_count=0

    # Selection
    if use_selection:
        initial_selection = context.selected_objects
    else :
        initial_selection = context.visible_objects
    obj_list = initial_selection
    obj_to_del = []

    # Position
    if origin_mode=="auto":
        # Find bounds
        xmax, ymax, zmax = -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
        xmin, ymin, zmin = 1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308
        
        for o in initial_selection :
            bbox_corners = [o.matrix_world @ Vector(corner) for corner in o.bound_box]
            oxmax, oymax, ozmax = np.array(bbox_corners).max(axis=0)
            xmax = oxmax if oxmax > xmax else xmax
            ymax = oymax if oymax > ymax else ymax
            zmax = ozmax if ozmax > zmax else zmax
            
            oxmin, oymin, ozmin = np.array(bbox_corners).min(axis=0)
            xmin = oxmin if oxmin < xmin else xmin
            ymin = oymin if oymin < ymin else ymin
            zmin = ozmin if ozmin < zmin else zmin

        

        #origin is in top-left corner
        axis1, axis2, _ = get_axis_ids_from_name(plane)
        ox = xmin #if axis1==0 else 0
        oy = ymax if axis2==1 else ymin
        oz = zmax #if axis2==2 else 0

        mx = xmax
        my = ymin if axis2==1 else ymax
        mz = zmin
        origin = Vector((ox, oy, oz))
        size3d = (Vector((mx,my,mz))-origin)*scale

        canvas_size = (abs(size3d[axis1]), abs(size3d[axis2]))
    else : #world
        origin = Vector((0,0,0))
        #considering there is high chance a fill is placed at less than 10 blender unit from the origin
        canvas_size = (10*scale,10*scale)

    # Main entity loop
    while(len(obj_list)>0): # itterates until ob_list is empty
        obj_newly_real = []

        for o in obj_list:
            gto = geom_type_of_object(o, context)

            match gto :
                case "planar" :
                    SPobj_count +=1
                    shapes.extend(new_svg_fill(o, context, plane, origin, scale, color_mode="material"))

                # case "curve" :
                #     SPobj_count +=1
                #     cu = new_svg_curve(o, context)
                #     aSew.Add(mirror_brep(o, cu))

                # case "collection_instance":
                #     pass

        obj_list=[]
        for onr in obj_newly_real:
            obj_list.append(onr)
            obj_to_del.append(onr)

    for o in obj_to_del : # clear realized objects
        bpy.data.objects.remove(o, do_unlink=True)
    
    if SPobj_count>0 :
        shapes_sorted = list(sorted(shapes, key=lambda x: x["z"]))
        return shapes_sorted, canvas_size
    else :
        return None




def write_svg_file(contours: List[Dict[str, str]], filepath: str, canvas_size):
    # Start SVG file structure
    svg_content = f'''<svg width="{canvas_size[0]}" height="{canvas_size[1]}" xmlns="http://www.w3.org/2000/svg">\n'''
    
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



def export_svg(context, filepath, use_selection, plane="XY", origin_mode="auto", scale=100, color_mode="material"):
    svg_shapes, canvas_size = prepare_svg(context, use_selection, plane,  origin_mode, scale, color_mode)
    if svg_shapes is not None :
        write_svg_file(svg_shapes, filepath, canvas_size)
        return True
    else:
        return False
