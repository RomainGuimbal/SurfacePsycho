# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
Geom2dLProp module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_geom2dlprop.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _Geom2dLProp
else:
    import _Geom2dLProp

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
    __swig_destroy__ = _Geom2dLProp.delete_SwigPyIterator

    def value(self):
        return _Geom2dLProp.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _Geom2dLProp.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _Geom2dLProp.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _Geom2dLProp.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _Geom2dLProp.SwigPyIterator_equal(self, x)

    def copy(self):
        return _Geom2dLProp.SwigPyIterator_copy(self)

    def next(self):
        return _Geom2dLProp.SwigPyIterator_next(self)

    def __next__(self):
        return _Geom2dLProp.SwigPyIterator___next__(self)

    def previous(self):
        return _Geom2dLProp.SwigPyIterator_previous(self)

    def advance(self, n):
        return _Geom2dLProp.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _Geom2dLProp.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _Geom2dLProp.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _Geom2dLProp.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _Geom2dLProp.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _Geom2dLProp.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _Geom2dLProp.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _Geom2dLProp:
_Geom2dLProp.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _Geom2dLProp.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.Geom2d
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.LProp
import OCC.Core.math
import OCC.Core.Message
import OCC.Core.OSD

from enum import IntEnum
from OCC.Core.Exception import *



