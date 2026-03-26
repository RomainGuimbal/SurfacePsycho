"""
Standalone test: highlights a random half of edges on a randomly picked mesh object.
Run from Blender's Text Editor (or via --python).
Re-run to pick a new random object/edges.
"""

import bpy
import gpu
import random
import numpy as np
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

# ── cleanup any previous handler ─────────────────────────────────────────────
_HANDLER_KEY = "_test_edge_highlight_handler"

prev = getattr(bpy.types.SpaceView3D, _HANDLER_KEY, None)
if prev is not None:
    try:
        bpy.types.SpaceView3D.draw_handler_remove(prev, "WINDOW")
    except Exception:
        pass
    delattr(bpy.types.SpaceView3D, _HANDLER_KEY)

# ── pick a random mesh object ─────────────────────────────────────────────────
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not mesh_objects:
    raise RuntimeError("No mesh objects in scene")

obj = random.choice(mesh_objects)
print(f"[test_edge_highlight] Object: {obj.name!r}, edges: {len(obj.data.edges)}")

# ── collect world-space edge line pairs ───────────────────────────────────────
mesh = obj.data
mat = obj.matrix_world

n_verts = len(mesh.vertices)
n_edges = len(mesh.edges)

pos = np.zeros(n_verts * 3, dtype=np.float64)
mesh.attributes["position"].data.foreach_get("vector", pos)
pos = pos.reshape((-1, 3))

pos_w = np.array([(mat @ Vector(p))[:] for p in pos], dtype=np.float32)

edge_vi = np.zeros(n_edges * 2, dtype=np.int32)
mesh.edges.foreach_get("vertices", edge_vi)
edge_vi = edge_vi.reshape((-1, 2))

# pick a random half
indices = list(range(n_edges))
random.shuffle(indices)
half = indices[: n_edges // 2]

coords = []
for i in half:
    coords.append(tuple(pos_w[edge_vi[i, 0]]))
    coords.append(tuple(pos_w[edge_vi[i, 1]]))

print(f"[test_edge_highlight] Drawing {len(half)} edges ({len(coords)} verts)")

# ── build shader + batch once ─────────────────────────────────────────────────
shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
batch = batch_for_shader(shader, 'LINES', {"pos": coords})

# ── draw callback ─────────────────────────────────────────────────────────────
def draw():
    viewport = gpu.state.viewport_get()
    gpu.state.blend_set('ALPHA')
    gpu.state.depth_test_set('NONE')  # draw on top
    shader.bind()
    shader.uniform_float("viewportSize", (float(viewport[2]), float(viewport[3])))
    shader.uniform_float("lineWidth", 4.0)
    shader.uniform_float("color", (1.0, 0.3, 0.0, 1.0))
    batch.draw(shader)
    gpu.state.blend_set('NONE')
    gpu.state.depth_test_set('LESS_EQUAL')

# ── register ──────────────────────────────────────────────────────────────────
handler = bpy.types.SpaceView3D.draw_handler_add(draw, (), "WINDOW", "POST_VIEW")
setattr(bpy.types.SpaceView3D, _HANDLER_KEY, handler)

# force redraw
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()

print("[test_edge_highlight] Handler registered. Run script again to refresh.")
