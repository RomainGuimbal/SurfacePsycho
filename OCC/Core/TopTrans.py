# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
TopTrans module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_toptrans.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _TopTrans
else:
    import _TopTrans

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
    __swig_destroy__ = _TopTrans.delete_SwigPyIterator

    def value(self):
        return _TopTrans.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _TopTrans.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _TopTrans.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _TopTrans.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _TopTrans.SwigPyIterator_equal(self, x)

    def copy(self):
        return _TopTrans.SwigPyIterator_copy(self)

    def next(self):
        return _TopTrans.SwigPyIterator_next(self)

    def __next__(self):
        return _TopTrans.SwigPyIterator___next__(self)

    def previous(self):
        return _TopTrans.SwigPyIterator_previous(self)

    def advance(self, n):
        return _TopTrans.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _TopTrans.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _TopTrans.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _TopTrans.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _TopTrans.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _TopTrans.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _TopTrans.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _TopTrans:
_TopTrans.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _TopTrans.process_exception(error, method_name, class_name)

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



class TopTrans_Array2OfOrientation(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _TopTrans.TopTrans_Array2OfOrientation_swiginit(self, _TopTrans.new_TopTrans_Array2OfOrientation(*args))

    def Init(self, theValue):
        return _TopTrans.TopTrans_Array2OfOrientation_Init(self, theValue)

    def Size(self):
        return _TopTrans.TopTrans_Array2OfOrientation_Size(self)

    def Length(self):
        return _TopTrans.TopTrans_Array2OfOrientation_Length(self)

    def NbRows(self):
        return _TopTrans.TopTrans_Array2OfOrientation_NbRows(self)

    def NbColumns(self):
        return _TopTrans.TopTrans_Array2OfOrientation_NbColumns(self)

    def RowLength(self):
        return _TopTrans.TopTrans_Array2OfOrientation_RowLength(self)

    def ColLength(self):
        return _TopTrans.TopTrans_Array2OfOrientation_ColLength(self)

    def LowerRow(self):
        return _TopTrans.TopTrans_Array2OfOrientation_LowerRow(self)

    def UpperRow(self):
        return _TopTrans.TopTrans_Array2OfOrientation_UpperRow(self)

    def LowerCol(self):
        return _TopTrans.TopTrans_Array2OfOrientation_LowerCol(self)

    def UpperCol(self):
        return _TopTrans.TopTrans_Array2OfOrientation_UpperCol(self)

    def IsDeletable(self):
        return _TopTrans.TopTrans_Array2OfOrientation_IsDeletable(self)

    def Assign(self, theOther):
        return _TopTrans.TopTrans_Array2OfOrientation_Assign(self, theOther)

    def Move(self, theOther):
        return _TopTrans.TopTrans_Array2OfOrientation_Move(self, theOther)

    def Set(self, *args):
        return _TopTrans.TopTrans_Array2OfOrientation_Set(self, *args)

    def Value(self, theRow, theCol):
        return _TopTrans.TopTrans_Array2OfOrientation_Value(self, theRow, theCol)

    def ChangeValue(self, theRow, theCol):
        return _TopTrans.TopTrans_Array2OfOrientation_ChangeValue(self, theRow, theCol)

    def __call__(self, *args):
        return _TopTrans.TopTrans_Array2OfOrientation___call__(self, *args)

    def SetValue(self, theRow, theCol, theItem):
        return _TopTrans.TopTrans_Array2OfOrientation_SetValue(self, theRow, theCol, theItem)

    def Resize(self, theRowLower, theRowUpper, theColLower, theColUpper, theToCopyData):
        return _TopTrans.TopTrans_Array2OfOrientation_Resize(self, theRowLower, theRowUpper, theColLower, theColUpper, theToCopyData)
    __swig_destroy__ = _TopTrans.delete_TopTrans_Array2OfOrientation

# Register TopTrans_Array2OfOrientation in _TopTrans:
_TopTrans.TopTrans_Array2OfOrientation_swigregister(TopTrans_Array2OfOrientation)
class TopTrans_CurveTransition(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Create an empty curve transition.

        """
        _TopTrans.TopTrans_CurveTransition_swiginit(self, _TopTrans.new_TopTrans_CurveTransition(*args))

    def Compare(self, *args):
        r"""

        Parameters
        ----------
        Tole: float
        Tang: gp_Dir
        Norm: gp_Dir
        Curv: float
        S: TopAbs_Orientation
        Or: TopAbs_Orientation

        Return
        -------
        None

        Description
        -----------
        Add a curve element to the boundary. if or is reversed the curve is before the intersection, else if or is forward the curv is after the intersection and if or is internal the intersection is in the middle of the curv.

        """
        return _TopTrans.TopTrans_CurveTransition_Compare(self, *args)

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
        Initialize a transition with the local description of a curve.

        Parameters
        ----------
        Tgt: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Initialize a transition with the local description of a straight line.

        """
        return _TopTrans.TopTrans_CurveTransition_Reset(self, *args)

    def StateAfter(self, *args):
        r"""
        Return
        -------
        TopAbs_State

        Description
        -----------
        Returns the state of the curve after the intersection, this is the position relative to the boundary of a point very close to the intersection on the positive side of the tangent.

        """
        return _TopTrans.TopTrans_CurveTransition_StateAfter(self, *args)

    def StateBefore(self, *args):
        r"""
        Return
        -------
        TopAbs_State

        Description
        -----------
        Returns the state of the curve before the intersection, this is the position relative to the boundary of a point very close to the intersection on the negative side of the tangent.

        """
        return _TopTrans.TopTrans_CurveTransition_StateBefore(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _TopTrans.delete_TopTrans_CurveTransition

# Register TopTrans_CurveTransition in _TopTrans:
_TopTrans.TopTrans_CurveTransition_swigregister(TopTrans_CurveTransition)
class TopTrans_SurfaceTransition(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Create an empty surface transition.

        """
        _TopTrans.TopTrans_SurfaceTransition_swiginit(self, _TopTrans.new_TopTrans_SurfaceTransition(*args))

    def Compare(self, *args):
        r"""

        Parameters
        ----------
        Tole: float
        Norm: gp_Dir
        MaxD: gp_Dir
        MinD: gp_Dir
        MaxCurv: float
        MinCurv: float
        S: TopAbs_Orientation
        O: TopAbs_Orientation

        Return
        -------
        None

        Description
        -----------
        Add a face element to the boundary. //! - s defines topological orientation for the face: s forward means: along the intersection curve on the reference surface, transition states while crossing the face are out,in. s reversed means states are in,out. s internal means states are in,in. //! - o defines curve's position on face: o forward means the face is before the intersection o reversed means the face is after o internal means the curve intersection is in the face. prequesitory: norm oriented outside 'geometric matter'.

        Parameters
        ----------
        Tole: float
        Norm: gp_Dir
        S: TopAbs_Orientation
        O: TopAbs_Orientation

        Return
        -------
        None

        Description
        -----------
        Add a plane or a cylindric face to the boundary.

        """
        return _TopTrans.TopTrans_SurfaceTransition_Compare(self, *args)

    @staticmethod
    def GetAfter(*args):
        r"""

        Parameters
        ----------
        Tran: TopAbs_Orientation

        Return
        -------
        TopAbs_State

        Description
        -----------
        No available documentation.

        """
        return _TopTrans.TopTrans_SurfaceTransition_GetAfter(*args)

    @staticmethod
    def GetBefore(*args):
        r"""

        Parameters
        ----------
        Tran: TopAbs_Orientation

        Return
        -------
        TopAbs_State

        Description
        -----------
        No available documentation.

        """
        return _TopTrans.TopTrans_SurfaceTransition_GetBefore(*args)

    def Reset(self, *args):
        r"""

        Parameters
        ----------
        Tgt: gp_Dir
        Norm: gp_Dir
        MaxD: gp_Dir
        MinD: gp_Dir
        MaxCurv: float
        MinCurv: float

        Return
        -------
        None

        Description
        -----------
        Initialize a surface transition with the local description of the intersection curve and of the reference surface. prequesitory: norm oriented outside 'geometric matter'.

        Parameters
        ----------
        Tgt: gp_Dir
        Norm: gp_Dir

        Return
        -------
        None

        Description
        -----------
        Initialize a surface transition with the local description of a straight line.

        """
        return _TopTrans.TopTrans_SurfaceTransition_Reset(self, *args)

    def StateAfter(self, *args):
        r"""
        Return
        -------
        TopAbs_State

        Description
        -----------
        Returns the state of the reference surface after interference, this is the position relative to the surface of a point very close to the intersection on the positive side of the tangent.

        """
        return _TopTrans.TopTrans_SurfaceTransition_StateAfter(self, *args)

    def StateBefore(self, *args):
        r"""
        Return
        -------
        TopAbs_State

        Description
        -----------
        Returns the state of the reference surface before the interference, this is the position relative to the surface of a point very close to the intersection on the negative side of the tangent.

        """
        return _TopTrans.TopTrans_SurfaceTransition_StateBefore(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _TopTrans.delete_TopTrans_SurfaceTransition

# Register TopTrans_SurfaceTransition in _TopTrans:
_TopTrans.TopTrans_SurfaceTransition_swigregister(TopTrans_SurfaceTransition)



@deprecated
def TopTrans_SurfaceTransition_GetAfter(*args):
	return TopTrans_SurfaceTransition.GetAfter(*args)

@deprecated
def TopTrans_SurfaceTransition_GetBefore(*args):
	return TopTrans_SurfaceTransition.GetBefore(*args)


