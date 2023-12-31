# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
OSD module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_osd.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_OSD')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_OSD')
    _OSD = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_OSD', [dirname(__file__)])
        except ImportError:
            import _OSD
            return _OSD
        try:
            _mod = imp.load_module('_OSD', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _OSD = swig_import_helper()
    del swig_import_helper
else:
    import _OSD
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _OSD.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _OSD.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _OSD.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _OSD.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _OSD.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _OSD.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _OSD.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _OSD.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _OSD.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _OSD.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _OSD.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _OSD.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _OSD.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _OSD.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _OSD.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _OSD.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _OSD.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _OSD.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)


def _dumps_object(klass):
    """ Overwrite default string output for any wrapped object.
    By default, __repr__ method returns something like:
    <OCC.Core.TopoDS.TopoDS_Shape; proxy of <Swig Object of type 'TopoDS_Shape *' at 0x02BB0758> >
    This is too much verbose.
    We prefer :
    <class 'gp_Pnt'>
    or
    <class 'TopoDS_Shape'>
    """
    klass_name = str(klass.__class__).split(".")[3].split("'")[0]
    repr_string = "<class '" + klass_name + "'"
# for TopoDS_Shape, we also look for the base type
    if klass_name == "TopoDS_Shape":
        if klass.IsNull():
            repr_string += ": Null>"
            return repr_string
        st = klass.ShapeType()
        types = {OCC.Core.TopAbs.TopAbs_VERTEX: "Vertex",
                 OCC.Core.TopAbs.TopAbs_SOLID: "Solid",
                 OCC.Core.TopAbs.TopAbs_EDGE: "Edge",
                 OCC.Core.TopAbs.TopAbs_FACE: "Face",
                 OCC.Core.TopAbs.TopAbs_SHELL: "Shell",
                 OCC.Core.TopAbs.TopAbs_WIRE: "Wire",
                 OCC.Core.TopAbs.TopAbs_COMPOUND: "Compound",
                 OCC.Core.TopAbs.TopAbs_COMPSOLID: "Compsolid"}
        repr_string += "; Type:%s" % types[st]        
    elif hasattr(klass, "IsNull"):
        if klass.IsNull():
            repr_string += "; Null"
    repr_string += ">"
    return repr_string


def process_exception(error: 'Standard_Failure', method_name: 'std::string', class_name: 'std::string') -> "void":
    return _OSD.process_exception(error, method_name, class_name)
process_exception = _OSD.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TCollection

from enum import IntEnum
from OCC.Core.Exception import *

