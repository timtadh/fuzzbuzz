#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import functools

from attr_types import Set, String

class UnboundValueError(RuntimeError): pass
class BoundValueError(RuntimeError): pass
class Unwritable(RuntimeError): pass

class Value(object):

    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    def writable(self, type): return False

    def type(self, objs):
        return getattr(self, '_%s__type' % self.__class__.__name__)

    def value(self, objs):
        return getattr(self, '_%s__value' % self.__class__.__name__)

    def has_value(self, *objs):
        value = None
        try:
            value = self.value(*objs)
        except UnboundValueError:
            return False
        return value is not None

    def set_value(self, value, objs):
        raise Unwritable, \
        "%s does not support setting the value" % (self.__class__.__name__)

class SetValue(Value):

    def __init__(self, values):
        self.values = values
        self.__type = Set

    def writable(self, type):
        return True

    def value(self, objs):
        return set(val.value(objs) for val in self.values)

    def set_value(self, objs, value):
        self.values = value
