#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Type(object):
    def __new__(self):
        raise RuntimeError, 'Type cannot be instantiated'

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
