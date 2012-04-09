#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import abc

class Value(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def type(self, objs): pass

    @abc.abstractmethod
    def value(self, objs): pass

    @abc.abstractmethod
    def has_value(self, *objs): pass

    @abc.abstractmethod
    def set_value(self, objs, value): pass

    @abc.abstractmethod
    def make_constraint(self, objs, value, type): pass


class Solvable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solvable(self, objs, answer):
        '''Computes whether or not the equation is satisfiable with the
        current namespace.
        @param objs : a namespace
        @returns : boolean'''


class Satisfiable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def satisfiable(self, objs):
        '''Computes whether or not the constraint is satisfiable with the
        current namespace.
        @param objs : a namespace
        @returns : boolean'''


class Substitute(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def substitute(self, from_sym, to_sym):
        '''Converts all symbols which match "from_sym" to "to_sym" in the
        equation.
        @param from_sym : (name, occurence) -> (string, int)
        @param to_sym : (name, occurence) -> (string, int)
        @returns : a new constraint of the same type'''


class Flow(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def flow(self, objs):
        '''Updates the namespace (objs) given the rules of the obj.
        @param objs : a namespace'''


class Produce(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def produce(self, objs, obj):
        '''Produce a value for obj, taking into account the context objs
        and the asserted values in the equation
        @param objs : a namespace
        @param obj : an object in the value heirarchy. (AttrChain?)
        @returns values, success
          values : a list of values (None on failure)
          success : boolean'''

