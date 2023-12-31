# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
CSLib module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_cslib.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_CSLib')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_CSLib')
    _CSLib = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_CSLib', [dirname(__file__)])
        except ImportError:
            import _CSLib
            return _CSLib
        try:
            _mod = imp.load_module('_CSLib', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _CSLib = swig_import_helper()
    del swig_import_helper
else:
    import _CSLib
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
    __swig_destroy__ = _CSLib.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _CSLib.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _CSLib.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _CSLib.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _CSLib.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _CSLib.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _CSLib.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _CSLib.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _CSLib.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _CSLib.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _CSLib.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _CSLib.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _CSLib.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _CSLib.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _CSLib.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _CSLib.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _CSLib.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _CSLib.SwigPyIterator_swigregister
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
    return _CSLib.process_exception(error, method_name, class_name)
process_exception = _CSLib.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TColgp
import OCC.Core.gp
import OCC.Core.TColStd
import OCC.Core.TCollection
import OCC.Core.math
import OCC.Core.Message
import OCC.Core.OSD

from enum import IntEnum
from OCC.Core.Exception import *

CSLib_Singular = _CSLib.CSLib_Singular
CSLib_Defined = _CSLib.CSLib_Defined
CSLib_InfinityOfSolutions = _CSLib.CSLib_InfinityOfSolutions
CSLib_D1NuIsNull = _CSLib.CSLib_D1NuIsNull
CSLib_D1NvIsNull = _CSLib.CSLib_D1NvIsNull
CSLib_D1NIsNull = _CSLib.CSLib_D1NIsNull
CSLib_D1NuNvRatioIsNull = _CSLib.CSLib_D1NuNvRatioIsNull
CSLib_D1NvNuRatioIsNull = _CSLib.CSLib_D1NvNuRatioIsNull
CSLib_D1NuIsParallelD1Nv = _CSLib.CSLib_D1NuIsParallelD1Nv
CSLib_Done = _CSLib.CSLib_Done
CSLib_D1uIsNull = _CSLib.CSLib_D1uIsNull
CSLib_D1vIsNull = _CSLib.CSLib_D1vIsNull
CSLib_D1IsNull = _CSLib.CSLib_D1IsNull
CSLib_D1uD1vRatioIsNull = _CSLib.CSLib_D1uD1vRatioIsNull
CSLib_D1vD1uRatioIsNull = _CSLib.CSLib_D1vD1uRatioIsNull
CSLib_D1uIsParallelD1v = _CSLib.CSLib_D1uIsParallelD1v


class CSLib_NormalStatus(IntEnum):
	CSLib_Singular = 0
	CSLib_Defined = 1
	CSLib_InfinityOfSolutions = 2
	CSLib_D1NuIsNull = 3
	CSLib_D1NvIsNull = 4
	CSLib_D1NIsNull = 5
	CSLib_D1NuNvRatioIsNull = 6
	CSLib_D1NvNuRatioIsNull = 7
	CSLib_D1NuIsParallelD1Nv = 8
CSLib_Singular = CSLib_NormalStatus.CSLib_Singular
CSLib_Defined = CSLib_NormalStatus.CSLib_Defined
CSLib_InfinityOfSolutions = CSLib_NormalStatus.CSLib_InfinityOfSolutions
CSLib_D1NuIsNull = CSLib_NormalStatus.CSLib_D1NuIsNull
CSLib_D1NvIsNull = CSLib_NormalStatus.CSLib_D1NvIsNull
CSLib_D1NIsNull = CSLib_NormalStatus.CSLib_D1NIsNull
CSLib_D1NuNvRatioIsNull = CSLib_NormalStatus.CSLib_D1NuNvRatioIsNull
CSLib_D1NvNuRatioIsNull = CSLib_NormalStatus.CSLib_D1NvNuRatioIsNull
CSLib_D1NuIsParallelD1Nv = CSLib_NormalStatus.CSLib_D1NuIsParallelD1Nv

class CSLib_DerivativeStatus(IntEnum):
	CSLib_Done = 0
	CSLib_D1uIsNull = 1
	CSLib_D1vIsNull = 2
	CSLib_D1IsNull = 3
	CSLib_D1uD1vRatioIsNull = 4
	CSLib_D1vD1uRatioIsNull = 5
	CSLib_D1uIsParallelD1v = 6
CSLib_Done = CSLib_DerivativeStatus.CSLib_Done
CSLib_D1uIsNull = CSLib_DerivativeStatus.CSLib_D1uIsNull
CSLib_D1vIsNull = CSLib_DerivativeStatus.CSLib_D1vIsNull
CSLib_D1IsNull = CSLib_DerivativeStatus.CSLib_D1IsNull
CSLib_D1uD1vRatioIsNull = CSLib_DerivativeStatus.CSLib_D1uD1vRatioIsNull
CSLib_D1vD1uRatioIsNull = CSLib_DerivativeStatus.CSLib_D1vD1uRatioIsNull
CSLib_D1uIsParallelD1v = CSLib_DerivativeStatus.CSLib_D1uIsParallelD1v

class cslib(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, cslib, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, cslib, name)
    __repr__ = _swig_repr

    def DNNUV(*args) -> "gp_Vec":
        """
        -- computes the derivative of order nu in the -- direction u and nv in the direction v of the not -- normalized normal vector at the point p(u,v) the array dersurf contain the derivative (i,j) of the surface for i=0,nu+1 ; j=0,nv+1.

        Parameters
        ----------
        Nu: int
        Nv: int
        DerSurf: TColgp_Array2OfVec

        Returns
        -------
        gp_Vec

        Computes the derivatives of order nu in the direction nu and nv in the direction nv of the not normalized vector n(u,v) = ds1/du * ds2/dv (cases where we use an osculating surface) dersurf1 are the derivatives of s1.

        Parameters
        ----------
        Nu: int
        Nv: int
        DerSurf1: TColgp_Array2OfVec
        DerSurf2: TColgp_Array2OfVec

        Returns
        -------
        gp_Vec

        """
        return _CSLib.cslib_DNNUV(*args)

    DNNUV = staticmethod(DNNUV)

    def DNNormal(*args) -> "gp_Vec":
        """
        -- computes the derivative of order nu in the -- direction u and nv in the direction v of the normalized normal vector at the point p(u,v) array dernuv contain the derivative (i+iduref,j+idvref) of d1u ^ d1v for i=0,nu ; j=0,nv iduref and idvref correspond to a derivative of d1u ^ d1v which can be used to compute the normalized normal vector. in the regular cases , iduref=idvref=0.

        Parameters
        ----------
        Nu: int
        Nv: int
        DerNUV: TColgp_Array2OfVec
        Iduref: int,optional
        	default value is 0
        Idvref: int,optional
        	default value is 0

        Returns
        -------
        gp_Vec

        """
        return _CSLib.cslib_DNNormal(*args)

    DNNormal = staticmethod(DNNormal)

    def Normal(*args) -> "CSLib_NormalStatus &, Standard_Integer &, Standard_Integer &":
        """
        The following functions computes the normal to a surface inherits functionwithderivative from math //! computes the normal direction of a surface as the cross product between d1u and d1v. if d1u has null length or d1v has null length or d1u and d1v are parallel the normal is undefined. to check that d1u and d1v are colinear the sinus of the angle between d1u and d1v is computed and compared with sintol. the normal is computed if thestatus == done else the thestatus gives the reason why the computation has failed.

        Parameters
        ----------
        D1U: gp_Vec
        D1V: gp_Vec
        SinTol: float
        Normal: gp_Dir

        Returns
        -------
        theStatus: CSLib_DerivativeStatus

        If there is a singularity on the surface the previous method cannot compute the local normal. this method computes an approched normal direction of a surface. it does a limited development and needs the second derivatives on the surface as input data. it computes the normal as follow : n(u, v) = d1u ^ d1v n(u0+du,v0+dv) = n0 + dn/du(u0,v0) * du + dn/dv(u0,v0) * dv + eps with eps->0 so we can have the equivalence n ~ dn/du + dn/dv. dnu = ||dn/du|| and dnv = ||dn/dv|| //! . if dnu isnull (dnu <= resolution from gp) the answer done = true the normal direction is given by dn/dv . if dnv isnull (dnv <= resolution from gp) the answer done = true the normal direction is given by dn/du . if the two directions dn/du and dn/dv are parallel done = true the normal direction is given either by dn/du or dn/dv. to check that the two directions are colinear the sinus of the angle between these directions is computed and compared with sintol. . if dnu/dnv or dnv/dnu is lower or equal than real epsilon done = false, the normal is undefined . if dnu isnull and dnv is null done = false, there is an indetermination and we should do a limited developpement at order 2 (it means that we cannot omit eps). . if dnu is not null and dnv is not null done = false, there are an infinity of normals at the considered point on the surface.

        Parameters
        ----------
        D1U: gp_Vec
        D1V: gp_Vec
        D2U: gp_Vec
        D2V: gp_Vec
        D2UV: gp_Vec
        SinTol: float
        Normal: gp_Dir

        Returns
        -------
        Done: bool
        theStatus: CSLib_NormalStatus

        Computes the normal direction of a surface as the cross product between d1u and d1v.

        Parameters
        ----------
        D1U: gp_Vec
        D1V: gp_Vec
        MagTol: float
        Normal: gp_Dir

        Returns
        -------
        theStatus: CSLib_NormalStatus

        Find the first order k0 of deriviative of nuv where: foreach order < k0 all the derivatives of nuv are null all the derivatives of nuv corresponding to the order k0 are collinear and have the same sens. in this case, normal at u,v is unique.

        Parameters
        ----------
        MaxOrder: int
        DerNUV: TColgp_Array2OfVec
        MagTol: float
        U: float
        V: float
        Umin: float
        Umax: float
        Vmin: float
        Vmax: float
        Normal: gp_Dir

        Returns
        -------
        theStatus: CSLib_NormalStatus
        OrderU: int
        OrderV: int

        """
        return _CSLib.cslib_Normal(*args)

    Normal = staticmethod(Normal)

    __repr__ = _dumps_object


    def __init__(self):
        this = _CSLib.new_cslib()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _CSLib.delete_cslib
    __del__ = lambda self: None
cslib_swigregister = _CSLib.cslib_swigregister
cslib_swigregister(cslib)

def cslib_DNNUV(*args) -> "gp_Vec":
    """
    -- computes the derivative of order nu in the -- direction u and nv in the direction v of the not -- normalized normal vector at the point p(u,v) the array dersurf contain the derivative (i,j) of the surface for i=0,nu+1 ; j=0,nv+1.

    Parameters
    ----------
    Nu: int
    Nv: int
    DerSurf: TColgp_Array2OfVec

    Returns
    -------
    gp_Vec

    Computes the derivatives of order nu in the direction nu and nv in the direction nv of the not normalized vector n(u,v) = ds1/du * ds2/dv (cases where we use an osculating surface) dersurf1 are the derivatives of s1.

    Parameters
    ----------
    Nu: int
    Nv: int
    DerSurf1: TColgp_Array2OfVec
    DerSurf2: TColgp_Array2OfVec

    Returns
    -------
    gp_Vec

    """
    return _CSLib.cslib_DNNUV(*args)

def cslib_DNNormal(*args) -> "gp_Vec":
    """
    -- computes the derivative of order nu in the -- direction u and nv in the direction v of the normalized normal vector at the point p(u,v) array dernuv contain the derivative (i+iduref,j+idvref) of d1u ^ d1v for i=0,nu ; j=0,nv iduref and idvref correspond to a derivative of d1u ^ d1v which can be used to compute the normalized normal vector. in the regular cases , iduref=idvref=0.

    Parameters
    ----------
    Nu: int
    Nv: int
    DerNUV: TColgp_Array2OfVec
    Iduref: int,optional
    	default value is 0
    Idvref: int,optional
    	default value is 0

    Returns
    -------
    gp_Vec

    """
    return _CSLib.cslib_DNNormal(*args)

def cslib_Normal(*args) -> "CSLib_NormalStatus &, Standard_Integer &, Standard_Integer &":
    """
    The following functions computes the normal to a surface inherits functionwithderivative from math //! computes the normal direction of a surface as the cross product between d1u and d1v. if d1u has null length or d1v has null length or d1u and d1v are parallel the normal is undefined. to check that d1u and d1v are colinear the sinus of the angle between d1u and d1v is computed and compared with sintol. the normal is computed if thestatus == done else the thestatus gives the reason why the computation has failed.

    Parameters
    ----------
    D1U: gp_Vec
    D1V: gp_Vec
    SinTol: float
    Normal: gp_Dir

    Returns
    -------
    theStatus: CSLib_DerivativeStatus

    If there is a singularity on the surface the previous method cannot compute the local normal. this method computes an approched normal direction of a surface. it does a limited development and needs the second derivatives on the surface as input data. it computes the normal as follow : n(u, v) = d1u ^ d1v n(u0+du,v0+dv) = n0 + dn/du(u0,v0) * du + dn/dv(u0,v0) * dv + eps with eps->0 so we can have the equivalence n ~ dn/du + dn/dv. dnu = ||dn/du|| and dnv = ||dn/dv|| //! . if dnu isnull (dnu <= resolution from gp) the answer done = true the normal direction is given by dn/dv . if dnv isnull (dnv <= resolution from gp) the answer done = true the normal direction is given by dn/du . if the two directions dn/du and dn/dv are parallel done = true the normal direction is given either by dn/du or dn/dv. to check that the two directions are colinear the sinus of the angle between these directions is computed and compared with sintol. . if dnu/dnv or dnv/dnu is lower or equal than real epsilon done = false, the normal is undefined . if dnu isnull and dnv is null done = false, there is an indetermination and we should do a limited developpement at order 2 (it means that we cannot omit eps). . if dnu is not null and dnv is not null done = false, there are an infinity of normals at the considered point on the surface.

    Parameters
    ----------
    D1U: gp_Vec
    D1V: gp_Vec
    D2U: gp_Vec
    D2V: gp_Vec
    D2UV: gp_Vec
    SinTol: float
    Normal: gp_Dir

    Returns
    -------
    Done: bool
    theStatus: CSLib_NormalStatus

    Computes the normal direction of a surface as the cross product between d1u and d1v.

    Parameters
    ----------
    D1U: gp_Vec
    D1V: gp_Vec
    MagTol: float
    Normal: gp_Dir

    Returns
    -------
    theStatus: CSLib_NormalStatus

    Find the first order k0 of deriviative of nuv where: foreach order < k0 all the derivatives of nuv are null all the derivatives of nuv corresponding to the order k0 are collinear and have the same sens. in this case, normal at u,v is unique.

    Parameters
    ----------
    MaxOrder: int
    DerNUV: TColgp_Array2OfVec
    MagTol: float
    U: float
    V: float
    Umin: float
    Umax: float
    Vmin: float
    Vmax: float
    Normal: gp_Dir

    Returns
    -------
    theStatus: CSLib_NormalStatus
    OrderU: int
    OrderV: int

    """
    return _CSLib.cslib_Normal(*args)

class CSLib_Class2d(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSLib_Class2d, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSLib_Class2d, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Constructs the 2d-polygon. thepnts2d is the set of the vertices (closed polygon will always be created inside of this constructor; consequently, there is no point in repeating first and last point in thepnts2d). thetolu and thetolv are tolerances. theumin, thevmin, theumax, thevmax are uv-bounds of the polygon.

        Parameters
        ----------
        thePnts2d: TColgp_Array1OfPnt2d
        theTolU: float
        theTolV: float
        theUMin: float
        theVMin: float
        theUMax: float
        theVMax: float

        Returns
        -------
        None

        Constructs the 2d-polygon. thepnts2d is the set of the vertices (closed polygon will always be created inside of this constructor; consequently, there is no point in repeating first and last point in thepnts2d). thetolu and thetolv are tolerances. theumin, thevmin, theumax, thevmax are uv-bounds of the polygon.

        Parameters
        ----------
        thePnts2d: TColgp_SequenceOfPnt2d
        theTolU: float
        theTolV: float
        theUMin: float
        theVMin: float
        theUMax: float
        theVMax: float

        Returns
        -------
        None

        """
        this = _CSLib.new_CSLib_Class2d(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def InternalSiDans(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Parameters
        ----------
        X: float
        Y: float

        Returns
        -------
        int

        """
        return _CSLib.CSLib_Class2d_InternalSiDans(self, *args)


    def InternalSiDansOuOn(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Parameters
        ----------
        X: float
        Y: float

        Returns
        -------
        int

        """
        return _CSLib.CSLib_Class2d_InternalSiDansOuOn(self, *args)


    def SiDans(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Parameters
        ----------
        P: gp_Pnt2d

        Returns
        -------
        int

        """
        return _CSLib.CSLib_Class2d_SiDans(self, *args)


    def SiDans_OnMode(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Parameters
        ----------
        P: gp_Pnt2d
        Tol: float

        Returns
        -------
        int

        """
        return _CSLib.CSLib_Class2d_SiDans_OnMode(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _CSLib.delete_CSLib_Class2d
    __del__ = lambda self: None
CSLib_Class2d_swigregister = _CSLib.CSLib_Class2d_swigregister
CSLib_Class2d_swigregister(CSLib_Class2d)

class CSLib_NormalPolyDef(OCC.Core.math.math_FunctionWithDerivative):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.math.math_FunctionWithDerivative]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSLib_NormalPolyDef, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.math.math_FunctionWithDerivative]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CSLib_NormalPolyDef, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Parameters
        ----------
        k0: int
        li: TColStd_Array1OfReal

        Returns
        -------
        None

        """
        this = _CSLib.new_CSLib_NormalPolyDef(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __repr__ = _dumps_object

    __swig_destroy__ = _CSLib.delete_CSLib_NormalPolyDef
    __del__ = lambda self: None
CSLib_NormalPolyDef_swigregister = _CSLib.CSLib_NormalPolyDef_swigregister
CSLib_NormalPolyDef_swigregister(CSLib_NormalPolyDef)



# This file is compatible with both classic and new-style classes.


