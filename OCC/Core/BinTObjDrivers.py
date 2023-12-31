# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
BinTObjDrivers module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_bintobjdrivers.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_BinTObjDrivers')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_BinTObjDrivers')
    _BinTObjDrivers = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_BinTObjDrivers', [dirname(__file__)])
        except ImportError:
            import _BinTObjDrivers
            return _BinTObjDrivers
        try:
            _mod = imp.load_module('_BinTObjDrivers', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _BinTObjDrivers = swig_import_helper()
    del swig_import_helper
else:
    import _BinTObjDrivers
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
    __swig_destroy__ = _BinTObjDrivers.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _BinTObjDrivers.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BinTObjDrivers.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BinTObjDrivers.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _BinTObjDrivers.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _BinTObjDrivers.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _BinTObjDrivers.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _BinTObjDrivers.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _BinTObjDrivers.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _BinTObjDrivers.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BinTObjDrivers.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _BinTObjDrivers.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _BinTObjDrivers.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BinTObjDrivers.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BinTObjDrivers.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BinTObjDrivers.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _BinTObjDrivers.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _BinTObjDrivers.SwigPyIterator_swigregister
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
    return _BinTObjDrivers.process_exception(error, method_name, class_name)
process_exception = _BinTObjDrivers.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.BinMDF
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TDF
import OCC.Core.BinObjMgt
import OCC.Core.Storage
import OCC.Core.TDocStd
import OCC.Core.CDF
import OCC.Core.CDM
import OCC.Core.Resource
import OCC.Core.PCDM
import OCC.Core.BinLDrivers

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_BinTObjDrivers_DocumentRetrievalDriver_Create() -> "opencascade::handle< BinTObjDrivers_DocumentRetrievalDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_Create()
Handle_BinTObjDrivers_DocumentRetrievalDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_Create

def Handle_BinTObjDrivers_DocumentRetrievalDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_DocumentRetrievalDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_DownCast(t)
Handle_BinTObjDrivers_DocumentRetrievalDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_DownCast

def Handle_BinTObjDrivers_DocumentRetrievalDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_DocumentRetrievalDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_IsNull(t)
Handle_BinTObjDrivers_DocumentRetrievalDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentRetrievalDriver_IsNull

def Handle_BinTObjDrivers_DocumentStorageDriver_Create() -> "opencascade::handle< BinTObjDrivers_DocumentStorageDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_Create()
Handle_BinTObjDrivers_DocumentStorageDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_Create

def Handle_BinTObjDrivers_DocumentStorageDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_DocumentStorageDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_DownCast(t)
Handle_BinTObjDrivers_DocumentStorageDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_DownCast

def Handle_BinTObjDrivers_DocumentStorageDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_DocumentStorageDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_IsNull(t)
Handle_BinTObjDrivers_DocumentStorageDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_DocumentStorageDriver_IsNull

def Handle_BinTObjDrivers_IntSparseArrayDriver_Create() -> "opencascade::handle< BinTObjDrivers_IntSparseArrayDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_Create()
Handle_BinTObjDrivers_IntSparseArrayDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_Create

def Handle_BinTObjDrivers_IntSparseArrayDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_IntSparseArrayDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_DownCast(t)
Handle_BinTObjDrivers_IntSparseArrayDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_DownCast

def Handle_BinTObjDrivers_IntSparseArrayDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_IntSparseArrayDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_IsNull(t)
Handle_BinTObjDrivers_IntSparseArrayDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_IntSparseArrayDriver_IsNull

def Handle_BinTObjDrivers_ModelDriver_Create() -> "opencascade::handle< BinTObjDrivers_ModelDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_Create()
Handle_BinTObjDrivers_ModelDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_Create

def Handle_BinTObjDrivers_ModelDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_ModelDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_DownCast(t)
Handle_BinTObjDrivers_ModelDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_DownCast

def Handle_BinTObjDrivers_ModelDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_ModelDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_IsNull(t)
Handle_BinTObjDrivers_ModelDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_ModelDriver_IsNull

def Handle_BinTObjDrivers_ObjectDriver_Create() -> "opencascade::handle< BinTObjDrivers_ObjectDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_Create()
Handle_BinTObjDrivers_ObjectDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_Create

def Handle_BinTObjDrivers_ObjectDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_ObjectDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_DownCast(t)
Handle_BinTObjDrivers_ObjectDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_DownCast

def Handle_BinTObjDrivers_ObjectDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_ObjectDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_IsNull(t)
Handle_BinTObjDrivers_ObjectDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_ObjectDriver_IsNull

def Handle_BinTObjDrivers_ReferenceDriver_Create() -> "opencascade::handle< BinTObjDrivers_ReferenceDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_Create()
Handle_BinTObjDrivers_ReferenceDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_Create

def Handle_BinTObjDrivers_ReferenceDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_ReferenceDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_DownCast(t)
Handle_BinTObjDrivers_ReferenceDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_DownCast

def Handle_BinTObjDrivers_ReferenceDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_ReferenceDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_IsNull(t)
Handle_BinTObjDrivers_ReferenceDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_ReferenceDriver_IsNull

def Handle_BinTObjDrivers_XYZDriver_Create() -> "opencascade::handle< BinTObjDrivers_XYZDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_Create()
Handle_BinTObjDrivers_XYZDriver_Create = _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_Create

def Handle_BinTObjDrivers_XYZDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinTObjDrivers_XYZDriver >":
    return _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_DownCast(t)
Handle_BinTObjDrivers_XYZDriver_DownCast = _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_DownCast

def Handle_BinTObjDrivers_XYZDriver_IsNull(t: 'opencascade::handle< BinTObjDrivers_XYZDriver > const &') -> "bool":
    return _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_IsNull(t)
Handle_BinTObjDrivers_XYZDriver_IsNull = _BinTObjDrivers.Handle_BinTObjDrivers_XYZDriver_IsNull
class bintobjdrivers(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, bintobjdrivers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, bintobjdrivers, name)
    __repr__ = _swig_repr

    def AddDrivers(*args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        aDriverTable: BinMDF_ADriverTable
        aMsgDrv: Message_Messenger

        Returns
        -------
        None

        """
        return _BinTObjDrivers.bintobjdrivers_AddDrivers(*args)

    AddDrivers = staticmethod(AddDrivers)

    def DefineFormat(*args) -> "void":
        """
        Defines format 'tobjbin' and registers its read and write drivers in the specified application.

        Parameters
        ----------
        theApp: TDocStd_Application

        Returns
        -------
        None

        """
        return _BinTObjDrivers.bintobjdrivers_DefineFormat(*args)

    DefineFormat = staticmethod(DefineFormat)

    def Factory(*args) -> "opencascade::handle< Standard_Transient > const &":
        """
        No available documentation.

        Parameters
        ----------
        aGUID: Standard_GUID

        Returns
        -------
        opencascade::handle<Standard_Transient>

        """
        return _BinTObjDrivers.bintobjdrivers_Factory(*args)

    Factory = staticmethod(Factory)

    __repr__ = _dumps_object


    def __init__(self):
        this = _BinTObjDrivers.new_bintobjdrivers()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _BinTObjDrivers.delete_bintobjdrivers
    __del__ = lambda self: None
bintobjdrivers_swigregister = _BinTObjDrivers.bintobjdrivers_swigregister
bintobjdrivers_swigregister(bintobjdrivers)

def bintobjdrivers_AddDrivers(*args) -> "void":
    """
    No available documentation.

    Parameters
    ----------
    aDriverTable: BinMDF_ADriverTable
    aMsgDrv: Message_Messenger

    Returns
    -------
    None

    """
    return _BinTObjDrivers.bintobjdrivers_AddDrivers(*args)

def bintobjdrivers_DefineFormat(*args) -> "void":
    """
    Defines format 'tobjbin' and registers its read and write drivers in the specified application.

    Parameters
    ----------
    theApp: TDocStd_Application

    Returns
    -------
    None

    """
    return _BinTObjDrivers.bintobjdrivers_DefineFormat(*args)

def bintobjdrivers_Factory(*args) -> "opencascade::handle< Standard_Transient > const &":
    """
    No available documentation.

    Parameters
    ----------
    aGUID: Standard_GUID

    Returns
    -------
    opencascade::handle<Standard_Transient>

    """
    return _BinTObjDrivers.bintobjdrivers_Factory(*args)

class BinTObjDrivers_DocumentRetrievalDriver(OCC.Core.BinLDrivers.BinLDrivers_DocumentRetrievalDriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinLDrivers.BinLDrivers_DocumentRetrievalDriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_DocumentRetrievalDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinLDrivers.BinLDrivers_DocumentRetrievalDriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_DocumentRetrievalDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_DocumentRetrievalDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this


    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_DocumentRetrievalDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_DocumentRetrievalDriver
    __del__ = lambda self: None
BinTObjDrivers_DocumentRetrievalDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_DocumentRetrievalDriver_swigregister
BinTObjDrivers_DocumentRetrievalDriver_swigregister(BinTObjDrivers_DocumentRetrievalDriver)

class BinTObjDrivers_DocumentStorageDriver(OCC.Core.BinLDrivers.BinLDrivers_DocumentStorageDriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinLDrivers.BinLDrivers_DocumentStorageDriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_DocumentStorageDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinLDrivers.BinLDrivers_DocumentStorageDriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_DocumentStorageDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_DocumentStorageDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this


    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_DocumentStorageDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_DocumentStorageDriver
    __del__ = lambda self: None
BinTObjDrivers_DocumentStorageDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_DocumentStorageDriver_swigregister
BinTObjDrivers_DocumentStorageDriver_swigregister(BinTObjDrivers_DocumentStorageDriver)

class BinTObjDrivers_IntSparseArrayDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_IntSparseArrayDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_IntSparseArrayDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_IntSparseArrayDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Paste(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        theSource: BinObjMgt_Persistent
        theTarget: TDF_Attribute
        theRelocTable: BinObjMgt_RRelocationTable

        Returns
        -------
        bool

        No available documentation.

        Parameters
        ----------
        theSource: TDF_Attribute
        theTarget: BinObjMgt_Persistent
        theRelocTable: BinObjMgt_SRelocationTable

        Returns
        -------
        None

        """
        return _BinTObjDrivers.BinTObjDrivers_IntSparseArrayDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_IntSparseArrayDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_IntSparseArrayDriver
    __del__ = lambda self: None
BinTObjDrivers_IntSparseArrayDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_IntSparseArrayDriver_swigregister
BinTObjDrivers_IntSparseArrayDriver_swigregister(BinTObjDrivers_IntSparseArrayDriver)

class BinTObjDrivers_ModelDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_ModelDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_ModelDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_ModelDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Paste(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Returns
        -------
        bool

        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Returns
        -------
        None

        """
        return _BinTObjDrivers.BinTObjDrivers_ModelDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_ModelDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_ModelDriver
    __del__ = lambda self: None
BinTObjDrivers_ModelDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_ModelDriver_swigregister
BinTObjDrivers_ModelDriver_swigregister(BinTObjDrivers_ModelDriver)

class BinTObjDrivers_ObjectDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_ObjectDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_ObjectDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_ObjectDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Paste(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Returns
        -------
        bool

        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Returns
        -------
        None

        """
        return _BinTObjDrivers.BinTObjDrivers_ObjectDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_ObjectDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_ObjectDriver
    __del__ = lambda self: None
BinTObjDrivers_ObjectDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_ObjectDriver_swigregister
BinTObjDrivers_ObjectDriver_swigregister(BinTObjDrivers_ObjectDriver)

class BinTObjDrivers_ReferenceDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_ReferenceDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_ReferenceDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_ReferenceDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Paste(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Returns
        -------
        bool

        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Returns
        -------
        None

        """
        return _BinTObjDrivers.BinTObjDrivers_ReferenceDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_ReferenceDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_ReferenceDriver
    __del__ = lambda self: None
BinTObjDrivers_ReferenceDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_ReferenceDriver_swigregister
BinTObjDrivers_ReferenceDriver_swigregister(BinTObjDrivers_ReferenceDriver)

class BinTObjDrivers_XYZDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinTObjDrivers_XYZDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinTObjDrivers_XYZDriver, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Returns
        -------
        None

        """
        this = _BinTObjDrivers.new_BinTObjDrivers_XYZDriver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Paste(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        theSource: BinObjMgt_Persistent
        theTarget: TDF_Attribute
        theRelocTable: BinObjMgt_RRelocationTable

        Returns
        -------
        bool

        No available documentation.

        Parameters
        ----------
        theSource: TDF_Attribute
        theTarget: BinObjMgt_Persistent
        theRelocTable: BinObjMgt_SRelocationTable

        Returns
        -------
        None

        """
        return _BinTObjDrivers.BinTObjDrivers_XYZDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinTObjDrivers_XYZDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinTObjDrivers.delete_BinTObjDrivers_XYZDriver
    __del__ = lambda self: None
BinTObjDrivers_XYZDriver_swigregister = _BinTObjDrivers.BinTObjDrivers_XYZDriver_swigregister
BinTObjDrivers_XYZDriver_swigregister(BinTObjDrivers_XYZDriver)



# This file is compatible with both classic and new-style classes.


