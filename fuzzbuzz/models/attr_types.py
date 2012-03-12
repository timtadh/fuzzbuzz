#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Type(object):
    def __new__(self, obj):
        if isinstance(obj, str): return String
        elif isinstance(obj, int): return Number
        elif isinstance(obj, set): return Set
        elif isinstance(obj, tuple): return Set
        elif isinstance(obj, dict): return Dict
        elif isinstance(obj, NoneType): return NoneType
        raise RuntimeError, "Obj did not map to any type %s" % str(obj)

class UnknownType(Type):
    def __new__(self):
        raise RuntimeError, 'Set cannot be instantiated'

class String(Type):
    def __new__(self, value):
        return str(value)

class Number(Type):
    def __new__(self, value):
        return int(value)

class Set(Type):
    def __new__(self):
        raise RuntimeError, 'Set cannot be instantiated'

class Namespace(Type):
    def __new__(self):
        raise RuntimeError, 'Namespace cannot be instantiated'

class NoneType(Type):
    def __new__(self):
        return object.__new__(NoneType)

    def __eq__(self, b):
        return isinstance(b, NoneType)

    def __ne__(self, b):
        return not isinstance(b, NoneType)
