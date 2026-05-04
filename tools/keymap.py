OBJ_KEYMAP = (
    ("view3d.segment_select_click", {"type": "LEFTMOUSE", "value": "PRESS"}, None),
    (
        "view3d.segment_select_click",
        {"type": "LEFTMOUSE", "value": "PRESS", "shift": True},
        None,
    ),
    ("object.sp_blend_surfaces", {"type": "B", "value": "PRESS", "ctrl": True}, None),
    ("object.sp_toggle_control_geom", {"type": "V", "value": "PRESS"}, None),
    ("object.sp_extract_segment", {"type": "E", "value": "PRESS"}, None),
    # ("wm.call_menu_pie", {"type": "F", "value": "PRESS", "shift": True}, None),
    ("object.sp_toggle_control_geom", {"type": "F", "value": "PRESS", "shift": True}, None),
)

EDIT_KEYMAP = (
    ("wm.call_menu_pie", {"type": "F", "value": "PRESS", "shift": True}, {"properties": [("name", "SP_MT_PIE_SegmentEdit")]}),
)