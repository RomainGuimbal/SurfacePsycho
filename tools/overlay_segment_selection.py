import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from mathutils import Vector
import numpy as np
import colorsys

shader = None
active_tool_idname = ""  # set by toolbar_tools

# Absolute mouse coords (window-relative), updated by the MOUSEMOVE keymap operator
_mouse_abs_x = 0
_mouse_abs_y = 0
_mouse_moved = False   # set True by MOUSEMOVE operator, consumed by draw_callback
_hovered_object = None  # last successfully raycasted object; kept during view rotation

LINE_WIDTH = 3.0
_NUM_COLORS = 32

_addon_keymaps = []


def _generate_colors(n):
    colors = []
    golden_ratio = 0.618033988749895
    h = 0.12
    for _ in range(n):
        h = (h + golden_ratio) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, 0.9, 1.0)
        colors.append((r, g, b, 1.0))
    return colors


_SEGMENT_COLORS = _generate_colors(_NUM_COLORS)


def get_edges_by_segment(obj, depsgraph):
    if obj is None or obj.type != 'MESH':
        return {}

    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.data
    if "segment_id" not in mesh.attributes:
        return {}

    n_verts = len(mesh.vertices)
    n_edges = len(mesh.edges)
    if n_verts == 0 or n_edges == 0:
        return {}

    mat = obj.matrix_world

    pos = np.zeros(n_verts * 3, dtype=np.float64)
    mesh.attributes["position"].data.foreach_get("vector", pos)
    pos = pos.reshape((-1, 3))

    pos_w = np.array([(mat @ Vector(p))[:] for p in pos], dtype=np.float32)

    seg_ids = np.zeros(n_edges, dtype=np.int32)
    mesh.attributes["segment_id"].data.foreach_get("value", seg_ids)

    edge_vi = np.zeros(n_edges * 2, dtype=np.int32)
    mesh.edges.foreach_get("vertices", edge_vi)
    edge_vi = edge_vi.reshape((-1, 2))

    # boundary edges: appear in exactly one face loop
    n_loops = len(mesh.loops)
    loop_edge_idx = np.zeros(n_loops, dtype=np.int32)
    mesh.loops.foreach_get("edge_index", loop_edge_idx)
    edge_face_count = np.bincount(loop_edge_idx, minlength=n_edges)
    boundary_mask = edge_face_count == 1

    result = {}
    for i in range(n_edges):
        if not boundary_mask[i]:
            continue
        sid = int(seg_ids[i])
        if sid not in result:
            result[sid] = []
        result[sid].append(tuple(pos_w[edge_vi[i, 0]]))
        result[sid].append(tuple(pos_w[edge_vi[i, 1]]))

    return result


class VIEW3D_OT_segment_update_mouse(bpy.types.Operator):
    """Internal: records mouse position for the segment ID overlay."""
    bl_idname = "view3d.segment_update_mouse"
    bl_label = "Segment Update Mouse"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        global _mouse_abs_x, _mouse_abs_y, _mouse_moved
        _mouse_abs_x = event.mouse_x
        _mouse_abs_y = event.mouse_y
        _mouse_moved = True
        if context.area:
            context.area.tag_redraw()
        return {'FINISHED'}



def draw_callback():
    global shader, _mouse_moved, _hovered_object

    if bpy.context.mode != 'OBJECT':
        return

    try:
        tool = bpy.context.workspace.tools.from_space_view3d_mode('OBJECT')
    except Exception:
        return

    if tool is None or tool.idname != active_tool_idname:
        return

    # Only raycast when mouse actually moved (MOUSEMOVE operator fired)
    # Otherwise reuse last hovered object so overlay persists during view rotation
    if _mouse_moved:
        _mouse_moved = False
        region = bpy.context.region
        rv3d = bpy.context.region_data
        if region is None or rv3d is None:
            pass
        else:
            mouse_region_x = _mouse_abs_x - region.x
            mouse_region_y = _mouse_abs_y - region.y
            try:
                depsgraph = bpy.context.evaluated_depsgraph_get()
                ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (mouse_region_x, mouse_region_y))
                ray_direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, (mouse_region_x, mouse_region_y))
                hit, _, _, _, obj, _ = bpy.context.scene.ray_cast(
                    depsgraph, ray_origin, ray_direction
                )
                _hovered_object = obj if hit else None
            except Exception:
                pass

    hovered = _hovered_object
    if hovered is None:
        return

    try:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        edges_by_seg = get_edges_by_segment(hovered, depsgraph)
    except ReferenceError:
        _hovered_object = None
        return

    if not edges_by_seg:
        return

    if shader is None:
        shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')

    viewport = gpu.state.viewport_get()
    viewport_size = (float(viewport[2]), float(viewport[3]))

    gpu.state.blend_set('ALPHA')
    gpu.state.depth_test_set('NONE')
    shader.bind()
    shader.uniform_float("viewportSize", viewport_size)
    shader.uniform_float("lineWidth", LINE_WIDTH)

    for seg_id, positions in edges_by_seg.items():
        color = _SEGMENT_COLORS[seg_id % _NUM_COLORS]
        batch = batch_for_shader(shader, 'LINES', {"pos": positions})
        shader.uniform_float("color", color)
        batch.draw(shader)

    gpu.state.blend_set('NONE')
    gpu.state.depth_test_set('LESS_EQUAL')


def register():
    bpy.utils.register_class(VIEW3D_OT_segment_update_mouse)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            VIEW3D_OT_segment_update_mouse.bl_idname, 'MOUSEMOVE', 'ANY'
        )
        _addon_keymaps.append((km, kmi))


def unregister():
    global shader
    shader = None
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
    bpy.utils.unregister_class(VIEW3D_OT_segment_update_mouse)
