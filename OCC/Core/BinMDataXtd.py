# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
BinMDataXtd module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_binmdataxtd.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _BinMDataXtd
else:
    import _BinMDataXtd

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _BinMDataXtd.delete_SwigPyIterator

    def value(self):
        return _BinMDataXtd.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _BinMDataXtd.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _BinMDataXtd.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _BinMDataXtd.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _BinMDataXtd.SwigPyIterator_equal(self, x)

    def copy(self):
        return _BinMDataXtd.SwigPyIterator_copy(self)

    def next(self):
        return _BinMDataXtd.SwigPyIterator_next(self)

    def __next__(self):
        return _BinMDataXtd.SwigPyIterator___next__(self)

    def previous(self):
        return _BinMDataXtd.SwigPyIterator_previous(self)

    def advance(self, n):
        return _BinMDataXtd.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _BinMDataXtd.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _BinMDataXtd.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _BinMDataXtd.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _BinMDataXtd.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _BinMDataXtd.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _BinMDataXtd.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _BinMDataXtd:
_BinMDataXtd.SwigPyIterator_swigregister(SwigPyIterator)

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


def process_exception(error, method_name, class_name):
    return _BinMDataXtd.process_exception(error, method_name, class_name)

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




def Handle_BinMDataXtd_ConstraintDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_Create()

def Handle_BinMDataXtd_ConstraintDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_DownCast(t)

def Handle_BinMDataXtd_ConstraintDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_ConstraintDriver_IsNull(t)

def Handle_BinMDataXtd_GeometryDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_Create()

def Handle_BinMDataXtd_GeometryDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_DownCast(t)

def Handle_BinMDataXtd_GeometryDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_GeometryDriver_IsNull(t)

def Handle_BinMDataXtd_PatternStdDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_Create()

def Handle_BinMDataXtd_PatternStdDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_DownCast(t)

def Handle_BinMDataXtd_PatternStdDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PatternStdDriver_IsNull(t)

def Handle_BinMDataXtd_PositionDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_Create()

def Handle_BinMDataXtd_PositionDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_DownCast(t)

def Handle_BinMDataXtd_PositionDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PositionDriver_IsNull(t)

def Handle_BinMDataXtd_PresentationDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_Create()

def Handle_BinMDataXtd_PresentationDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_DownCast(t)

def Handle_BinMDataXtd_PresentationDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_PresentationDriver_IsNull(t)

def Handle_BinMDataXtd_TriangulationDriver_Create():
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_Create()

def Handle_BinMDataXtd_TriangulationDriver_DownCast(t):
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_DownCast(t)

def Handle_BinMDataXtd_TriangulationDriver_IsNull(t):
    return _BinMDataXtd.Handle_BinMDataXtd_TriangulationDriver_IsNull(t)
class binmdataxtd(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def AddDrivers(*args):
        r"""

        Parameters
        ----------
        theDriverTable: BinMDF_ADriverTable
        aMsgDrv: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        Adds the attribute drivers to <thedrivertable>.

        """
        return _BinMDataXtd.binmdataxtd_AddDrivers(*args)

    @staticmethod
    def DocumentVersion(*args):
        r"""
        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.binmdataxtd_DocumentVersion(*args)

    @staticmethod
    def SetDocumentVersion(*args):
        r"""

        Parameters
        ----------
        DocVersion: int

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.binmdataxtd_SetDocumentVersion(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _BinMDataXtd.binmdataxtd_swiginit(self, _BinMDataXtd.new_binmdataxtd())
    __swig_destroy__ = _BinMDataXtd.delete_binmdataxtd

# Register binmdataxtd in _BinMDataXtd:
_BinMDataXtd.binmdataxtd_swigregister(binmdataxtd)
class BinMDataXtd_ConstraintDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_ConstraintDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_ConstraintDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_ConstraintDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_ConstraintDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_ConstraintDriver

# Register BinMDataXtd_ConstraintDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_ConstraintDriver_swigregister(BinMDataXtd_ConstraintDriver)
class BinMDataXtd_GeometryDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_GeometryDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_GeometryDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_GeometryDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_GeometryDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_GeometryDriver

# Register BinMDataXtd_GeometryDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_GeometryDriver_swigregister(BinMDataXtd_GeometryDriver)
class BinMDataXtd_PatternStdDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_PatternStdDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_PatternStdDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_PatternStdDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PatternStdDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PatternStdDriver

# Register BinMDataXtd_PatternStdDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_PatternStdDriver_swigregister(BinMDataXtd_PatternStdDriver)
class BinMDataXtd_PositionDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_PositionDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_PositionDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_PositionDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PositionDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PositionDriver

# Register BinMDataXtd_PositionDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_PositionDriver_swigregister(BinMDataXtd_PositionDriver)
class BinMDataXtd_PresentationDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_PresentationDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_PresentationDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_PresentationDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_PresentationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_PresentationDriver

# Register BinMDataXtd_PresentationDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_PresentationDriver_swigregister(BinMDataXtd_PresentationDriver)
class BinMDataXtd_TriangulationDriver(OCC.Core.BinMDF.BinMDF_ADriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theMessageDriver: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BinMDataXtd.BinMDataXtd_TriangulationDriver_swiginit(self, _BinMDataXtd.new_BinMDataXtd_TriangulationDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: BinObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: BinObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: BinObjMgt_Persistent
        RelocTable: BinObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BinMDataXtd.BinMDataXtd_TriangulationDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BinMDataXtd_TriangulationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BinMDataXtd.delete_BinMDataXtd_TriangulationDriver

# Register BinMDataXtd_TriangulationDriver in _BinMDataXtd:
_BinMDataXtd.BinMDataXtd_TriangulationDriver_swigregister(BinMDataXtd_TriangulationDriver)



@deprecated
def binmdataxtd_AddDrivers(*args):
	return binmdataxtd.AddDrivers(*args)

@deprecated
def binmdataxtd_DocumentVersion(*args):
	return binmdataxtd.DocumentVersion(*args)

@deprecated
def binmdataxtd_SetDocumentVersion(*args):
	return binmdataxtd.SetDocumentVersion(*args)