OSD_NoLock = _OSD.OSD_NoLock
OSD_ReadLock = _OSD.OSD_ReadLock
OSD_WriteLock = _OSD.OSD_WriteLock
OSD_ExclusiveLock = _OSD.OSD_ExclusiveLock
OSD_RTLD_LAZY = _OSD.OSD_RTLD_LAZY
OSD_RTLD_NOW = _OSD.OSD_RTLD_NOW
OSD_ReadOnly = _OSD.OSD_ReadOnly
OSD_WriteOnly = _OSD.OSD_WriteOnly
OSD_ReadWrite = _OSD.OSD_ReadWrite
OSD_Unavailable = _OSD.OSD_Unavailable
OSD_SUN = _OSD.OSD_SUN
OSD_DEC = _OSD.OSD_DEC
OSD_SGI = _OSD.OSD_SGI
OSD_NEC = _OSD.OSD_NEC
OSD_MAC = _OSD.OSD_MAC
OSD_PC = _OSD.OSD_PC
OSD_HP = _OSD.OSD_HP
OSD_IBM = _OSD.OSD_IBM
OSD_VAX = _OSD.OSD_VAX
OSD_LIN = _OSD.OSD_LIN
OSD_AIX = _OSD.OSD_AIX
OSD_WDirectory = _OSD.OSD_WDirectory
OSD_WDirectoryIterator = _OSD.OSD_WDirectoryIterator
OSD_WEnvironment = _OSD.OSD_WEnvironment
OSD_WFile = _OSD.OSD_WFile
OSD_WFileNode = _OSD.OSD_WFileNode
OSD_WFileIterator = _OSD.OSD_WFileIterator
OSD_WPath = _OSD.OSD_WPath
OSD_WProcess = _OSD.OSD_WProcess
OSD_WProtection = _OSD.OSD_WProtection
OSD_WHost = _OSD.OSD_WHost
OSD_WDisk = _OSD.OSD_WDisk
OSD_WChronometer = _OSD.OSD_WChronometer
OSD_WTimer = _OSD.OSD_WTimer
OSD_WPackage = _OSD.OSD_WPackage
OSD_WEnvironmentIterator = _OSD.OSD_WEnvironmentIterator
OSD_Unknown = _OSD.OSD_Unknown
OSD_Default = _OSD.OSD_Default
OSD_UnixBSD = _OSD.OSD_UnixBSD
OSD_UnixSystemV = _OSD.OSD_UnixSystemV
OSD_VMS = _OSD.OSD_VMS
OSD_OS2 = _OSD.OSD_OS2
OSD_OSF = _OSD.OSD_OSF
OSD_MacOs = _OSD.OSD_MacOs
OSD_Taligent = _OSD.OSD_Taligent
OSD_WindowsNT = _OSD.OSD_WindowsNT
OSD_LinuxREDHAT = _OSD.OSD_LinuxREDHAT
OSD_Aix = _OSD.OSD_Aix
OSD_FILE = _OSD.OSD_FILE
OSD_DIRECTORY = _OSD.OSD_DIRECTORY
OSD_LINK = _OSD.OSD_LINK
OSD_SOCKET = _OSD.OSD_SOCKET
OSD_UNKNOWN = _OSD.OSD_UNKNOWN
OSD_SignalMode_AsIs = _OSD.OSD_SignalMode_AsIs
OSD_SignalMode_Set = _OSD.OSD_SignalMode_Set
OSD_SignalMode_SetUnhandled = _OSD.OSD_SignalMode_SetUnhandled
OSD_SignalMode_Unset = _OSD.OSD_SignalMode_Unset
OSD_FromBeginning = _OSD.OSD_FromBeginning
OSD_FromHere = _OSD.OSD_FromHere
OSD_FromEnd = _OSD.OSD_FromEnd
OSD_None = _OSD.OSD_None
OSD_R = _OSD.OSD_R
OSD_W = _OSD.OSD_W
OSD_RW = _OSD.OSD_RW
OSD_X = _OSD.OSD_X
OSD_RX = _OSD.OSD_RX
OSD_WX = _OSD.OSD_WX
OSD_RWX = _OSD.OSD_RWX
OSD_D = _OSD.OSD_D
OSD_RD = _OSD.OSD_RD
OSD_WD = _OSD.OSD_WD
OSD_RWD = _OSD.OSD_RWD
OSD_XD = _OSD.OSD_XD
OSD_RXD = _OSD.OSD_RXD
OSD_WXD = _OSD.OSD_WXD
OSD_RWXD = _OSD.OSD_RWXD


class OSD_LockType(IntEnum):
	OSD_NoLock = 0
	OSD_ReadLock = 1
	OSD_WriteLock = 2
	OSD_ExclusiveLock = 3
OSD_NoLock = OSD_LockType.OSD_NoLock
OSD_ReadLock = OSD_LockType.OSD_ReadLock
OSD_WriteLock = OSD_LockType.OSD_WriteLock
OSD_ExclusiveLock = OSD_LockType.OSD_ExclusiveLock

class OSD_LoadMode(IntEnum):
	OSD_RTLD_LAZY = 0
	OSD_RTLD_NOW = 1
OSD_RTLD_LAZY = OSD_LoadMode.OSD_RTLD_LAZY
OSD_RTLD_NOW = OSD_LoadMode.OSD_RTLD_NOW

class OSD_OpenMode(IntEnum):
	OSD_ReadOnly = 0
	OSD_WriteOnly = 1
	OSD_ReadWrite = 2
OSD_ReadOnly = OSD_OpenMode.OSD_ReadOnly
OSD_WriteOnly = OSD_OpenMode.OSD_WriteOnly
OSD_ReadWrite = OSD_OpenMode.OSD_ReadWrite

