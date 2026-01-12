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

bl_info = {
    "name": "Surface Psycho",
    "author": "Romain Guimbal",
    "version": (0, 9, 1),
    "blender": (5, 0, 0),
    "description": "Precision Surface Design",
    "warning": "Alpha",
    "doc_url": "https://github.com/RomainGuimbal/SurfacePsycho/wiki",
    "category": "3D View",
    "location": "View3D > Add > Surface/Curve  |  Viewport > N Panel > Tool",
}

import bpy
from .common import gui
import time
# start_time = time.time()

class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("object.sp_add_library", text="Add Assets Path")

def register():
    gui.register()
    bpy.utils.register_class(SP_AddonPreferences)
    # print("--- %s seconds ---" % (time.time() - start_time))


def unregister():
    bpy.utils.unregister_class(SP_AddonPreferences)
    gui.unregister()


if __package__ == "__main__":
    register()