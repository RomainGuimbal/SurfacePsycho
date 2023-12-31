# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
LProp3d module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_lprop3d.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_LProp3d')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_LProp3d')
    _LProp3d = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_LProp3d', [dirname(__file__)])
        except ImportError:
            import _LProp3d
            return _LProp3d
        try:
            _mod = imp.load_module('_LProp3d', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _LProp3d = swig_import_helper()
    del swig_import_helper
else:
    import _LProp3d
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
    __swig_destroy__ = _LProp3d.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _LProp3d.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _LProp3d.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _LProp3d.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _LProp3d.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _LProp3d.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _LProp3d.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _LProp3d.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _LProp3d.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _LProp3d.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _LProp3d.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _LProp3d.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _LProp3d.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _LProp3d.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _LProp3d.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _LProp3d.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _LProp3d.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _LProp3d.SwigPyIterator_swigregister
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
    return _LProp3d.process_exception(error, method_name, class_name)
process_exception = _LProp3d.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.Adaptor3d
import OCC.Core.Geom
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.TopAbs
import OCC.Core.Adaptor2d
import OCC.Core.Geom2d
import OCC.Core.math
import OCC.Core.Message
import OCC.Core.OSD

from enum import IntEnum
from OCC.Core.Exception import *



class LProp3d_CLProps(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LProp3d_CLProps, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LProp3d_CLProps, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Initializes the local properties of the curve <c> the current point and the derivatives are computed at the same time, which allows an optimization of the computation time. <n> indicates the maximum number of derivations to be done (0, 1, 2 or 3). for example, to compute only the tangent, n should be equal to 1. <resolution> is the linear tolerance (it is used to test if a vector is null).

        Parameters
        ----------
        C: Adaptor3d_HCurve
        N: int
        Resolution: float

        Returns
        -------
        None

        Same as previous constructor but here the parameter is set to the value <u>. all the computations done will be related to <c> and <u>.

        Parameters
        ----------
        C: Adaptor3d_HCurve
        U: float
        N: int
        Resolution: float

        Returns
        -------
        None

        Same as previous constructor but here the parameter is set to the value <u> and the curve is set with setcurve. the curve can have a empty constructor all the computations done will be related to <c> and <u> when the functions 'set' will be done.

        Parameters
        ----------
        N: int
        Resolution: float

        Returns
        -------
        None

        """
        this = _LProp3d.new_LProp3d_CLProps(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def CentreOfCurvature(self, *args) -> "void":
        """
        Returns the centre of curvature <p>.

        Parameters
        ----------
        P: gp_Pnt

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CLProps_CentreOfCurvature(self, *args)


    def Curvature(self, *args) -> "Standard_Real":
        """
        Returns the curvature.

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_CLProps_Curvature(self, *args)


    def D1(self, *args) -> "gp_Vec const":
        """
        Returns the first derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_CLProps_D1(self, *args)


    def D2(self, *args) -> "gp_Vec const":
        """
        Returns the second derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_CLProps_D2(self, *args)


    def D3(self, *args) -> "gp_Vec const":
        """
        Returns the third derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_CLProps_D3(self, *args)


    def IsTangentDefined(self, *args) -> "Standard_Boolean":
        """
        Returns true if the tangent is defined. for example, the tangent is not defined if the three first derivatives are all null.

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_CLProps_IsTangentDefined(self, *args)


    def Normal(self, *args) -> "void":
        """
        Returns the normal direction <n>.

        Parameters
        ----------
        N: gp_Dir

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CLProps_Normal(self, *args)


    def SetCurve(self, *args) -> "void":
        """
        Initializes the local properties of the curve for the new curve.

        Parameters
        ----------
        C: Adaptor3d_HCurve

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CLProps_SetCurve(self, *args)


    def SetParameter(self, *args) -> "void":
        """
        Initializes the local properties of the curve for the parameter value <u>.

        Parameters
        ----------
        U: float

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CLProps_SetParameter(self, *args)


    def Tangent(self, *args) -> "void":
        """
        Output the tangent direction <d>.

        Parameters
        ----------
        D: gp_Dir

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CLProps_Tangent(self, *args)


    def Value(self, *args) -> "gp_Pnt const":
        """
        Returns the point.

        Returns
        -------
        gp_Pnt

        """
        return _LProp3d.LProp3d_CLProps_Value(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _LProp3d.delete_LProp3d_CLProps
    __del__ = lambda self: None
LProp3d_CLProps_swigregister = _LProp3d.LProp3d_CLProps_swigregister
LProp3d_CLProps_swigregister(LProp3d_CLProps)

class LProp3d_CurveTool(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LProp3d_CurveTool, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LProp3d_CurveTool, name)
    __repr__ = _swig_repr

    def Continuity(*args) -> "Standard_Integer":
        """
        Returns the order of continuity of the hcurve <c>. returns 1 : first derivative only is computable returns 2 : first and second derivative only are computable. returns 3 : first, second and third are computable.

        Parameters
        ----------
        C: Adaptor3d_HCurve

        Returns
        -------
        int

        """
        return _LProp3d.LProp3d_CurveTool_Continuity(*args)

    Continuity = staticmethod(Continuity)

    def D1(*args) -> "void":
        """
        Computes the point <p> and first derivative <v1> of parameter <u> on the hcurve <c>.

        Parameters
        ----------
        C: Adaptor3d_HCurve
        U: float
        P: gp_Pnt
        V1: gp_Vec

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CurveTool_D1(*args)

    D1 = staticmethod(D1)

    def D2(*args) -> "void":
        """
        Computes the point <p>, the first derivative <v1> and second derivative <v2> of parameter <u> on the hcurve <c>.

        Parameters
        ----------
        C: Adaptor3d_HCurve
        U: float
        P: gp_Pnt
        V1: gp_Vec
        V2: gp_Vec

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CurveTool_D2(*args)

    D2 = staticmethod(D2)

    def D3(*args) -> "void":
        """
        Computes the point <p>, the first derivative <v1>, the second derivative <v2> and third derivative <v3> of parameter <u> on the hcurve <c>.

        Parameters
        ----------
        C: Adaptor3d_HCurve
        U: float
        P: gp_Pnt
        V1: gp_Vec
        V2: gp_Vec
        V3: gp_Vec

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CurveTool_D3(*args)

    D3 = staticmethod(D3)

    def FirstParameter(*args) -> "Standard_Real":
        """
        Returns the first parameter bound of the hcurve.

        Parameters
        ----------
        C: Adaptor3d_HCurve

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_CurveTool_FirstParameter(*args)

    FirstParameter = staticmethod(FirstParameter)

    def LastParameter(*args) -> "Standard_Real":
        """
        Returns the last parameter bound of the hcurve. firstparameter must be less than lastparamenter.

        Parameters
        ----------
        C: Adaptor3d_HCurve

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_CurveTool_LastParameter(*args)

    LastParameter = staticmethod(LastParameter)

    def Value(*args) -> "void":
        """
        Computes the point <p> of parameter <u> on the hcurve <c>.

        Parameters
        ----------
        C: Adaptor3d_HCurve
        U: float
        P: gp_Pnt

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_CurveTool_Value(*args)

    Value = staticmethod(Value)

    __repr__ = _dumps_object


    def __init__(self):
        this = _LProp3d.new_LProp3d_CurveTool()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _LProp3d.delete_LProp3d_CurveTool
    __del__ = lambda self: None
LProp3d_CurveTool_swigregister = _LProp3d.LProp3d_CurveTool_swigregister
LProp3d_CurveTool_swigregister(LProp3d_CurveTool)

def LProp3d_CurveTool_Continuity(*args) -> "Standard_Integer":
    """
    Returns the order of continuity of the hcurve <c>. returns 1 : first derivative only is computable returns 2 : first and second derivative only are computable. returns 3 : first, second and third are computable.

    Parameters
    ----------
    C: Adaptor3d_HCurve

    Returns
    -------
    int

    """
    return _LProp3d.LProp3d_CurveTool_Continuity(*args)

def LProp3d_CurveTool_D1(*args) -> "void":
    """
    Computes the point <p> and first derivative <v1> of parameter <u> on the hcurve <c>.

    Parameters
    ----------
    C: Adaptor3d_HCurve
    U: float
    P: gp_Pnt
    V1: gp_Vec

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_CurveTool_D1(*args)

def LProp3d_CurveTool_D2(*args) -> "void":
    """
    Computes the point <p>, the first derivative <v1> and second derivative <v2> of parameter <u> on the hcurve <c>.

    Parameters
    ----------
    C: Adaptor3d_HCurve
    U: float
    P: gp_Pnt
    V1: gp_Vec
    V2: gp_Vec

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_CurveTool_D2(*args)

def LProp3d_CurveTool_D3(*args) -> "void":
    """
    Computes the point <p>, the first derivative <v1>, the second derivative <v2> and third derivative <v3> of parameter <u> on the hcurve <c>.

    Parameters
    ----------
    C: Adaptor3d_HCurve
    U: float
    P: gp_Pnt
    V1: gp_Vec
    V2: gp_Vec
    V3: gp_Vec

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_CurveTool_D3(*args)

def LProp3d_CurveTool_FirstParameter(*args) -> "Standard_Real":
    """
    Returns the first parameter bound of the hcurve.

    Parameters
    ----------
    C: Adaptor3d_HCurve

    Returns
    -------
    float

    """
    return _LProp3d.LProp3d_CurveTool_FirstParameter(*args)

def LProp3d_CurveTool_LastParameter(*args) -> "Standard_Real":
    """
    Returns the last parameter bound of the hcurve. firstparameter must be less than lastparamenter.

    Parameters
    ----------
    C: Adaptor3d_HCurve

    Returns
    -------
    float

    """
    return _LProp3d.LProp3d_CurveTool_LastParameter(*args)

def LProp3d_CurveTool_Value(*args) -> "void":
    """
    Computes the point <p> of parameter <u> on the hcurve <c>.

    Parameters
    ----------
    C: Adaptor3d_HCurve
    U: float
    P: gp_Pnt

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_CurveTool_Value(*args)

class LProp3d_SLProps(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LProp3d_SLProps, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LProp3d_SLProps, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Initializes the local properties of the surface <s> for the parameter values (<u>, <v>). the current point and the derivatives are computed at the same time, which allows an optimization of the computation time. <n> indicates the maximum number of derivations to be done (0, 1, or 2). for example, to compute only the tangent, n should be equal to 1. <resolution> is the linear tolerance (it is used to test if a vector is null).

        Parameters
        ----------
        S: Adaptor3d_HSurface
        U: float
        V: float
        N: int
        Resolution: float

        Returns
        -------
        None

        Idem as previous constructor but without setting the value of parameters <u> and <v>.

        Parameters
        ----------
        S: Adaptor3d_HSurface
        N: int
        Resolution: float

        Returns
        -------
        None

        Idem as previous constructor but without setting the value of parameters <u> and <v> and the surface. the surface can have an empty constructor.

        Parameters
        ----------
        N: int
        Resolution: float

        Returns
        -------
        None

        """
        this = _LProp3d.new_LProp3d_SLProps(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def CurvatureDirections(self, *args) -> "void":
        """
        Returns the direction of the maximum and minimum curvature <maxd> and <mind>.

        Parameters
        ----------
        MaxD: gp_Dir
        MinD: gp_Dir

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SLProps_CurvatureDirections(self, *args)


    def D1U(self, *args) -> "gp_Vec const":
        """
        Returns the first u derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SLProps_D1U(self, *args)


    def D1V(self, *args) -> "gp_Vec const":
        """
        Returns the first v derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SLProps_D1V(self, *args)


    def D2U(self, *args) -> "gp_Vec const":
        """
        Returns the second u derivatives the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SLProps_D2U(self, *args)


    def D2V(self, *args) -> "gp_Vec const":
        """
        Returns the second v derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SLProps_D2V(self, *args)


    def DUV(self, *args) -> "gp_Vec const":
        """
        Returns the second uv cross-derivative. the derivative is computed if it has not been yet.

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SLProps_DUV(self, *args)


    def GaussianCurvature(self, *args) -> "Standard_Real":
        """
        Returns the gaussian curvature.

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_SLProps_GaussianCurvature(self, *args)


    def IsCurvatureDefined(self, *args) -> "Standard_Boolean":
        """
        Returns true if the curvature is defined.

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_SLProps_IsCurvatureDefined(self, *args)


    def IsNormalDefined(self, *args) -> "Standard_Boolean":
        """
        Tells if the normal is defined.

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_SLProps_IsNormalDefined(self, *args)


    def IsTangentUDefined(self, *args) -> "Standard_Boolean":
        """
        Returns true if the u tangent is defined. for example, the tangent is not defined if the two first u derivatives are null.

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_SLProps_IsTangentUDefined(self, *args)


    def IsTangentVDefined(self, *args) -> "Standard_Boolean":
        """
        Returns if the v tangent is defined. for example, the tangent is not defined if the two first v derivatives are null.

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_SLProps_IsTangentVDefined(self, *args)


    def IsUmbilic(self, *args) -> "Standard_Boolean":
        """
        Returns true if the point is umbilic (i.e. if the curvature is constant).

        Returns
        -------
        bool

        """
        return _LProp3d.LProp3d_SLProps_IsUmbilic(self, *args)


    def MaxCurvature(self, *args) -> "Standard_Real":
        """
        Returns the maximum curvature.

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_SLProps_MaxCurvature(self, *args)


    def MeanCurvature(self, *args) -> "Standard_Real":
        """
        Returns the mean curvature.

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_SLProps_MeanCurvature(self, *args)


    def MinCurvature(self, *args) -> "Standard_Real":
        """
        Returns the minimum curvature.

        Returns
        -------
        float

        """
        return _LProp3d.LProp3d_SLProps_MinCurvature(self, *args)


    def Normal(self, *args) -> "gp_Dir const":
        """
        Returns the normal direction.

        Returns
        -------
        gp_Dir

        """
        return _LProp3d.LProp3d_SLProps_Normal(self, *args)


    def SetParameters(self, *args) -> "void":
        """
        Initializes the local properties of the surface s for the new parameter values (<u>, <v>).

        Parameters
        ----------
        U: float
        V: float

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SLProps_SetParameters(self, *args)


    def SetSurface(self, *args) -> "void":
        """
        Initializes the local properties of the surface s for the new surface.

        Parameters
        ----------
        S: Adaptor3d_HSurface

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SLProps_SetSurface(self, *args)


    def TangentU(self, *args) -> "void":
        """
        Returns the tangent direction <d> on the iso-v.

        Parameters
        ----------
        D: gp_Dir

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SLProps_TangentU(self, *args)


    def TangentV(self, *args) -> "void":
        """
        Returns the tangent direction <d> on the iso-v.

        Parameters
        ----------
        D: gp_Dir

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SLProps_TangentV(self, *args)


    def Value(self, *args) -> "gp_Pnt const":
        """
        Returns the point.

        Returns
        -------
        gp_Pnt

        """
        return _LProp3d.LProp3d_SLProps_Value(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _LProp3d.delete_LProp3d_SLProps
    __del__ = lambda self: None
LProp3d_SLProps_swigregister = _LProp3d.LProp3d_SLProps_swigregister
LProp3d_SLProps_swigregister(LProp3d_SLProps)

class LProp3d_SurfaceTool(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LProp3d_SurfaceTool, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LProp3d_SurfaceTool, name)
    __repr__ = _swig_repr

    def Bounds(*args) -> "Standard_Real &, Standard_Real &, Standard_Real &, Standard_Real &":
        """
        Returns the bounds of the hsurface.

        Parameters
        ----------
        S: Adaptor3d_HSurface

        Returns
        -------
        U1: float
        V1: float
        U2: float
        V2: float

        """
        return _LProp3d.LProp3d_SurfaceTool_Bounds(*args)

    Bounds = staticmethod(Bounds)

    def Continuity(*args) -> "Standard_Integer":
        """
        Returns the order of continuity of the hsurface <s>. returns 1 : first derivative only is computable returns 2 : first and second derivative only are computable.

        Parameters
        ----------
        S: Adaptor3d_HSurface

        Returns
        -------
        int

        """
        return _LProp3d.LProp3d_SurfaceTool_Continuity(*args)

    Continuity = staticmethod(Continuity)

    def D1(*args) -> "void":
        """
        Computes the point <p> and first derivative <d1*> of parameter <u> and <v> on the hsurface <s>.

        Parameters
        ----------
        S: Adaptor3d_HSurface
        U: float
        V: float
        P: gp_Pnt
        D1U: gp_Vec
        D1V: gp_Vec

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SurfaceTool_D1(*args)

    D1 = staticmethod(D1)

    def D2(*args) -> "void":
        """
        Computes the point <p>, the first derivative <d1*> and second derivative <d2*> of parameter <u> and <v> on the hsurface <s>.

        Parameters
        ----------
        S: Adaptor3d_HSurface
        U: float
        V: float
        P: gp_Pnt
        D1U: gp_Vec
        D1V: gp_Vec
        D2U: gp_Vec
        D2V: gp_Vec
        DUV: gp_Vec

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SurfaceTool_D2(*args)

    D2 = staticmethod(D2)

    def DN(*args) -> "gp_Vec":
        """
        No available documentation.

        Parameters
        ----------
        S: Adaptor3d_HSurface
        U: float
        V: float
        IU: int
        IV: int

        Returns
        -------
        gp_Vec

        """
        return _LProp3d.LProp3d_SurfaceTool_DN(*args)

    DN = staticmethod(DN)

    def Value(*args) -> "void":
        """
        Computes the point <p> of parameter <u> and <v> on the hsurface <s>.

        Parameters
        ----------
        S: Adaptor3d_HSurface
        U: float
        V: float
        P: gp_Pnt

        Returns
        -------
        None

        """
        return _LProp3d.LProp3d_SurfaceTool_Value(*args)

    Value = staticmethod(Value)

    __repr__ = _dumps_object


    def __init__(self):
        this = _LProp3d.new_LProp3d_SurfaceTool()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _LProp3d.delete_LProp3d_SurfaceTool
    __del__ = lambda self: None
LProp3d_SurfaceTool_swigregister = _LProp3d.LProp3d_SurfaceTool_swigregister
LProp3d_SurfaceTool_swigregister(LProp3d_SurfaceTool)

def LProp3d_SurfaceTool_Bounds(*args) -> "Standard_Real &, Standard_Real &, Standard_Real &, Standard_Real &":
    """
    Returns the bounds of the hsurface.

    Parameters
    ----------
    S: Adaptor3d_HSurface

    Returns
    -------
    U1: float
    V1: float
    U2: float
    V2: float

    """
    return _LProp3d.LProp3d_SurfaceTool_Bounds(*args)

def LProp3d_SurfaceTool_Continuity(*args) -> "Standard_Integer":
    """
    Returns the order of continuity of the hsurface <s>. returns 1 : first derivative only is computable returns 2 : first and second derivative only are computable.

    Parameters
    ----------
    S: Adaptor3d_HSurface

    Returns
    -------
    int

    """
    return _LProp3d.LProp3d_SurfaceTool_Continuity(*args)

def LProp3d_SurfaceTool_D1(*args) -> "void":
    """
    Computes the point <p> and first derivative <d1*> of parameter <u> and <v> on the hsurface <s>.

    Parameters
    ----------
    S: Adaptor3d_HSurface
    U: float
    V: float
    P: gp_Pnt
    D1U: gp_Vec
    D1V: gp_Vec

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_SurfaceTool_D1(*args)

def LProp3d_SurfaceTool_D2(*args) -> "void":
    """
    Computes the point <p>, the first derivative <d1*> and second derivative <d2*> of parameter <u> and <v> on the hsurface <s>.

    Parameters
    ----------
    S: Adaptor3d_HSurface
    U: float
    V: float
    P: gp_Pnt
    D1U: gp_Vec
    D1V: gp_Vec
    D2U: gp_Vec
    D2V: gp_Vec
    DUV: gp_Vec

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_SurfaceTool_D2(*args)

def LProp3d_SurfaceTool_DN(*args) -> "gp_Vec":
    """
    No available documentation.

    Parameters
    ----------
    S: Adaptor3d_HSurface
    U: float
    V: float
    IU: int
    IV: int

    Returns
    -------
    gp_Vec

    """
    return _LProp3d.LProp3d_SurfaceTool_DN(*args)

def LProp3d_SurfaceTool_Value(*args) -> "void":
    """
    Computes the point <p> of parameter <u> and <v> on the hsurface <s>.

    Parameters
    ----------
    S: Adaptor3d_HSurface
    U: float
    V: float
    P: gp_Pnt

    Returns
    -------
    None

    """
    return _LProp3d.LProp3d_SurfaceTool_Value(*args)



# This file is compatible with both classic and new-style classes.


