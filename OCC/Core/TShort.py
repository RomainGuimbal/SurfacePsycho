# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
TShort module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_tshort.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _TShort
else:
    import _TShort

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
    __swig_destroy__ = _TShort.delete_SwigPyIterator

    def value(self):
        return _TShort.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _TShort.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _TShort.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _TShort.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _TShort.SwigPyIterator_equal(self, x)

    def copy(self):
        return _TShort.SwigPyIterator_copy(self)

    def next(self):
        return _TShort.SwigPyIterator_next(self)

    def __next__(self):
        return _TShort.SwigPyIterator___next__(self)

    def previous(self):
        return _TShort.SwigPyIterator_previous(self)

    def advance(self, n):
        return _TShort.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _TShort.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _TShort.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _TShort.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _TShort.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _TShort.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _TShort.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _TShort:
_TShort.SwigPyIterator_swigregister(SwigPyIterator)

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
    return _TShort.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_TShort_HArray1OfShortReal_Create():
    return _TShort.Handle_TShort_HArray1OfShortReal_Create()

def Handle_TShort_HArray1OfShortReal_DownCast(t):
    return _TShort.Handle_TShort_HArray1OfShortReal_DownCast(t)

def Handle_TShort_HArray1OfShortReal_IsNull(t):
    return _TShort.Handle_TShort_HArray1OfShortReal_IsNull(t)

def Handle_TShort_HArray2OfShortReal_Create():
    return _TShort.Handle_TShort_HArray2OfShortReal_Create()

def Handle_TShort_HArray2OfShortReal_DownCast(t):
    return _TShort.Handle_TShort_HArray2OfShortReal_DownCast(t)

def Handle_TShort_HArray2OfShortReal_IsNull(t):
    return _TShort.Handle_TShort_HArray2OfShortReal_IsNull(t)

def Handle_TShort_HSequenceOfShortReal_Create():
    return _TShort.Handle_TShort_HSequenceOfShortReal_Create()

def Handle_TShort_HSequenceOfShortReal_DownCast(t):
    return _TShort.Handle_TShort_HSequenceOfShortReal_DownCast(t)

def Handle_TShort_HSequenceOfShortReal_IsNull(t):
    return _TShort.Handle_TShort_HSequenceOfShortReal_IsNull(t)
