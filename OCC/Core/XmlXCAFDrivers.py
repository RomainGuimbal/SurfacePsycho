# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
XmlXCAFDrivers module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_xmlxcafdrivers.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _XmlXCAFDrivers
else:
    import _XmlXCAFDrivers

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
    __swig_destroy__ = _XmlXCAFDrivers.delete_SwigPyIterator

    def value(self):
        return _XmlXCAFDrivers.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _XmlXCAFDrivers.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _XmlXCAFDrivers.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _XmlXCAFDrivers.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _XmlXCAFDrivers.SwigPyIterator_equal(self, x)

    def copy(self):
        return _XmlXCAFDrivers.SwigPyIterator_copy(self)

    def next(self):
        return _XmlXCAFDrivers.SwigPyIterator_next(self)

    def __next__(self):
        return _XmlXCAFDrivers.SwigPyIterator___next__(self)

    def previous(self):
        return _XmlXCAFDrivers.SwigPyIterator_previous(self)

    def advance(self, n):
        return _XmlXCAFDrivers.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _XmlXCAFDrivers.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _XmlXCAFDrivers.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _XmlXCAFDrivers.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _XmlXCAFDrivers.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _XmlXCAFDrivers.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _XmlXCAFDrivers.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _XmlXCAFDrivers:
_XmlXCAFDrivers.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _XmlXCAFDrivers.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TDocStd
import OCC.Core.TDF
import OCC.Core.TCollection
import OCC.Core.TColStd
import OCC.Core.CDF
import OCC.Core.CDM
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.Resource
import OCC.Core.PCDM
import OCC.Core.Storage
import OCC.Core.XmlDrivers
import OCC.Core.XmlMDF
import OCC.Core.XmlObjMgt
import OCC.Core.LDOM
import OCC.Core.gp
import OCC.Core.XmlLDrivers

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_XmlXCAFDrivers_DocumentRetrievalDriver_Create():
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentRetrievalDriver_Create()

def Handle_XmlXCAFDrivers_DocumentRetrievalDriver_DownCast(t):
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentRetrievalDriver_DownCast(t)

def Handle_XmlXCAFDrivers_DocumentRetrievalDriver_IsNull(t):
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentRetrievalDriver_IsNull(t)

def Handle_XmlXCAFDrivers_DocumentStorageDriver_Create():
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentStorageDriver_Create()

def Handle_XmlXCAFDrivers_DocumentStorageDriver_DownCast(t):
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentStorageDriver_DownCast(t)

def Handle_XmlXCAFDrivers_DocumentStorageDriver_IsNull(t):
    return _XmlXCAFDrivers.Handle_XmlXCAFDrivers_DocumentStorageDriver_IsNull(t)
class xmlxcafdrivers(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def DefineFormat(*args):
        r"""

        Parameters
        ----------
        theApp: TDocStd_Application

        Return
        -------
        None

        Description
        -----------
        Defines format 'xmlxcaf' and registers its read and write drivers in the specified application.

        """
        return _XmlXCAFDrivers.xmlxcafdrivers_DefineFormat(*args)

    @staticmethod
    def Factory(*args):
        r"""

        Parameters
        ----------
        aGUID: Standard_GUID

        Return
        -------
        opencascade::handle<Standard_Transient>

        Description
        -----------
        Depending from the id, returns a list of storage or retrieval attribute drivers. used for plugin. //! standard data model drivers =========================== 47b0b826-d931-11d1-b5da-00a0c9064368 transient-persistent 47b0b827-d931-11d1-b5da-00a0c9064368 persistent-transient //! xcaf data model drivers ================================= ed8793f8-3142-11d4-b9b5-0060b0ee281b transient-persistent ed8793f9-3142-11d4-b9b5-0060b0ee281b persistent-transient ed8793fa-3142-11d4-b9b5-0060b0ee281b xcafschema.

        """
        return _XmlXCAFDrivers.xmlxcafdrivers_Factory(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _XmlXCAFDrivers.xmlxcafdrivers_swiginit(self, _XmlXCAFDrivers.new_xmlxcafdrivers())
    __swig_destroy__ = _XmlXCAFDrivers.delete_xmlxcafdrivers

# Register xmlxcafdrivers in _XmlXCAFDrivers:
_XmlXCAFDrivers.xmlxcafdrivers_swigregister(xmlxcafdrivers)
class XmlXCAFDrivers_DocumentRetrievalDriver(OCC.Core.XmlDrivers.XmlDrivers_DocumentRetrievalDriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _XmlXCAFDrivers.XmlXCAFDrivers_DocumentRetrievalDriver_swiginit(self, _XmlXCAFDrivers.new_XmlXCAFDrivers_DocumentRetrievalDriver(*args))


    @staticmethod
    def DownCast(t):
      return Handle_XmlXCAFDrivers_DocumentRetrievalDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlXCAFDrivers.delete_XmlXCAFDrivers_DocumentRetrievalDriver

# Register XmlXCAFDrivers_DocumentRetrievalDriver in _XmlXCAFDrivers:
_XmlXCAFDrivers.XmlXCAFDrivers_DocumentRetrievalDriver_swigregister(XmlXCAFDrivers_DocumentRetrievalDriver)
class XmlXCAFDrivers_DocumentStorageDriver(OCC.Core.XmlDrivers.XmlDrivers_DocumentStorageDriver):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theCopyright: str

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _XmlXCAFDrivers.XmlXCAFDrivers_DocumentStorageDriver_swiginit(self, _XmlXCAFDrivers.new_XmlXCAFDrivers_DocumentStorageDriver(*args))


    @staticmethod
    def DownCast(t):
      return Handle_XmlXCAFDrivers_DocumentStorageDriver_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _XmlXCAFDrivers.delete_XmlXCAFDrivers_DocumentStorageDriver

# Register XmlXCAFDrivers_DocumentStorageDriver in _XmlXCAFDrivers:
_XmlXCAFDrivers.XmlXCAFDrivers_DocumentStorageDriver_swigregister(XmlXCAFDrivers_DocumentStorageDriver)



@deprecated
def xmlxcafdrivers_DefineFormat(*args):
	return xmlxcafdrivers.DefineFormat(*args)

@deprecated
def xmlxcafdrivers_Factory(*args):
	return xmlxcafdrivers.Factory(*args)


