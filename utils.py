import bpy
import bmesh
import numpy as np
import sys
from os.path import dirname, abspath
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
ASSETSPATH = addonpath + "/assets/assets.blend"



def geom_type_of_object(o, context):
    type = None
    if o.type == 'EMPTY' and o.instance_collection != None :
        type = 'collection_instance'
    else : 
        ob = o.evaluated_get(context.evaluated_depsgraph_get())
        if hasattr(ob.data, "attributes") :

            for k in ob.data.attributes.keys() :
                match k:
                    case 'CP_bezier_surf' :
                        type = 'bezier_surf'
                        break
                    case 'CP_any_order_surf' :
                        type = 'surf_any'
                        break
                    case 'CP_planar' :
                        type = 'planar'
                        break
                    case 'CP_any_order_curve':
                        type = 'curve_any'
                        break
                    case 'CP_bezier_chain':
                        type = 'bezier_chain'
                        break
                    case 'CP_curve':
                        type = 'curve'
                        break
    return type


def get_attribute_by_name(ob_deps_graph, name, type='vec3', len_attr=None):
    ge = ob_deps_graph.data
    match type :
        case 'first_int':
            attribute = ge.attributes[name].data[0].value
        case 'second_int':
            attribute = ge.attributes[name].data[1].value
        case 'int':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.zeros(len_raw)
            ge.attributes[name].data.foreach_get("value", attribute)
            attribute = attribute[0:len_attr]
        case 'vec3':
            len_raw = len(ge.attributes[name].data)
            if len_attr==None :
                len_attr = len_raw
            attribute = np.empty(3 * len_raw)
            ge.attributes[name].data.foreach_get("vector", attribute)
            attribute = attribute.reshape((-1, 3))[0:len_attr]
    return attribute



def append_object_by_name(obj_name, context):# for importing from the asset file
    with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name==obj_name]

    cursor_loc = context.scene.cursor.location

    for o in data_to.objects:
        if o is not None:
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            context.collection.objects.link(o)
            o.location = cursor_loc
            o.asset_clear()
            o.select_set(True)
            bpy.context.view_layer.objects.active = o


def classify_strings_by_prefix(strings):
    import re
    strings.sort()
    object_dict = {}
    for string in strings:
        # Use regex to extract the common prefix
        match = re.match(r'(\D+)(\d*.*)', string)
        if match:
            prefix = match.group(1)
            if prefix not in object_dict:
                object_dict[prefix] = [string]
            else:
                object_dict[prefix].append(string)
    return object_dict


def highest_suffix_of_each_object_name(names):
    classified_objects=classify_strings_by_prefix(names)
    last_string = []
    for key, value in classified_objects.items():
        if value:
            last_string+= [value[-1]]
    return last_string


def create_grid(vertices):
    n,m = np.shape(vertices)
    vertices_flat = vertices.reshape(-1)
    return vertices_flat, [], [(i, i + 1, i + m + 1, i + m) for i in range((n - 1) * m) if (i + 1) % m != 0]