class OSD_OEMType(IntEnum):
	OSD_Unavailable = 0
	OSD_SUN = 1
	OSD_DEC = 2
	OSD_SGI = 3
	OSD_NEC = 4
	OSD_MAC = 5
	OSD_PC = 6
	OSD_HP = 7
	OSD_IBM = 8
	OSD_VAX = 9
	OSD_LIN = 10
	OSD_AIX = 11
OSD_Unavailable = OSD_OEMType.OSD_Unavailable
OSD_SUN = OSD_OEMType.OSD_SUN
OSD_DEC = OSD_OEMType.OSD_DEC
OSD_SGI = OSD_OEMType.OSD_SGI
OSD_NEC = OSD_OEMType.OSD_NEC
OSD_MAC = OSD_OEMType.OSD_MAC
OSD_PC = OSD_OEMType.OSD_PC
OSD_HP = OSD_OEMType.OSD_HP
OSD_IBM = OSD_OEMType.OSD_IBM
OSD_VAX = OSD_OEMType.OSD_VAX
OSD_LIN = OSD_OEMType.OSD_LIN
OSD_AIX = OSD_OEMType.OSD_AIX

class OSD_WhoAmI(IntEnum):
	OSD_WDirectory = 0
	OSD_WDirectoryIterator = 1
	OSD_WEnvironment = 2
	OSD_WFile = 3
	OSD_WFileNode = 4
	OSD_WFileIterator = 5
	OSD_WPath = 6
	OSD_WProcess = 7
	OSD_WProtection = 8
	OSD_WHost = 9
	OSD_WDisk = 10
	OSD_WChronometer = 11
	OSD_WTimer = 12
	OSD_WPackage = 13
	OSD_WEnvironmentIterator = 14
OSD_WDirectory = OSD_WhoAmI.OSD_WDirectory
OSD_WDirectoryIterator = OSD_WhoAmI.OSD_WDirectoryIterator
OSD_WEnvironment = OSD_WhoAmI.OSD_WEnvironment
OSD_WFile = OSD_WhoAmI.OSD_WFile
OSD_WFileNode = OSD_WhoAmI.OSD_WFileNode
OSD_WFileIterator = OSD_WhoAmI.OSD_WFileIterator
OSD_WPath = OSD_WhoAmI.OSD_WPath
OSD_WProcess = OSD_WhoAmI.OSD_WProcess
OSD_WProtection = OSD_WhoAmI.OSD_WProtection
OSD_WHost = OSD_WhoAmI.OSD_WHost
OSD_WDisk = OSD_WhoAmI.OSD_WDisk
OSD_WChronometer = OSD_WhoAmI.OSD_WChronometer
OSD_WTimer = OSD_WhoAmI.OSD_WTimer
OSD_WPackage = OSD_WhoAmI.OSD_WPackage
OSD_WEnvironmentIterator = OSD_WhoAmI.OSD_WEnvironmentIterator

class OSD_SysType(IntEnum):
	OSD_Unknown = 0
	OSD_Default = 1
	OSD_UnixBSD = 2
	OSD_UnixSystemV = 3
	OSD_VMS = 4
	OSD_OS2 = 5
	OSD_OSF = 6
	OSD_MacOs = 7
	OSD_Taligent = 8
	OSD_WindowsNT = 9
	OSD_LinuxREDHAT = 10
	OSD_Aix = 11
OSD_Unknown = OSD_SysType.OSD_Unknown
OSD_Default = OSD_SysType.OSD_Default
OSD_UnixBSD = OSD_SysType.OSD_UnixBSD
OSD_UnixSystemV = OSD_SysType.OSD_UnixSystemV
OSD_VMS = OSD_SysType.OSD_VMS
OSD_OS2 = OSD_SysType.OSD_OS2
OSD_OSF = OSD_SysType.OSD_OSF
OSD_MacOs = OSD_SysType.OSD_MacOs
OSD_Taligent = OSD_SysType.OSD_Taligent
OSD_WindowsNT = OSD_SysType.OSD_WindowsNT
OSD_LinuxREDHAT = OSD_SysType.OSD_LinuxREDHAT
OSD_Aix = OSD_SysType.OSD_Aix

class OSD_KindFile(IntEnum):
	OSD_FILE = 0
	OSD_DIRECTORY = 1
	OSD_LINK = 2
	OSD_SOCKET = 3
	OSD_UNKNOWN = 4
