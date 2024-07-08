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
    "version": (0, 6),
    "blender": (4, 1, 0),
    "description": "Surface design for the mechanical industry",
    "warning": "Alpha",
    "doc_url": "https://github.com/RomainGuimbal/SurfacePsycho/wiki",
    "category": "3D View",
    "location": "View3D > Add > Surface/Curve  |  View3D > N Panel > Edit"
}

import sys
from os.path import dirname, abspath
file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

from utils import *
from macros import *
from gui import *