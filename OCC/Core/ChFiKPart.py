# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
ChFiKPart module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_chfikpart.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _ChFiKPart
else:
    import _ChFiKPart

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
    __swig_destroy__ = _ChFiKPart.delete_SwigPyIterator

    def value(self):
        return _ChFiKPart.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _ChFiKPart.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _ChFiKPart.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _ChFiKPart.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _ChFiKPart.SwigPyIterator_equal(self, x)

    def copy(self):
        return _ChFiKPart.SwigPyIterator_copy(self)

    def next(self):
        return _ChFiKPart.SwigPyIterator_next(self)

    def __next__(self):
        return _ChFiKPart.SwigPyIterator___next__(self)

    def previous(self):
        return _ChFiKPart.SwigPyIterator_previous(self)

    def advance(self, n):
        return _ChFiKPart.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _ChFiKPart.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _ChFiKPart.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _ChFiKPart.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _ChFiKPart.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _ChFiKPart.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _ChFiKPart.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _ChFiKPart:
_ChFiKPart.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _ChFiKPart.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.Adaptor2d
import OCC.Core.Geom2d
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.TopOpeBRepDS
import OCC.Core.Geom
import OCC.Core.TopAbs
import OCC.Core.TopOpeBRepTool
import OCC.Core.BRepClass3d
import OCC.Core.TopoDS
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TopLoc
import OCC.Core.IntCurveSurface
import OCC.Core.math
import OCC.Core.Adaptor3d
import OCC.Core.Intf
import OCC.Core.Bnd
import OCC.Core.BVH
import OCC.Core.IntSurf
import OCC.Core.TopTools
import OCC.Core.IntCurvesFace
import OCC.Core.BRepAdaptor
import OCC.Core.GeomAdaptor
import OCC.Core.Geom2dAdaptor
import OCC.Core.TopExp
import OCC.Core.Extrema
import OCC.Core.ChFiDS
import OCC.Core.Law

from enum import IntEnum
from OCC.Core.Exception import *



