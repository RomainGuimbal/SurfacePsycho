# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
BRepTopAdaptor module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_breptopadaptor.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _BRepTopAdaptor
else:
    import _BRepTopAdaptor

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
    __swig_destroy__ = _BRepTopAdaptor.delete_SwigPyIterator

    def value(self):
        return _BRepTopAdaptor.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _BRepTopAdaptor.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _BRepTopAdaptor.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _BRepTopAdaptor.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _BRepTopAdaptor.SwigPyIterator_equal(self, x)

    def copy(self):
        return _BRepTopAdaptor.SwigPyIterator_copy(self)

    def next(self):
        return _BRepTopAdaptor.SwigPyIterator_next(self)

    def __next__(self):
        return _BRepTopAdaptor.SwigPyIterator___next__(self)

    def previous(self):
        return _BRepTopAdaptor.SwigPyIterator_previous(self)

    def advance(self, n):
        return _BRepTopAdaptor.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _BRepTopAdaptor.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _BRepTopAdaptor.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _BRepTopAdaptor.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _BRepTopAdaptor.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _BRepTopAdaptor.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _BRepTopAdaptor.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _BRepTopAdaptor:
_BRepTopAdaptor.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _BRepTopAdaptor.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.TopoDS
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.Adaptor3d
import OCC.Core.Geom
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.Adaptor2d
import OCC.Core.Geom2d
import OCC.Core.math
import OCC.Core.BRepAdaptor
import OCC.Core.GeomAdaptor
import OCC.Core.Geom2dAdaptor

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_BRepTopAdaptor_HVertex_Create():
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_HVertex_Create()

def Handle_BRepTopAdaptor_HVertex_DownCast(t):
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_HVertex_DownCast(t)

def Handle_BRepTopAdaptor_HVertex_IsNull(t):
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_HVertex_IsNull(t)

def Handle_BRepTopAdaptor_TopolTool_Create():
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_TopolTool_Create()

def Handle_BRepTopAdaptor_TopolTool_DownCast(t):
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_TopolTool_DownCast(t)

def Handle_BRepTopAdaptor_TopolTool_IsNull(t):
    return _BRepTopAdaptor.Handle_BRepTopAdaptor_TopolTool_IsNull(t)
class BRepTopAdaptor_MapOfShapeTool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def begin(self):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_begin(self)

    def end(self):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_end(self)

    def cbegin(self):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_cbegin(self)

    def cend(self):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_cend(self)

    def __init__(self, *args):
        _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_swiginit(self, _BRepTopAdaptor.new_BRepTopAdaptor_MapOfShapeTool(*args))

    def Exchange(self, theOther):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Exchange(self, theOther)

    def Assign(self, theOther):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Assign(self, theOther)

    def Set(self, theOther):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Set(self, theOther)

    def ReSize(self, N):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_ReSize(self, N)

    def Bind(self, theKey, theItem):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Bind(self, theKey, theItem)

    def Bound(self, theKey, theItem):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Bound(self, theKey, theItem)

    def IsBound(self, theKey):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_IsBound(self, theKey)

    def UnBind(self, theKey):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_UnBind(self, theKey)

    def Seek(self, theKey):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Seek(self, theKey)

    def Find(self, *args):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Find(self, *args)

    def ChangeSeek(self, theKey):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_ChangeSeek(self, theKey)

    def ChangeFind(self, theKey):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_ChangeFind(self, theKey)

    def __call__(self, *args):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool___call__(self, *args)

    def Clear(self, *args):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Clear(self, *args)
    __swig_destroy__ = _BRepTopAdaptor.delete_BRepTopAdaptor_MapOfShapeTool

    def Size(self):
        return _BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_Size(self)

