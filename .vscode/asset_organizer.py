import bpy
from os.path import isfile
import subprocess
from pathlib import Path


def append_node_group_to_file(target_filepath, node_group_name):
    source_path = bpy.data.filepath.replace("\\", "/")

    command = [
        "blender",
        "--background",
        target_filepath,
        "--python-expr",
        f"import bpy;\nwith bpy.data.libraries.load('{source_path}', link=False, set_fake=True, recursive=True) as (_, data_to):\n data_to.node_groups = ['{node_group_name}']\nbpy.ops.wm.save_mainfile()",
    ]

    # Run the command
    subprocess.run(command, check=True)


def link_node_group(target_filepath, ng_name: str) -> list[bpy.types.NodeGroup]:
    with bpy.data.libraries.load(target_filepath, link=True) as (_, data_to):
        data_to.node_groups = [ng_name]

    linked_ng = data_to.node_groups[0]
    return linked_ng


def create_file(filepath):
    """Create an empty .blend file at the specified path without affecting the current session or leaving temporary files."""
    # Command to run Blender in the background and execute a Python command directly
    command = [
        "blender",
        "--background",
        "--python-expr",
        f"import bpy; bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.wm.save_as_mainfile(filepath='{filepath}')",
    ]

    # Run the command
    subprocess.run(command, check=True)


def move_ng_to_level_file(ng_name: str, level):
    target_filepath = f"C:/Users/romai/Documents/Projets/26 - Bezier Quest/SP Assets Level {level}.blend"

    # Create file
    if not isfile(target_filepath):
        create_file(target_filepath)

    replaced_ng = bpy.data.node_groups[ng_name]

    append_node_group_to_file(target_filepath, ng_name)
    linked_ng = link_node_group(target_filepath, ng_name)
    if linked_ng is not None:
        replaced_ng.user_remap(linked_ng)
        return True
    return False


class SPO_OT_move_node_group(bpy.types.Operator):
    bl_idname = "wm.spo_move_node_group"
    bl_label = "SPO - Move Node Group"
    bl_options = {"REGISTER", "UNDO"}

    level: bpy.props.IntProperty(
        name="Dependency Level", description="", default=0, min=0
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "NODE_EDITOR"

    def execute(self, context):
        ng_name = context.space_data.edit_tree.nodes.active.node_tree.name
        print(ng_name)
        if move_ng_to_level_file(ng_name, self.level):
            self.report({"INFO"}, f"Node group moved successfully")
        else:
            self.report({"ERROR"}, f"Node group move failed")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "level")

    def invoke(self, context, event):
        # call itself and run
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


classes = [
    SPO_OT_move_node_group,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)


register()

# TODO after a move, must remap in other files which links it too !
# TODO auto find which level : - all contained ng must be at lower levels
# TODO move between level : Must use linking and not append somehow
# TODO auto move all children when a group is upgraded
# TODO de-duplicate utils and stuff

# Level 0 : small utils ----> Level n : end user tools
# SPO "SurfacePsycho Organizer"
