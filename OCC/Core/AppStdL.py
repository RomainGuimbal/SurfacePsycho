# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
AppStdL module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_appstdl.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_AppStdL')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_AppStdL')
    _AppStdL = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_AppStdL', [dirname(__file__)])
        except ImportError:
            import _AppStdL
            return _AppStdL
        try:
            _mod = imp.load_module('_AppStdL', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _AppStdL = swig_import_helper()
    del swig_import_helper
else:
    import _AppStdL
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
    __swig_destroy__ = _AppStdL.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _AppStdL.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _AppStdL.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _AppStdL.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _AppStdL.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _AppStdL.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _AppStdL.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _AppStdL.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _AppStdL.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _AppStdL.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _AppStdL.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _AppStdL.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _AppStdL.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _AppStdL.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _AppStdL.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _AppStdL.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _AppStdL.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _AppStdL.SwigPyIterator_swigregister
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
    return _AppStdL.process_exception(error, method_name, class_name)
process_exception = _AppStdL.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TDocStd
import OCC.Core.TDF
import OCC.Core.TCollection
import OCC.Core.TColStd
import OCC.Core.CDF
import OCC.Core.CDM
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.Resource
import OCC.Core.PCDM
import OCC.Core.Storage

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_AppStdL_Application_Create() -> "opencascade::handle< AppStdL_Application >":
    return _AppStdL.Handle_AppStdL_Application_Create()
Handle_AppStdL_Application_Create = _AppStdL.Handle_AppStdL_Application_Create

def Handle_AppStdL_Application_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< AppStdL_Application >":
    return _AppStdL.Handle_AppStdL_Application_DownCast(t)
Handle_AppStdL_Application_DownCast = _AppStdL.Handle_AppStdL_Application_DownCast

def Handle_AppStdL_Application_IsNull(t: 'opencascade::handle< AppStdL_Application > const &') -> "bool":
    return _AppStdL.Handle_AppStdL_Application_IsNull(t)
Handle_AppStdL_Application_IsNull = _AppStdL.Handle_AppStdL_Application_IsNull
class AppStdL_Application(OCC.Core.TDocStd.TDocStd_Application):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.TDocStd.TDocStd_Application]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AppStdL_Application, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.TDocStd.TDocStd_Application]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AppStdL_Application, name)
    __repr__ = _swig_repr

    def DumpJsonToString(self, depth: 'int'=-1) -> "std::string":
        """
        DumpJsonToString(AppStdL_Application self, int depth=-1) -> std::string
        DumpJsonToString(AppStdL_Application self) -> std::string
        """
        return _AppStdL.AppStdL_Application_DumpJsonToString(self, depth)



    @staticmethod
    def DownCast(t):
      return Handle_AppStdL_Application_DownCast(t)


    __repr__ = _dumps_object


    def __init__(self):
        """__init__(AppStdL_Application self) -> AppStdL_Application"""
        this = _AppStdL.new_AppStdL_Application()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _AppStdL.delete_AppStdL_Application
    __del__ = lambda self: None
AppStdL_Application_swigregister = _AppStdL.AppStdL_Application_swigregister
AppStdL_Application_swigregister(AppStdL_Application)



# This file is compatible with both classic and new-style classes.