class TShort_Array1OfShortReal(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def begin(self):
        return _TShort.TShort_Array1OfShortReal_begin(self)

    def end(self):
        return _TShort.TShort_Array1OfShortReal_end(self)

    def cbegin(self):
        return _TShort.TShort_Array1OfShortReal_cbegin(self)

    def cend(self):
        return _TShort.TShort_Array1OfShortReal_cend(self)

    def __init__(self, *args):
        _TShort.TShort_Array1OfShortReal_swiginit(self, _TShort.new_TShort_Array1OfShortReal(*args))

    def Init(self, theValue):
        return _TShort.TShort_Array1OfShortReal_Init(self, theValue)

    def Size(self):
        return _TShort.TShort_Array1OfShortReal_Size(self)

    def Length(self):
        return _TShort.TShort_Array1OfShortReal_Length(self)

    def IsEmpty(self):
        return _TShort.TShort_Array1OfShortReal_IsEmpty(self)

    def Lower(self):
        return _TShort.TShort_Array1OfShortReal_Lower(self)

    def Upper(self):
        return _TShort.TShort_Array1OfShortReal_Upper(self)

    def IsDeletable(self):
        return _TShort.TShort_Array1OfShortReal_IsDeletable(self)

    def IsAllocated(self):
        return _TShort.TShort_Array1OfShortReal_IsAllocated(self)

    def Assign(self, theOther):
        return _TShort.TShort_Array1OfShortReal_Assign(self, theOther)

    def Move(self, theOther):
        return _TShort.TShort_Array1OfShortReal_Move(self, theOther)

    def Set(self, *args):
        return _TShort.TShort_Array1OfShortReal_Set(self, *args)

    def First(self):
        return _TShort.TShort_Array1OfShortReal_First(self)

    def ChangeFirst(self):
        return _TShort.TShort_Array1OfShortReal_ChangeFirst(self)

    def Last(self):
        return _TShort.TShort_Array1OfShortReal_Last(self)

    def ChangeLast(self):
        return _TShort.TShort_Array1OfShortReal_ChangeLast(self)

    def Value(self, theIndex):
        return _TShort.TShort_Array1OfShortReal_Value(self, theIndex)

    def ChangeValue(self, theIndex):
        return _TShort.TShort_Array1OfShortReal_ChangeValue(self, theIndex)

    def __call__(self, *args):
        return _TShort.TShort_Array1OfShortReal___call__(self, *args)

    def SetValue(self, theIndex, theItem):
        return _TShort.TShort_Array1OfShortReal_SetValue(self, theIndex, theItem)

    def Resize(self, theLower, theUpper, theToCopyData):
        return _TShort.TShort_Array1OfShortReal_Resize(self, theLower, theUpper, theToCopyData)
    __swig_destroy__ = _TShort.delete_TShort_Array1OfShortReal

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


# Register TShort_Array1OfShortReal in _TShort:
_TShort.TShort_Array1OfShortReal_swigregister(TShort_Array1OfShortReal)
class TShort_Array2OfShortReal(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _TShort.TShort_Array2OfShortReal_swiginit(self, _TShort.new_TShort_Array2OfShortReal(*args))

    def Init(self, theValue):
        return _TShort.TShort_Array2OfShortReal_Init(self, theValue)

    def Size(self):
        return _TShort.TShort_Array2OfShortReal_Size(self)

    def Length(self):
        return _TShort.TShort_Array2OfShortReal_Length(self)

    def NbRows(self):
        return _TShort.TShort_Array2OfShortReal_NbRows(self)

    def NbColumns(self):
        return _TShort.TShort_Array2OfShortReal_NbColumns(self)

    def RowLength(self):
        return _TShort.TShort_Array2OfShortReal_RowLength(self)

    def ColLength(self):
        return _TShort.TShort_Array2OfShortReal_ColLength(self)

    def LowerRow(self):
        return _TShort.TShort_Array2OfShortReal_LowerRow(self)

    def UpperRow(self):
        return _TShort.TShort_Array2OfShortReal_UpperRow(self)

    def LowerCol(self):
        return _TShort.TShort_Array2OfShortReal_LowerCol(self)

    def UpperCol(self):
        return _TShort.TShort_Array2OfShortReal_UpperCol(self)

    def IsDeletable(self):
        return _TShort.TShort_Array2OfShortReal_IsDeletable(self)

    def Assign(self, theOther):
        return _TShort.TShort_Array2OfShortReal_Assign(self, theOther)

    def Move(self, theOther):
        return _TShort.TShort_Array2OfShortReal_Move(self, theOther)

    def Set(self, *args):
        return _TShort.TShort_Array2OfShortReal_Set(self, *args)

    def Value(self, theRow, theCol):
        return _TShort.TShort_Array2OfShortReal_Value(self, theRow, theCol)

    def ChangeValue(self, theRow, theCol):
        return _TShort.TShort_Array2OfShortReal_ChangeValue(self, theRow, theCol)

    def __call__(self, *args):
        return _TShort.TShort_Array2OfShortReal___call__(self, *args)

    def SetValue(self, theRow, theCol, theItem):
        return _TShort.TShort_Array2OfShortReal_SetValue(self, theRow, theCol, theItem)

    def Resize(self, theRowLower, theRowUpper, theColLower, theColUpper, theToCopyData):
        return _TShort.TShort_Array2OfShortReal_Resize(self, theRowLower, theRowUpper, theColLower, theColUpper, theToCopyData)
    __swig_destroy__ = _TShort.delete_TShort_Array2OfShortReal

# Register TShort_Array2OfShortReal in _TShort:
_TShort.TShort_Array2OfShortReal_swigregister(TShort_Array2OfShortReal)
class TShort_SequenceOfShortReal(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def begin(self):
        return _TShort.TShort_SequenceOfShortReal_begin(self)

    def end(self):
        return _TShort.TShort_SequenceOfShortReal_end(self)

    def cbegin(self):
        return _TShort.TShort_SequenceOfShortReal_cbegin(self)

    def cend(self):
        return _TShort.TShort_SequenceOfShortReal_cend(self)

    def __init__(self, *args):
        _TShort.TShort_SequenceOfShortReal_swiginit(self, _TShort.new_TShort_SequenceOfShortReal(*args))

    def Size(self):
        return _TShort.TShort_SequenceOfShortReal_Size(self)

    def Length(self):
        return _TShort.TShort_SequenceOfShortReal_Length(self)

    def Lower(self):
        return _TShort.TShort_SequenceOfShortReal_Lower(self)

    def Upper(self):
        return _TShort.TShort_SequenceOfShortReal_Upper(self)

    def IsEmpty(self):
        return _TShort.TShort_SequenceOfShortReal_IsEmpty(self)

    def Reverse(self):
        return _TShort.TShort_SequenceOfShortReal_Reverse(self)

    def Exchange(self, I, J):
        return _TShort.TShort_SequenceOfShortReal_Exchange(self, I, J)

    @staticmethod
    def delNode(theNode, theAl):
        return _TShort.TShort_SequenceOfShortReal_delNode(theNode, theAl)

    def Clear(self, theAllocator=0):
        return _TShort.TShort_SequenceOfShortReal_Clear(self, theAllocator)

    def Assign(self, theOther):
        return _TShort.TShort_SequenceOfShortReal_Assign(self, theOther)

    def Set(self, theOther):
        return _TShort.TShort_SequenceOfShortReal_Set(self, theOther)

    def Remove(self, *args):
        return _TShort.TShort_SequenceOfShortReal_Remove(self, *args)

    def Append(self, *args):
        return _TShort.TShort_SequenceOfShortReal_Append(self, *args)

    def Prepend(self, *args):
        return _TShort.TShort_SequenceOfShortReal_Prepend(self, *args)

    def InsertBefore(self, *args):
        return _TShort.TShort_SequenceOfShortReal_InsertBefore(self, *args)

    def InsertAfter(self, *args):
        return _TShort.TShort_SequenceOfShortReal_InsertAfter(self, *args)

    def Split(self, theIndex, theSeq):
        return _TShort.TShort_SequenceOfShortReal_Split(self, theIndex, theSeq)

    def First(self):
        return _TShort.TShort_SequenceOfShortReal_First(self)

    def ChangeFirst(self):
        return _TShort.TShort_SequenceOfShortReal_ChangeFirst(self)

    def Last(self):
        return _TShort.TShort_SequenceOfShortReal_Last(self)

    def ChangeLast(self):
        return _TShort.TShort_SequenceOfShortReal_ChangeLast(self)

    def Value(self, theIndex):
        return _TShort.TShort_SequenceOfShortReal_Value(self, theIndex)

    def ChangeValue(self, theIndex):
        return _TShort.TShort_SequenceOfShortReal_ChangeValue(self, theIndex)

    def __call__(self, *args):
        return _TShort.TShort_SequenceOfShortReal___call__(self, *args)

    def SetValue(self, theIndex, theItem):
        return _TShort.TShort_SequenceOfShortReal_SetValue(self, theIndex, theItem)
    __swig_destroy__ = _TShort.delete_TShort_SequenceOfShortReal

    def __len__(self):
        return self.Size()


# Register TShort_SequenceOfShortReal in _TShort:
_TShort.TShort_SequenceOfShortReal_swigregister(TShort_SequenceOfShortReal)
class TShort_HArray1OfShortReal(TShort_Array1OfShortReal, OCC.Core.Standard.Standard_Transient):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _TShort.TShort_HArray1OfShortReal_swiginit(self, _TShort.new_TShort_HArray1OfShortReal(*args))

    def Array1(self):
        return _TShort.TShort_HArray1OfShortReal_Array1(self)

    def ChangeArray1(self):
        return _TShort.TShort_HArray1OfShortReal_ChangeArray1(self)


    @staticmethod
    def DownCast(t):
      return Handle_TShort_HArray1OfShortReal_DownCast(t)

    __swig_destroy__ = _TShort.delete_TShort_HArray1OfShortReal

# Register TShort_HArray1OfShortReal in _TShort:
_TShort.TShort_HArray1OfShortReal_swigregister(TShort_HArray1OfShortReal)
class TShort_HArray2OfShortReal(TShort_Array2OfShortReal, OCC.Core.Standard.Standard_Transient):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _TShort.TShort_HArray2OfShortReal_swiginit(self, _TShort.new_TShort_HArray2OfShortReal(*args))

    def Array2(self):
        return _TShort.TShort_HArray2OfShortReal_Array2(self)

    def ChangeArray2(self):
        return _TShort.TShort_HArray2OfShortReal_ChangeArray2(self)


    @staticmethod
    def DownCast(t):
      return Handle_TShort_HArray2OfShortReal_DownCast(t)

    __swig_destroy__ = _TShort.delete_TShort_HArray2OfShortReal

# Register TShort_HArray2OfShortReal in _TShort:
_TShort.TShort_HArray2OfShortReal_swigregister(TShort_HArray2OfShortReal)
class TShort_HSequenceOfShortReal(TShort_SequenceOfShortReal, OCC.Core.Standard.Standard_Transient):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _TShort.TShort_HSequenceOfShortReal_swiginit(self, _TShort.new_TShort_HSequenceOfShortReal(*args))

    def Sequence(self):
        return _TShort.TShort_HSequenceOfShortReal_Sequence(self)

    def Append(self, *args):
        return _TShort.TShort_HSequenceOfShortReal_Append(self, *args)

    def ChangeSequence(self):
        return _TShort.TShort_HSequenceOfShortReal_ChangeSequence(self)


    @staticmethod
    def DownCast(t):
      return Handle_TShort_HSequenceOfShortReal_DownCast(t)

    __swig_destroy__ = _TShort.delete_TShort_HSequenceOfShortReal

# Register TShort_HSequenceOfShortReal in _TShort:
_TShort.TShort_HSequenceOfShortReal_swigregister(TShort_HSequenceOfShortReal)



