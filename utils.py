import bpy
import bmesh
import numpy as np
# from multiprocessing import Process
# import sys
# from os.path import dirname, abspath

# addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
# ASSETSPATH = addonpath + "/assets/assets.blend"
ASSETSPATH = None


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
                        type = 'bicubic_surf'
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
                    case 'CP_curve':
                        type = 'curve'
                        break
                    case 'CP_NURBS_curve' :
                        type = 'NURBS_curve'
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

        case 'float':
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

    o = data_to.objects[0]
    if o is not None:
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        context.collection.objects.link(o)
        o.location = cursor_loc
        o.asset_clear()
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        # Iterate through all objects and their geometry node modifiers
        for mod in o.modifiers:
            if mod.type == 'NODES' and mod.node_group:
                mod.node_group.asset_clear()


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


# def modifier_exists_in_file(modifier_name):
#     for mod in bpy.data.modifiers:
#         if mod.name == modifier_name:
#             return True
#     return False


# def add_modifier(object, modifier_name):
#     if not modifier_exists_in_file(modifier_name):
#         append_modifier_from_sp_lib(modifier_name)

#     for mod in bpy.data.modifiers:
#         if mod.name == modifier_name:
#             appended_modifier = mod
#             break

#     object.modifiers.new(name=modifier_name, type=appended_modifier.type)


# def append_modifier_from_sp_lib(modifier_name):
#     with bpy.data.libraries.load(ASSETSPATH, link=False) as (data_from, data_to):
#         if modifier_name in data_from.modifiers:
#             data_to.modifiers.append(modifier_name)

# def progress_bar(self, context):
#     row = self.layout.row()
#     row.progress(
#         factor=context.window_manager.progress,
#         type="BAR",
#         text="Import in progress..." if context.window_manager.progress < 1 else "Import Successful"
#     )
#     row.scale_x = 1


# def runInParallel(fns):
#   proc = []
#   for fn in fns:
#     p = Process(target=fn)
#     p.start()
#     proc.append(p)
#   for p in proc:
#     p.join()

def change_node_socket_value(ob, value, potential_names, socket_type, context):
    for m in ob.modifiers :
        if m.type == "NODES" and m.node_group.name[:5]=='SP - ':
            for it in m.node_group.interface.items_tree :
                if it.name in potential_names and it.socket_type == socket_type:
                    input_id = it.identifier
                    m[input_id] = value
                    m.node_group.interface_update(context)