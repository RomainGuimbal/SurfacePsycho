import bpy
import numpy as np
from .enums import SP_obj_type, MESHER_NAMES
from .asset_append import add_sp_modifier

def create_objects_from_instances(source_obj, depsgraph, suffix=""):
    """
    Create individual mesh objects from Geometry Nodes instances
    """
    created_objects = []
    i = 0
    for obj_instance in depsgraph.object_instances:
        if obj_instance.parent and obj_instance.parent.original == source_obj:
            if obj_instance.object.type == "MESH":
                name = f"{source_obj.name}.{i:03d}{suffix}"

                # C-level copy: copies geometry, attributes and materials at once
                new_mesh = obj_instance.object.data.copy()
                new_mesh.name = name

                n_polys = len(new_mesh.polygons)
                if n_polys > 0:
                    smooth = np.ones(n_polys, dtype=bool)
                    new_mesh.polygons.foreach_set("use_smooth", smooth)
                    new_mesh.update()

                new_obj = bpy.data.objects.new(name, new_mesh)
                new_obj.matrix_world = obj_instance.matrix_world.copy()

                created_objects.append(new_obj)
                i += 1

    return created_objects


# Instance domain fails /!\
# def get_instance_patch_type(o, context):
#     ob = o.evaluated_get(context.evaluated_depsgraph_get())
#     data = np.zeros(len(attr.data), dtype=np.int32)

#     for attr in ob.data.attributes:
#         if (
#             attr.domain == "INSTANCE" # Instance domain fails /!\
#             and attr.name == "SP_type"
#             and attr.data_type == "INT"
#         ):
#             attr.data.foreach_get("value", data)
#     return data


def convert_compound_to_patches(o, context, initial_depsgraph, objects_suffix="", resolution=16, ):
    # Find compound meshing modifier
    mod = None
    for m in reversed(o.modifiers):
        if m.node_group.name[:-4] in ["SP - Compound Mes", "SP - Compound Meshing"]:
            mod = m
            break

    if mod == None:
        return None

    # Get types
    ob = o.evaluated_get(initial_depsgraph)
    types = np.zeros(len(o.data.vertices), dtype=np.int32)
    for att in ob.data.attributes:
        if att.domain == "POINT" and att.name == "SP_type" and att.data_type == "INT":
            types = np.zeros(len(att.data), dtype=np.int32)
            att.data.foreach_get("value", types)
            break

    # Create objects
    # Disable modifier to access non meshed data
    mod.show_viewport = False
    depsgraph = context.evaluated_depsgraph_get()
    created_objects = create_objects_from_instances(o, depsgraph, objects_suffix)
    mod.show_viewport = True

    # Add modifiers
    for i, obj in enumerate(created_objects):
        settings_dict = {}
        if SP_obj_type(types[i]) in [
            SP_obj_type.BEZIER_SURFACE,
            SP_obj_type.BSPLINE_SURFACE,
        ]:
            add_sp_modifier(obj, "SP - Reorder Grid Index", append=False)
            settings_dict = {
                "Resolution U": resolution,
                "Resolution V": resolution,
            }  # TODO "Evaluate": False
        if SP_obj_type(types[i]) == SP_obj_type.PLANE:
            settings_dict = {"Orient": True}

        add_sp_modifier(
            obj,
            MESHER_NAMES[SP_obj_type(types[i])],
            settings_dict,
            pin=True,
            append=False,
        )

    return created_objects
