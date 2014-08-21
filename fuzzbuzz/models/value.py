#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import functools

from attr_types import Set, Namespace, String
from constraints import *

class UnboundValueError(RuntimeError): pass
class BoundValueError(RuntimeError): pass
class Unwritable(RuntimeError): pass

class Value(object):

    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    def __eq__(self, o):
        if not isinstance(o, Value): return False
        return (
          self.value(None) == o.value(None) and self.type(None) and o.type(None)
        )

    def __repr__(self): return str(self)

    def __str__(self):
        if self.__class__ == Value:
            return "<Value (%s, %s)>" % (str(self.value(None)), str(self.type(None)))
        else:
            return object.__repr__(self)

    def replace(self, from_sym, to_sym):
        '''Converts all symbols which match "from_sym" to "to_sym" in the
        constraint
        @param from_sym : (name, occurence) -> (string, int)
        @param to_sym : (name, occurence) -> (string, int)
        @returns : a new value of the same type'''
        return self

    def allows(self, type):
        '''Detirmines whether objects of type are allowed to be the value of
        this object
        @param type : a type from models.attr_types
        @returns : a boolean'''
        return True

    def type(self, objs):
        return getattr(self, '_%s__type' % self.__class__.__name__)

    def value(self, objs):
        return getattr(self, '_%s__value' % self.__class__.__name__)

    def make_constraint(self, obj, value, type):
        myval = getattr(self, '_%s__value' % self.__class__.__name__)
        if myval != value: return FalseConstraint()
        return TrueConstraint()

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

    def replace(self, from_sym, to_sym):
        return SetValue([
          val.replace(from_sym, to_sym) if isinstance(val, Value) else val
          for val in self.values
        ])

    def allows(self, type):
        return True

    def make_constraint(self, objs, value, type):
        #print values
        assert type == Set
        constraints = list()
        for val in self.values:
            constraints.append(MultiValueConstraint(val, tuple(value)))
        if len(constraints) > 1:
            return AndConstraint(constraints)
        elif len(constraints) == 1:
            return constraints[0]
        else:
            return TrueConstraint()

    def value(self, objs):
        return set(val.value(objs) if isinstance(val, Value) else val
                  for val in self.values)

    def set_value(self, objs, value):
        self.values = tuple(val for val in value)

class DictValue(Value):

    def __init__(self, values):
        self.values = values
        self.__type = Namespace

    def replace(self, from_sym, to_sym):
        return DictValue([
          (
            (key.replace(from_sym, to_sym) if isinstance(key, Value) else key),
            (val.replace(from_sym, to_sym) if isinstance(val, Value) else val),
          )
          for (key,val) in self.values
        ])

    def allows(self, type):
        return True

    def make_constraint(self, objs, value, type):
        return TrueConstraint()

    def value(self, objs):
        return dict(
            (
              (key.value(objs) if isinstance(key, Value) else key),
              (val.value(objs) if isinstance(val, Value) else val),
            )
            for (key,val) in self.values
        )

    def set_value(self, objs, value):
        self.values = tuple((key,val) for (key,val) in value)
