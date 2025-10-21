import bpy
import numpy as np
from .utils import *


def create_objects_from_instances(source_obj, context=bpy.context):
    """
    Create individual mesh objects from Geometry Nodes instances
    """
    depsgraph = context.evaluated_depsgraph_get()

    # Extract instance data immediately to avoid reference errors
    instance_data = []
    for obj_instance in depsgraph.object_instances:
        if obj_instance.parent and obj_instance.parent.original == source_obj:
            if obj_instance.object.type == "MESH":
                # Extract data immediately
                data = {
                    "mesh": obj_instance.object.data,
                    "matrix": obj_instance.matrix_world.copy(),
                    "name": obj_instance.object.name,
                }
                instance_data.append(data)

    print(f"Found {len(instance_data)} instances from depsgraph")

    created_objects = []

    # Create objects from extracted data
    for i, data in enumerate(instance_data):
        # Create new mesh and object
        new_mesh = bpy.data.meshes.new(f"{source_obj.name}.{i:03d}")
        new_obj = bpy.data.objects.new(f"{source_obj.name}.{i:03d}", new_mesh)

        # Copy mesh data
        copy_mesh_data(data["mesh"], new_mesh)

        values = [True] * len(new_mesh.polygons)
        new_mesh.polygons.foreach_set("use_smooth", values)
        new_mesh.update()

        # Apply transformation
        new_obj.matrix_world = data["matrix"]

        # Link to collection
        created_objects.append(new_obj)

    print(f"{len(created_objects)} objects created")
    return created_objects


def copy_mesh_data(source_mesh, target_mesh):
    """Copy mesh data including vertices, faces, and custom attributes"""

    # Copy basic mesh data
    vertices = [v.co[:] for v in source_mesh.vertices]
    edges = [e.vertices[:] for e in source_mesh.edges]
    faces = [f.vertices[:] for f in source_mesh.polygons]

    target_mesh.from_pydata(vertices, edges, faces)
    target_mesh.update()

    # Copy custom attributes
    copy_mesh_attributes(source_mesh, target_mesh)

    # Copy materials
    for material in source_mesh.materials:
        target_mesh.materials.append(material)


def copy_mesh_attributes(source_mesh, target_mesh):
    """Copy custom attributes from source to target mesh"""

    for source_attr in source_mesh.attributes:
        # Skip built-in attributes that are handled elsewhere
        if source_attr.name in [
            "position",
            ".edge_verts",
            ".corner_vert",
            ".corner_edge",
        ]:
            continue

        try:
            # Create new attribute
            target_attr = target_mesh.attributes.new(
                source_attr.name, source_attr.data_type, source_attr.domain
            )

            # Copy attribute data based on type
            if source_attr.data_type == "FLOAT":
                data = [0.0] * len(source_attr.data)
                source_attr.data.foreach_get("value", data)
                target_attr.data.foreach_set("value", data)

            elif source_attr.data_type == "INT":
                data = [0] * len(source_attr.data)
                source_attr.data.foreach_get("value", data)
                target_attr.data.foreach_set("value", data)

            elif source_attr.data_type == "FLOAT_VECTOR":
                data = [0.0] * (len(source_attr.data) * 3)
                source_attr.data.foreach_get("vector", data)
                target_attr.data.foreach_set("vector", data)

            elif source_attr.data_type == "FLOAT_COLOR":
                data = [0.0] * (len(source_attr.data) * 4)
                source_attr.data.foreach_get("color", data)
                target_attr.data.foreach_set("color", data)

            elif source_attr.data_type == "BOOLEAN":
                data = [False] * len(source_attr.data)
                source_attr.data.foreach_get("value", data)
                target_attr.data.foreach_set("value", data)

            elif source_attr.data_type == "FLOAT2":
                data = [0.0] * (len(source_attr.data) * 2)
                source_attr.data.foreach_get("vector", data)
                target_attr.data.foreach_set("vector", data)

            elif source_attr.data_type == "INT32_2D":
                data = [0] * (len(source_attr.data) * 2)
                source_attr.data.foreach_get("value", data)
                target_attr.data.foreach_set("value", data)

        except Exception as e:
            print(f"Failed to copy attribute {source_attr.name}: {e}")


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


def convert_compound_to_patches(o, context):
    mod = o.modifiers[-1]
    if mod.node_group.name[:-4] in ["SP - Compound Mes", "SP - Compound Meshing"]:
        # Disable modifier to access non meshed data
        mod.show_viewport = False
        created_objects = create_objects_from_instances(o, context)
        mod.show_viewport = True

        types = np.zeros(len(created_objects), dtype=np.int32)

        ob = o.evaluated_get(context.evaluated_depsgraph_get())
        for att in ob.data.attributes:
            if (
                att.domain == "POINT"
                and att.name == "SP_type"
                and att.data_type == "INT"
            ):
                types = np.zeros(len(att.data), dtype=np.int32)
                att.data.foreach_get("value", types)
                break

        for i, obj in enumerate(created_objects):
            add_sp_modifier(
                obj, MESHER_NAMES[SP_obj_type(types[i])], pin=True, append=False
            )
        
        return created_objects

