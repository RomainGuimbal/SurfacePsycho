# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
Sweep module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_sweep.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _Sweep
else:
    import _Sweep

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
    __swig_destroy__ = _Sweep.delete_SwigPyIterator

    def value(self):
        return _Sweep.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _Sweep.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _Sweep.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _Sweep.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _Sweep.SwigPyIterator_equal(self, x)

    def copy(self):
        return _Sweep.SwigPyIterator_copy(self)

    def next(self):
        return _Sweep.SwigPyIterator_next(self)

    def __next__(self):
        return _Sweep.SwigPyIterator___next__(self)

    def previous(self):
        return _Sweep.SwigPyIterator_previous(self)

    def advance(self, n):
        return _Sweep.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _Sweep.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _Sweep.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _Sweep.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _Sweep.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _Sweep.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _Sweep.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _Sweep:
_Sweep.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _Sweep.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TopAbs

from enum import IntEnum
from OCC.Core.Exception import *



class Sweep_NumShape(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Creates a dummy indexed edge.

        Parameters
        ----------
        Index: int
        Type: TopAbs_ShapeEnum
        Closed: bool (optional, default to Standard_False)
        BegInf: bool (optional, default to Standard_False)
        EndInf: bool (optional, default to Standard_False)

        Return
        -------
        None

        Description
        -----------
        Creates a new simple indexed edge. //! for an edge: index is the number of vertices (0, 1 or 2),type is topabs_edge, closed is true if it is a closed edge, beginf is true if the edge is infinite at the begenning, endinf is true if the edge is infinite at the end. //! for a vertex: index is the index of the vertex in the edge (1 or 2), type is topabsvertex, all the other fields have no meanning.

        """
        _Sweep.Sweep_NumShape_swiginit(self, _Sweep.new_Sweep_NumShape(*args))

    def BegInfinite(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_BegInfinite(self, *args)

    def Closed(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_Closed(self, *args)

    def EndInfinite(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_EndInfinite(self, *args)

    def Index(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_Index(self, *args)

    def Init(self, *args):
        r"""

        Parameters
        ----------
        Index: int
        Type: TopAbs_ShapeEnum
        Closed: bool (optional, default to Standard_False)
        BegInf: bool (optional, default to Standard_False)
        EndInf: bool (optional, default to Standard_False)

        Return
        -------
        None

        Description
        -----------
        Reinitialize a simple indexed edge. //! for an edge: index is the number of vertices (0, 1 or 2),type is topabs_edge, closed is true if it is a closed edge, beginf is true if the edge is infinite at the begenning, endinf is true if the edge is infinite at the end. //! for a vertex: index is the index of the vertex in the edge (1 or 2), type is topabsvertex, closed is true if it is the vertex of a closed edge, all the other fields have no meanning.

        """
        return _Sweep.Sweep_NumShape_Init(self, *args)

    def Orientation(self, *args):
        r"""
        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_Orientation(self, *args)

    def Type(self, *args):
        r"""
        Return
        -------
        TopAbs_ShapeEnum

        Description
        -----------
        No available documentation.

        """
        return _Sweep.Sweep_NumShape_Type(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Sweep.delete_Sweep_NumShape

# Register Sweep_NumShape in _Sweep:
_Sweep.Sweep_NumShape_swigregister(Sweep_NumShape)
class Sweep_NumShapeIterator(object):
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
        _Sweep.Sweep_NumShapeIterator_swiginit(self, _Sweep.new_Sweep_NumShapeIterator(*args))

    def Init(self, *args):
        r"""

        Parameters
        ----------
        aShape: Sweep_NumShape

        Return
        -------
        None

        Description
        -----------
        Reset the numshapeiterator on sub-shapes of <ashape>.

        """
        return _Sweep.Sweep_NumShapeIterator_Init(self, *args)

    def More(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if there is a current sub-shape.

        """
        return _Sweep.Sweep_NumShapeIterator_More(self, *args)

    def Next(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        Moves to the next sub-shape.

        """
        return _Sweep.Sweep_NumShapeIterator_Next(self, *args)

    def Orientation(self, *args):
        r"""
        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        Returns the orientation of the current sub-shape.

        """
        return _Sweep.Sweep_NumShapeIterator_Orientation(self, *args)

    def Value(self, *args):
        r"""
        Return
        -------
        Sweep_NumShape

        Description
        -----------
        Returns the current sub-shape.

        """
        return _Sweep.Sweep_NumShapeIterator_Value(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Sweep.delete_Sweep_NumShapeIterator

# Register Sweep_NumShapeIterator in _Sweep:
_Sweep.Sweep_NumShapeIterator_swigregister(Sweep_NumShapeIterator)
class Sweep_NumShapeTool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        aShape: Sweep_NumShape

        Return
        -------
        None

        Description
        -----------
        Create a new numshapetool with <ashape>. the tool must prepare an indexation for all the subshapes of this shape.

        """
        _Sweep.Sweep_NumShapeTool_swiginit(self, _Sweep.new_Sweep_NumShapeTool(*args))

    def FirstVertex(self, *args):
        r"""
        Return
        -------
        Sweep_NumShape

        Description
        -----------
        Returns the first vertex.

        """
        return _Sweep.Sweep_NumShapeTool_FirstVertex(self, *args)

    def HasFirstVertex(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if there is a first vertex in the shape.

        """
        return _Sweep.Sweep_NumShapeTool_HasFirstVertex(self, *args)

    def HasLastVertex(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if there is a last vertex in the shape.

        """
        return _Sweep.Sweep_NumShapeTool_HasLastVertex(self, *args)

    def Index(self, *args):
        r"""

        Parameters
        ----------
        aShape: Sweep_NumShape

        Return
        -------
        int

        Description
        -----------
        Returns the index of <ashape>.

        """
        return _Sweep.Sweep_NumShapeTool_Index(self, *args)

    def LastVertex(self, *args):
        r"""
        Return
        -------
        Sweep_NumShape

        Description
        -----------
        Returns the last vertex.

        """
        return _Sweep.Sweep_NumShapeTool_LastVertex(self, *args)

    def NbShapes(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of subshapes in the shape.

        """
        return _Sweep.Sweep_NumShapeTool_NbShapes(self, *args)

    def Orientation(self, *args):
        r"""

        Parameters
        ----------
        aShape: Sweep_NumShape

        Return
        -------
        TopAbs_Orientation

        Description
        -----------
        Returns the orientation of <ashape>.

        """
        return _Sweep.Sweep_NumShapeTool_Orientation(self, *args)

    def Shape(self, *args):
        r"""

        Parameters
        ----------
        anIndex: int

        Return
        -------
        Sweep_NumShape

        Description
        -----------
        Returns the shape at index anindex.

        """
        return _Sweep.Sweep_NumShapeTool_Shape(self, *args)

    def Type(self, *args):
        r"""

        Parameters
        ----------
        aShape: Sweep_NumShape

        Return
        -------
        TopAbs_ShapeEnum

        Description
        -----------
        Returns the type of <ashape>.

        """
        return _Sweep.Sweep_NumShapeTool_Type(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _Sweep.delete_Sweep_NumShapeTool

# Register Sweep_NumShapeTool in _Sweep:
_Sweep.Sweep_NumShapeTool_swigregister(Sweep_NumShapeTool)


