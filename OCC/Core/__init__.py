PYTHONOCC_VERSION_MAJOR = 7
PYTHONOCC_VERSION_MINOR = 7
PYTHONOCC_VERSION_PATCH = 2

#  Empty for official releases, set to -dev, -rc1, etc for development releases
PYTHONOCC_VERSION_DEVEL = ""

VERSION = f"{PYTHONOCC_VERSION_MAJOR}.{PYTHONOCC_VERSION_MINOR}.{PYTHONOCC_VERSION_PATCH}{PYTHONOCC_VERSION_DEVEL}"


import os
import ctypes
import glob

# Determine the path to the package directory
package_dir = os.path.dirname(__file__)


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# # List all .so, .so.7.7, and .so.7.7.2 files
# so_files = glob.glob(os.path.join(script_dir, '*.so')) \
#         + glob.glob(os.path.join(script_dir, '*.so.7.7')) \
#         + glob.glob(os.path.join(script_dir, '*.so.7.7.2'))

# print([os.path.basename(s) for s in so_files])

shared_libs=('libTKG3d.so.7.7',
             'libTKTopAlgo.so.7.7',
             'libTKMesh.so.7.7',
             'libTKXDEIGES.so.7.7',
             'libTKSTL.so.7.7',
             'libTKSTEP.so.7.7',
             'libTKXDESTEP.so.7.7',
             'libTKRWMesh.so.7.7'
             )


# Load the shared library
for s in shared_libs :
    # print(s)
    lib_path = os.path.join(package_dir,s)
    ctypes.CDLL(lib_path)
