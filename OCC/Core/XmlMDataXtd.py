# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
XmlMDataXtd module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_xmlmdataxtd.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _XmlMDataXtd
else:
    import _XmlMDataXtd

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
    __swig_destroy__ = _XmlMDataXtd.delete_SwigPyIterator

    def value(self):
        return _XmlMDataXtd.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _XmlMDataXtd.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _XmlMDataXtd.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _XmlMDataXtd.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _XmlMDataXtd.SwigPyIterator_equal(self, x)

    def copy(self):
        return _XmlMDataXtd.SwigPyIterator_copy(self)

    def next(self):
        return _XmlMDataXtd.SwigPyIterator_next(self)

    def __next__(self):
        return _XmlMDataXtd.SwigPyIterator___next__(self)

    def previous(self):
        return _XmlMDataXtd.SwigPyIterator_previous(self)

    def advance(self, n):
        return _XmlMDataXtd.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _XmlMDataXtd.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _XmlMDataXtd.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _XmlMDataXtd.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _XmlMDataXtd.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _XmlMDataXtd.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _XmlMDataXtd.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _XmlMDataXtd:
_XmlMDataXtd.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _XmlMDataXtd.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.XmlMDF
import OCC.Core.Message
import OCC.Core.TCollection
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.TDF
import OCC.Core.XmlObjMgt
import OCC.Core.LDOM
import OCC.Core.gp
import OCC.Core.Storage

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_XmlMDataXtd_ConstraintDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_ConstraintDriver_Create()

def Handle_XmlMDataXtd_ConstraintDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_ConstraintDriver_DownCast(t)

def Handle_XmlMDataXtd_ConstraintDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_ConstraintDriver_IsNull(t)

def Handle_XmlMDataXtd_GeometryDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_GeometryDriver_Create()

def Handle_XmlMDataXtd_GeometryDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_GeometryDriver_DownCast(t)

def Handle_XmlMDataXtd_GeometryDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_GeometryDriver_IsNull(t)

def Handle_XmlMDataXtd_PatternStdDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_PatternStdDriver_Create()

def Handle_XmlMDataXtd_PatternStdDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PatternStdDriver_DownCast(t)

def Handle_XmlMDataXtd_PatternStdDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PatternStdDriver_IsNull(t)

def Handle_XmlMDataXtd_PositionDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_PositionDriver_Create()

def Handle_XmlMDataXtd_PositionDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PositionDriver_DownCast(t)

def Handle_XmlMDataXtd_PositionDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PositionDriver_IsNull(t)

def Handle_XmlMDataXtd_PresentationDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_PresentationDriver_Create()

def Handle_XmlMDataXtd_PresentationDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PresentationDriver_DownCast(t)

def Handle_XmlMDataXtd_PresentationDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_PresentationDriver_IsNull(t)

def Handle_XmlMDataXtd_TriangulationDriver_Create():
    return _XmlMDataXtd.Handle_XmlMDataXtd_TriangulationDriver_Create()

def Handle_XmlMDataXtd_TriangulationDriver_DownCast(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_TriangulationDriver_DownCast(t)

def Handle_XmlMDataXtd_TriangulationDriver_IsNull(t):
    return _XmlMDataXtd.Handle_XmlMDataXtd_TriangulationDriver_IsNull(t)
class xmlmdataxtd(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def AddDrivers(*args):
        r"""

        Parameters
        ----------
        aDriverTable: XmlMDF_ADriverTable
        anMsgDrv: Message_Messenger

        Return
        -------
        None

        Description
        -----------
        Adds the attribute drivers to <adrivertable>.

        """
        return _XmlMDataXtd.xmlmdataxtd_AddDrivers(*args)

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
        return _XmlMDataXtd.xmlmdataxtd_DocumentVersion(*args)

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
        return _XmlMDataXtd.xmlmdataxtd_SetDocumentVersion(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _XmlMDataXtd.xmlmdataxtd_swiginit(self, _XmlMDataXtd.new_xmlmdataxtd())
    __swig_destroy__ = _XmlMDataXtd.delete_xmlmdataxtd

# Register xmlmdataxtd in _XmlMDataXtd:
_XmlMDataXtd.xmlmdataxtd_swigregister(xmlmdataxtd)
class XmlMDataXtd_ConstraintDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_ConstraintDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_ConstraintDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_ConstraintDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_ConstraintDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_ConstraintDriver

# Register XmlMDataXtd_ConstraintDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_ConstraintDriver_swigregister(XmlMDataXtd_ConstraintDriver)
class XmlMDataXtd_GeometryDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_GeometryDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_GeometryDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_GeometryDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_GeometryDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_GeometryDriver

# Register XmlMDataXtd_GeometryDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_GeometryDriver_swigregister(XmlMDataXtd_GeometryDriver)
class XmlMDataXtd_PatternStdDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_PatternStdDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_PatternStdDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_PatternStdDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_PatternStdDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_PatternStdDriver

# Register XmlMDataXtd_PatternStdDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_PatternStdDriver_swigregister(XmlMDataXtd_PatternStdDriver)
class XmlMDataXtd_PositionDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_PositionDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_PositionDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_PositionDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_PositionDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_PositionDriver

# Register XmlMDataXtd_PositionDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_PositionDriver_swigregister(XmlMDataXtd_PositionDriver)
class XmlMDataXtd_PresentationDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_PresentationDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_PresentationDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_PresentationDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_PresentationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_PresentationDriver

# Register XmlMDataXtd_PresentationDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_PresentationDriver_swigregister(XmlMDataXtd_PresentationDriver)
class XmlMDataXtd_TriangulationDriver(OCC.Core.XmlMDF.XmlMDF_ADriver):
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
        _XmlMDataXtd.XmlMDataXtd_TriangulationDriver_swiginit(self, _XmlMDataXtd.new_XmlMDataXtd_TriangulationDriver(*args))

    def Paste(self, *args):
        r"""

        Parameters
        ----------
        Source: XmlObjMgt_Persistent
        Target: TDF_Attribute
        RelocTable: XmlObjMgt_RRelocationTable

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Source: TDF_Attribute
        Target: XmlObjMgt_Persistent
        RelocTable: XmlObjMgt_SRelocationTable

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _XmlMDataXtd.XmlMDataXtd_TriangulationDriver_Paste(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_XmlMDataXtd_TriangulationDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlMDataXtd.delete_XmlMDataXtd_TriangulationDriver

# Register XmlMDataXtd_TriangulationDriver in _XmlMDataXtd:
_XmlMDataXtd.XmlMDataXtd_TriangulationDriver_swigregister(XmlMDataXtd_TriangulationDriver)



@deprecated
def xmlmdataxtd_AddDrivers(*args):
	return xmlmdataxtd.AddDrivers(*args)

@deprecated
def xmlmdataxtd_DocumentVersion(*args):
	return xmlmdataxtd.DocumentVersion(*args)

@deprecated
def xmlmdataxtd_SetDocumentVersion(*args):
	return xmlmdataxtd.SetDocumentVersion(*args)


