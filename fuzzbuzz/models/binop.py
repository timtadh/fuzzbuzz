#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import abc

from attr_types import Set, Number
from value import Value

class BinOp(Value):

    __metaclass__ = abc.ABCMeta

    def __init__(self, a, b, expected_type):
        self.a = a
        self.b = b
        self._expected_type = expected_type

    def _get_ab(self, objs):
        a = self.a.value(objs)
        b = self.b.value(objs)
        assert isinstance(a, self._expected_type)
        assert isinstance(b, self._expected_type)
        return a,b

    @abc.abstractmethod
    def type(self, objs): pass

    @abc.abstractmethod
    def value(self, objs): pass

    @abc.abstractmethod
    def flow_constraints(self, objs, prior_constraint): pass

    @abc.abstractmethod
    def satisfiable(self, objs, answer): pass

class SetOp(BinOp):

    def __init__(self, a,b):
        super(SetOp, self).__init__(a,b,set)

    def type(self, objs):
        return Set

    def flow_constraints(self, objs, prior_constraint):
        raise Exception, NotImplemented

    def satisfiable(self, objs, answer):
        raise Exception, NotImplemented

class Union(SetOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a | b

class Intersection(SetOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a & b

class Difference(SetOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a - b


class ArithOp(BinOp):

    def __init__(self, a,b):
        super(ArithOp, self).__init__(a,b,int)

    def type(self, objs):
        return Number

    def flow_constraints(self, objs, prior_constraint):
        raise Exception, NotImplemented

    def satisfiable(self, objs, answer):
        raise Exception, NotImplemented

class Add(ArithOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a + b


class Sub(ArithOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a - b

class Mul(ArithOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a * b

class Div(ArithOp):

    def value(self, objs):
        a,b = self._get_ab(objs)
        return a / b
