# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
TopCnx module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_topcnx.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _TopCnx
else:
    import _TopCnx

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
    __swig_destroy__ = _TopCnx.delete_SwigPyIterator

    def value(self):
        return _TopCnx.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _TopCnx.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _TopCnx.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _TopCnx.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _TopCnx.SwigPyIterator_equal(self, x)

    def copy(self):
        return _TopCnx.SwigPyIterator_copy(self)

    def next(self):
        return _TopCnx.SwigPyIterator_next(self)

    def __next__(self):
        return _TopCnx.SwigPyIterator___next__(self)

    def previous(self):
        return _TopCnx.SwigPyIterator_previous(self)

    def advance(self, n):
        return _TopCnx.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _TopCnx.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _TopCnx.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _TopCnx.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _TopCnx.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _TopCnx.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _TopCnx.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _TopCnx:
_TopCnx.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _TopCnx.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.TopAbs

from enum import IntEnum
from OCC.Core.Exception import *



class TopCnx_EdgeFaceTransition(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Creates an empty algorithm.

        """
        _TopCnx.TopCnx_EdgeFaceTransition_swiginit(self, _TopCnx.new_TopCnx_EdgeFaceTransition(*args))

    def AddInterference(self, *args):
        r"""

        Parameters
        ----------
        Tole: float
        Tang: gp_Dir
        Norm: gp_Dir
        Curv: float
        Or: TopAbs_Orientation
        Tr: TopAbs_Orientation
        BTr: TopAbs_Orientation

        Return
        -------
        None

        Description
        -----------
        Add a curve element to the boundary. or is the orientation of the interference on the boundary curve. tr is the transition of the interference. btr is the boundary transition of the interference.

        """
        return _TopCnx.TopCnx_EdgeFaceTransition_AddInterference(self, *args)

    def BoundaryTransition(self, *args):
        r"""
        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        Returns the current cumulated boundarytransition.

        """
        return _TopCnx.TopCnx_EdgeFaceTransition_BoundaryTransition(self, *args)

    def Reset(self, *args):
        r"""

        Parameters
        ----------
        Tgt: gp_Dir
        Norm: gp_Dir
        Curv: float

        Return
        -------
        None

        Description
        -----------
        Initialize the algorithm with the local description of the edge.

        Parameters
        ----------
        Tgt: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Initialize the algorithm with a linear edge.

        """
        return _TopCnx.TopCnx_EdgeFaceTransition_Reset(self, *args)

    def Transition(self, *args):
        r"""
        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        Returns the current cumulated transition.

        """
        return _TopCnx.TopCnx_EdgeFaceTransition_Transition(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _TopCnx.delete_TopCnx_EdgeFaceTransition

# Register TopCnx_EdgeFaceTransition in _TopCnx:
_TopCnx.TopCnx_EdgeFaceTransition_swigregister(TopCnx_EdgeFaceTransition)


