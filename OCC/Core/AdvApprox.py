# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
AdvApprox module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_advapprox.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _AdvApprox
else:
    import _AdvApprox

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
    __swig_destroy__ = _AdvApprox.delete_SwigPyIterator

    def value(self):
        return _AdvApprox.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _AdvApprox.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _AdvApprox.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _AdvApprox.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _AdvApprox.SwigPyIterator_equal(self, x)

    def copy(self):
        return _AdvApprox.SwigPyIterator_copy(self)

    def next(self):
        return _AdvApprox.SwigPyIterator_next(self)

    def __next__(self):
        return _AdvApprox.SwigPyIterator___next__(self)

    def previous(self):
        return _AdvApprox.SwigPyIterator_previous(self)

    def advance(self, n):
        return _AdvApprox.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _AdvApprox.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _AdvApprox.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _AdvApprox.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _AdvApprox.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _AdvApprox.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _AdvApprox.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _AdvApprox:
_AdvApprox.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _AdvApprox.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.PLib
import OCC.Core.math
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.gp

from enum import IntEnum
from OCC.Core.Exception import *



class AdvApprox_ApproxAFunction(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Num1DSS: int
        Num2DSS: int
        Num3DSS: int
        OneDTol: TColStd_HArray1OfReal
        TwoDTol: TColStd_HArray1OfReal
        ThreeDTol: TColStd_HArray1OfReal
        First: float
        Last: float
        Continuity: GeomAbs_Shape
        MaxDeg: int
        MaxSeg: int
        Func: AdvApprox_EvaluatorFunction

        Return
        -------
        None

        Description
        -----------
        Constructs approximator tool. //! warning: the func should be valid reference to object of type inherited from class evaluatorfunction from approx with life time longer than that of the approximator tool; //! the result should be formatted in the following way: <--num1dss--> <--2 * num2dss--> <--3 * num3dss--> r[0] .... r[num1dss].....  r[dimension-1] //! the order in which each subspace appears should be consistent with the tolerances given in the create function and the results will be given in that order as well that is: curve2d(n) will correspond to the nth entry described by num2dss, curve(n) will correspond to the nth entry described by num3dss the same type of schema applies to the poles1d, poles2d and poles.

        Parameters
        ----------
        Num1DSS: int
        Num2DSS: int
        Num3DSS: int
        OneDTol: TColStd_HArray1OfReal
        TwoDTol: TColStd_HArray1OfReal
        ThreeDTol: TColStd_HArray1OfReal
        First: float
        Last: float
        Continuity: GeomAbs_Shape
        MaxDeg: int
        MaxSeg: int
        Func: AdvApprox_EvaluatorFunction
        CutTool: AdvApprox_Cutting

        Return
        -------
        None

        Description
        -----------
        Approximation with user methode of cutting.

        """
        _AdvApprox.AdvApprox_ApproxAFunction_swiginit(self, _AdvApprox.new_AdvApprox_ApproxAFunction(*args))

    @staticmethod
    def Approximation(*args):
        r"""

        Parameters
        ----------
        TotalDimension: int
        TotalNumSS: int
        LocalDimension: TColStd_Array1OfInteger
        First: float
        Last: float
        Evaluator: AdvApprox_EvaluatorFunction
        CutTool: AdvApprox_Cutting
        ContinuityOrder: int
        NumMaxCoeffs: int
        MaxSegments: int
        TolerancesArray: TColStd_Array1OfReal
        code_precis: int
        NumCoeffPerCurveArray: TColStd_Array1OfInteger
        LocalCoefficientArray: TColStd_Array1OfReal
        IntervalsArray: TColStd_Array1OfReal
        ErrorMaxArray: TColStd_Array1OfReal
        AverageErrorArray: TColStd_Array1OfReal

        Return
        -------
        NumCurves: int
        ErrorCode: int

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Approximation(*args)

    def AverageError(self, *args):
        r"""

        Parameters
        ----------
        Dimension: int

        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        Returns the error as is in the algorithms.

        Parameters
        ----------
        Dimension: int
        Index: int

        Return
        -------
        float

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_AverageError(self, *args)

    def Degree(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Degree(self, *args)

    def DumpToString(self):
        r"""DumpToString(AdvApprox_ApproxAFunction self) -> std::string"""
        return _AdvApprox.AdvApprox_ApproxAFunction_DumpToString(self)

    def HasResult(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_HasResult(self, *args)

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_IsDone(self, *args)

    def Knots(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Knots(self, *args)

    def MaxError(self, *args):
        r"""

        Parameters
        ----------
        Dimension: int

        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        Returns the error as is in the algorithms.

        Parameters
        ----------
        Dimension: int
        Index: int

        Return
        -------
        float

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_MaxError(self, *args)

    def Multiplicities(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray1OfInteger>

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Multiplicities(self, *args)

    def NbKnots(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_NbKnots(self, *args)

    def NbPoles(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        As the name says.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_NbPoles(self, *args)

    def NumSubSpaces(self, *args):
        r"""

        Parameters
        ----------
        Dimension: int

        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_NumSubSpaces(self, *args)

    def Poles(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColgp_HArray2OfPnt>

        Description
        -----------
        -- returns the poles from the algorithms as is.

        Parameters
        ----------
        Index: int
        P: TColgp_Array1OfPnt

        Return
        -------
        None

        Description
        -----------
        Returns the poles at index from the 3d subspace.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Poles(self, *args)

    def Poles1d(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray2OfReal>

        Description
        -----------
        Returns the poles from the algorithms as is.

        Parameters
        ----------
        Index: int
        P: TColStd_Array1OfReal

        Return
        -------
        None

        Description
        -----------
        Returns the poles at index from the 1d subspace.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Poles1d(self, *args)

    def Poles2d(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColgp_HArray2OfPnt2d>

        Description
        -----------
        Returns the poles from the algorithms as is.

        Parameters
        ----------
        Index: int
        P: TColgp_Array1OfPnt2d

        Return
        -------
        None

        Description
        -----------
        Returns the poles at index from the 2d subspace.

        """
        return _AdvApprox.AdvApprox_ApproxAFunction_Poles2d(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_ApproxAFunction

# Register AdvApprox_ApproxAFunction in _AdvApprox:
_AdvApprox.AdvApprox_ApproxAFunction_swigregister(AdvApprox_ApproxAFunction)
class AdvApprox_Cutting(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def Value(self, *args):
        r"""

        Parameters
        ----------
        a: float
        b: float

        Return
        -------
        cuttingvalue: float

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_Cutting_Value(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_Cutting

# Register AdvApprox_Cutting in _AdvApprox:
_AdvApprox.AdvApprox_Cutting_swigregister(AdvApprox_Cutting)
class AdvApprox_SimpleApprox(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        TotalDimension: int
        TotalNumSS: int
        Continuity: GeomAbs_Shape
        WorkDegree: int
        NbGaussPoints: int
        JacobiBase: PLib_JacobiPolynomial
        Func: AdvApprox_EvaluatorFunction

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _AdvApprox.AdvApprox_SimpleApprox_swiginit(self, _AdvApprox.new_AdvApprox_SimpleApprox(*args))

    def AverageError(self, *args):
        r"""

        Parameters
        ----------
        Index: int

        Return
        -------
        float

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_AverageError(self, *args)

    def Coefficients(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        Returns the coefficients in the jacobi base.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_Coefficients(self, *args)

    def Degree(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_Degree(self, *args)

    def DifTab(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_DifTab(self, *args)

    def DumpToString(self):
        r"""DumpToString(AdvApprox_SimpleApprox self) -> std::string"""
        return _AdvApprox.AdvApprox_SimpleApprox_DumpToString(self)

    def FirstConstr(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray2OfReal>

        Description
        -----------
        Returns the constraints at first.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_FirstConstr(self, *args)

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_IsDone(self, *args)

    def LastConstr(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray2OfReal>

        Description
        -----------
        Returns the constraints at last.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_LastConstr(self, *args)

    def MaxError(self, *args):
        r"""

        Parameters
        ----------
        Index: int

        Return
        -------
        float

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_MaxError(self, *args)

    def Perform(self, *args):
        r"""

        Parameters
        ----------
        LocalDimension: TColStd_Array1OfInteger
        LocalTolerancesArray: TColStd_Array1OfReal
        First: float
        Last: float
        MaxDegree: int

        Return
        -------
        None

        Description
        -----------
        Constructs approximator tool. //! warning: the func should be valid reference to object of type inherited from class evaluatorfunction from approx with life time longer than that of the approximator tool;.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_Perform(self, *args)

    def SomTab(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TColStd_HArray1OfReal>

        Description
        -----------
        No available documentation.

        """
        return _AdvApprox.AdvApprox_SimpleApprox_SomTab(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_SimpleApprox

# Register AdvApprox_SimpleApprox in _AdvApprox:
_AdvApprox.AdvApprox_SimpleApprox_swigregister(AdvApprox_SimpleApprox)
class AdvApprox_DichoCutting(AdvApprox_Cutting):
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
        _AdvApprox.AdvApprox_DichoCutting_swiginit(self, _AdvApprox.new_AdvApprox_DichoCutting(*args))

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_DichoCutting

# Register AdvApprox_DichoCutting in _AdvApprox:
_AdvApprox.AdvApprox_DichoCutting_swigregister(AdvApprox_DichoCutting)
class AdvApprox_PrefAndRec(AdvApprox_Cutting):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        RecomendedCut: TColStd_Array1OfReal
        PrefferedCut: TColStd_Array1OfReal
        Weight: float (optional, default to 5)

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _AdvApprox.AdvApprox_PrefAndRec_swiginit(self, _AdvApprox.new_AdvApprox_PrefAndRec(*args))

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_PrefAndRec

# Register AdvApprox_PrefAndRec in _AdvApprox:
_AdvApprox.AdvApprox_PrefAndRec_swigregister(AdvApprox_PrefAndRec)
class AdvApprox_PrefCutting(AdvApprox_Cutting):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        CutPnts: TColStd_Array1OfReal

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _AdvApprox.AdvApprox_PrefCutting_swiginit(self, _AdvApprox.new_AdvApprox_PrefCutting(*args))

    __repr__ = _dumps_object

    __swig_destroy__ = _AdvApprox.delete_AdvApprox_PrefCutting

# Register AdvApprox_PrefCutting in _AdvApprox:
_AdvApprox.AdvApprox_PrefCutting_swigregister(AdvApprox_PrefCutting)

@classnotwrapped
class AdvApprox_EvaluatorFunction:
	pass





@deprecated
def AdvApprox_ApproxAFunction_Approximation(*args):
	return AdvApprox_ApproxAFunction.Approximation(*args)


