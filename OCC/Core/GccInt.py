# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
GccInt module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_gccint.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _GccInt
else:
    import _GccInt

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
    __swig_destroy__ = _GccInt.delete_SwigPyIterator

    def value(self):
        return _GccInt.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _GccInt.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _GccInt.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _GccInt.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _GccInt.SwigPyIterator_equal(self, x)

    def copy(self):
        return _GccInt.SwigPyIterator_copy(self)

    def next(self):
        return _GccInt.SwigPyIterator_next(self)

    def __next__(self):
        return _GccInt.SwigPyIterator___next__(self)

    def previous(self):
        return _GccInt.SwigPyIterator_previous(self)

    def advance(self, n):
        return _GccInt.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _GccInt.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _GccInt.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _GccInt.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _GccInt.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _GccInt.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _GccInt.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _GccInt:
_GccInt.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _GccInt.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection

from enum import IntEnum
from OCC.Core.Exception import *

GccInt_Lin = _GccInt.GccInt_Lin
GccInt_Cir = _GccInt.GccInt_Cir
GccInt_Ell = _GccInt.GccInt_Ell
GccInt_Par = _GccInt.GccInt_Par
GccInt_Hpr = _GccInt.GccInt_Hpr
GccInt_Pnt = _GccInt.GccInt_Pnt


class GccInt_IType(IntEnum):
	GccInt_Lin = 0
	GccInt_Cir = 1
	GccInt_Ell = 2
	GccInt_Par = 3
	GccInt_Hpr = 4
	GccInt_Pnt = 5
GccInt_Lin = GccInt_IType.GccInt_Lin
GccInt_Cir = GccInt_IType.GccInt_Cir
GccInt_Ell = GccInt_IType.GccInt_Ell
GccInt_Par = GccInt_IType.GccInt_Par
GccInt_Hpr = GccInt_IType.GccInt_Hpr
GccInt_Pnt = GccInt_IType.GccInt_Pnt


def Handle_GccInt_Bisec_Create():
    return _GccInt.Handle_GccInt_Bisec_Create()

def Handle_GccInt_Bisec_DownCast(t):
    return _GccInt.Handle_GccInt_Bisec_DownCast(t)

def Handle_GccInt_Bisec_IsNull(t):
    return _GccInt.Handle_GccInt_Bisec_IsNull(t)

def Handle_GccInt_BCirc_Create():
    return _GccInt.Handle_GccInt_BCirc_Create()

def Handle_GccInt_BCirc_DownCast(t):
    return _GccInt.Handle_GccInt_BCirc_DownCast(t)

def Handle_GccInt_BCirc_IsNull(t):
    return _GccInt.Handle_GccInt_BCirc_IsNull(t)

def Handle_GccInt_BElips_Create():
    return _GccInt.Handle_GccInt_BElips_Create()

def Handle_GccInt_BElips_DownCast(t):
    return _GccInt.Handle_GccInt_BElips_DownCast(t)

def Handle_GccInt_BElips_IsNull(t):
    return _GccInt.Handle_GccInt_BElips_IsNull(t)

def Handle_GccInt_BHyper_Create():
    return _GccInt.Handle_GccInt_BHyper_Create()

def Handle_GccInt_BHyper_DownCast(t):
    return _GccInt.Handle_GccInt_BHyper_DownCast(t)

def Handle_GccInt_BHyper_IsNull(t):
    return _GccInt.Handle_GccInt_BHyper_IsNull(t)

def Handle_GccInt_BLine_Create():
    return _GccInt.Handle_GccInt_BLine_Create()

def Handle_GccInt_BLine_DownCast(t):
    return _GccInt.Handle_GccInt_BLine_DownCast(t)

def Handle_GccInt_BLine_IsNull(t):
    return _GccInt.Handle_GccInt_BLine_IsNull(t)

def Handle_GccInt_BParab_Create():
    return _GccInt.Handle_GccInt_BParab_Create()

def Handle_GccInt_BParab_DownCast(t):
    return _GccInt.Handle_GccInt_BParab_DownCast(t)

def Handle_GccInt_BParab_IsNull(t):
    return _GccInt.Handle_GccInt_BParab_IsNull(t)

def Handle_GccInt_BPoint_Create():
    return _GccInt.Handle_GccInt_BPoint_Create()

def Handle_GccInt_BPoint_DownCast(t):
    return _GccInt.Handle_GccInt_BPoint_DownCast(t)

def Handle_GccInt_BPoint_IsNull(t):
    return _GccInt.Handle_GccInt_BPoint_IsNull(t)
