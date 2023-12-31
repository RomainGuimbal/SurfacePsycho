# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
Plugin module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_plugin.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_Plugin')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_Plugin')
    _Plugin = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_Plugin', [dirname(__file__)])
        except ImportError:
            import _Plugin
            return _Plugin
        try:
            _mod = imp.load_module('_Plugin', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _Plugin = swig_import_helper()
    del swig_import_helper
else:
    import _Plugin
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
    __swig_destroy__ = _Plugin.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _Plugin.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _Plugin.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _Plugin.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _Plugin.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _Plugin.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _Plugin.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _Plugin.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _Plugin.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _Plugin.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _Plugin.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _Plugin.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _Plugin.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _Plugin.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _Plugin.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _Plugin.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _Plugin.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _Plugin.SwigPyIterator_swigregister
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
    return _Plugin.process_exception(error, method_name, class_name)
process_exception = _Plugin.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection

from enum import IntEnum
from OCC.Core.Exception import *



class Plugin_MapOfFunctions(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Plugin_MapOfFunctions, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Plugin_MapOfFunctions, name)
    __repr__ = _swig_repr

    def begin(self) -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString >::iterator":
        return _Plugin.Plugin_MapOfFunctions_begin(self)

    def end(self) -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString >::iterator":
        return _Plugin.Plugin_MapOfFunctions_end(self)

    def cbegin(self) -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString >::const_iterator":
        return _Plugin.Plugin_MapOfFunctions_cbegin(self)

    def cend(self) -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString >::const_iterator":
        return _Plugin.Plugin_MapOfFunctions_cend(self)

    def __init__(self, *args):
        this = _Plugin.new_Plugin_MapOfFunctions(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Exchange(self, theOther: 'Plugin_MapOfFunctions') -> "void":
        return _Plugin.Plugin_MapOfFunctions_Exchange(self, theOther)

    def Assign(self, theOther: 'Plugin_MapOfFunctions') -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString > &":
        return _Plugin.Plugin_MapOfFunctions_Assign(self, theOther)

    def Set(self, theOther: 'Plugin_MapOfFunctions') -> "NCollection_DataMap< TCollection_AsciiString,OSD_Function,TCollection_AsciiString > &":
        return _Plugin.Plugin_MapOfFunctions_Set(self, theOther)

    def ReSize(self, N: 'Standard_Integer const') -> "void":
        return _Plugin.Plugin_MapOfFunctions_ReSize(self, N)

    def Bind(self, theKey: 'TCollection_AsciiString const &', theItem: 'OSD_Function const &') -> "Standard_Boolean":
        return _Plugin.Plugin_MapOfFunctions_Bind(self, theKey, theItem)

    def Bound(self, theKey: 'TCollection_AsciiString const &', theItem: 'OSD_Function const &') -> "OSD_Function *":
        return _Plugin.Plugin_MapOfFunctions_Bound(self, theKey, theItem)

    def IsBound(self, theKey: 'TCollection_AsciiString const &') -> "Standard_Boolean":
        return _Plugin.Plugin_MapOfFunctions_IsBound(self, theKey)

    def UnBind(self, theKey: 'TCollection_AsciiString const &') -> "Standard_Boolean":
        return _Plugin.Plugin_MapOfFunctions_UnBind(self, theKey)

    def Seek(self, theKey: 'TCollection_AsciiString const &') -> "OSD_Function const *":
        return _Plugin.Plugin_MapOfFunctions_Seek(self, theKey)

    def Find(self, *args) -> "Standard_Boolean":
        return _Plugin.Plugin_MapOfFunctions_Find(self, *args)

    def ChangeSeek(self, theKey: 'TCollection_AsciiString const &') -> "OSD_Function *":
        return _Plugin.Plugin_MapOfFunctions_ChangeSeek(self, theKey)

    def ChangeFind(self, theKey: 'TCollection_AsciiString const &') -> "OSD_Function &":
        return _Plugin.Plugin_MapOfFunctions_ChangeFind(self, theKey)

    def __call__(self, *args) -> "OSD_Function &":
        return _Plugin.Plugin_MapOfFunctions___call__(self, *args)

    def Clear(self, *args) -> "void":
        return _Plugin.Plugin_MapOfFunctions_Clear(self, *args)
    __swig_destroy__ = _Plugin.delete_Plugin_MapOfFunctions
    __del__ = lambda self: None

    def Size(self) -> "Standard_Integer":
        return _Plugin.Plugin_MapOfFunctions_Size(self)
Plugin_MapOfFunctions_swigregister = _Plugin.Plugin_MapOfFunctions_swigregister
Plugin_MapOfFunctions_swigregister(Plugin_MapOfFunctions)


@classnotwrapped
class Plugin:
	pass




# This file is compatible with both classic and new-style classes.


