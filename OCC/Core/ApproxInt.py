# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
ApproxInt module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_approxint.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _ApproxInt
else:
    import _ApproxInt

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
    __swig_destroy__ = _ApproxInt.delete_SwigPyIterator

    def value(self):
        return _ApproxInt.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _ApproxInt.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _ApproxInt.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _ApproxInt.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _ApproxInt.SwigPyIterator_equal(self, x)

    def copy(self):
        return _ApproxInt.SwigPyIterator_copy(self)

    def next(self):
        return _ApproxInt.SwigPyIterator_next(self)

    def __next__(self):
        return _ApproxInt.SwigPyIterator___next__(self)

    def previous(self):
        return _ApproxInt.SwigPyIterator_previous(self)

    def advance(self, n):
        return _ApproxInt.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _ApproxInt.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _ApproxInt.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _ApproxInt.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _ApproxInt.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _ApproxInt.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _ApproxInt.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _ApproxInt:
_ApproxInt.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _ApproxInt.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.math
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.gp
import OCC.Core.TColgp
import OCC.Core.IntPatch
import OCC.Core.Intf
import OCC.Core.Bnd
import OCC.Core.BVH
import OCC.Core.Adaptor3d
import OCC.Core.Geom
import OCC.Core.GeomAbs
import OCC.Core.TopAbs
import OCC.Core.Adaptor2d
import OCC.Core.Geom2d
import OCC.Core.IntSurf
import OCC.Core.IntAna
import OCC.Core.Approx
import OCC.Core.AppCont
import OCC.Core.AppParCurves

from enum import IntEnum
from OCC.Core.Exception import *



class ApproxInt_KnotTools(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def BuildCurvature(*args):
        r"""

        Parameters
        ----------
        theCoords: NCollection_LocalArray<float>
        theDim: int
        thePars: math_Vector
        theCurv: TColStd_Array1OfReal

        Return
        -------
        theMaxCurv: float

        Description
        -----------
        Builds discrete curvature.

        """
        return _ApproxInt.ApproxInt_KnotTools_BuildCurvature(*args)

    @staticmethod
    def BuildKnots(*args):
        r"""

        Parameters
        ----------
        thePntsXYZ: TColgp_Array1OfPnt
        thePntsU1V1: TColgp_Array1OfPnt2d
        thePntsU2V2: TColgp_Array1OfPnt2d
        thePars: math_Vector
        theApproxXYZ: bool
        theApproxU1V1: bool
        theApproxU2V2: bool
        theMinNbPnts: int
        theKnots: NCollection_Vector<int>

        Return
        -------
        None

        Description
        -----------
        Main function to build optimal knot sequence. at least one set from (thepntsxyz, thepntsu1v1, thepntsu2v2) should exist. @param thepntsxyz - set of 3d points. @param thepntsu1v1 - set of 2d points. @param thepntsu2v2 - set of 2d points. @param thepars - expected parameters associated with set. @param theapproxxyz - flag, existence of 3d set. @param theapproxu1v1 - flag existence of first 2d set. @param theapproxu2v2 - flag existence of second 2d set. @param theminnbpnts - minimal number of points per knot interval. @param theknots - output knots sequence.

        """
        return _ApproxInt.ApproxInt_KnotTools_BuildKnots(*args)

    @staticmethod
    def DefineParType(*args):
        r"""

        Parameters
        ----------
        theWL: IntPatch_WLine
        theFpar: int
        theLpar: int
        theApproxXYZ: bool
        theApproxU1V1: bool
        theApproxU2V2: bool

        Return
        -------
        Approx_ParametrizationType

        Description
        -----------
        Defines preferable parametrization type for thewl .

        """
        return _ApproxInt.ApproxInt_KnotTools_DefineParType(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _ApproxInt.ApproxInt_KnotTools_swiginit(self, _ApproxInt.new_ApproxInt_KnotTools())
    __swig_destroy__ = _ApproxInt.delete_ApproxInt_KnotTools

# Register ApproxInt_KnotTools in _ApproxInt:
_ApproxInt.ApproxInt_KnotTools_swigregister(ApproxInt_KnotTools)
class ApproxInt_SvSurfaces(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def Compute(self, *args):
        r"""

        Parameters
        ----------
        Pt: gp_Pnt
        Tg: gp_Vec
        Tguv1: gp_Vec2d
        Tguv2: gp_Vec2d

        Return
        -------
        u1: float
        v1: float
        u2: float
        v2: float

        Description
        -----------
        Returns true if tg,tguv1 tguv2 can be computed.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_Compute(self, *args)

    def GetUseSolver(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_GetUseSolver(self, *args)

    def Pnt(self, *args):
        r"""

        Parameters
        ----------
        u1: float
        v1: float
        u2: float
        v2: float
        P: gp_Pnt

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_Pnt(self, *args)

    def SeekPoint(self, *args):
        r"""

        Parameters
        ----------
        u1: float
        v1: float
        u2: float
        v2: float
        Point: IntSurf_PntOn2S

        Return
        -------
        bool

        Description
        -----------
        Computes point on curve and parameters on the surfaces.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_SeekPoint(self, *args)

    def SetUseSolver(self, *args):
        r"""

        Parameters
        ----------
        theUseSol: bool

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_SetUseSolver(self, *args)

    def Tangency(self, *args):
        r"""

        Parameters
        ----------
        u1: float
        v1: float
        u2: float
        v2: float
        Tg: gp_Vec

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_Tangency(self, *args)

    def TangencyOnSurf1(self, *args):
        r"""

        Parameters
        ----------
        u1: float
        v1: float
        u2: float
        v2: float
        Tg: gp_Vec2d

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_TangencyOnSurf1(self, *args)

    def TangencyOnSurf2(self, *args):
        r"""

        Parameters
        ----------
        u1: float
        v1: float
        u2: float
        v2: float
        Tg: gp_Vec2d

        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _ApproxInt.ApproxInt_SvSurfaces_TangencyOnSurf2(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _ApproxInt.delete_ApproxInt_SvSurfaces

# Register ApproxInt_SvSurfaces in _ApproxInt:
_ApproxInt.ApproxInt_SvSurfaces_swigregister(ApproxInt_SvSurfaces)



@deprecated
def ApproxInt_KnotTools_BuildCurvature(*args):
	return ApproxInt_KnotTools.BuildCurvature(*args)

@deprecated
def ApproxInt_KnotTools_BuildKnots(*args):
	return ApproxInt_KnotTools.BuildKnots(*args)

@deprecated
def ApproxInt_KnotTools_DefineParType(*args):
	return ApproxInt_KnotTools.DefineParType(*args)