OSD_FILE = OSD_KindFile.OSD_FILE
OSD_DIRECTORY = OSD_KindFile.OSD_DIRECTORY
OSD_LINK = OSD_KindFile.OSD_LINK
OSD_SOCKET = OSD_KindFile.OSD_SOCKET
OSD_UNKNOWN = OSD_KindFile.OSD_UNKNOWN

class OSD_SignalMode(IntEnum):
	OSD_SignalMode_AsIs = 0
	OSD_SignalMode_Set = 1
	OSD_SignalMode_SetUnhandled = 2
	OSD_SignalMode_Unset = 3
OSD_SignalMode_AsIs = OSD_SignalMode.OSD_SignalMode_AsIs
OSD_SignalMode_Set = OSD_SignalMode.OSD_SignalMode_Set
OSD_SignalMode_SetUnhandled = OSD_SignalMode.OSD_SignalMode_SetUnhandled
OSD_SignalMode_Unset = OSD_SignalMode.OSD_SignalMode_Unset

class OSD_FromWhere(IntEnum):
	OSD_FromBeginning = 0
	OSD_FromHere = 1
	OSD_FromEnd = 2
OSD_FromBeginning = OSD_FromWhere.OSD_FromBeginning
OSD_FromHere = OSD_FromWhere.OSD_FromHere
OSD_FromEnd = OSD_FromWhere.OSD_FromEnd

class OSD_SingleProtection(IntEnum):
	OSD_None = 0
	OSD_R = 1
	OSD_W = 2
	OSD_RW = 3
	OSD_X = 4
	OSD_RX = 5
	OSD_WX = 6
	OSD_RWX = 7
	OSD_D = 8
	OSD_RD = 9
	OSD_WD = 10
	OSD_RWD = 11
	OSD_XD = 12
	OSD_RXD = 13
	OSD_WXD = 14
	OSD_RWXD = 15
OSD_None = OSD_SingleProtection.OSD_None
OSD_R = OSD_SingleProtection.OSD_R
OSD_W = OSD_SingleProtection.OSD_W
OSD_RW = OSD_SingleProtection.OSD_RW
OSD_X = OSD_SingleProtection.OSD_X
OSD_RX = OSD_SingleProtection.OSD_RX
OSD_WX = OSD_SingleProtection.OSD_WX
OSD_RWX = OSD_SingleProtection.OSD_RWX
OSD_D = OSD_SingleProtection.OSD_D
OSD_RD = OSD_SingleProtection.OSD_RD
OSD_WD = OSD_SingleProtection.OSD_WD
OSD_RWD = OSD_SingleProtection.OSD_RWD
OSD_XD = OSD_SingleProtection.OSD_XD
OSD_RXD = OSD_SingleProtection.OSD_RXD
OSD_WXD = OSD_SingleProtection.OSD_WXD
OSD_RWXD = OSD_SingleProtection.OSD_RWXD


@classnotwrapped
class OSD_Timer:
	pass

@classnotwrapped
class OSD_PerfMeter:
	pass

@classnotwrapped
class OSD_Disk:
	pass

@classnotwrapped
class OSD_Protection:
	pass

@classnotwrapped
class OSD_MemInfo:
	pass

@classnotwrapped
class OSD_DirectoryIterator:
	pass

@classnotwrapped
class OSD_Chronometer:
	pass

@classnotwrapped
class OSD_ThreadPool:
	pass

@classnotwrapped
class OSD_SharedLibrary:
	pass

@classnotwrapped
class OSD_Error:
	pass

@classnotwrapped
class OSD_Host:
	pass

@classnotwrapped
class OSD_Parallel:
	pass

@classnotwrapped
class OSD_Directory:
	pass

@classnotwrapped
class OSD_Path:
	pass

@classnotwrapped
class OSD_Process:
	pass

@classnotwrapped
class OSD_MAllocHook:
	pass

@classnotwrapped
class OSD_FileNode:
	pass

@classnotwrapped
class OSD_File:
	pass

@classnotwrapped
class OSD_FileIterator:
	pass

@classnotwrapped
class OSD_Thread:
	pass

@classnotwrapped
class OSD_Environment:
	pass

@classnotwrapped
class OSD:
	pass




# This file is compatible with both classic and new-style classes.