class ChFiKPart_RstMap(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def begin(self):
        return _ChFiKPart.ChFiKPart_RstMap_begin(self)

    def end(self):
        return _ChFiKPart.ChFiKPart_RstMap_end(self)

    def cbegin(self):
        return _ChFiKPart.ChFiKPart_RstMap_cbegin(self)

    def cend(self):
        return _ChFiKPart.ChFiKPart_RstMap_cend(self)

    def __init__(self, *args):
        _ChFiKPart.ChFiKPart_RstMap_swiginit(self, _ChFiKPart.new_ChFiKPart_RstMap(*args))

    def Exchange(self, theOther):
        return _ChFiKPart.ChFiKPart_RstMap_Exchange(self, theOther)

    def Assign(self, theOther):
        return _ChFiKPart.ChFiKPart_RstMap_Assign(self, theOther)

    def Set(self, theOther):
        return _ChFiKPart.ChFiKPart_RstMap_Set(self, theOther)

    def ReSize(self, N):
        return _ChFiKPart.ChFiKPart_RstMap_ReSize(self, N)

    def Bind(self, theKey, theItem):
        return _ChFiKPart.ChFiKPart_RstMap_Bind(self, theKey, theItem)

    def Bound(self, theKey, theItem):
        return _ChFiKPart.ChFiKPart_RstMap_Bound(self, theKey, theItem)

    def IsBound(self, theKey):
        return _ChFiKPart.ChFiKPart_RstMap_IsBound(self, theKey)

    def UnBind(self, theKey):
        return _ChFiKPart.ChFiKPart_RstMap_UnBind(self, theKey)

    def Seek(self, theKey):
        return _ChFiKPart.ChFiKPart_RstMap_Seek(self, theKey)

    def Find(self, *args):
        return _ChFiKPart.ChFiKPart_RstMap_Find(self, *args)

    def ChangeSeek(self, theKey):
        return _ChFiKPart.ChFiKPart_RstMap_ChangeSeek(self, theKey)

    def ChangeFind(self, theKey):
        return _ChFiKPart.ChFiKPart_RstMap_ChangeFind(self, theKey)

    def __call__(self, *args):
        return _ChFiKPart.ChFiKPart_RstMap___call__(self, *args)

    def Clear(self, *args):
        return _ChFiKPart.ChFiKPart_RstMap_Clear(self, *args)
    __swig_destroy__ = _ChFiKPart.delete_ChFiKPart_RstMap

    def Size(self):
        return _ChFiKPart.ChFiKPart_RstMap_Size(self)

    def Keys(self):
        return _ChFiKPart.ChFiKPart_RstMap_Keys(self)

# Register ChFiKPart_RstMap in _ChFiKPart:
_ChFiKPart.ChFiKPart_RstMap_swigregister(ChFiKPart_RstMap)
class ChFiKPart_ComputeData(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def Compute(*args):
        r"""

        Parameters
        ----------
        DStr: TopOpeBRepDS_DataStructure
        Data: ChFiDS_SurfData
        S1: Adaptor3d_Surface
        S2: Adaptor3d_Surface
        Or1: TopAbs_Orientation
        Or2: TopAbs_Orientation
        Sp: ChFiDS_Spine
        Iedge: int

        Return
        -------
        bool

        Description
        -----------
        Computes a simple fillet in several particular cases.

        """
        return _ChFiKPart.ChFiKPart_ComputeData_Compute(*args)

    @staticmethod
    def ComputeCorner(*args):
        r"""

        Parameters
        ----------
        DStr: TopOpeBRepDS_DataStructure
        Data: ChFiDS_SurfData
        S1: Adaptor3d_Surface
        S2: Adaptor3d_Surface
        OrFace1: TopAbs_Orientation
        OrFace2: TopAbs_Orientation
        Or1: TopAbs_Orientation
        Or2: TopAbs_Orientation
        minRad: float
        majRad: float
        P1S1: gp_Pnt2d
        P2S1: gp_Pnt2d
        P1S2: gp_Pnt2d
        P2S2: gp_Pnt2d

        Return
        -------
        bool

        Description
        -----------
        Computes a toric or spheric corner fillet.

        Parameters
        ----------
        DStr: TopOpeBRepDS_DataStructure
        Data: ChFiDS_SurfData
        S1: Adaptor3d_Surface
        S2: Adaptor3d_Surface
        OrFace1: TopAbs_Orientation
        OrFace2: TopAbs_Orientation
        Or1: TopAbs_Orientation
        Or2: TopAbs_Orientation
        Rad: float
        PS1: gp_Pnt2d
        P1S2: gp_Pnt2d
        P2S2: gp_Pnt2d

        Return
        -------
        bool

        Description
        -----------
        Computes spheric corner fillet with non iso pcurve on s2.

        Parameters
        ----------
        DStr: TopOpeBRepDS_DataStructure
        Data: ChFiDS_SurfData
        S: Adaptor3d_Surface
        S1: Adaptor3d_Surface
        S2: Adaptor3d_Surface
        OfS: TopAbs_Orientation
        OS: TopAbs_Orientation
        OS1: TopAbs_Orientation
        OS2: TopAbs_Orientation
        Radius: float

        Return
        -------
        bool

        Description
        -----------
        Computes a toric corner rotule.

        """
        return _ChFiKPart.ChFiKPart_ComputeData_ComputeCorner(*args)

    __repr__ = _dumps_object


    def __init__(self):
        _ChFiKPart.ChFiKPart_ComputeData_swiginit(self, _ChFiKPart.new_ChFiKPart_ComputeData())
    __swig_destroy__ = _ChFiKPart.delete_ChFiKPart_ComputeData

# Register ChFiKPart_ComputeData in _ChFiKPart:
_ChFiKPart.ChFiKPart_ComputeData_swigregister(ChFiKPart_ComputeData)



@deprecated
def ChFiKPart_ComputeData_Compute(*args):
	return ChFiKPart_ComputeData.Compute(*args)

@deprecated
def ChFiKPart_ComputeData_ComputeCorner(*args):
	return ChFiKPart_ComputeData.ComputeCorner(*args)

@deprecated
def ChFiKPart_ComputeData_ComputeCorner(*args):
	return ChFiKPart_ComputeData.ComputeCorner(*args)

@deprecated
def ChFiKPart_ComputeData_ComputeCorner(*args):
	return ChFiKPart_ComputeData.ComputeCorner(*args)


