# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
Geom2dConvert module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_geom2dconvert.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _Geom2dConvert
else:
    import _Geom2dConvert

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
    __swig_destroy__ = _Geom2dConvert.delete_SwigPyIterator

    def value(self):
        return _Geom2dConvert.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _Geom2dConvert.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _Geom2dConvert.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _Geom2dConvert.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _Geom2dConvert.SwigPyIterator_equal(self, x)

    def copy(self):
        return _Geom2dConvert.SwigPyIterator_copy(self)

    def next(self):
        return _Geom2dConvert.SwigPyIterator_next(self)

    def __next__(self):
        return _Geom2dConvert.SwigPyIterator___next__(self)

    def previous(self):
        return _Geom2dConvert.SwigPyIterator_previous(self)

    def advance(self, n):
        return _Geom2dConvert.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _Geom2dConvert.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _Geom2dConvert.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _Geom2dConvert.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _Geom2dConvert.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _Geom2dConvert.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _Geom2dConvert.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _Geom2dConvert:
_Geom2dConvert.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _Geom2dConvert.process_exception(error, method_name, class_name)

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
import OCC.Core.TColGeom2d
import OCC.Core.Convert
import OCC.Core.Adaptor2d

from enum import IntEnum
from OCC.Core.Exception import *



class Geom2dConvert_SequenceOfPPoint(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def begin(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_begin(self)

    def end(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_end(self)

    def cbegin(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_cbegin(self)

    def cend(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_cend(self)

    def __init__(self, *args):
        _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_swiginit(self, _Geom2dConvert.new_Geom2dConvert_SequenceOfPPoint(*args))

    def Size(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Size(self)

    def Length(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Length(self)

    def Lower(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Lower(self)

    def Upper(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Upper(self)

    def IsEmpty(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_IsEmpty(self)

    def Reverse(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Reverse(self)

    def Exchange(self, I, J):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Exchange(self, I, J)

    @staticmethod
    def delNode(theNode, theAl):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_delNode(theNode, theAl)

    def Clear(self, theAllocator=0):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Clear(self, theAllocator)

    def Assign(self, theOther):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Assign(self, theOther)

    def Set(self, theOther):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Set(self, theOther)

    def Remove(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Remove(self, *args)

    def Append(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Append(self, *args)

    def Prepend(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Prepend(self, *args)

    def InsertBefore(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_InsertBefore(self, *args)

    def InsertAfter(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_InsertAfter(self, *args)

    def Split(self, theIndex, theSeq):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Split(self, theIndex, theSeq)

    def First(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_First(self)

    def ChangeFirst(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_ChangeFirst(self)

    def Last(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Last(self)

    def ChangeLast(self):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_ChangeLast(self)

    def Value(self, theIndex):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_Value(self, theIndex)

    def ChangeValue(self, theIndex):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_ChangeValue(self, theIndex)

    def __call__(self, *args):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint___call__(self, *args)

    def SetValue(self, theIndex, theItem):
        return _Geom2dConvert.Geom2dConvert_SequenceOfPPoint_SetValue(self, theIndex, theItem)
    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_SequenceOfPPoint

    def __len__(self):
        return self.Size()


# Register Geom2dConvert_SequenceOfPPoint in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_SequenceOfPPoint_swigregister(Geom2dConvert_SequenceOfPPoint)
class geom2dconvert(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def C0BSplineToArrayOfC1BSplineCurve(*args):
        r"""

        Parameters
        ----------
        BS: Geom2d_BSplineCurve
        tabBS: TColGeom2d_HArray1OfBSplineCurve
        Tolerance: float

        Return
        -------
        None

        Description
        -----------
        This method reduces as far as it is possible the multiplicities of the knots of the bspline bs.(keeping the geometry). it returns an array of bspline c1. tolerance is a geometrical tolerance.

        Parameters
        ----------
        BS: Geom2d_BSplineCurve
        tabBS: TColGeom2d_HArray1OfBSplineCurve
        AngularTolerance: float
        Tolerance: float

        Return
        -------
        None

        Description
        -----------
        This method reduces as far as it is possible the multiplicities of the knots of the bspline bs.(keeping the geometry). it returns an array of bspline c1. tolerance is a geometrical tolerance.

        """
        return _Geom2dConvert.geom2dconvert_C0BSplineToArrayOfC1BSplineCurve(*args)

    @staticmethod
    def C0BSplineToC1BSplineCurve(*args):
        r"""

        Parameters
        ----------
        BS: Geom2d_BSplineCurve
        Tolerance: float

        Return
        -------
        None

        Description
        -----------
        This method reduces as far as it is possible the multiplicities of the knots of the bspline bs.(keeping the geometry). it returns a new bspline which could still be c0. tolerance is a geometrical tolerance.

        """
        return _Geom2dConvert.geom2dconvert_C0BSplineToC1BSplineCurve(*args)

    @staticmethod
    def ConcatC1(*args):
        r"""

        Parameters
        ----------
        ArrayOfCurves: TColGeom2d_Array1OfBSplineCurve
        ArrayOfToler: TColStd_Array1OfReal
        ArrayOfIndices: TColStd_HArray1OfInteger
        ArrayOfConcatenated: TColGeom2d_HArray1OfBSplineCurve
        ClosedTolerance: float

        Return
        -------
        ClosedFlag: bool

        Description
        -----------
        This method concatenates c1 the arrayofcurves as far as it is possible. arrayofcurves[0..n-1] arrayoftoler contains the biggest tolerance of the two points shared by two consecutives curves. its dimension: [0..n-2] closedflag indicates if the arrayofcurves is closed. in this case closedtolerance contains the biggest tolerance of the two points which are at the closure. otherwise its value is 0.0 closedflag becomes false on the output if it is impossible to build closed curve.

        Parameters
        ----------
        ArrayOfCurves: TColGeom2d_Array1OfBSplineCurve
        ArrayOfToler: TColStd_Array1OfReal
        ArrayOfIndices: TColStd_HArray1OfInteger
        ArrayOfConcatenated: TColGeom2d_HArray1OfBSplineCurve
        ClosedTolerance: float
        AngularTolerance: float

        Return
        -------
        ClosedFlag: bool

        Description
        -----------
        This method concatenates c1 the arrayofcurves as far as it is possible. arrayofcurves[0..n-1] arrayoftoler contains the biggest tolerance of the two points shared by two consecutives curves. its dimension: [0..n-2] closedflag indicates if the arrayofcurves is closed. in this case closedtolerance contains the biggest tolerance of the two points which are at the closure. otherwise its value is 0.0 closedflag becomes false on the output if it is impossible to build closed curve.

        """
        return _Geom2dConvert.geom2dconvert_ConcatC1(*args)

    @staticmethod
    def ConcatG1(*args):
        r"""

        Parameters
        ----------
        ArrayOfCurves: TColGeom2d_Array1OfBSplineCurve
        ArrayOfToler: TColStd_Array1OfReal
        ArrayOfConcatenated: TColGeom2d_HArray1OfBSplineCurve
        ClosedTolerance: float

        Return
        -------
        ClosedFlag: bool

        Description
        -----------
        This method concatenates g1 the arrayofcurves as far as it is possible. arrayofcurves[0..n-1] arrayoftoler contains the biggest tolerance of the two points shared by two consecutives curves. its dimension: [0..n-2] closedflag indicates if the arrayofcurves is closed. in this case closedtolerance contains the biggest tolerance of the two points which are at the closure. otherwise its value is 0.0 closedflag becomes false on the output if it is impossible to build closed curve.

        """
        return _Geom2dConvert.geom2dconvert_ConcatG1(*args)

    @staticmethod
    def CurveToBSplineCurve(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_Curve
        Parameterisation: Convert_ParameterisationType (optional, default to Convert_TgtThetaOver2)

        Return
        -------
        opencascade::handle<Geom2d_BSplineCurve>

        Description
        -----------
        This function converts a non infinite curve from geom into a b-spline curve. c must be an ellipse or a circle or a trimmed conic or a trimmed line or a bezier curve or a trimmed bezier curve or a bspline curve or a trimmed bspline curve or an offset curve or a trimmed offset curve. the returned b-spline is not periodic except if c is a circle or an ellipse. parameterisationtype applies only if the curve is a circle or an ellipse: tgtthetaover2, tgtthetaover2_1, tgtthetaover2_2, tgtthetaover2_3, tgtthetaover2_4, purpose: this is the classical rational parameterisation 2 1 - t cos(theta) = ------ 2 1 + t //! 2t sin(theta) = ------ 2 1 + t //! t = tan (theta/2) //! with tgtthetaover2 the routine will compute the number of spans using the rule num_spans = [ (ulast - ufirst) / 1.2 ] + 1 with tgtthetaover2_n, n spans will be forced: an error will be raized if (ulast - ufirst) >= pi and n = 1, ulast - ufirst >= 2 pi and n = 2 //! quasiangular, here t is a rational function that approximates theta ----> tan(theta/2). nevetheless the composing with above function yields exact functions whose square sum up to 1 rationalc1 ; t is replaced by a polynomial function of u so as to grant c1 contiuity across knots. exceptions standard_domainerror if the curve c is infinite. standard_constructionerror: - if c is a complete circle or ellipse, and if parameterisation is not equal to convert_tgtthetaover2 or to convert_rationalc1, or - if c is a trimmed circle or ellipse and if parameterisation is equal to convert_tgtthetaover2_1 and if u2 - u1 > 0.9999 * pi where u1 and u2 are respectively the first and the last parameters of the trimmed curve (this method of parameterization cannot be used to convert a half-circle or a half-ellipse, for example), or - if c is a trimmed circle or ellipse and parameterisation is equal to convert_tgtthetaover2_2 and u2 - u1 > 1.9999 * pi where u1 and u2 are respectively the first and the last parameters of the trimmed curve (this method of parameterization cannot be used to convert a quasi-complete circle or ellipse).

        """
        return _Geom2dConvert.geom2dconvert_CurveToBSplineCurve(*args)

    @staticmethod
    def SplitBSplineCurve(*args):
        r"""

        Parameters
        ----------
        C: Geom2d_BSplineCurve
        FromK1: int
        ToK2: int
        SameOrientation: bool (optional, default to Standard_True)

        Return
        -------
        opencascade::handle<Geom2d_BSplineCurve>

        Description
        -----------
        -- convert a curve to bspline by approximation //! this method computes the arc of b-spline curve between the two knots fromk1 and tok2. if c is periodic the arc has the same orientation as c if sameorientation = standard_true. if c is not periodic sameorientation is not used for the computation and c is oriented from the knot fromk1 to the knot tok2. we just keep the local definition of c between the knots fromk1 and tok2. the returned b-spline curve has its first and last knots with a multiplicity equal to degree + 1, where degree is the polynomial degree of c. the indexes of the knots fromk1 and tok2 doesn't include the repetition of multiple knots in their definition. //! raised if fromk1 or tok2 are out of the bounds [firstuknotindex, lastuknotindex] raised if fromk1 = tok2.

        Parameters
        ----------
        C: Geom2d_BSplineCurve
        FromU1: float
        ToU2: float
        ParametricTolerance: float
        SameOrientation: bool (optional, default to Standard_True)

        Return
        -------
        opencascade::handle<Geom2d_BSplineCurve>

        Description
        -----------
        This function computes the segment of b-spline curve between the parametric values fromu1, tou2. if c is periodic the arc has the same orientation as c if sameorientation = true. if c is not periodic sameorientation is not used for the computation and c is oriented fromu1 tou2. if u1 and u2 and two parametric values we consider that u1 = u2 if abs (u1 - u2) <= parametrictolerance and parametrictolerance must be greater or equal to resolution from package gp. //! raised if fromu1 or tou2 are out of the parametric bounds of the curve (the tolerance criterion is parametrictolerance). raised if abs (fromu1 - tou2) <= parametrictolerance raised if parametrictolerance < resolution from gp.

        """
        return _Geom2dConvert.geom2dconvert_SplitBSplineCurve(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _Geom2dConvert.geom2dconvert_swiginit(self, _Geom2dConvert.new_geom2dconvert())
    __swig_destroy__ = _Geom2dConvert.delete_geom2dconvert

# Register geom2dconvert in _Geom2dConvert:
_Geom2dConvert.geom2dconvert_swigregister(geom2dconvert)
class Geom2dConvert_ApproxArcsSegments(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    StatusOK = _Geom2dConvert.Geom2dConvert_ApproxArcsSegments_StatusOK
    StatusNotDone = _Geom2dConvert.Geom2dConvert_ApproxArcsSegments_StatusNotDone
    StatusError = _Geom2dConvert.Geom2dConvert_ApproxArcsSegments_StatusError


    class Status(IntEnum):
    	StatusOK = 0
    	StatusNotDone = 1
    	StatusError = 2
    StatusOK = Status.StatusOK
    StatusNotDone = Status.StatusNotDone
    StatusError = Status.StatusError


    def __init__(self, *args):
        r"""

        Parameters
        ----------
        theCurve: Adaptor2d_Curve2d
        theTolerance: float
        theAngleTol: float

        Return
        -------
        None

        Description
        -----------
        Constructor.

        """
        _Geom2dConvert.Geom2dConvert_ApproxArcsSegments_swiginit(self, _Geom2dConvert.new_Geom2dConvert_ApproxArcsSegments(*args))

    def GetResult(self, *args):
        r"""
        Return
        -------
        TColGeom2d_SequenceOfCurve

        Description
        -----------
        Get the result curve after approximation.

        """
        return _Geom2dConvert.Geom2dConvert_ApproxArcsSegments_GetResult(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_ApproxArcsSegments

# Register Geom2dConvert_ApproxArcsSegments in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_ApproxArcsSegments_swigregister(Geom2dConvert_ApproxArcsSegments)
class Geom2dConvert_ApproxCurve(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Curve: Geom2d_Curve
        Tol2d: float
        Order: GeomAbs_Shape
        MaxSegments: int
        MaxDegree: int

        Return
        -------
        None

        Description
        -----------
        Constructs an approximation framework defined by - the 2d conic curve - the tolerance value tol2d - the degree of continuity order - the maximum number of segments allowed maxsegments - the highest degree maxdegree which the polynomial defining the bspline is allowed to have.

        Parameters
        ----------
        Curve: Adaptor2d_Curve2d
        Tol2d: float
        Order: GeomAbs_Shape
        MaxSegments: int
        MaxDegree: int

        Return
        -------
        None

        Description
        -----------
        Constructs an approximation framework defined by - the 2d conic curve - the tolerance value tol2d - the degree of continuity order - the maximum number of segments allowed maxsegments - the highest degree maxdegree which the polynomial defining the bspline is allowed to have.

        """
        _Geom2dConvert.Geom2dConvert_ApproxCurve_swiginit(self, _Geom2dConvert.new_Geom2dConvert_ApproxCurve(*args))

    def Curve(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Geom2d_BSplineCurve>

        Description
        -----------
        Returns the 2d bspline curve resulting from the approximation algorithm.

        """
        return _Geom2dConvert.Geom2dConvert_ApproxCurve_Curve(self, *args)

    def DumpToString(self):
        r"""DumpToString(Geom2dConvert_ApproxCurve self) -> std::string"""
        return _Geom2dConvert.Geom2dConvert_ApproxCurve_DumpToString(self)

    def HasResult(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns standard_true if the approximation did come out with a result that is not necessarely within the required tolerance.

        """
        return _Geom2dConvert.Geom2dConvert_ApproxCurve_HasResult(self, *args)

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns standard_true if the approximation has been done with within required tolerance.

        """
        return _Geom2dConvert.Geom2dConvert_ApproxCurve_IsDone(self, *args)

    def MaxError(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Returns the greatest distance between a point on the source conic and the bspline curve resulting from the approximation. (>0 when an approximation has been done, 0 if no approximation).

        """
        return _Geom2dConvert.Geom2dConvert_ApproxCurve_MaxError(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_ApproxCurve

# Register Geom2dConvert_ApproxCurve in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_ApproxCurve_swigregister(Geom2dConvert_ApproxCurve)
class Geom2dConvert_BSplineCurveKnotSplitting(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        BasisCurve: Geom2d_BSplineCurve
        ContinuityRange: int

        Return
        -------
        None

        Description
        -----------
        Determines points at which the bspline curve basiscurve should be split in order to obtain arcs with a degree of continuity equal to continuityrange. these points are knot values of basiscurve. they are identified by indices in the knots table of basiscurve. use the available interrogation functions to access computed values, followed by the global function splitbsplinecurve (provided by the package geom2dconvert) to split the curve. exceptions standard_rangeerror if continuityrange is less than zero.

        """
        _Geom2dConvert.Geom2dConvert_BSplineCurveKnotSplitting_swiginit(self, _Geom2dConvert.new_Geom2dConvert_BSplineCurveKnotSplitting(*args))

    def NbSplits(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of points at which the analysed bspline curve should be split, in order to obtain arcs with the continuity required by this framework. all these points correspond to knot values. note that the first and last points of the curve, which bound the first and last arcs, are counted among these splitting points.

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveKnotSplitting_NbSplits(self, *args)

    def SplitValue(self, *args):
        r"""

        Parameters
        ----------
        Index: int

        Return
        -------
        int

        Description
        -----------
        Returns the split knot of index index to the split knots table computed in this framework. the returned value is an index in the knots table of the bspline curve analysed by this algorithm. notes: - if index is equal to 1, the corresponding knot gives the first point of the curve. - if index is equal to the number of split knots computed in this framework, the corresponding point is the last point of the curve. exceptions standard_rangeerror if index is less than 1 or greater than the number of split knots computed in this framework.

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveKnotSplitting_SplitValue(self, *args)

    def Splitting(self, *args):
        r"""

        Parameters
        ----------
        SplitValues: TColStd_Array1OfInteger

        Return
        -------
        None

        Description
        -----------
        Loads the splitvalues table with the split knots values computed in this framework. each value in the table is an index in the knots table of the bspline curve analysed by this algorithm. the values in splitvalues are given in ascending order and comprise the indices of the knots which give the first and last points of the curve. use two consecutive values from the table as arguments of the global function splitbsplinecurve (provided by the package geom2dconvert) to split the curve. exceptions standard_dimensionerror if the array splitvalues was not created with the following bounds: - 1, and - the number of split points computed in this framework (as given by the function nbsplits).

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveKnotSplitting_Splitting(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_BSplineCurveKnotSplitting

# Register Geom2dConvert_BSplineCurveKnotSplitting in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_BSplineCurveKnotSplitting_swigregister(Geom2dConvert_BSplineCurveKnotSplitting)
class Geom2dConvert_BSplineCurveToBezierCurve(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        BasisCurve: Geom2d_BSplineCurve

        Return
        -------
        None

        Description
        -----------
        Computes all the data needed to convert - the bspline curve basiscurve, into a series of adjacent bezier arcs. the result consists of a series of basiscurve arcs limited by points corresponding to knot values of the curve. use the available interrogation functions to ascertain the number of computed bezier arcs, and then to construct each individual bezier curve (or all bezier curves). note: parametrictolerance is not used.

        Parameters
        ----------
        BasisCurve: Geom2d_BSplineCurve
        U1: float
        U2: float
        ParametricTolerance: float

        Return
        -------
        None

        Description
        -----------
        Computes all the data needed to convert the portion of the bspline curve basiscurve limited by the two parameter values u1 and u2 for example if there is a knot uk and uk < u < uk + parametrictolerance/2 the last curve corresponds to the span [uk-1, uk] and not to [uk, uk+1] the result consists of a series of basiscurve arcs limited by points corresponding to knot values of the curve. use the available interrogation functions to ascertain the number of computed bezier arcs, and then to construct each individual bezier curve (or all bezier curves). note: parametrictolerance is not used. raises domainerror if u1 or u2 are out of the parametric bounds of the basis curve [firstparameter, lastparameter]. the tolerance criterion is parametrictolerance. raised if abs (u2 - u1) <= parametrictolerance.

        """
        _Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_swiginit(self, _Geom2dConvert.new_Geom2dConvert_BSplineCurveToBezierCurve(*args))

    def Arc(self, *args):
        r"""

        Parameters
        ----------
        Index: int

        Return
        -------
        opencascade::handle<Geom2d_BezierCurve>

        Description
        -----------
        Constructs and returns the bezier curve of index index to the table of adjacent bezier arcs computed by this algorithm. this bezier curve has the same orientation as the bspline curve analyzed in this framework. exceptions standard_outofrange if index is less than 1 or greater than the number of adjacent bezier arcs computed by this algorithm.

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_Arc(self, *args)

    def Arcs(self, *args):
        r"""

        Parameters
        ----------
        Curves: TColGeom2d_Array1OfBezierCurve

        Return
        -------
        None

        Description
        -----------
        Constructs all the bezier curves whose data is computed by this algorithm and loads these curves into the curves table. the bezier curves have the same orientation as the bspline curve analyzed in this framework. exceptions standard_dimensionerror if the curves array was not created with the following bounds: - 1 , and - the number of adjacent bezier arcs computed by this algorithm (as given by the function nbarcs).

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_Arcs(self, *args)

    def Knots(self, *args):
        r"""

        Parameters
        ----------
        TKnots: TColStd_Array1OfReal

        Return
        -------
        None

        Description
        -----------
        This methode returns the bspline's knots associated to the converted arcs raises dimensionerror if the length of curves is not equal to nbarcs + 1.

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_Knots(self, *args)

    def NbArcs(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of beziercurve arcs. if at the creation time you have decomposed the basis curve between the parametric values ufirst, ulast the number of beziercurve arcs depends on the number of knots included inside the interval [ufirst, ulast]. if you have decomposed the whole basis b-spline curve the number of beziercurve arcs nbarcs is equal to the number of knots less one.

        """
        return _Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_NbArcs(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_BSplineCurveToBezierCurve

# Register Geom2dConvert_BSplineCurveToBezierCurve in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_BSplineCurveToBezierCurve_swigregister(Geom2dConvert_BSplineCurveToBezierCurve)
class Geom2dConvert_CompCurveToBSplineCurve(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Parameterisation: Convert_ParameterisationType (optional, default to Convert_TgtThetaOver2)

        Return
        -------
        None

        Description
        -----------
        Initialize the algorithme - parameterisation is used to convert.

        Parameters
        ----------
        BasisCurve: Geom2d_BoundedCurve
        Parameterisation: Convert_ParameterisationType (optional, default to Convert_TgtThetaOver2)

        Return
        -------
        None

        Description
        -----------
        Initialize the algorithme with one curve - parameterisation is used to convert.

        """
        _Geom2dConvert.Geom2dConvert_CompCurveToBSplineCurve_swiginit(self, _Geom2dConvert.new_Geom2dConvert_CompCurveToBSplineCurve(*args))

    def Add(self, *args):
        r"""

        Parameters
        ----------
        NewCurve: Geom2d_BoundedCurve
        Tolerance: float
        After: bool (optional, default to Standard_False)

        Return
        -------
        bool

        Description
        -----------
        Append a curve in the bspline return false if the curve is not g0 with the bsplinecurve. tolerance is used to check continuity and decrease multiplicty at the common knot after is useful if basiscurve is a closed curve .

        """
        return _Geom2dConvert.Geom2dConvert_CompCurveToBSplineCurve_Add(self, *args)

    def BSplineCurve(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Geom2d_BSplineCurve>

        Description
        -----------
        No available documentation.

        """
        return _Geom2dConvert.Geom2dConvert_CompCurveToBSplineCurve_BSplineCurve(self, *args)

    def Clear(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Clear result curve.

        """
        return _Geom2dConvert.Geom2dConvert_CompCurveToBSplineCurve_Clear(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_CompCurveToBSplineCurve

# Register Geom2dConvert_CompCurveToBSplineCurve in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_CompCurveToBSplineCurve_swigregister(Geom2dConvert_CompCurveToBSplineCurve)
class Geom2dConvert_PPoint(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Empty constructor.

        Parameters
        ----------
        theParameter: float
        thePoint: gp_XY
        theD1: gp_XY

        Return
        -------
        None

        Description
        -----------
        Constructor.

        Parameters
        ----------
        theParameter: float
        theAdaptor: Adaptor2d_Curve2d

        Return
        -------
        None

        Description
        -----------
        Constructor.

        """
        _Geom2dConvert.Geom2dConvert_PPoint_swiginit(self, _Geom2dConvert.new_Geom2dConvert_PPoint(*args))

    def D1(self, *args):
        r"""
        Return
        -------
        gp_XY

        Description
        -----------
        Query the first derivatives.

        """
        return _Geom2dConvert.Geom2dConvert_PPoint_D1(self, *args)

    def Dist(self, *args):
        r"""

        Parameters
        ----------
        theOth: Geom2dConvert_PPoint

        Return
        -------
        float

        Description
        -----------
        Compute the distance betwwen two 2d points.

        """
        return _Geom2dConvert.Geom2dConvert_PPoint_Dist(self, *args)

    def Parameter(self, *args):
        r"""
        Return
        -------
        float

        Description
        -----------
        Query the parmeter value.

        """
        return _Geom2dConvert.Geom2dConvert_PPoint_Parameter(self, *args)

    def Point(self, *args):
        r"""
        Return
        -------
        gp_XY

        Description
        -----------
        Query the point location.

        """
        return _Geom2dConvert.Geom2dConvert_PPoint_Point(self, *args)

    def SetD1(self, *args):
        r"""

        Parameters
        ----------
        theD1: gp_XY

        Return
        -------
        None

        Description
        -----------
        Change the value of the derivative at the point.

        """
        return _Geom2dConvert.Geom2dConvert_PPoint_SetD1(self, *args)

    def __ne_wrapper__(self, other):
        return _Geom2dConvert.Geom2dConvert_PPoint___ne_wrapper__(self, other)

    def __ne__(self, right):
        try:
            return self.__ne_wrapper__(right)
        except:
            return True


    def __eq_wrapper__(self, other):
        return _Geom2dConvert.Geom2dConvert_PPoint___eq_wrapper__(self, other)

    def __eq__(self, right):
        try:
            return self.__eq_wrapper__(right)
        except:
            return False


    __repr__ = _dumps_object

    __swig_destroy__ = _Geom2dConvert.delete_Geom2dConvert_PPoint

# Register Geom2dConvert_PPoint in _Geom2dConvert:
_Geom2dConvert.Geom2dConvert_PPoint_swigregister(Geom2dConvert_PPoint)



@deprecated
def geom2dconvert_C0BSplineToArrayOfC1BSplineCurve(*args):
	return geom2dconvert.C0BSplineToArrayOfC1BSplineCurve(*args)

@deprecated
def geom2dconvert_C0BSplineToArrayOfC1BSplineCurve(*args):
	return geom2dconvert.C0BSplineToArrayOfC1BSplineCurve(*args)

@deprecated
def geom2dconvert_C0BSplineToC1BSplineCurve(*args):
	return geom2dconvert.C0BSplineToC1BSplineCurve(*args)

@deprecated
def geom2dconvert_ConcatC1(*args):
	return geom2dconvert.ConcatC1(*args)

@deprecated
def geom2dconvert_ConcatC1(*args):
	return geom2dconvert.ConcatC1(*args)

@deprecated
def geom2dconvert_ConcatG1(*args):
	return geom2dconvert.ConcatG1(*args)

@deprecated
def geom2dconvert_CurveToBSplineCurve(*args):
	return geom2dconvert.CurveToBSplineCurve(*args)

@deprecated
def geom2dconvert_SplitBSplineCurve(*args):
	return geom2dconvert.SplitBSplineCurve(*args)

@deprecated
def geom2dconvert_SplitBSplineCurve(*args):
	return geom2dconvert.SplitBSplineCurve(*args)