# Register BRepTopAdaptor_MapOfShapeTool in _BRepTopAdaptor:
_BRepTopAdaptor.BRepTopAdaptor_MapOfShapeTool_swigregister(BRepTopAdaptor_MapOfShapeTool)
class BRepTopAdaptor_FClass2d(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        F: TopoDS_Face
        Tol: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BRepTopAdaptor.BRepTopAdaptor_FClass2d_swiginit(self, _BRepTopAdaptor.new_BRepTopAdaptor_FClass2d(*args))

    def Copy(self, *args):
        r"""

        Parameters
        ----------
        Other: BRepTopAdaptor_FClass2d

        Return
        -------
        BRepTopAdaptor_FClass2d

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_FClass2d_Copy(self, *args)

    def Destroy(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_FClass2d_Destroy(self, *args)

    def Perform(self, *args):
        r"""

        Parameters
        ----------
        Puv: gp_Pnt2d
        RecadreOnPeriodic: bool (optional, default to Standard_True)

        Return
        -------
        TopAbs_State

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_FClass2d_Perform(self, *args)

    def PerformInfinitePoint(self, *args):
        r"""
        Return
        -------
        TopAbs_State

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_FClass2d_PerformInfinitePoint(self, *args)

    def TestOnRestriction(self, *args):
        r"""

        Parameters
        ----------
        Puv: gp_Pnt2d
        Tol: float
        RecadreOnPeriodic: bool (optional, default to Standard_True)

        Return
        -------
        TopAbs_State

        Description
        -----------
        Test a point with +- an offset (tol) and returns on if some points are out an some are in (caution: internal use . see the code for more details).

        """
        return _BRepTopAdaptor.BRepTopAdaptor_FClass2d_TestOnRestriction(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _BRepTopAdaptor.delete_BRepTopAdaptor_FClass2d

# Register BRepTopAdaptor_FClass2d in _BRepTopAdaptor:
_BRepTopAdaptor.BRepTopAdaptor_FClass2d_swigregister(BRepTopAdaptor_FClass2d)
class BRepTopAdaptor_HVertex(OCC.Core.Adaptor3d.Adaptor3d_HVertex):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        Vtx: TopoDS_Vertex
        Curve: BRepAdaptor_Curve2d

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BRepTopAdaptor.BRepTopAdaptor_HVertex_swiginit(self, _BRepTopAdaptor.new_BRepTopAdaptor_HVertex(*args))

    def ChangeVertex(self, *args):
        r"""
        Return
        -------
        TopoDS_Vertex

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_HVertex_ChangeVertex(self, *args)

    def Vertex(self, *args):
        r"""
        Return
        -------
        TopoDS_Vertex

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_HVertex_Vertex(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BRepTopAdaptor_HVertex_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepTopAdaptor.delete_BRepTopAdaptor_HVertex

# Register BRepTopAdaptor_HVertex in _BRepTopAdaptor:
_BRepTopAdaptor.BRepTopAdaptor_HVertex_swigregister(BRepTopAdaptor_HVertex)
class BRepTopAdaptor_Tool(object):
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

        Parameters
        ----------
        F: TopoDS_Face
        Tol2d: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Surface: Adaptor3d_Surface
        Tol2d: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BRepTopAdaptor.BRepTopAdaptor_Tool_swiginit(self, _BRepTopAdaptor.new_BRepTopAdaptor_Tool(*args))

    def Destroy(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_Tool_Destroy(self, *args)

    def GetSurface(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Adaptor3d_Surface>

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_Tool_GetSurface(self, *args)

    def GetTopolTool(self, *args):
        r"""
        Return
        -------
        opencascade::handle<BRepTopAdaptor_TopolTool>

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_Tool_GetTopolTool(self, *args)

    def Init(self, *args):
        r"""

        Parameters
        ----------
        F: TopoDS_Face
        Tol2d: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Surface: Adaptor3d_Surface
        Tol2d: float

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_Tool_Init(self, *args)

    def SetTopolTool(self, *args):
        r"""

        Parameters
        ----------
        TT: BRepTopAdaptor_TopolTool

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_Tool_SetTopolTool(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _BRepTopAdaptor.delete_BRepTopAdaptor_Tool

# Register BRepTopAdaptor_Tool in _BRepTopAdaptor:
_BRepTopAdaptor.BRepTopAdaptor_Tool_swigregister(BRepTopAdaptor_Tool)
class BRepTopAdaptor_TopolTool(OCC.Core.Adaptor3d.Adaptor3d_TopolTool):
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

        Parameters
        ----------
        Surface: Adaptor3d_Surface

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _BRepTopAdaptor.BRepTopAdaptor_TopolTool_swiginit(self, _BRepTopAdaptor.new_BRepTopAdaptor_TopolTool(*args))

    def Destroy(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_TopolTool_Destroy(self, *args)

    def Initialize(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        S: Adaptor3d_Surface

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        Parameters
        ----------
        Curve: Adaptor2d_Curve2d

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_TopolTool_Initialize(self, *args)

    def Orientation(self, *args):
        r"""

        Parameters
        ----------
        C: Adaptor2d_Curve2d

        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        If the function returns the orientation of the arc. if the orientation is forward or reversed, the arc is a 'real' limit of the surface. if the orientation is internal or external, the arc is considered as an arc on the surface.

        Parameters
        ----------
        C: Adaptor3d_HVertex

        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        If the function returns the orientation of the arc. if the orientation is forward or reversed, the arc is a 'real' limit of the surface. if the orientation is internal or external, the arc is considered as an arc on the surface.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_TopolTool_Orientation(self, *args)

    def Tol3d(self, *args):
        r"""

        Parameters
        ----------
        C: Adaptor2d_Curve2d

        Return
        -------
        float

        Description
        -----------
        Returns 3d tolerance of the arc c.

        Parameters
        ----------
        V: Adaptor3d_HVertex

        Return
        -------
        float

        Description
        -----------
        Returns 3d tolerance of the vertex v.

        """
        return _BRepTopAdaptor.BRepTopAdaptor_TopolTool_Tol3d(self, *args)


    @staticmethod
    def DownCast(t):
      return Handle_BRepTopAdaptor_TopolTool_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepTopAdaptor.delete_BRepTopAdaptor_TopolTool

# Register BRepTopAdaptor_TopolTool in _BRepTopAdaptor:
_BRepTopAdaptor.BRepTopAdaptor_TopolTool_swigregister(BRepTopAdaptor_TopolTool)

BRepTopAdaptor_SeqOfPtr=OCC.Core.TColStd.TColStd_SequenceOfAddress


