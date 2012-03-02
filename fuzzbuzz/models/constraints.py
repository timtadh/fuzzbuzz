#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from random import choice
import abc


class Constraint(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def satisfiable(self, objs): pass

    @abc.abstractmethod
    def flow(self, objs): pass


class FalseConstraint(Constraint):

    def satisfiable(self, objs): return False

    def flow(self, objs): pass

class TrueConstraint(Constraint):

    def satisfiable(self, objs): return True

    def flow(self, objs): pass

class AndConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return all(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        for con in self.constraints:
            con.flow(objs)

class OrConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return any(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        satisfiable = [con for con in self.constraints if con.satisfiable(objs)]
        constraint = choice(satisfiable)
        constraint.flow(objs)

class SingleValueConstraint(Constraint):

    def __init__(self, obj, value):
        self.obj = obj
        self.value = value

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs) == self.value
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs) == self.value
        else:
            self.obj.set_value(objs, self.value)

class MultiValueConstraint(Constraint):

    def __init__(self, obj, values):
        self.obj = obj
        self.values = values

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs) in self.values
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs) in self.values
        else:
            self.obj.set_value(objs, choice(self.values))

