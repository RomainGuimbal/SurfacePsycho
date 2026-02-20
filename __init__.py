# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from .config import bl_info
from .common import gui
from .tools import macros
# import time
# start_time = time.time()

class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    matcaps : bpy.props.BoolProperty(
        name = "matcaps installed",
        default= False,
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("wm.sp_add_library", text="Add Assets Path")
        row = col.row(align=True)
        row.label(text="Psycho Matcaps")
        row.operator("wm.sp_add_matcaps", text="Add")
        row.operator("wm.sp_remove_matcaps", text="Remove")


def register():
    macros.register()
    gui.register()
    bpy.utils.register_class(SP_AddonPreferences)
    # print("--- %s seconds ---" % (time.time() - start_time))


def unregister():
    bpy.utils.unregister_class(SP_AddonPreferences)
    gui.unregister()
    macros.unregister()


if __package__ == "__main__":
    register()