import bpy
import bmesh
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
import numpy as np

# Global variables
draw_handler = None
shader = None
active_object = None
active_group_name = None
valid_tool_idnames = set()
POINT_SIZE = 15.0  # Change this to adjust point size


def get_vertex_attribute_positions(o, group_name):
    """Get world positions of vertices with the specified attribute, split by selection state.
    Returns (selected, unselected) lists of world-space positions."""
    if o.type != 'MESH':
        return [], []

    mat = o.matrix_world

    if o.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(o.data)
        bm.verts.ensure_lookup_table()
        layer = (bm.verts.layers.bool.get(group_name) or
                 bm.verts.layers.int.get(group_name))
        if layer is None:
            return [], []
        selected = [mat @ v.co for v in bm.verts if v[layer] and v.select]
        unselected = [mat @ v.co for v in bm.verts if v[layer] and not v.select]
        return selected, unselected

    # Object mode: attributes are available
    if group_name not in o.data.attributes:
        return [], []
    pos_att = o.data.attributes["position"]
    mask_att = o.data.attributes[group_name]
    len_att = len(mask_att.data)
    mask = np.zeros(len_att, dtype=bool)
    mask_att.data.foreach_get("value", mask)
    pos = np.zeros(len_att * 3, dtype=float)
    pos_att.data.foreach_get("vector", pos)
    pos = pos.reshape((-1, 3))
    return [], [mat @ Vector(pos[i]) for i in range(len(pos)) if mask[i]]


def draw_callback():
    """Draw function called by Blender."""
    global shader, active_object, active_group_name

    if not valid_tool_idnames:
        return
    try:
        tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
        if tool.idname not in valid_tool_idnames:
            return
    except Exception:
        return

    obj = bpy.context.active_object
    if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
        return
    active_object = obj

    if shader is None:
        shader = gpu.shader.from_builtin('POINT_UNIFORM_COLOR')

    # Rebuild batch every frame so edits are reflected immediately
    selected_pos, unselected_pos = get_vertex_attribute_positions(active_object, active_group_name)
    if not selected_pos and not unselected_pos:
        return

    gpu.state.point_size_set(POINT_SIZE)
    gpu.state.blend_set('ALPHA')
    shader.bind()

    if unselected_pos:
        batch = batch_for_shader(shader, 'POINTS', {"pos": [p[:] for p in unselected_pos]})
        wire_color = bpy.context.preferences.themes[0].view_3d.wire_edit
        shader.uniform_float("color", (*wire_color, 1.0))
        batch.draw(shader)

    if selected_pos:
        batch = batch_for_shader(shader, 'POINTS', {"pos": [p[:] for p in selected_pos]})
        sel_color = bpy.context.preferences.themes[0].view_3d.vertex_select
        shader.uniform_float("color", (*sel_color, 1.0))
        batch.draw(shader)

    gpu.state.blend_set('NONE')


class MESH_OT_vertex_attribute_overlay(bpy.types.Operator):
    """Toggle vertex attribute overlay visualization"""
    bl_idname = "mesh.vertex_attribute_overlay"
    bl_label = "Vertex Attribute Overlay"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def execute(self, context):
        global draw_handler, shader, active_object, active_group_name

        # If already running, remove the handler
        if draw_handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
            draw_handler = None
            shader = None
            active_object = None
            active_group_name = None
            self.report({'INFO'}, "Overlay disabled")
            return {'FINISHED'}

        obj = context.active_object
        group_name = "Endpoints"

        # Validate that the attribute exists before enabling
        selected, unselected = get_vertex_attribute_positions(obj, group_name)
        if not selected and not unselected:
            self.report({'WARNING'}, f"No vertices found in group '{group_name}'")
            return {'CANCELLED'}

        active_object = obj
        active_group_name = group_name
        shader = gpu.shader.from_builtin('POINT_UNIFORM_COLOR')

        draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback, (), 'WINDOW', 'POST_VIEW'
        )

        context.area.tag_redraw()
        self.report({'INFO'}, f"Overlay enabled for '{group_name}' ({len(selected) + len(unselected)} vertices)")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MESH_OT_vertex_attribute_overlay)


def unregister():
    global draw_handler, active_object, active_group_name

    if draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
        active_object = None
        active_group_name = None

    bpy.utils.unregister_class(MESH_OT_vertex_attribute_overlay)