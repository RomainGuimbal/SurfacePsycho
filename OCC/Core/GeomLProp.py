# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
GeomLProp module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_geomlprop.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _GeomLProp
else:
    import _GeomLProp

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
    __swig_destroy__ = _GeomLProp.delete_SwigPyIterator

    def value(self):
        return _GeomLProp.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _GeomLProp.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _GeomLProp.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _GeomLProp.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _GeomLProp.SwigPyIterator_equal(self, x)

    def copy(self):
        return _GeomLProp.SwigPyIterator_copy(self)

    def next(self):
        return _GeomLProp.SwigPyIterator_next(self)

    def __next__(self):
        return _GeomLProp.SwigPyIterator___next__(self)

    def previous(self):
        return _GeomLProp.SwigPyIterator_previous(self)

    def advance(self, n):
        return _GeomLProp.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _GeomLProp.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _GeomLProp.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _GeomLProp.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _GeomLProp.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _GeomLProp.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _GeomLProp.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _GeomLProp:
_GeomLProp.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _GeomLProp.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.Geom
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.GeomAbs
import OCC.Core.TColgp

from enum import IntEnum
from OCC.Core.Exception import *



class geomlprop(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def Continuity(*args):
        r"""

        Parameters
        ----------
        C1: Geom_Curve
        C2: Geom_Curve
        u1: float
        u2: float
        r1: bool
        r2: bool
        tl: float
        ta: float

        Return
        -------
        GeomAbs_Shape

        Description
        -----------
        Computes the regularity at the junction between c1 and c2. the booleans r1 and r2 are true if the curves must be taken reversed. the point u1 on c1 and the point u2 on c2 must be confused. tl and ta are the linear and angular tolerance used two compare the derivative.

        Parameters
        ----------
        C1: Geom_Curve
        C2: Geom_Curve
        u1: float
        u2: float
        r1: bool
        r2: bool

        Return
        -------
        GeomAbs_Shape

        Description
        -----------
        The same as preceding but using the standard tolerances from package precision.

        """
        return _GeomLProp.geomlprop_Continuity(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _GeomLProp.geomlprop_swiginit(self, _GeomLProp.new_geomlprop())
    __swig_destroy__ = _GeomLProp.delete_geomlprop

# Register geomlprop in _GeomLProp:
_GeomLProp.geomlprop_swigregister(geomlprop)
class GeomLProp_CLProps(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        C: Geom_Curve
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
        C: Geom_Curve
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
        _GeomLProp.GeomLProp_CLProps_swiginit(self, _GeomLProp.new_GeomLProp_CLProps(*args))

    def CentreOfCurvature(self, *args):
        r"""

        Parameters
        ----------
        P: gp_Pnt

        Return
        -------
        None

        Description
        -----------
        Returns the centre of curvature <p>.

        """
        return _GeomLProp.GeomLProp_CLProps_CentreOfCurvature(self, *args)

    def Curvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the curvature.

        """
        return _GeomLProp.GeomLProp_CLProps_Curvature(self, *args)

    def D1(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the first derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_CLProps_D1(self, *args)

    def D2(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the second derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_CLProps_D2(self, *args)

    def D3(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the third derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_CLProps_D3(self, *args)

    def IsTangentDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if the tangent is defined. for example, the tangent is not defined if the three first derivatives are all null.

        """
        return _GeomLProp.GeomLProp_CLProps_IsTangentDefined(self, *args)

    def Normal(self, *args):
        r"""

        Parameters
        ----------
        N: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Returns the normal direction <n>.

        """
        return _GeomLProp.GeomLProp_CLProps_Normal(self, *args)

    def SetCurve(self, *args):
        r"""

        Parameters
        ----------
        C: Geom_Curve

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the curve for the new curve.

        """
        return _GeomLProp.GeomLProp_CLProps_SetCurve(self, *args)

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
        return _GeomLProp.GeomLProp_CLProps_SetParameter(self, *args)

    def Tangent(self, *args):
        r"""

        Parameters
        ----------
        D: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Output the tangent direction <d>.

        """
        return _GeomLProp.GeomLProp_CLProps_Tangent(self, *args)

    def Value(self, *args):
        r"""
        Return
        -------
        gp_Pnt

        Description
        -----------
        Returns the point.

        """
        return _GeomLProp.GeomLProp_CLProps_Value(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _GeomLProp.delete_GeomLProp_CLProps

# Register GeomLProp_CLProps in _GeomLProp:
_GeomLProp.GeomLProp_CLProps_swigregister(GeomLProp_CLProps)
class GeomLProp_CurveTool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def Continuity(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve

        Return
        -------
        int

        Description
        -----------
        Returns the order of continuity of the curve <c>. returns 1: first derivative only is computable returns 2: first and second derivative only are computable. returns 3: first, second and third are computable.

        """
        return _GeomLProp.GeomLProp_CurveTool_Continuity(*args)

    @staticmethod
    def D1(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve
        U: float
        P: gp_Pnt
        V1: gp_Vec

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> and first derivative <v1> of parameter <u> on the curve <c>.

        """
        return _GeomLProp.GeomLProp_CurveTool_D1(*args)

    @staticmethod
    def D2(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve
        U: float
        P: gp_Pnt
        V1: gp_Vec
        V2: gp_Vec

        Return
        -------
        None

        Description
        -----------
        Computes the point <p>, the first derivative <v1> and second derivative <v2> of parameter <u> on the curve <c>.

        """
        return _GeomLProp.GeomLProp_CurveTool_D2(*args)

    @staticmethod
    def D3(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve
        U: float
        P: gp_Pnt
        V1: gp_Vec
        V2: gp_Vec
        V3: gp_Vec

        Return
        -------
        None

        Description
        -----------
        Computes the point <p>, the first derivative <v1>, the second derivative <v2> and third derivative <v3> of parameter <u> on the curve <c>.

        """
        return _GeomLProp.GeomLProp_CurveTool_D3(*args)

    @staticmethod
    def FirstParameter(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve

        Return
        -------
        float

        Description
        -----------
        Returns the first parameter bound of the curve.

        """
        return _GeomLProp.GeomLProp_CurveTool_FirstParameter(*args)

    @staticmethod
    def LastParameter(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve

        Return
        -------
        float

        Description
        -----------
        Returns the last parameter bound of the curve. firstparameter must be less than lastparamenter.

        """
        return _GeomLProp.GeomLProp_CurveTool_LastParameter(*args)

    @staticmethod
    def Value(*args):
        r"""

        Parameters
        ----------
        C: Geom_Curve
        U: float
        P: gp_Pnt

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> of parameter <u> on the curve <c>.

        """
        return _GeomLProp.GeomLProp_CurveTool_Value(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _GeomLProp.GeomLProp_CurveTool_swiginit(self, _GeomLProp.new_GeomLProp_CurveTool())
    __swig_destroy__ = _GeomLProp.delete_GeomLProp_CurveTool

# Register GeomLProp_CurveTool in _GeomLProp:
_GeomLProp.GeomLProp_CurveTool_swigregister(GeomLProp_CurveTool)
class GeomLProp_SLProps(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        S: Geom_Surface
        U: float
        V: float
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the surface <s> for the parameter values (<u>, <v>). the current point and the derivatives are computed at the same time, which allows an optimization of the computation time. <n> indicates the maximum number of derivations to be done (0, 1, or 2). for example, to compute only the tangent, n should be equal to 1. <resolution> is the linear tolerance (it is used to test if a vector is null).

        Parameters
        ----------
        S: Geom_Surface
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Idem as previous constructor but without setting the value of parameters <u> and <v>.

        Parameters
        ----------
        N: int
        Resolution: float

        Return
        -------
        None

        Description
        -----------
        Idem as previous constructor but without setting the value of parameters <u> and <v> and the surface. the surface can have an empty constructor.

        """
        _GeomLProp.GeomLProp_SLProps_swiginit(self, _GeomLProp.new_GeomLProp_SLProps(*args))

    def CurvatureDirections(self, *args):
        r"""

        Parameters
        ----------
        MaxD: gp_Dir
        MinD: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Returns the direction of the maximum and minimum curvature <maxd> and <mind>.

        """
        return _GeomLProp.GeomLProp_SLProps_CurvatureDirections(self, *args)

    def D1U(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the first u derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_SLProps_D1U(self, *args)

    def D1V(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the first v derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_SLProps_D1V(self, *args)

    def D2U(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the second u derivatives the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_SLProps_D2U(self, *args)

    def D2V(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the second v derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_SLProps_D2V(self, *args)

    def DUV(self, *args):
        r"""
        Return
        -------
        gp_Vec

        Description
        -----------
        Returns the second uv cross-derivative. the derivative is computed if it has not been yet.

        """
        return _GeomLProp.GeomLProp_SLProps_DUV(self, *args)

    def GaussianCurvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the gaussian curvature.

        """
        return _GeomLProp.GeomLProp_SLProps_GaussianCurvature(self, *args)

    def IsCurvatureDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if the curvature is defined.

        """
        return _GeomLProp.GeomLProp_SLProps_IsCurvatureDefined(self, *args)

    def IsNormalDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Tells if the normal is defined.

        """
        return _GeomLProp.GeomLProp_SLProps_IsNormalDefined(self, *args)

    def IsTangentUDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if the u tangent is defined. for example, the tangent is not defined if the two first u derivatives are null.

        """
        return _GeomLProp.GeomLProp_SLProps_IsTangentUDefined(self, *args)

    def IsTangentVDefined(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns if the v tangent is defined. for example, the tangent is not defined if the two first v derivatives are null.

        """
        return _GeomLProp.GeomLProp_SLProps_IsTangentVDefined(self, *args)

    def IsUmbilic(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if the point is umbilic (i.e. if the curvature is constant).

        """
        return _GeomLProp.GeomLProp_SLProps_IsUmbilic(self, *args)

    def MaxCurvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the maximum curvature.

        """
        return _GeomLProp.GeomLProp_SLProps_MaxCurvature(self, *args)

    def MeanCurvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the mean curvature.

        """
        return _GeomLProp.GeomLProp_SLProps_MeanCurvature(self, *args)

    def MinCurvature(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the minimum curvature.

        """
        return _GeomLProp.GeomLProp_SLProps_MinCurvature(self, *args)

    def Normal(self, *args):
        r"""
        Return
        -------
        gp_Dir

        Description
        -----------
        Returns the normal direction.

        """
        return _GeomLProp.GeomLProp_SLProps_Normal(self, *args)

    def SetParameters(self, *args):
        r"""

        Parameters
        ----------
        U: float
        V: float

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the surface s for the new parameter values (<u>, <v>).

        """
        return _GeomLProp.GeomLProp_SLProps_SetParameters(self, *args)

    def SetSurface(self, *args):
        r"""

        Parameters
        ----------
        S: Geom_Surface

        Return
        -------
        None

        Description
        -----------
        Initializes the local properties of the surface s for the new surface.

        """
        return _GeomLProp.GeomLProp_SLProps_SetSurface(self, *args)

    def TangentU(self, *args):
        r"""

        Parameters
        ----------
        D: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Returns the tangent direction <d> on the iso-v.

        """
        return _GeomLProp.GeomLProp_SLProps_TangentU(self, *args)

    def TangentV(self, *args):
        r"""

        Parameters
        ----------
        D: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Returns the tangent direction <d> on the iso-v.

        """
        return _GeomLProp.GeomLProp_SLProps_TangentV(self, *args)

    def Value(self, *args):
        r"""
        Return
        -------
        gp_Pnt

        Description
        -----------
        Returns the point.

        """
        return _GeomLProp.GeomLProp_SLProps_Value(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _GeomLProp.delete_GeomLProp_SLProps

# Register GeomLProp_SLProps in _GeomLProp:
_GeomLProp.GeomLProp_SLProps_swigregister(GeomLProp_SLProps)
class GeomLProp_SurfaceTool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def Bounds(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface

        Return
        -------
        U1: float
        V1: float
        U2: float
        V2: float

        Description
        -----------
        Returns the bounds of the surface.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_Bounds(*args)

    @staticmethod
    def Continuity(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface

        Return
        -------
        int

        Description
        -----------
        Returns the order of continuity of the surface <s>. returns 1: first derivative only is computable returns 2: first and second derivative only are computable.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_Continuity(*args)

    @staticmethod
    def D1(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface
        U: float
        V: float
        P: gp_Pnt
        D1U: gp_Vec
        D1V: gp_Vec

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> and first derivative <d1*> of parameter <u> and <v> on the surface <s>.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_D1(*args)

    @staticmethod
    def D2(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface
        U: float
        V: float
        P: gp_Pnt
        D1U: gp_Vec
        D1V: gp_Vec
        D2U: gp_Vec
        D2V: gp_Vec
        DUV: gp_Vec

        Return
        -------
        None

        Description
        -----------
        Computes the point <p>, the first derivative <d1*> and second derivative <d2*> of parameter <u> and <v> on the surface <s>.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_D2(*args)

    @staticmethod
    def DN(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface
        U: float
        V: float
        IU: int
        IV: int

        Return
        -------
        gp_Vec

        Description
        -----------
        No available documentation.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_DN(*args)

    @staticmethod
    def Value(*args):
        r"""

        Parameters
        ----------
        S: Geom_Surface
        U: float
        V: float
        P: gp_Pnt

        Return
        -------
        None

        Description
        -----------
        Computes the point <p> of parameter <u> and <v> on the surface <s>.

        """
        return _GeomLProp.GeomLProp_SurfaceTool_Value(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _GeomLProp.GeomLProp_SurfaceTool_swiginit(self, _GeomLProp.new_GeomLProp_SurfaceTool())
    __swig_destroy__ = _GeomLProp.delete_GeomLProp_SurfaceTool

# Register GeomLProp_SurfaceTool in _GeomLProp:
_GeomLProp.GeomLProp_SurfaceTool_swigregister(GeomLProp_SurfaceTool)



@deprecated
def geomlprop_Continuity(*args):
	return geomlprop.Continuity(*args)

@deprecated
def geomlprop_Continuity(*args):
	return geomlprop.Continuity(*args)

@deprecated
def GeomLProp_CurveTool_Continuity(*args):
	return GeomLProp_CurveTool.Continuity(*args)

@deprecated
def GeomLProp_CurveTool_D1(*args):
	return GeomLProp_CurveTool.D1(*args)

@deprecated
def GeomLProp_CurveTool_D2(*args):
	return GeomLProp_CurveTool.D2(*args)

@deprecated
def GeomLProp_CurveTool_D3(*args):
	return GeomLProp_CurveTool.D3(*args)

@deprecated
def GeomLProp_CurveTool_FirstParameter(*args):
	return GeomLProp_CurveTool.FirstParameter(*args)

@deprecated
def GeomLProp_CurveTool_LastParameter(*args):
	return GeomLProp_CurveTool.LastParameter(*args)

@deprecated
def GeomLProp_CurveTool_Value(*args):
	return GeomLProp_CurveTool.Value(*args)

@deprecated
def GeomLProp_SurfaceTool_Bounds(*args):
	return GeomLProp_SurfaceTool.Bounds(*args)

@deprecated
def GeomLProp_SurfaceTool_Continuity(*args):
	return GeomLProp_SurfaceTool.Continuity(*args)

@deprecated
def GeomLProp_SurfaceTool_D1(*args):
	return GeomLProp_SurfaceTool.D1(*args)

@deprecated
def GeomLProp_SurfaceTool_D2(*args):
	return GeomLProp_SurfaceTool.D2(*args)

@deprecated
def GeomLProp_SurfaceTool_DN(*args):
	return GeomLProp_SurfaceTool.DN(*args)

@deprecated
def GeomLProp_SurfaceTool_Value(*args):
	return GeomLProp_SurfaceTool.Value(*args)



