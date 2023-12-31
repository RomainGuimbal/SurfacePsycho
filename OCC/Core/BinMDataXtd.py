# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
BinMDataXtd module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_binmdataxtd.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_BinMDataXtd')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_BinMDataXtd')
    _BinMDataXtd = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_BinMDataXtd', [dirname(__file__)])
        except ImportError:
            import _BinMDataXtd
            return _BinMDataXtd
        try:
            _mod = imp.load_module('_BinMDataXtd', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _BinMDataXtd = swig_import_helper()
    del swig_import_helper
else:
    import _BinMDataXtd
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
    __swig_destroy__ = _BinMDataXtd.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _BinMDataXtd.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BinMDataXtd.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BinMDataXtd.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _BinMDataXtd.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _BinMDataXtd.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _BinMDataXtd.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _BinMDataXtd.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _BinMDataXtd.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _BinMDataXtd.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BinMDataXtd.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _BinMDataXtd.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _BinMDataXtd.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BinMDataXtd.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BinMDataXtd.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BinMDataXtd.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _BinMDataXtd.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _BinMDataXtd.SwigPyIterator_swigregister
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
    return _BinMDataXtd.process_exception(error, method_name, class_name)
process_exception = _BinMDataXtd.process_exception

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

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_BinMDataXtd_ConstraintDriver_Create() -> "opencascade::handle< BinMDataXtd_ConstraintDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_Create()
Handle_BinMDataXtd_ConstraintDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_Create

def Handle_BinMDataXtd_ConstraintDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_ConstraintDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_DownCast(t)
Handle_BinMDataXtd_ConstraintDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_DownCast

def Handle_BinMDataXtd_ConstraintDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_ConstraintDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_IsNull(t)
Handle_BinMDataXtd_ConstraintDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_IsNull

def Handle_BinMDataXtd_GeometryDriver_Create() -> "opencascade::handle< BinMDataXtd_GeometryDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_Create()
Handle_BinMDataXtd_GeometryDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_Create

def Handle_BinMDataXtd_GeometryDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_GeometryDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_DownCast(t)
Handle_BinMDataXtd_GeometryDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_DownCast

def Handle_BinMDataXtd_GeometryDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_GeometryDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_IsNull(t)
Handle_BinMDataXtd_GeometryDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_IsNull

def Handle_BinMDataXtd_PatternStdDriver_Create() -> "opencascade::handle< BinMDataXtd_PatternStdDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_Create()
Handle_BinMDataXtd_PatternStdDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_Create

def Handle_BinMDataXtd_PatternStdDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_PatternStdDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_DownCast(t)
Handle_BinMDataXtd_PatternStdDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_DownCast

def Handle_BinMDataXtd_PatternStdDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_PatternStdDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_IsNull(t)
Handle_BinMDataXtd_PatternStdDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_IsNull

def Handle_BinMDataXtd_PositionDriver_Create() -> "opencascade::handle< BinMDataXtd_PositionDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_Create()
Handle_BinMDataXtd_PositionDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_Create

def Handle_BinMDataXtd_PositionDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_PositionDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_DownCast(t)
Handle_BinMDataXtd_PositionDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_DownCast

def Handle_BinMDataXtd_PositionDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_PositionDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_IsNull(t)
Handle_BinMDataXtd_PositionDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_IsNull

def Handle_BinMDataXtd_PresentationDriver_Create() -> "opencascade::handle< BinMDataXtd_PresentationDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_Create()
Handle_BinMDataXtd_PresentationDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_Create

def Handle_BinMDataXtd_PresentationDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_PresentationDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_DownCast(t)
Handle_BinMDataXtd_PresentationDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_DownCast

def Handle_BinMDataXtd_PresentationDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_PresentationDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_IsNull(t)
Handle_BinMDataXtd_PresentationDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_IsNull

def Handle_BinMDataXtd_TriangulationDriver_Create() -> "opencascade::handle< BinMDataXtd_TriangulationDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_Create()
Handle_BinMDataXtd_TriangulationDriver_Create = _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_Create

def Handle_BinMDataXtd_TriangulationDriver_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BinMDataXtd_TriangulationDriver >":
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_DownCast(t)
Handle_BinMDataXtd_TriangulationDriver_DownCast = _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_DownCast

def Handle_BinMDataXtd_TriangulationDriver_IsNull(t: 'opencascade::handle< BinMDataXtd_TriangulationDriver > const &') -> "bool":
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_IsNull(t)
Handle_BinMDataXtd_TriangulationDriver_IsNull = _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_IsNull
class binmdataxtd(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, binmdataxtd, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, binmdataxtd, name)
    __repr__ = _swig_repr

    def AddDrivers(*args) -> "void":
        """
        Adds the attribute drivers to <thedrivertable>.

        Parameters
        ----------
        theDriverTable: BinMDF_ADriverTable
        aMsgDrv: Message_Messenger

        Returns
        -------
        None

        """
        return _BinMDataXtd.binmdataxtd_AddDrivers(*args)

    AddDrivers = staticmethod(AddDrivers)

    def DocumentVersion(*args) -> "Standard_Integer":
        """
        No available documentation.

        Returns
        -------
        int

        """
        return _BinMDataXtd.binmdataxtd_DocumentVersion(*args)

    DocumentVersion = staticmethod(DocumentVersion)

    def SetDocumentVersion(*args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        DocVersion: int

        Returns
        -------
        None

        """
        return _BinMDataXtd.binmdataxtd_SetDocumentVersion(*args)

    SetDocumentVersion = staticmethod(SetDocumentVersion)

    __repr__ = _dumps_object


    def __init__(self):
        this = _BinMDataXtd.new_binmdataxtd()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _BinMDataXtd.delete_binmdataxtd
    __del__ = lambda self: None
binmdataxtd_swigregister = _BinMDataXtd.binmdataxtd_swigregister
binmdataxtd_swigregister(binmdataxtd)

def binmdataxtd_AddDrivers(*args) -> "void":
    """
    Adds the attribute drivers to <thedrivertable>.

    Parameters
    ----------
    theDriverTable: BinMDF_ADriverTable
    aMsgDrv: Message_Messenger

    Returns
    -------
    None

    """
    return _BinMDataXtd.binmdataxtd_AddDrivers(*args)

def binmdataxtd_DocumentVersion(*args) -> "Standard_Integer":
    """
    No available documentation.

    Returns
    -------
    int

    """
    return _BinMDataXtd.binmdataxtd_DocumentVersion(*args)

def binmdataxtd_SetDocumentVersion(*args) -> "void":
    """
    No available documentation.

    Parameters
    ----------
    DocVersion: int

    Returns
    -------
    None

    """
    return _BinMDataXtd.binmdataxtd_SetDocumentVersion(*args)

class BinMDataXtd_ConstraintDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_ConstraintDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_ConstraintDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_ConstraintDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_ConstraintDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_ConstraintDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_ConstraintDriver
    __del__ = lambda self: None
BinMDataXtd_ConstraintDriver_swigregister = _BinMDataXtd.BinMDataXtd_ConstraintDriver_swigregister
BinMDataXtd_ConstraintDriver_swigregister(BinMDataXtd_ConstraintDriver)

class BinMDataXtd_GeometryDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_GeometryDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_GeometryDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_GeometryDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_GeometryDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_GeometryDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_GeometryDriver
    __del__ = lambda self: None
BinMDataXtd_GeometryDriver_swigregister = _BinMDataXtd.BinMDataXtd_GeometryDriver_swigregister
BinMDataXtd_GeometryDriver_swigregister(BinMDataXtd_GeometryDriver)

class BinMDataXtd_PatternStdDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_PatternStdDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_PatternStdDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_PatternStdDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_PatternStdDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PatternStdDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PatternStdDriver
    __del__ = lambda self: None
BinMDataXtd_PatternStdDriver_swigregister = _BinMDataXtd.BinMDataXtd_PatternStdDriver_swigregister
BinMDataXtd_PatternStdDriver_swigregister(BinMDataXtd_PatternStdDriver)

class BinMDataXtd_PositionDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_PositionDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_PositionDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_PositionDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_PositionDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PositionDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PositionDriver
    __del__ = lambda self: None
BinMDataXtd_PositionDriver_swigregister = _BinMDataXtd.BinMDataXtd_PositionDriver_swigregister
BinMDataXtd_PositionDriver_swigregister(BinMDataXtd_PositionDriver)

class BinMDataXtd_PresentationDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_PresentationDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_PresentationDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_PresentationDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_PresentationDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PresentationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PresentationDriver
    __del__ = lambda self: None
BinMDataXtd_PresentationDriver_swigregister = _BinMDataXtd.BinMDataXtd_PresentationDriver_swigregister
BinMDataXtd_PresentationDriver_swigregister(BinMDataXtd_PresentationDriver)

class BinMDataXtd_TriangulationDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BinMDataXtd_TriangulationDriver, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.BinMDF.BinMDF_ADriver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BinMDataXtd_TriangulationDriver, name)
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
        this = _BinMDataXtd.new_BinMDataXtd_TriangulationDriver(*args)
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
        return _BinMDataXtd.BinMDataXtd_TriangulationDriver_Paste(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_TriangulationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_TriangulationDriver
    __del__ = lambda self: None
BinMDataXtd_TriangulationDriver_swigregister = _BinMDataXtd.BinMDataXtd_TriangulationDriver_swigregister
BinMDataXtd_TriangulationDriver_swigregister(BinMDataXtd_TriangulationDriver)



# This file is compatible with both classic and new-style classes.


