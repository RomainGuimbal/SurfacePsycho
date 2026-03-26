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
        print(f"[seg_overlay] get_edges_by_segment: skip — not a mesh ({obj})")
        return {}

    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.data
    attr_names = list(mesh.attributes.keys())
    if "segment_id" not in mesh.attributes:
        print(f"[seg_overlay] get_edges_by_segment: no 'segment_id' on {obj.name!r}. Attributes: {attr_names}")
        return {}

    attr = mesh.attributes["segment_id"]
    print(f"[seg_overlay] get_edges_by_segment: found segment_id on {obj.name!r}, domain={attr.domain!r}, type={attr.data_type!r}")

    n_verts = len(mesh.vertices)
    n_edges = len(mesh.edges)
    print(f"[seg_overlay] get_edges_by_segment: {n_verts} verts, {n_edges} edges")
    if n_verts == 0 or n_edges == 0:
        return {}

    mat = obj.matrix_world

    pos = np.zeros(n_verts * 3, dtype=np.float64)
    mesh.attributes["position"].data.foreach_get("vector", pos)
    pos = pos.reshape((-1, 3))

    pos_w = np.array([(mat @ Vector(p))[:] for p in pos], dtype=np.float32)

    seg_ids = np.zeros(n_edges, dtype=np.int32)
    mesh.attributes["segment_id"].data.foreach_get("value", seg_ids)
    print(f"[seg_overlay] get_edges_by_segment: seg_ids sample={seg_ids[:10]}, unique={np.unique(seg_ids)}")

    edge_vi = np.zeros(n_edges * 2, dtype=np.int32)
    mesh.edges.foreach_get("vertices", edge_vi)
    edge_vi = edge_vi.reshape((-1, 2))

    result = {}
    for i in range(n_edges):
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
        global _mouse_abs_x, _mouse_abs_y
        prev = (_mouse_abs_x, _mouse_abs_y)
        _mouse_abs_x = event.mouse_x
        _mouse_abs_y = event.mouse_y
        if prev == (0, 0):
            print(f"[seg_overlay] MOUSEMOVE operator FIRST FIRE: ({_mouse_abs_x},{_mouse_abs_y})")
        return {'FINISHED'}


_draw_call_count = 0

def draw_callback():
    global shader, _draw_call_count

    _draw_call_count += 1
    verbose = (_draw_call_count % 60 == 1)  # print once per ~60 redraws

    if verbose:
        print(f"[seg_overlay] draw_callback called (#{_draw_call_count}), mode={bpy.context.mode!r}")

    if bpy.context.mode != 'OBJECT':
        return

    try:
        tool = bpy.context.workspace.tools.from_space_view3d_mode('OBJECT')
    except Exception as e:
        print(f"[seg_overlay] from_space_view3d_mode ERROR: {e}")
        return

    if verbose:
        print(f"[seg_overlay] tool={tool!r}, idname={tool.idname if tool else None!r}, expected={active_tool_idname!r}")

    if tool is None or tool.idname != active_tool_idname:
        return

    region = bpy.context.region
    rv3d = bpy.context.region_data
    if region is None or rv3d is None:
        print(f"[seg_overlay] region or rv3d is None: region={region}, rv3d={rv3d}")
        return

    mouse_region_x = _mouse_abs_x - region.x
    mouse_region_y = _mouse_abs_y - region.y

    if verbose:
        print(f"[seg_overlay] mouse abs=({_mouse_abs_x},{_mouse_abs_y})  region=({region.x},{region.y})  relative=({mouse_region_x},{mouse_region_y})")

    try:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (mouse_region_x, mouse_region_y))
        ray_direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, (mouse_region_x, mouse_region_y))
        hit, _, _, _, obj, _ = bpy.context.scene.ray_cast(
            depsgraph, ray_origin, ray_direction
        )
        hovered = obj if hit else None
    except Exception as e:
        print(f"[seg_overlay] ray_cast ERROR: {e}")
        return

    if verbose:
        print(f"[seg_overlay] ray_cast hit={hit}, hovered={hovered.name if hovered else None!r}")

    if hovered is None:
        return

    edges_by_seg = get_edges_by_segment(hovered, depsgraph)
    if verbose:
        print(f"[seg_overlay] edges_by_seg segments={list(edges_by_seg.keys())}")

    if not edges_by_seg:
        return

    if shader is None:
        shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
        print(f"[seg_overlay] shader created: {shader}")

    viewport = gpu.state.viewport_get()
    viewport_size = (float(viewport[2]), float(viewport[3]))

    if verbose:
        print(f"[seg_overlay] drawing {len(edges_by_seg)} segments, viewport={viewport_size}")

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
    print(f"[seg_overlay] register() called — operator registered")
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            VIEW3D_OT_segment_update_mouse.bl_idname, 'MOUSEMOVE', 'ANY'
        )
        _addon_keymaps.append((km, kmi))
        print(f"[seg_overlay] MOUSEMOVE keymap item registered: {kmi}")
    else:
        print(f"[seg_overlay] WARNING: keyconfigs.addon is None — keymap NOT registered")


def unregister():
    global shader
    shader = None
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
    bpy.utils.unregister_class(VIEW3D_OT_segment_update_mouse)