class Geom2dLProp_CLProps2d(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the curve <c> the current point and the derivatives are computed at the same time, which allows an optimization of the computation time. <n> indicates the maximum number of derivations to be done (0, 1, 2 or 3). for example, to compute only the tangent, n should be equal to 1. <resolution> is the linear tolerance (it is used to test if a vector is null).

        Parameters
        ----------
        C: Geom2d_Curve
        U: float
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Same as previous constructor but here the parameter is set to the value <u>. all the computations done will be related to <c> and <u>.

        Parameters
        ----------
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Same as previous constructor but here the parameter is set to the value <u> and the curve is set with setcurve. the curve can have a empty constructor all the computations done will be related to <c> and <u> when the functions 'set' will be done.

        """
        _Geom2dLProp.Geom2dLProp_CLProps2d_swiginit(self, _Geom2dLProp.new_Geom2dLProp_CLProps2d(*args))

    def CentreOfCurvature(self, *args):
        r"""

        Parameters
        ----------
        P: gp_Pnt2d

        Return
        -------
        None

        Description
        -----------
        Returns the centre of curvature <p>.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_CentreOfCurvature(self, *args)

    def Curvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the curvature.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_Curvature(self, *args)

    def D1(self, *args):
        r"""
        Return
        -------
        gp_Vec2d

        Description
        -----------
        Returns the first derivative. the derivative is computed if it has not been yet.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_D1(self, *args)

    def D2(self, *args):
        r"""
        Return
        -------
        gp_Vec2d

        Description
        -----------
        Returns the second derivative. the derivative is computed if it has not been yet.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_D2(self, *args)

    def D3(self, *args):
        r"""
        Return
        -------
        gp_Vec2d

        Description
        -----------
        Returns the third derivative. the derivative is computed if it has not been yet.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_D3(self, *args)

    def IsTangentDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if the tangent is defined. for example, the tangent is not defined if the three first derivatives are all null.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_IsTangentDefined(self, *args)

    def Normal(self, *args):
        r"""

        Parameters
        ----------
        N: gp_Dir2d

        Return
        -------
        None

        Description
        -----------
        Returns the normal direction <n>.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_Normal(self, *args)

    def SetCurve(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the curve for the new curve.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_SetCurve(self, *args)

    def SetParameter(self, *args):
        r"""

        Parameters
        ----------
        U: float

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the curve for the parameter value <u>.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_SetParameter(self, *args)

    def Tangent(self, *args):
        r"""

        Parameters
        ----------
        D: gp_Dir2d

        Return
        -------
        None

        Description
        -----------
        Output the tangent direction <d>.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_Tangent(self, *args)

    def Value(self, *args):
        r"""
        Return
        -------
        gp_Pnt2d

        Description
        -----------
        Returns the point.

        """
        return _Geom2dLProp.Geom2dLProp_CLProps2d_Value(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_CLProps2d

# Register Geom2dLProp_CLProps2d in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_CLProps2d_swigregister(Geom2dLProp_CLProps2d)
class Geom2dLProp_CurAndInf2d(OCC.Core.LProp.LProp_CurAndInf):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Initializes the framework. note: the curve on which the local properties are computed is defined using one of the following functions: perform, performcurext or performinf.

        """
        _Geom2dLProp.Geom2dLProp_CurAndInf2d_swiginit(self, _Geom2dLProp.new_Geom2dLProp_CurAndInf2d(*args))

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        True if the solutions are found.

        """
        return _Geom2dLProp.Geom2dLProp_CurAndInf2d_IsDone(self, *args)

    def Perform(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        None

        Description
        -----------
        For the curve c, computes both the inflection points and the maximum and minimum curvatures.

        """
        return _Geom2dLProp.Geom2dLProp_CurAndInf2d_Perform(self, *args)

    def PerformCurExt(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        None

        Description
        -----------
        For the curve c, computes the locals extremas of curvature.

        """
        return _Geom2dLProp.Geom2dLProp_CurAndInf2d_PerformCurExt(self, *args)

    def PerformInf(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        None

        Description
        -----------
        For the curve c, computes the inflections. after computation, the following functions can be used: - isdone to check if the computation was successful - nbpoints to obtain the number of computed particular points - parameter to obtain the parameter on the curve for each particular point - type to check if the point is an inflection point or an extremum of curvature of the curve c. warning these functions can be used to analyze a series of curves, however it is necessary to clear the table of results between each computation.

        """
        return _Geom2dLProp.Geom2dLProp_CurAndInf2d_PerformInf(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_CurAndInf2d

# Register Geom2dLProp_CurAndInf2d in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_CurAndInf2d_swigregister(Geom2dLProp_CurAndInf2d)
class Geom2dLProp_Curve2dTool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def Continuity(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        int

        Description
        -----------
        Returns the order of continuity of the curve <c>. returns 1: first derivative only is computable returns 2: first and second derivative only are computable. returns 3: first, second and third are computable.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_Continuity(*args)

    @staticmethod
    def D1(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        U: float
        P: gp_Pnt2d
        V1: gp_Vec2d

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> and first derivative <v1> of parameter <u> on the curve <c>.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_D1(*args)

    @staticmethod
    def D2(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        U: float
        P: gp_Pnt2d
        V1: gp_Vec2d
        V2: gp_Vec2d

        Return
        -------
        None

        Description
        -----------
        Computes the point <p>, the first derivative <v1> and second derivative <v2> of parameter <u> on the curve <c>.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_D2(*args)

    @staticmethod
    def D3(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        U: float
        P: gp_Pnt2d
        V1: gp_Vec2d
        V2: gp_Vec2d
        V3: gp_Vec2d

        Return
        -------
        None

        Description
        -----------
        Computes the point <p>, the first derivative <v1>, the second derivative <v2> and third derivative <v3> of parameter <u> on the curve <c>.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_D3(*args)

    @staticmethod
    def FirstParameter(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        float

        Description
        -----------
        Returns the first parameter bound of the curve.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_FirstParameter(*args)

    @staticmethod
    def LastParameter(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        float

        Description
        -----------
        Returns the last parameter bound of the curve. firstparameter must be less than lastparameter.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_LastParameter(*args)

    @staticmethod
    def Value(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        U: float
        P: gp_Pnt2d

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> of parameter <u> on the curve <c>.

        """
        return _Geom2dLProp.Geom2dLProp_Curve2dTool_Value(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _Geom2dLProp.Geom2dLProp_Curve2dTool_swiginit(self, _Geom2dLProp.new_Geom2dLProp_Curve2dTool())
    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_Curve2dTool

# Register Geom2dLProp_Curve2dTool in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_Curve2dTool_swigregister(Geom2dLProp_Curve2dTool)
class Geom2dLProp_FuncCurExt(OCC.Core.math.math_FunctionWithDerivative):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        Tol: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _Geom2dLProp.Geom2dLProp_FuncCurExt_swiginit(self, _Geom2dLProp.new_Geom2dLProp_FuncCurExt(*args))

    def IsMinKC(self, *args):
        r"""

        Parameters
        ----------
        Param: float

        Return
        -------
        bool

        Description
        -----------
        True if param corresponds to a minus of the radius of curvature.

        """
        return _Geom2dLProp.Geom2dLProp_FuncCurExt_IsMinKC(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_FuncCurExt

# Register Geom2dLProp_FuncCurExt in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_FuncCurExt_swigregister(Geom2dLProp_FuncCurExt)
class Geom2dLProp_FuncCurNul(OCC.Core.math.math_FunctionWithDerivative):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _Geom2dLProp.Geom2dLProp_FuncCurNul_swiginit(self, _Geom2dLProp.new_Geom2dLProp_FuncCurNul(*args))

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_FuncCurNul

# Register Geom2dLProp_FuncCurNul in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_FuncCurNul_swigregister(Geom2dLProp_FuncCurNul)
class Geom2dLProp_NumericCurInf2d(object):
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
        _Geom2dLProp.Geom2dLProp_NumericCurInf2d_swiginit(self, _Geom2dLProp.new_Geom2dLProp_NumericCurInf2d(*args))

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        True if the solutions are found.

        """
        return _Geom2dLProp.Geom2dLProp_NumericCurInf2d_IsDone(self, *args)

    def PerformCurExt(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        Result: LProp_CurAndInf

        Return
        -------
        None

        Description
        -----------
        Computes the locals extremas of curvature.

        Parameters
        ----------
        C: Geom2d_Curve
        UMin: float
        UMax: float
        Result: LProp_CurAndInf

        Return
        -------
        None

        Description
        -----------
        Computes the locals extremas of curvature. in the interval of parameters [umin,umax].

        """
        return _Geom2dLProp.Geom2dLProp_NumericCurInf2d_PerformCurExt(self, *args)

    def PerformInf(self, *args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        Result: LProp_CurAndInf

        Return
        -------
        None

        Description
        -----------
        Computes the inflections.

        Parameters
        ----------
        C: Geom2d_Curve
        UMin: float
        UMax: float
        Result: LProp_CurAndInf

        Return
        -------
        None

        Description
        -----------
        Computes the inflections in the interval of parameters [umin,umax].

        """
        return _Geom2dLProp.Geom2dLProp_NumericCurInf2d_PerformInf(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dLProp.delete_Geom2dLProp_NumericCurInf2d

# Register Geom2dLProp_NumericCurInf2d in _Geom2dLProp:
_Geom2dLProp.Geom2dLProp_NumericCurInf2d_swigregister(Geom2dLProp_NumericCurInf2d)



@deprecated
def Geom2dLProp_Curve2dTool_Continuity(*args):
	return Geom2dLProp_Curve2dTool.Continuity(*args)

@deprecated
def Geom2dLProp_Curve2dTool_D1(*args):
	return Geom2dLProp_Curve2dTool.D1(*args)

@deprecated
def Geom2dLProp_Curve2dTool_D2(*args):
	return Geom2dLProp_Curve2dTool.D2(*args)

@deprecated
def Geom2dLProp_Curve2dTool_D3(*args):
	return Geom2dLProp_Curve2dTool.D3(*args)

@deprecated
def Geom2dLProp_Curve2dTool_FirstParameter(*args):
	return Geom2dLProp_Curve2dTool.FirstParameter(*args)

@deprecated
def Geom2dLProp_Curve2dTool_LastParameter(*args):
	return Geom2dLProp_Curve2dTool.LastParameter(*args)

@deprecated
def Geom2dLProp_Curve2dTool_Value(*args):
	return Geom2dLProp_Curve2dTool.Value(*args)