class GccInt_Bisec(OCC.Core.Standard.Standard_Transient):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def ArcType(self, *args):
        r"""
        Return
        -------
        GccInt_IType

        Description
        -----------
        Returns the type of bisecting object (line, circle, parabola, hyperbola, ellipse, point).

        """
        return _GccInt.GccInt_Bisec_ArcType(self, *args)

    def Circle(self, *args):
        r"""
        Return
        -------
        gp_Circ2d

        Description
        -----------
        Returns the bisecting line when arctype returns cir. an exception domainerror is raised if arctype is not a cir.

        """
        return _GccInt.GccInt_Bisec_Circle(self, *args)

    def Ellipse(self, *args):
        r"""
        Return
        -------
        gp_Elips2d

        Description
        -----------
        Returns the bisecting line when arctype returns ell. an exception domainerror is raised if arctype is not an ell.

        """
        return _GccInt.GccInt_Bisec_Ellipse(self, *args)

    def Hyperbola(self, *args):
        r"""
        Return
        -------
        gp_Hypr2d

        Description
        -----------
        Returns the bisecting line when arctype returns hpr. an exception domainerror is raised if arctype is not a hpr.

        """
        return _GccInt.GccInt_Bisec_Hyperbola(self, *args)

    def Line(self, *args):
        r"""
        Return
        -------
        gp_Lin2d

        Description
        -----------
        Returns the bisecting line when arctype returns lin. an exception domainerror is raised if arctype is not a lin.

        """
        return _GccInt.GccInt_Bisec_Line(self, *args)

    def Parabola(self, *args):
        r"""
        Return
        -------
        gp_Parab2d

        Description
        -----------
        Returns the bisecting line when arctype returns par. an exception domainerror is raised if arctype is not a par.

        """
        return _GccInt.GccInt_Bisec_Parabola(self, *args)

    def Point(self, *args):
        r"""
        Return
        -------
        gp_Pnt2d

        Description
        -----------
        Returns the bisecting line when arctype returns pnt. an exception domainerror is raised if arctype is not a pnt.

        """
        return _GccInt.GccInt_Bisec_Point(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_Bisec_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_Bisec

# Register GccInt_Bisec in _GccInt:
_GccInt.GccInt_Bisec_swigregister(GccInt_Bisec)
class GccInt_BCirc(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Circ: gp_Circ2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting curve whose geometry is the 2d circle circ.

        """
        _GccInt.GccInt_BCirc_swiginit(self, _GccInt.new_GccInt_BCirc(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BCirc_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BCirc

# Register GccInt_BCirc in _GccInt:
_GccInt.GccInt_BCirc_swigregister(GccInt_BCirc)
class GccInt_BElips(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Ellipse: gp_Elips2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting curve whose geometry is the 2d ellipse ellipse.

        """
        _GccInt.GccInt_BElips_swiginit(self, _GccInt.new_GccInt_BElips(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BElips_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BElips

# Register GccInt_BElips in _GccInt:
_GccInt.GccInt_BElips_swigregister(GccInt_BElips)
class GccInt_BHyper(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Hyper: gp_Hypr2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting curve whose geometry is the 2d hyperbola hyper.

        """
        _GccInt.GccInt_BHyper_swiginit(self, _GccInt.new_GccInt_BHyper(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BHyper_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BHyper

# Register GccInt_BHyper in _GccInt:
_GccInt.GccInt_BHyper_swigregister(GccInt_BHyper)
class GccInt_BLine(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Line: gp_Lin2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting line whose geometry is the 2d line line.

        """
        _GccInt.GccInt_BLine_swiginit(self, _GccInt.new_GccInt_BLine(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BLine_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BLine

# Register GccInt_BLine in _GccInt:
_GccInt.GccInt_BLine_swigregister(GccInt_BLine)
class GccInt_BParab(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Parab: gp_Parab2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting curve whose geometry is the 2d parabola parab.

        """
        _GccInt.GccInt_BParab_swiginit(self, _GccInt.new_GccInt_BParab(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BParab_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BParab

# Register GccInt_BParab in _GccInt:
_GccInt.GccInt_BParab_swigregister(GccInt_BParab)
class GccInt_BPoint(GccInt_Bisec):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Point: gp_Pnt2d

        Return
        -------
        None

        Description
        -----------
        Constructs a bisecting object whose geometry is the 2d point point.

        """
        _GccInt.GccInt_BPoint_swiginit(self, _GccInt.new_GccInt_BPoint(*args))


    @staticmethod
    def DownCast(t):
      return Handle_GccInt_BPoint_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _GccInt.delete_GccInt_BPoint

# Register GccInt_BPoint in _GccInt:
_GccInt.GccInt_BPoint_swigregister(GccInt_BPoint)


