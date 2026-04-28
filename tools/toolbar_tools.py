import os
import bpy
from . import overlay_endpoints
from . import overlay_segment_selection
from .keymap import OBJ_KEYMAP, EDIT_KEYMAP

_ICON_NAME = "ops.generic.surface_psycho"
_custom_icon_value = None


def _load_custom_icon():
    global _custom_icon_value
    icon_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "icons", _ICON_NAME + ".dat"
    )
    try:
        _custom_icon_value = bpy.app.icons.new_triangles_from_file(icon_path)
        from bl_ui.space_toolsystem_common import _icon_cache

        _icon_cache[_ICON_NAME] = _custom_icon_value
    except Exception as e:
        print(f"SurfacePsycho: Failed to load custom icon: {e}")
        _custom_icon_value = 0


def _unload_custom_icon():
    global _custom_icon_value
    if _custom_icon_value:
        bpy.app.icons.release(_custom_icon_value)
        from bl_ui.space_toolsystem_common import _icon_cache

        _icon_cache.pop(_ICON_NAME, None)
    _custom_icon_value = None


def _tag_redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def remove_draw_handler():
    overlay_endpoints.active_object = None
    _tag_redraw()


_TOOL_IDNAMES = ["object.sp_mode_tool", "mesh.sp_mode_tool"]
_MODES = ["OBJECT", "EDIT_MESH"]


def _make_tool_class(mode, id_name):
    attrs = {
        "bl_space_type": "VIEW_3D",
        "bl_context_mode": mode,
        "bl_idname": id_name,
        "bl_label": "Psycho Mode",
        "bl_icon": "ops.generic.surface_psycho",
    }
    if mode == "OBJECT":
        attrs["bl_keymap"] = OBJ_KEYMAP
    elif mode == "EDIT_MESH":
        attrs["bl_keymap"] = EDIT_KEYMAP
        
    return type(
        f"SP_mode_tool_{mode}",
        (bpy.types.WorkSpaceTool,),
        attrs,
    )


_tool_classes = []
_endpoints_draw_handler = None
_segment_draw_handler = None

_msgbus_owner = object()


def _on_tool_changed():
    remove_draw_handler()
    return None


def _subscribe_to_tool():
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.WorkSpaceTool, "idname"),
        owner=_msgbus_owner,
        args=(),
        notify=_on_tool_changed,
    )


@bpy.app.handlers.persistent
def _on_load_post(*_):
    _subscribe_to_tool()


def register():
    global _tool_classes, _endpoints_draw_handler, _segment_draw_handler
    _load_custom_icon()
    _tool_classes = [
        _make_tool_class(mode, id_name)
        for mode, id_name in (
            ("OBJECT", "object.sp_mode_tool"),
            ("EDIT_MESH", "mesh.sp_mode_tool"),
        )
    ]
    for i, cls in enumerate(_tool_classes):
        bpy.utils.register_tool(cls, separator=(i == 0))

    # Endpoints overlay
    overlay_endpoints.active_group_name = "Endpoints"
    overlay_endpoints.valid_tool_idnames = set(_TOOL_IDNAMES)
    _endpoints_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        overlay_endpoints.draw_callback, (), "WINDOW", "POST_VIEW"
    )

    # Segment selection overlay
    overlay_segment_selection.active_tool_idname = "object.sp_mode_tool"
    overlay_segment_selection.register()
    _segment_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        overlay_segment_selection.draw_callback, (), "WINDOW", "POST_VIEW"
    )

    _subscribe_to_tool()
    bpy.app.handlers.load_post.append(_on_load_post)


def unregister():
    global _endpoints_draw_handler, _segment_draw_handler
    bpy.app.handlers.load_post.remove(_on_load_post)
    bpy.msgbus.clear_by_owner(_msgbus_owner)

    if _segment_draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_segment_draw_handler, "WINDOW")
    overlay_segment_selection.unregister()
    remove_draw_handler()

    if _endpoints_draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_endpoints_draw_handler, "WINDOW")
        _endpoints_draw_handler = None
        overlay_endpoints.shader = None
        overlay_endpoints.batch = None
        overlay_endpoints.active_group_name = None
        overlay_endpoints.valid_tool_idnames = set()

    for cls in reversed(_tool_classes):
        bpy.utils.unregister_tool(cls)
    _unload_custom_icon()
