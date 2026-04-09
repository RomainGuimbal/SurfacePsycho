import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from mathutils import Vector
import numpy as np

shader = None
active_tool_idname = ""  # set by toolbar_tools

# Absolute mouse coords (window-relative), updated by the MOUSEMOVE keymap operator
_mouse_abs_x = 0
_mouse_abs_y = 0
_mouse_region_x = 0
_mouse_region_y = 0
_hovered_object = None  # object under cursor, updated by the MOUSEMOVE operator via view3d.select

LINE_WIDTH = 3.0
_HOVER_COLOR = (0.8, 0.5, 0.0, 1.0)
_WHITE = (1.0, 1.0, 1.0, 1.0)

# Selection: set of (obj_name, segment_id) tuples
SELECTED_SEGMENTS = set()

# The segment id closest to the cursor on the hovered object, updated each draw
_hovered_sid = None

_addon_keymaps = []

# Declared here so toolbar_tools.py can assign them to bl_keymap on the tool class.
# Blender activates these only while the tool is the active workspace tool.
TOOL_KEYMAP = (
    ("view3d.segment_select_click", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
    ("view3d.segment_select_click", {"type": 'LEFTMOUSE', "value": 'PRESS', "shift": True}, None),
)


def get_boundary_edge_data(obj, depsgraph):
    """Returns (edges_by_seg, midpoints) for boundary edges.
    edges_by_seg: {segment_id: [v0, v1, v0, v1, ...]}
    midpoints: [(mid_3d, segment_id), ...]
    """
    if obj is None or obj.type != 'MESH':
        return {}, []

    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.data
    if "segment_id" not in mesh.attributes:
        return {}, []

    n_verts = len(mesh.vertices)
    n_edges = len(mesh.edges)
    if n_verts == 0 or n_edges == 0:
        return {}, []

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
    boundary_mask = edge_face_count <= 1

    edges_by_seg = {}
    midpoints = []
    for i in range(n_edges):
        if not boundary_mask[i]:
            continue
        sid = int(seg_ids[i])
        v0 = pos_w[edge_vi[i, 0]]
        v1 = pos_w[edge_vi[i, 1]]
        if sid not in edges_by_seg:
            edges_by_seg[sid] = []
        edges_by_seg[sid].append(tuple(v0))
        edges_by_seg[sid].append(tuple(v1))
        mid = (
            (float(v0[0]) + float(v1[0])) * 0.5,
            (float(v0[1]) + float(v1[1])) * 0.5,
            (float(v0[2]) + float(v1[2])) * 0.5,
        )
        midpoints.append((mid, sid))

    return edges_by_seg, midpoints


class VIEW3D_OT_segment_update_mouse(bpy.types.Operator):
    """Internal: records mouse position for the segment ID overlay."""
    bl_idname = "view3d.segment_update_mouse"
    bl_label = "Segment Update Mouse"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        global _mouse_abs_x, _mouse_abs_y, _mouse_region_x, _mouse_region_y, _hovered_object
        _mouse_abs_x = event.mouse_x
        _mouse_abs_y = event.mouse_y

        region = context.region
        if region is not None:
            _mouse_region_x = event.mouse_x - region.x
            _mouse_region_y = event.mouse_y - region.y

        if context.mode == 'OBJECT':
            try:
                tool = context.workspace.tools.from_space_view3d_mode('OBJECT')
            except Exception:
                tool = None

            if tool is not None and tool.idname == active_tool_idname:
                old_active = context.view_layer.objects.active
                old_selected = list(context.selected_objects)

                select_ran = False
                try:
                    bpy.ops.view3d.select(
                        'EXEC_REGION_WIN',
                        extend=False, deselect=False, toggle=False,
                        center=False, enumerate=False, object=False,
                        location=(_mouse_region_x, _mouse_region_y),
                    )
                    select_ran = True
                except Exception:
                    pass

                if select_ran:
                    picked = context.selected_objects[0] if context.selected_objects else None
                else:
                    picked = None
                _hovered_object = picked

                # Restore original selection state
                if picked is not None:
                    try:
                        picked.select_set(False)
                    except ReferenceError:
                        pass
                for obj in old_selected:
                    try:
                        obj.select_set(True)
                    except ReferenceError:
                        pass
                try:
                    context.view_layer.objects.active = old_active
                except ReferenceError:
                    pass
            else:
                _hovered_object = None

        if context.area:
            context.area.tag_redraw()
        return {'PASS_THROUGH'}


class VIEW3D_OT_segment_select_click(bpy.types.Operator):
    """Internal: toggle segment selection on left click."""
    bl_idname = "view3d.segment_select_click"
    bl_label = "Segment Select Click"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        global SELECTED_SEGMENTS

        try:
            tool = context.workspace.tools.from_space_view3d_mode('OBJECT')
        except Exception:
            return {'PASS_THROUGH'}

        if tool is None or tool.idname != active_tool_idname:
            return {'PASS_THROUGH'}

        if _hovered_object is None or _hovered_sid is None:
            SELECTED_SEGMENTS.clear()
            if context.area:
                context.area.tag_redraw()
            return {'FINISHED'}

        key = (_hovered_object.name, _hovered_sid)
        if event.shift:
            if key in SELECTED_SEGMENTS:
                SELECTED_SEGMENTS.discard(key)
            else:
                SELECTED_SEGMENTS.add(key)
        else:
            SELECTED_SEGMENTS = {key}

        if context.area:
            context.area.tag_redraw()
        return {'FINISHED'}



def draw_callback():
    global shader, _hovered_object, _mouse_region_x, _mouse_region_y, _hovered_sid

    if bpy.context.mode != 'OBJECT':
        return

    try:
        tool = bpy.context.workspace.tools.from_space_view3d_mode('OBJECT')
    except Exception:
        return

    if tool is None or tool.idname != active_tool_idname:
        return

    region = bpy.context.region
    rv3d = bpy.context.region_data
    if region is None or rv3d is None:
        return

    depsgraph = bpy.context.evaluated_depsgraph_get()

    if shader is None:
        shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')

    viewport = gpu.state.viewport_get()
    viewport_size = (float(viewport[2]), float(viewport[3]))

    gpu.state.blend_set('ALPHA')
    gpu.state.depth_test_set('NONE')
    shader.bind()
    shader.uniform_float("viewportSize", viewport_size)
    shader.uniform_float("lineWidth", LINE_WIDTH)

    # Draw selected segments in white, grouped by object to minimise get_boundary_edge_data calls
    if SELECTED_SEGMENTS:
        sids_by_obj_name = {}
        for obj_name, sid in SELECTED_SEGMENTS:
            sids_by_obj_name.setdefault(obj_name, set()).add(sid)

        scene_objects = {obj.name: obj for obj in bpy.context.scene.objects if obj.type == 'MESH'}
        for obj_name, sids in sids_by_obj_name.items():
            obj = scene_objects.get(obj_name)
            if obj is None:
                continue
            try:
                edges_by_seg, _ = get_boundary_edge_data(obj, depsgraph)
            except ReferenceError:
                continue
            for sid in sids:
                if sid not in edges_by_seg:
                    continue
                batch = batch_for_shader(shader, 'LINES', {"pos": edges_by_seg[sid]})
                shader.uniform_float("color", _WHITE)
                batch.draw(shader)

    # Hover detection: find closest segment on the hovered object only.
    _hovered_sid = None
    hovered = _hovered_object
    if hovered is not None:
        try:
            edges_by_seg, midpoints = get_boundary_edge_data(hovered, depsgraph)
        except ReferenceError:
            _hovered_object = None
            edges_by_seg, midpoints = {}, []

        closest_sid = None
        min_dist_sq = float('inf')
        for mid_3d, sid in midpoints:
            p2d = view3d_utils.location_3d_to_region_2d(region, rv3d, Vector(mid_3d))
            if p2d is None:
                continue
            dx = p2d.x - _mouse_region_x
            dy = p2d.y - _mouse_region_y
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_sid = sid

        _hovered_sid = closest_sid
        if closest_sid is not None and closest_sid in edges_by_seg:
            batch = batch_for_shader(shader, 'LINES', {"pos": edges_by_seg[closest_sid]})
            shader.uniform_float("color", _HOVER_COLOR)
            batch.draw(shader)

    gpu.state.blend_set('NONE')
    gpu.state.depth_test_set('LESS_EQUAL')


def register():
    bpy.utils.register_class(VIEW3D_OT_segment_update_mouse)
    bpy.utils.register_class(VIEW3D_OT_segment_select_click)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            VIEW3D_OT_segment_update_mouse.bl_idname, 'MOUSEMOVE', 'ANY', any=True
        )
        _addon_keymaps.append((km, kmi))


def unregister():
    global shader, SELECTED_SEGMENTS, _hovered_sid
    shader = None
    SELECTED_SEGMENTS = set()
    _hovered_sid = None
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
    bpy.utils.unregister_class(VIEW3D_OT_segment_select_click)
    bpy.utils.unregister_class(VIEW3D_OT_segment_update_mouse)
