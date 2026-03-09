import bpy
import gpu
from . import overlays

# Store the handle so we can remove it later
_draw_handler = None


def _tag_redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def add_draw_handler():
    global _draw_handler
    if _draw_handler is None:
        obj = bpy.context.active_object
        if obj and obj.type == "MESH":
            overlays.active_object = obj
            overlays.active_group_name = "Endpoints"
            overlays.shader = gpu.shader.from_builtin("POINT_UNIFORM_COLOR")
        _draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            overlays.draw_callback, (), "WINDOW", "POST_VIEW"
        )
        _tag_redraw()


def remove_draw_handler():
    global _draw_handler
    if _draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, "WINDOW")
        _draw_handler = None
        overlays.shader = None
        overlays.batch = None
        overlays.active_object = None
        overlays.active_group_name = None
        _tag_redraw()


_TOOL_IDNAMES = ["object.sp_mode_tool", "mesh.sp_mode_tool"]
_MODES = ["OBJECT", "EDIT_MESH"]


def _make_tool_class(mode, id_name):
    return type(
        f"SP_mode_tool_{mode}",
        (bpy.types.WorkSpaceTool,),
        {
            "bl_space_type": "VIEW_3D",
            "bl_context_mode": mode,
            "bl_idname": id_name,
            "bl_label": "Psycho Mode",
            "bl_icon": "ops.generic.select_circle",
            "bl_keymap": (
                ("object.sp_select_all", {"type": "LEFTMOUSE", "value": "CLICK"}, None),
            ),
        },
    )


_tool_classes = []

_last_tool_idname = None


def _poll_tool():
    global _last_tool_idname
    try:
        tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
    except Exception:
        return 0.2

    idname = tool.idname
    if idname != _last_tool_idname:
        _last_tool_idname = idname
        if idname in _TOOL_IDNAMES:
            add_draw_handler()
        else:
            remove_draw_handler()

    return 0.2


def register():
    global _tool_classes
    _tool_classes = [
        _make_tool_class(mode, id_name) for mode, id_name in zip(_MODES, _TOOL_IDNAMES)
    ]
    for i, cls in enumerate(_tool_classes):
        bpy.utils.register_tool(cls, separator=(i == 0))
    bpy.app.timers.register(_poll_tool, persistent=True)


def unregister():
    remove_draw_handler()
    if bpy.app.timers.is_registered(_poll_tool):
        bpy.app.timers.unregister(_poll_tool)
    for cls in reversed(_tool_classes):
        bpy.utils.unregister_tool(cls)
