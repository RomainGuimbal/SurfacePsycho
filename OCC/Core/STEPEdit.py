# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
STEPEdit module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_stepedit.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _STEPEdit
else:
    import _STEPEdit

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
    __swig_destroy__ = _STEPEdit.delete_SwigPyIterator

    def value(self):
        return _STEPEdit.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _STEPEdit.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _STEPEdit.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _STEPEdit.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _STEPEdit.SwigPyIterator_equal(self, x)

    def copy(self):
        return _STEPEdit.SwigPyIterator_copy(self)

    def next(self):
        return _STEPEdit.SwigPyIterator_next(self)

    def __next__(self):
        return _STEPEdit.SwigPyIterator___next__(self)

    def previous(self):
        return _STEPEdit.SwigPyIterator_previous(self)

    def advance(self, n):
        return _STEPEdit.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _STEPEdit.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _STEPEdit.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _STEPEdit.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _STEPEdit.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _STEPEdit.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _STEPEdit.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _STEPEdit:
_STEPEdit.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _STEPEdit.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.StepData
import OCC.Core.Interface
import OCC.Core.TCollection
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.MoniTool
import OCC.Core.TopoDS
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.Resource
import OCC.Core.IFSelect

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_STEPEdit_EditContext_Create():
    return _STEPEdit.Handle_STEPEdit_EditContext_Create()

def Handle_STEPEdit_EditContext_DownCast(t):
    return _STEPEdit.Handle_STEPEdit_EditContext_DownCast(t)

def Handle_STEPEdit_EditContext_IsNull(t):
    return _STEPEdit.Handle_STEPEdit_EditContext_IsNull(t)

def Handle_STEPEdit_EditSDR_Create():
    return _STEPEdit.Handle_STEPEdit_EditSDR_Create()

def Handle_STEPEdit_EditSDR_DownCast(t):
    return _STEPEdit.Handle_STEPEdit_EditSDR_DownCast(t)

def Handle_STEPEdit_EditSDR_IsNull(t):
    return _STEPEdit.Handle_STEPEdit_EditSDR_IsNull(t)
class stepedit(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def NewModel(*args):
        r"""
        Return
        -------
        opencascade::handle<StepData_StepModel>

        Description
        -----------
        Returns a new empty stepmodel fit for step i.e. with its header determined from protocol.

        """
        return _STEPEdit.stepedit_NewModel(*args)

    @staticmethod
    def NewSelectPlacedItem(*args):
        r"""
        Return
        -------
        opencascade::handle<IFSelect_SelectSignature>

        Description
        -----------
        Creates a selection for placed items, i.e. mappeditem or contextdependentshaperepresentation, which itself refers to a representationrelationship with possible subtypes (shape... and/or ...withtransformation) by default in the whole stepmodel.

        """
        return _STEPEdit.stepedit_NewSelectPlacedItem(*args)

    @staticmethod
    def NewSelectSDR(*args):
        r"""
        Return
        -------
        opencascade::handle<IFSelect_SelectSignature>

        Description
        -----------
        Creates a selection for shapedefinitionrepresentation by default searches among root entities.

        """
        return _STEPEdit.stepedit_NewSelectSDR(*args)

    @staticmethod
    def NewSelectShapeRepr(*args):
        r"""
        Return
        -------
        opencascade::handle<IFSelect_SelectSignature>

        Description
        -----------
        Creates a selection for shaperepresentation and its sub-types, plus contextdependentshaperepresentation (which is not a sub-type of shaperepresentation) by default in the whole stepmodel.

        """
        return _STEPEdit.stepedit_NewSelectShapeRepr(*args)

    @staticmethod
    def Protocol(*args):
        r"""
        Return
        -------
        opencascade::handle<Interface_Protocol>

        Description
        -----------
        Returns a protocol fit for step (creates the first time).

        """
        return _STEPEdit.stepedit_Protocol(*args)

    @staticmethod
    def SignType(*args):
        r"""
        Return
        -------
        opencascade::handle<IFSelect_Signature>

        Description
        -----------
        Returns a signtype fit for step (creates the first time).

        """
        return _STEPEdit.stepedit_SignType(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _STEPEdit.stepedit_swiginit(self, _STEPEdit.new_stepedit())
    __swig_destroy__ = _STEPEdit.delete_stepedit

# Register stepedit in _STEPEdit:
_STEPEdit.stepedit_swigregister(stepedit)
class STEPEdit_EditContext(OCC.Core.IFSelect.IFSelect_Editor):
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
        _STEPEdit.STEPEdit_EditContext_swiginit(self, _STEPEdit.new_STEPEdit_EditContext(*args))


    @staticmethod
    def DownCast(t):
      return Handle_STEPEdit_EditContext_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _STEPEdit.delete_STEPEdit_EditContext

# Register STEPEdit_EditContext in _STEPEdit:
_STEPEdit.STEPEdit_EditContext_swigregister(STEPEdit_EditContext)
class STEPEdit_EditSDR(OCC.Core.IFSelect.IFSelect_Editor):
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
        _STEPEdit.STEPEdit_EditSDR_swiginit(self, _STEPEdit.new_STEPEdit_EditSDR(*args))


    @staticmethod
    def DownCast(t):
      return Handle_STEPEdit_EditSDR_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _STEPEdit.delete_STEPEdit_EditSDR

# Register STEPEdit_EditSDR in _STEPEdit:
_STEPEdit.STEPEdit_EditSDR_swigregister(STEPEdit_EditSDR)



@deprecated
def stepedit_NewModel(*args):
	return stepedit.NewModel(*args)

@deprecated
def stepedit_NewSelectPlacedItem(*args):
	return stepedit.NewSelectPlacedItem(*args)

@deprecated
def stepedit_NewSelectSDR(*args):
	return stepedit.NewSelectSDR(*args)

@deprecated
def stepedit_NewSelectShapeRepr(*args):
	return stepedit.NewSelectShapeRepr(*args)

@deprecated
def stepedit_Protocol(*args):
	return stepedit.Protocol(*args)

@deprecated
def stepedit_SignType(*args):
	return stepedit.SignType(*args)


