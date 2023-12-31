# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
BiTgte module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_bitgte.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_BiTgte')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_BiTgte')
    _BiTgte = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_BiTgte', [dirname(__file__)])
        except ImportError:
            import _BiTgte
            return _BiTgte
        try:
            _mod = imp.load_module('_BiTgte', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _BiTgte = swig_import_helper()
    del swig_import_helper
else:
    import _BiTgte
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
    __swig_destroy__ = _BiTgte.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _BiTgte.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BiTgte.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BiTgte.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _BiTgte.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _BiTgte.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _BiTgte.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _BiTgte.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _BiTgte.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _BiTgte.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BiTgte.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _BiTgte.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _BiTgte.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BiTgte.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BiTgte.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BiTgte.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _BiTgte.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _BiTgte.SwigPyIterator_swigregister
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
    return _BiTgte.process_exception(error, method_name, class_name)
process_exception = _BiTgte.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TopoDS
import OCC.Core.Message
import OCC.Core.TCollection
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.TopTools
import OCC.Core.Geom
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.Geom2d
import OCC.Core.Adaptor3d
import OCC.Core.Adaptor2d
import OCC.Core.math

from enum import IntEnum
from OCC.Core.Exception import *

BiTgte_FaceFace = _BiTgte.BiTgte_FaceFace
BiTgte_FaceEdge = _BiTgte.BiTgte_FaceEdge
BiTgte_FaceVertex = _BiTgte.BiTgte_FaceVertex
BiTgte_EdgeEdge = _BiTgte.BiTgte_EdgeEdge
BiTgte_EdgeVertex = _BiTgte.BiTgte_EdgeVertex
BiTgte_VertexVertex = _BiTgte.BiTgte_VertexVertex


class BiTgte_ContactType(IntEnum):
	BiTgte_FaceFace = 0
	BiTgte_FaceEdge = 1
	BiTgte_FaceVertex = 2
	BiTgte_EdgeEdge = 3
	BiTgte_EdgeVertex = 4
	BiTgte_VertexVertex = 5
BiTgte_FaceFace = BiTgte_ContactType.BiTgte_FaceFace
BiTgte_FaceEdge = BiTgte_ContactType.BiTgte_FaceEdge
BiTgte_FaceVertex = BiTgte_ContactType.BiTgte_FaceVertex
BiTgte_EdgeEdge = BiTgte_ContactType.BiTgte_EdgeEdge
BiTgte_EdgeVertex = BiTgte_ContactType.BiTgte_EdgeVertex
BiTgte_VertexVertex = BiTgte_ContactType.BiTgte_VertexVertex


def Handle_BiTgte_HCurveOnEdge_Create() -> "opencascade::handle< BiTgte_HCurveOnEdge >":
    return _BiTgte.Handle_BiTgte_HCurveOnEdge_Create()
Handle_BiTgte_HCurveOnEdge_Create = _BiTgte.Handle_BiTgte_HCurveOnEdge_Create

def Handle_BiTgte_HCurveOnEdge_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BiTgte_HCurveOnEdge >":
    return _BiTgte.Handle_BiTgte_HCurveOnEdge_DownCast(t)
Handle_BiTgte_HCurveOnEdge_DownCast = _BiTgte.Handle_BiTgte_HCurveOnEdge_DownCast

def Handle_BiTgte_HCurveOnEdge_IsNull(t: 'opencascade::handle< BiTgte_HCurveOnEdge > const &') -> "bool":
    return _BiTgte.Handle_BiTgte_HCurveOnEdge_IsNull(t)
Handle_BiTgte_HCurveOnEdge_IsNull = _BiTgte.Handle_BiTgte_HCurveOnEdge_IsNull

def Handle_BiTgte_HCurveOnVertex_Create() -> "opencascade::handle< BiTgte_HCurveOnVertex >":
    return _BiTgte.Handle_BiTgte_HCurveOnVertex_Create()
Handle_BiTgte_HCurveOnVertex_Create = _BiTgte.Handle_BiTgte_HCurveOnVertex_Create

def Handle_BiTgte_HCurveOnVertex_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BiTgte_HCurveOnVertex >":
    return _BiTgte.Handle_BiTgte_HCurveOnVertex_DownCast(t)
Handle_BiTgte_HCurveOnVertex_DownCast = _BiTgte.Handle_BiTgte_HCurveOnVertex_DownCast

def Handle_BiTgte_HCurveOnVertex_IsNull(t: 'opencascade::handle< BiTgte_HCurveOnVertex > const &') -> "bool":
    return _BiTgte.Handle_BiTgte_HCurveOnVertex_IsNull(t)
Handle_BiTgte_HCurveOnVertex_IsNull = _BiTgte.Handle_BiTgte_HCurveOnVertex_IsNull
class BiTgte_Blend(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BiTgte_Blend, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BiTgte_Blend, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        <s>: shape to be rounded <radius>: radius of the fillet <tol>: tol3d used in approximations <nubs>: if true, generate only nubs surfaces, if false, generate analytical surfaces if possible.

        Parameters
        ----------
        S: TopoDS_Shape
        Radius: float
        Tol: float
        NUBS: bool

        Returns
        -------
        None

        """
        this = _BiTgte.new_BiTgte_Blend(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def CenterLines(self, *args) -> "void":
        """
        Set in <lc> all the center lines.

        Parameters
        ----------
        LC: TopTools_ListOfShape

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_CenterLines(self, *args)


    def Clear(self, *args) -> "void":
        """
        Clear all the fields.

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_Clear(self, *args)


    def ComputeCenters(self, *args) -> "void":
        """
        Computes the center lines.

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_ComputeCenters(self, *args)


    def ContactType(self, *args) -> "BiTgte_ContactType":
        """
        Returns the type of contact.

        Parameters
        ----------
        Index: int

        Returns
        -------
        BiTgte_ContactType

        """
        return _BiTgte.BiTgte_Blend_ContactType(self, *args)


    def CurveOnShape1(self, *args) -> "opencascade::handle< Geom_Curve >":
        """
        Gives the 3d curve of surfacefillet(index) on supportshape1(index).

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom_Curve>

        """
        return _BiTgte.BiTgte_Blend_CurveOnShape1(self, *args)


    def CurveOnShape2(self, *args) -> "opencascade::handle< Geom_Curve >":
        """
        Gives the 3d curve of surfacefillet(index) on supportshape2(index).

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom_Curve>

        """
        return _BiTgte.BiTgte_Blend_CurveOnShape2(self, *args)


    def Face(self, *args) -> "TopoDS_Face const":
        """
        Returns the surface of range index.

        Parameters
        ----------
        Index: int

        Returns
        -------
        TopoDS_Face

        Returns the face generated by the centerline. <centerline> may be - an edge : generate a pipe. - a vertex : generate a sphere. warning: returns a null shape if <centerline> generates no surface.

        Parameters
        ----------
        CenterLine: TopoDS_Shape

        Returns
        -------
        TopoDS_Face

        """
        return _BiTgte.BiTgte_Blend_Face(self, *args)


    def IndicesOfBranche(self, *args) -> "void":
        """
        Set in <from>,<to> the indices of the faces of the branche <index>. //! i.e: branche<index> = face(from) + face(from+1) + ..+ face(to).

        Parameters
        ----------
        Index: int

        Returns
        -------
        From: int
        To: int

        """
        return _BiTgte.BiTgte_Blend_IndicesOfBranche(self, *args)


    def Init(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        S: TopoDS_Shape
        Radius: float
        Tol: float
        NUBS: bool

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_Init(self, *args)


    def IsDone(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _BiTgte.BiTgte_Blend_IsDone(self, *args)


    def NbBranches(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Returns
        -------
        int

        """
        return _BiTgte.BiTgte_Blend_NbBranches(self, *args)


    def NbSurfaces(self, *args) -> "Standard_Integer":
        """
        Returns the number of generated surfaces.

        Returns
        -------
        int

        """
        return _BiTgte.BiTgte_Blend_NbSurfaces(self, *args)


    def PCurve1OnFillet(self, *args) -> "opencascade::handle< Geom2d_Curve >":
        """
        Gives the pcurve associated to curveonshape1(index) on the fillet.

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom2d_Curve>

        """
        return _BiTgte.BiTgte_Blend_PCurve1OnFillet(self, *args)


    def PCurve2OnFillet(self, *args) -> "opencascade::handle< Geom2d_Curve >":
        """
        Gives the pcurve associated to curveonshape2(index) on the fillet.

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom2d_Curve>

        """
        return _BiTgte.BiTgte_Blend_PCurve2OnFillet(self, *args)


    def PCurveOnFace1(self, *args) -> "opencascade::handle< Geom2d_Curve >":
        """
        Gives the pcurve associated to curvonshape1(index) on the support face warning: returns a null handle if supportshape1 is not a face.

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom2d_Curve>

        """
        return _BiTgte.BiTgte_Blend_PCurveOnFace1(self, *args)


    def PCurveOnFace2(self, *args) -> "opencascade::handle< Geom2d_Curve >":
        """
        Gives the pcurve associated to curveonshape2(index) on the support face warning: returns a null handle if supportshape2 is not a face.

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom2d_Curve>

        """
        return _BiTgte.BiTgte_Blend_PCurveOnFace2(self, *args)


    def Perform(self, *args) -> "void":
        """
        Compute the generated surfaces. if <buildshape> is true, compute the resulting shape. if false, only the blending surfaces are computed.

        Parameters
        ----------
        BuildShape: bool,optional
        	default value is Standard_True

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_Perform(self, *args)


    def SetEdge(self, *args) -> "void":
        """
        Set an edge of <myshape> to be rounded.

        Parameters
        ----------
        Edge: TopoDS_Edge

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_SetEdge(self, *args)


    def SetFaces(self, *args) -> "void":
        """
        Set two faces of <myshape> on which the sphere must roll.

        Parameters
        ----------
        F1: TopoDS_Face
        F2: TopoDS_Face

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_SetFaces(self, *args)


    def SetStoppingFace(self, *args) -> "void":
        """
        Set a face on which the fillet must stop.

        Parameters
        ----------
        Face: TopoDS_Face

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_Blend_SetStoppingFace(self, *args)


    def Shape(self, *args) -> "TopoDS_Shape const":
        """
        Returns the result.

        Returns
        -------
        TopoDS_Shape

        """
        return _BiTgte.BiTgte_Blend_Shape(self, *args)


    def SupportShape1(self, *args) -> "TopoDS_Shape const":
        """
        Gives the first support shape relative to surfacefillet(index);.

        Parameters
        ----------
        Index: int

        Returns
        -------
        TopoDS_Shape

        """
        return _BiTgte.BiTgte_Blend_SupportShape1(self, *args)


    def SupportShape2(self, *args) -> "TopoDS_Shape const":
        """
        Gives the second support shape relative to surfacefillet(index);.

        Parameters
        ----------
        Index: int

        Returns
        -------
        TopoDS_Shape

        """
        return _BiTgte.BiTgte_Blend_SupportShape2(self, *args)


    def Surface(self, *args) -> "opencascade::handle< Geom_Surface >":
        """
        Returns the surface of range index.

        Parameters
        ----------
        Index: int

        Returns
        -------
        opencascade::handle<Geom_Surface>

        Returns the surface generated by the centerline. <centerline> may be - an edge : generate a pipe. - a vertex : generate a sphere. warning: returns a null handle if <centerline> generates no surface.

        Parameters
        ----------
        CenterLine: TopoDS_Shape

        Returns
        -------
        opencascade::handle<Geom_Surface>

        """
        return _BiTgte.BiTgte_Blend_Surface(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BiTgte.delete_BiTgte_Blend
    __del__ = lambda self: None
BiTgte_Blend_swigregister = _BiTgte.BiTgte_Blend_swigregister
BiTgte_Blend_swigregister(BiTgte_Blend)

class BiTgte_CurveOnEdge(OCC.Core.Adaptor3d.Adaptor3d_Curve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BiTgte_CurveOnEdge, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BiTgte_CurveOnEdge, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        EonF: TopoDS_Edge
        Edge: TopoDS_Edge

        Returns
        -------
        None

        """
        this = _BiTgte.new_BiTgte_CurveOnEdge(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Init(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        EonF: TopoDS_Edge
        Edge: TopoDS_Edge

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_CurveOnEdge_Init(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BiTgte.delete_BiTgte_CurveOnEdge
    __del__ = lambda self: None
BiTgte_CurveOnEdge_swigregister = _BiTgte.BiTgte_CurveOnEdge_swigregister
BiTgte_CurveOnEdge_swigregister(BiTgte_CurveOnEdge)

class BiTgte_CurveOnVertex(OCC.Core.Adaptor3d.Adaptor3d_Curve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BiTgte_CurveOnVertex, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BiTgte_CurveOnVertex, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        EonF: TopoDS_Edge
        V: TopoDS_Vertex

        Returns
        -------
        None

        """
        this = _BiTgte.new_BiTgte_CurveOnVertex(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Init(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        EonF: TopoDS_Edge
        V: TopoDS_Vertex

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_CurveOnVertex_Init(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BiTgte.delete_BiTgte_CurveOnVertex
    __del__ = lambda self: None
BiTgte_CurveOnVertex_swigregister = _BiTgte.BiTgte_CurveOnVertex_swigregister
BiTgte_CurveOnVertex_swigregister(BiTgte_CurveOnVertex)

class BiTgte_HCurveOnEdge(OCC.Core.Adaptor3d.Adaptor3d_HCurve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BiTgte_HCurveOnEdge, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BiTgte_HCurveOnEdge, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an empty genhcurve.

        Returns
        -------
        None

        Creates a genhcurve from a curve.

        Parameters
        ----------
        C: BiTgte_CurveOnEdge

        Returns
        -------
        None

        """
        this = _BiTgte.new_BiTgte_HCurveOnEdge(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeCurve(self, *args) -> "BiTgte_CurveOnEdge &":
        """
        Returns the curve used to create the genhcurve.

        Returns
        -------
        BiTgte_CurveOnEdge

        """
        return _BiTgte.BiTgte_HCurveOnEdge_ChangeCurve(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhcurve.

        Parameters
        ----------
        C: BiTgte_CurveOnEdge

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_HCurveOnEdge_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BiTgte_HCurveOnEdge_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BiTgte.delete_BiTgte_HCurveOnEdge
    __del__ = lambda self: None
BiTgte_HCurveOnEdge_swigregister = _BiTgte.BiTgte_HCurveOnEdge_swigregister
BiTgte_HCurveOnEdge_swigregister(BiTgte_HCurveOnEdge)

class BiTgte_HCurveOnVertex(OCC.Core.Adaptor3d.Adaptor3d_HCurve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BiTgte_HCurveOnVertex, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BiTgte_HCurveOnVertex, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an empty genhcurve.

        Returns
        -------
        None

        Creates a genhcurve from a curve.

        Parameters
        ----------
        C: BiTgte_CurveOnVertex

        Returns
        -------
        None

        """
        this = _BiTgte.new_BiTgte_HCurveOnVertex(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeCurve(self, *args) -> "BiTgte_CurveOnVertex &":
        """
        Returns the curve used to create the genhcurve.

        Returns
        -------
        BiTgte_CurveOnVertex

        """
        return _BiTgte.BiTgte_HCurveOnVertex_ChangeCurve(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhcurve.

        Parameters
        ----------
        C: BiTgte_CurveOnVertex

        Returns
        -------
        None

        """
        return _BiTgte.BiTgte_HCurveOnVertex_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BiTgte_HCurveOnVertex_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BiTgte.delete_BiTgte_HCurveOnVertex
    __del__ = lambda self: None
BiTgte_HCurveOnVertex_swigregister = _BiTgte.BiTgte_HCurveOnVertex_swigregister
BiTgte_HCurveOnVertex_swigregister(BiTgte_HCurveOnVertex)



# This file is compatible with both classic and new-style classes.


