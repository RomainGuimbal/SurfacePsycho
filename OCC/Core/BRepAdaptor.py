# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
BRepAdaptor module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_brepadaptor.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_BRepAdaptor')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_BRepAdaptor')
    _BRepAdaptor = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_BRepAdaptor', [dirname(__file__)])
        except ImportError:
            import _BRepAdaptor
            return _BRepAdaptor
        try:
            _mod = imp.load_module('_BRepAdaptor', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _BRepAdaptor = swig_import_helper()
    del swig_import_helper
else:
    import _BRepAdaptor
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
    __swig_destroy__ = _BRepAdaptor.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _BRepAdaptor.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BRepAdaptor.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _BRepAdaptor.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _BRepAdaptor.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _BRepAdaptor.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _BRepAdaptor.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _BRepAdaptor.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _BRepAdaptor.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _BRepAdaptor.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BRepAdaptor.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _BRepAdaptor.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _BRepAdaptor.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BRepAdaptor.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _BRepAdaptor.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _BRepAdaptor.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _BRepAdaptor.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _BRepAdaptor.SwigPyIterator_swigregister
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
    return _BRepAdaptor.process_exception(error, method_name, class_name)
process_exception = _BRepAdaptor.process_exception

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
import OCC.Core.TopoDS
import OCC.Core.TopLoc
import OCC.Core.GeomAdaptor
import OCC.Core.Geom2dAdaptor

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_BRepAdaptor_HCompCurve_Create() -> "opencascade::handle< BRepAdaptor_HCompCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_Create()
Handle_BRepAdaptor_HCompCurve_Create = _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_Create

def Handle_BRepAdaptor_HCompCurve_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BRepAdaptor_HCompCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_DownCast(t)
Handle_BRepAdaptor_HCompCurve_DownCast = _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_DownCast

def Handle_BRepAdaptor_HCompCurve_IsNull(t: 'opencascade::handle< BRepAdaptor_HCompCurve > const &') -> "bool":
    return _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_IsNull(t)
Handle_BRepAdaptor_HCompCurve_IsNull = _BRepAdaptor.Handle_BRepAdaptor_HCompCurve_IsNull

def Handle_BRepAdaptor_HCurve_Create() -> "opencascade::handle< BRepAdaptor_HCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve_Create()
Handle_BRepAdaptor_HCurve_Create = _BRepAdaptor.Handle_BRepAdaptor_HCurve_Create

def Handle_BRepAdaptor_HCurve_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BRepAdaptor_HCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve_DownCast(t)
Handle_BRepAdaptor_HCurve_DownCast = _BRepAdaptor.Handle_BRepAdaptor_HCurve_DownCast

def Handle_BRepAdaptor_HCurve_IsNull(t: 'opencascade::handle< BRepAdaptor_HCurve > const &') -> "bool":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve_IsNull(t)
Handle_BRepAdaptor_HCurve_IsNull = _BRepAdaptor.Handle_BRepAdaptor_HCurve_IsNull

def Handle_BRepAdaptor_HCurve2d_Create() -> "opencascade::handle< BRepAdaptor_HCurve2d >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_Create()
Handle_BRepAdaptor_HCurve2d_Create = _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_Create

def Handle_BRepAdaptor_HCurve2d_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BRepAdaptor_HCurve2d >":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_DownCast(t)
Handle_BRepAdaptor_HCurve2d_DownCast = _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_DownCast

def Handle_BRepAdaptor_HCurve2d_IsNull(t: 'opencascade::handle< BRepAdaptor_HCurve2d > const &') -> "bool":
    return _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_IsNull(t)
Handle_BRepAdaptor_HCurve2d_IsNull = _BRepAdaptor.Handle_BRepAdaptor_HCurve2d_IsNull

def Handle_BRepAdaptor_HSurface_Create() -> "opencascade::handle< BRepAdaptor_HSurface >":
    return _BRepAdaptor.Handle_BRepAdaptor_HSurface_Create()
Handle_BRepAdaptor_HSurface_Create = _BRepAdaptor.Handle_BRepAdaptor_HSurface_Create

def Handle_BRepAdaptor_HSurface_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BRepAdaptor_HSurface >":
    return _BRepAdaptor.Handle_BRepAdaptor_HSurface_DownCast(t)
Handle_BRepAdaptor_HSurface_DownCast = _BRepAdaptor.Handle_BRepAdaptor_HSurface_DownCast

def Handle_BRepAdaptor_HSurface_IsNull(t: 'opencascade::handle< BRepAdaptor_HSurface > const &') -> "bool":
    return _BRepAdaptor.Handle_BRepAdaptor_HSurface_IsNull(t)
Handle_BRepAdaptor_HSurface_IsNull = _BRepAdaptor.Handle_BRepAdaptor_HSurface_IsNull

def Handle_BRepAdaptor_HArray1OfCurve_Create() -> "opencascade::handle< BRepAdaptor_HArray1OfCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_Create()
Handle_BRepAdaptor_HArray1OfCurve_Create = _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_Create

def Handle_BRepAdaptor_HArray1OfCurve_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< BRepAdaptor_HArray1OfCurve >":
    return _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_DownCast(t)
Handle_BRepAdaptor_HArray1OfCurve_DownCast = _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_DownCast

def Handle_BRepAdaptor_HArray1OfCurve_IsNull(t: 'opencascade::handle< BRepAdaptor_HArray1OfCurve > const &') -> "bool":
    return _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_IsNull(t)
Handle_BRepAdaptor_HArray1OfCurve_IsNull = _BRepAdaptor.Handle_BRepAdaptor_HArray1OfCurve_IsNull
class BRepAdaptor_Array1OfCurve(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_Array1OfCurve, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_Array1OfCurve, name)
    __repr__ = _swig_repr

    def begin(self) -> "NCollection_Array1< BRepAdaptor_Curve >::iterator":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_begin(self)

    def end(self) -> "NCollection_Array1< BRepAdaptor_Curve >::iterator":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_end(self)

    def cbegin(self) -> "NCollection_Array1< BRepAdaptor_Curve >::const_iterator":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_cbegin(self)

    def cend(self) -> "NCollection_Array1< BRepAdaptor_Curve >::const_iterator":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_cend(self)

    def __init__(self, *args):
        this = _BRepAdaptor.new_BRepAdaptor_Array1OfCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Init(self, theValue: 'BRepAdaptor_Curve') -> "void":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Init(self, theValue)

    def Size(self) -> "Standard_Integer":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Size(self)

    def Length(self) -> "Standard_Integer":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Length(self)

    def IsEmpty(self) -> "Standard_Boolean":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_IsEmpty(self)

    def Lower(self) -> "Standard_Integer":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Lower(self)

    def Upper(self) -> "Standard_Integer":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Upper(self)

    def IsDeletable(self) -> "Standard_Boolean":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_IsDeletable(self)

    def IsAllocated(self) -> "Standard_Boolean":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_IsAllocated(self)

    def Assign(self, theOther: 'BRepAdaptor_Array1OfCurve') -> "NCollection_Array1< BRepAdaptor_Curve > &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Assign(self, theOther)

    def Move(self, theOther: 'BRepAdaptor_Array1OfCurve') -> "NCollection_Array1< BRepAdaptor_Curve > &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Move(self, theOther)

    def Set(self, *args) -> "NCollection_Array1< BRepAdaptor_Curve > &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Set(self, *args)

    def First(self) -> "BRepAdaptor_Curve const &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_First(self)

    def ChangeFirst(self) -> "BRepAdaptor_Curve &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_ChangeFirst(self)

    def Last(self) -> "BRepAdaptor_Curve const &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Last(self)

    def ChangeLast(self) -> "BRepAdaptor_Curve &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_ChangeLast(self)

    def Value(self, theIndex: 'Standard_Integer const') -> "BRepAdaptor_Curve const &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Value(self, theIndex)

    def ChangeValue(self, theIndex: 'Standard_Integer const') -> "BRepAdaptor_Curve &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_ChangeValue(self, theIndex)

    def __call__(self, *args) -> "BRepAdaptor_Curve &":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve___call__(self, *args)

    def SetValue(self, theIndex: 'Standard_Integer const', theItem: 'BRepAdaptor_Curve') -> "void":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_SetValue(self, theIndex, theItem)

    def Resize(self, theLower: 'Standard_Integer const', theUpper: 'Standard_Integer const', theToCopyData: 'Standard_Boolean const') -> "void":
        return _BRepAdaptor.BRepAdaptor_Array1OfCurve_Resize(self, theLower, theUpper, theToCopyData)
    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_Array1OfCurve
    __del__ = lambda self: None

    def __getitem__(self, index):
        if index + self.Lower() > self.Upper():
            raise IndexError("index out of range")
        else:
            return self.Value(index + self.Lower())

    def __setitem__(self, index, value):
        if index + self.Lower() > self.Upper():
            raise IndexError("index out of range")
        else:
            self.SetValue(index + self.Lower(), value)

    def __len__(self):
        return self.Length()

    def __iter__(self):
        self.low = self.Lower()
        self.up = self.Upper()
        self.current = self.Lower() - 1
        return self

    def next(self):
        if self.current >= self.Upper():
            raise StopIteration
        else:
            self.current += 1
        return self.Value(self.current)

    __next__ = next

BRepAdaptor_Array1OfCurve_swigregister = _BRepAdaptor.BRepAdaptor_Array1OfCurve_swigregister
BRepAdaptor_Array1OfCurve_swigregister(BRepAdaptor_Array1OfCurve)

class BRepAdaptor_CompCurve(OCC.Core.Adaptor3d.Adaptor3d_Curve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_CompCurve, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_CompCurve, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an undefined curve with no wire loaded.

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        W: TopoDS_Wire
        KnotByCurvilinearAbcissa: bool,optional
        	default value is Standard_False

        Returns
        -------
        None

        Creates a curve to acces to the geometry of edge <w>.

        Parameters
        ----------
        W: TopoDS_Wire
        KnotByCurvilinearAbcissa: bool
        First: float
        Last: float
        Tol: float

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_CompCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Edge(self, *args) -> "void":
        """
        Returns an edge and one parameter on them corresponding to the parameter u.

        Parameters
        ----------
        U: float
        E: TopoDS_Edge

        Returns
        -------
        UonE: float

        """
        return _BRepAdaptor.BRepAdaptor_CompCurve_Edge(self, *args)


    def Initialize(self, *args) -> "void":
        """
        Sets the wire <w>.

        Parameters
        ----------
        W: TopoDS_Wire
        KnotByCurvilinearAbcissa: bool

        Returns
        -------
        None

        Sets wire <w> and trimmed parameter.

        Parameters
        ----------
        W: TopoDS_Wire
        KnotByCurvilinearAbcissa: bool
        First: float
        Last: float
        Tol: float

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_CompCurve_Initialize(self, *args)


    def Wire(self, *args) -> "TopoDS_Wire const":
        """
        Returns the wire.

        Returns
        -------
        TopoDS_Wire

        """
        return _BRepAdaptor.BRepAdaptor_CompCurve_Wire(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_CompCurve
    __del__ = lambda self: None
BRepAdaptor_CompCurve_swigregister = _BRepAdaptor.BRepAdaptor_CompCurve_swigregister
BRepAdaptor_CompCurve_swigregister(BRepAdaptor_CompCurve)

class BRepAdaptor_Curve(OCC.Core.Adaptor3d.Adaptor3d_Curve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_Curve, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Curve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_Curve, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an undefined curve with no edge loaded.

        Returns
        -------
        None

        Creates a curve to acces to the geometry of edge <e>.

        Parameters
        ----------
        E: TopoDS_Edge

        Returns
        -------
        None

        Creates a curve to acces to the geometry of edge <e>. the geometry will be computed using the parametric curve of <e> on the face <f>. an error is raised if the edge does not have a pcurve on the face.

        Parameters
        ----------
        E: TopoDS_Edge
        F: TopoDS_Face

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_Curve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Curve(self, *args) -> "GeomAdaptor_Curve const &":
        """
        Returns the curve of the edge.

        Returns
        -------
        GeomAdaptor_Curve

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Curve(self, *args)


    def CurveOnSurface(self, *args) -> "Adaptor3d_CurveOnSurface const &":
        """
        Returns the curveonsurface of the edge.

        Returns
        -------
        Adaptor3d_CurveOnSurface

        """
        return _BRepAdaptor.BRepAdaptor_Curve_CurveOnSurface(self, *args)


    def Edge(self, *args) -> "TopoDS_Edge const":
        """
        Returns the edge.

        Returns
        -------
        TopoDS_Edge

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Edge(self, *args)


    def Initialize(self, *args) -> "void":
        """
        Sets the curve <self> to acces to the geometry of edge <e>.

        Parameters
        ----------
        E: TopoDS_Edge

        Returns
        -------
        None

        Sets the curve <self> to acces to the geometry of edge <e>. the geometry will be computed using the parametric curve of <e> on the face <f>. an error is raised if the edge does not have a pcurve on the face.

        Parameters
        ----------
        E: TopoDS_Edge
        F: TopoDS_Face

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Initialize(self, *args)


    def Is3DCurve(self, *args) -> "Standard_Boolean":
        """
        Returns true if the edge geometry is computed from a 3d curve.

        Returns
        -------
        bool

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Is3DCurve(self, *args)


    def IsCurveOnSurface(self, *args) -> "Standard_Boolean":
        """
        Returns true if the edge geometry is computed from a pcurve on a surface.

        Returns
        -------
        bool

        """
        return _BRepAdaptor.BRepAdaptor_Curve_IsCurveOnSurface(self, *args)


    def Reset(self, *args) -> "void":
        """
        Reset currently loaded curve (undone load()).

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Reset(self, *args)


    def Tolerance(self, *args) -> "Standard_Real":
        """
        Returns the edge tolerance.

        Returns
        -------
        float

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Tolerance(self, *args)


    def Trsf(self, *args) -> "gp_Trsf const":
        """
        Returns the coordinate system of the curve.

        Returns
        -------
        gp_Trsf

        """
        return _BRepAdaptor.BRepAdaptor_Curve_Trsf(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_Curve
    __del__ = lambda self: None
BRepAdaptor_Curve_swigregister = _BRepAdaptor.BRepAdaptor_Curve_swigregister
BRepAdaptor_Curve_swigregister(BRepAdaptor_Curve)

class BRepAdaptor_Curve2d(OCC.Core.Geom2dAdaptor.Geom2dAdaptor_Curve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Geom2dAdaptor.Geom2dAdaptor_Curve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_Curve2d, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Geom2dAdaptor.Geom2dAdaptor_Curve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_Curve2d, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an uninitialized curve2d.

        Returns
        -------
        None

        Creates with the pcurve of <e> on <f>.

        Parameters
        ----------
        E: TopoDS_Edge
        F: TopoDS_Face

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_Curve2d(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Edge(self, *args) -> "TopoDS_Edge const":
        """
        Returns the edge.

        Returns
        -------
        TopoDS_Edge

        """
        return _BRepAdaptor.BRepAdaptor_Curve2d_Edge(self, *args)


    def Face(self, *args) -> "TopoDS_Face const":
        """
        Returns the face.

        Returns
        -------
        TopoDS_Face

        """
        return _BRepAdaptor.BRepAdaptor_Curve2d_Face(self, *args)


    def Initialize(self, *args) -> "void":
        """
        Initialize with the pcurve of <e> on <f>.

        Parameters
        ----------
        E: TopoDS_Edge
        F: TopoDS_Face

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_Curve2d_Initialize(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_Curve2d
    __del__ = lambda self: None
BRepAdaptor_Curve2d_swigregister = _BRepAdaptor.BRepAdaptor_Curve2d_swigregister
BRepAdaptor_Curve2d_swigregister(BRepAdaptor_Curve2d)

class BRepAdaptor_HCompCurve(OCC.Core.Adaptor3d.Adaptor3d_HCurve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_HCompCurve, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_HCompCurve, name)
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
        C: BRepAdaptor_CompCurve

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_HCompCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeCurve(self, *args) -> "BRepAdaptor_CompCurve &":
        """
        Returns the curve used to create the genhcurve.

        Returns
        -------
        BRepAdaptor_CompCurve

        """
        return _BRepAdaptor.BRepAdaptor_HCompCurve_ChangeCurve(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhcurve.

        Parameters
        ----------
        C: BRepAdaptor_CompCurve

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_HCompCurve_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BRepAdaptor_HCompCurve_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_HCompCurve
    __del__ = lambda self: None
BRepAdaptor_HCompCurve_swigregister = _BRepAdaptor.BRepAdaptor_HCompCurve_swigregister
BRepAdaptor_HCompCurve_swigregister(BRepAdaptor_HCompCurve)

class BRepAdaptor_HCurve(OCC.Core.Adaptor3d.Adaptor3d_HCurve):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_HCurve, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HCurve]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_HCurve, name)
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
        C: BRepAdaptor_Curve

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_HCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeCurve(self, *args) -> "BRepAdaptor_Curve &":
        """
        Returns the curve used to create the genhcurve.

        Returns
        -------
        BRepAdaptor_Curve

        """
        return _BRepAdaptor.BRepAdaptor_HCurve_ChangeCurve(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhcurve.

        Parameters
        ----------
        C: BRepAdaptor_Curve

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_HCurve_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BRepAdaptor_HCurve_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_HCurve
    __del__ = lambda self: None
BRepAdaptor_HCurve_swigregister = _BRepAdaptor.BRepAdaptor_HCurve_swigregister
BRepAdaptor_HCurve_swigregister(BRepAdaptor_HCurve)

class BRepAdaptor_HCurve2d(OCC.Core.Adaptor2d.Adaptor2d_HCurve2d):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor2d.Adaptor2d_HCurve2d]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_HCurve2d, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor2d.Adaptor2d_HCurve2d]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_HCurve2d, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an empty genhcurve2d.

        Returns
        -------
        None

        Creates a genhcurve2d from a curve.

        Parameters
        ----------
        C: BRepAdaptor_Curve2d

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_HCurve2d(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeCurve2d(self, *args) -> "BRepAdaptor_Curve2d &":
        """
        Returns the curve used to create the genhcurve.

        Returns
        -------
        BRepAdaptor_Curve2d

        """
        return _BRepAdaptor.BRepAdaptor_HCurve2d_ChangeCurve2d(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhcurve2d.

        Parameters
        ----------
        C: BRepAdaptor_Curve2d

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_HCurve2d_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BRepAdaptor_HCurve2d_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_HCurve2d
    __del__ = lambda self: None
BRepAdaptor_HCurve2d_swigregister = _BRepAdaptor.BRepAdaptor_HCurve2d_swigregister
BRepAdaptor_HCurve2d_swigregister(BRepAdaptor_HCurve2d)

class BRepAdaptor_HSurface(OCC.Core.Adaptor3d.Adaptor3d_HSurface):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HSurface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_HSurface, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_HSurface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_HSurface, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an empty genhsurface.

        Returns
        -------
        None

        Creates a genhsurface from a surface.

        Parameters
        ----------
        S: BRepAdaptor_Surface

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_HSurface(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeSurface(self, *args) -> "BRepAdaptor_Surface &":
        """
        Returns the surface used to create the genhsurface.

        Returns
        -------
        BRepAdaptor_Surface

        """
        return _BRepAdaptor.BRepAdaptor_HSurface_ChangeSurface(self, *args)


    def Set(self, *args) -> "void":
        """
        Sets the field of the genhsurface.

        Parameters
        ----------
        S: BRepAdaptor_Surface

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_HSurface_Set(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_BRepAdaptor_HSurface_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_HSurface
    __del__ = lambda self: None
BRepAdaptor_HSurface_swigregister = _BRepAdaptor.BRepAdaptor_HSurface_swigregister
BRepAdaptor_HSurface_swigregister(BRepAdaptor_HSurface)

class BRepAdaptor_Surface(OCC.Core.Adaptor3d.Adaptor3d_Surface):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Surface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_Surface, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Adaptor3d.Adaptor3d_Surface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_Surface, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates an undefined surface with no face loaded.

        Returns
        -------
        None

        Creates a surface to access the geometry of <f>. if <restriction> is true the parameter range is the parameter range in the uv space of the restriction.

        Parameters
        ----------
        F: TopoDS_Face
        R: bool,optional
        	default value is Standard_True

        Returns
        -------
        None

        """
        this = _BRepAdaptor.new_BRepAdaptor_Surface(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def ChangeSurface(self, *args) -> "GeomAdaptor_Surface &":
        """
        Returns the surface.

        Returns
        -------
        GeomAdaptor_Surface

        """
        return _BRepAdaptor.BRepAdaptor_Surface_ChangeSurface(self, *args)


    def Face(self, *args) -> "TopoDS_Face const":
        """
        Returns the face.

        Returns
        -------
        TopoDS_Face

        """
        return _BRepAdaptor.BRepAdaptor_Surface_Face(self, *args)


    def Initialize(self, *args) -> "void":
        """
        Sets the surface to the geometry of <f>.

        Parameters
        ----------
        F: TopoDS_Face
        Restriction: bool,optional
        	default value is Standard_True

        Returns
        -------
        None

        """
        return _BRepAdaptor.BRepAdaptor_Surface_Initialize(self, *args)


    def Surface(self, *args) -> "GeomAdaptor_Surface const &":
        """
        Returns the surface.

        Returns
        -------
        GeomAdaptor_Surface

        """
        return _BRepAdaptor.BRepAdaptor_Surface_Surface(self, *args)


    def Tolerance(self, *args) -> "Standard_Real":
        """
        Returns the face tolerance.

        Returns
        -------
        float

        """
        return _BRepAdaptor.BRepAdaptor_Surface_Tolerance(self, *args)


    def Trsf(self, *args) -> "gp_Trsf const":
        """
        Returns the surface coordinate system.

        Returns
        -------
        gp_Trsf

        """
        return _BRepAdaptor.BRepAdaptor_Surface_Trsf(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_Surface
    __del__ = lambda self: None
BRepAdaptor_Surface_swigregister = _BRepAdaptor.BRepAdaptor_Surface_swigregister
BRepAdaptor_Surface_swigregister(BRepAdaptor_Surface)

class BRepAdaptor_HArray1OfCurve(BRepAdaptor_Array1OfCurve, OCC.Core.Standard.Standard_Transient):
    __swig_setmethods__ = {}
    for _s in [BRepAdaptor_Array1OfCurve, OCC.Core.Standard.Standard_Transient]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BRepAdaptor_HArray1OfCurve, name, value)
    __swig_getmethods__ = {}
    for _s in [BRepAdaptor_Array1OfCurve, OCC.Core.Standard.Standard_Transient]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BRepAdaptor_HArray1OfCurve, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _BRepAdaptor.new_BRepAdaptor_HArray1OfCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Array1(self) -> "BRepAdaptor_Array1OfCurve const &":
        return _BRepAdaptor.BRepAdaptor_HArray1OfCurve_Array1(self)

    def ChangeArray1(self) -> "BRepAdaptor_Array1OfCurve &":
        return _BRepAdaptor.BRepAdaptor_HArray1OfCurve_ChangeArray1(self)


    @staticmethod
    def DownCast(t):
      return Handle_BRepAdaptor_HArray1OfCurve_DownCast(t)

    __swig_destroy__ = _BRepAdaptor.delete_BRepAdaptor_HArray1OfCurve
    __del__ = lambda self: None
BRepAdaptor_HArray1OfCurve_swigregister = _BRepAdaptor.BRepAdaptor_HArray1OfCurve_swigregister
BRepAdaptor_HArray1OfCurve_swigregister(BRepAdaptor_HArray1OfCurve)



# This file is compatible with both classic and new-style classes.


