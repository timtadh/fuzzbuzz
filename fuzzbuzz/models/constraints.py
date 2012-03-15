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
    def satisfiable(self, objs):
      '''Computes whether or not the constraint is satisfiable with the
      current namespace.
      @param objs : a namespace
      @returns : boolean'''

    @abc.abstractmethod
    def flow(self, objs):
      '''Solves the constraint equations updating the objs namespace where
      appropriate.
      @param objs : a namespace'''

    @abc.abstractmethod
    def replace(self, from_sym, to_sym):
        '''Converts all symbols which match "from_sym" to "to_sym" in the
        constraint
        @param from_sym : (name, occurence) -> (string, int)
        @param to_sym : (name, occurence) -> (string, int)
        @returns : a new constraint of the same type'''

    @abc.abstractmethod
    def produce(self, obj):
        '''Produce a value for obj, taking into account the context objs
        and the asserted values of constraint
        @param obj : an object in the value heirarchy. (AttrChain?)
        @returns values, success
          values : a list of values (None on failure)
          success : boolean'''

    @abc.abstractmethod
    def constrains(self, obj):
        '''Find out whether or not this object is full constrained by this
        formula
        @param obj : an object in the value heirarchy. (AttrChain?)
        @returns boolean'''

class FalseConstraint(Constraint):

    def satisfiable(self, objs): return False
    def flow(self, objs): pass
    def replace(self, from_sym, to_sym): return self
    def produce(self, obj): return None, False
    def constrains(self, obj): return False

class TrueConstraint(Constraint):

    def satisfiable(self, objs): return True
    def flow(self, objs): pass
    def replace(self, from_sym, to_sym): return self
    def produce(self, obj): return None, False
    def constrains(self, obj): return False

class AndConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return all(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        for con in self.constraints:
            con.flow(objs)

    def replace(self, from_sym, to_sym):
        return AndConstraint([
          con.replace(from_sym, to_sym) for con in self.constraints
        ])

    def produce(self, obj):
        for con in self.constraints:
            v, ok = con.produce(obj)
            if ok: return v, ok
        return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<AndConstraint %s>" % str(self.constraints)

class OrConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return any(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        #print 'statisfiable ? ', self.constraints
        satisfiable = [con for con in self.constraints if con.satisfiable(objs)]
        #print 'those which are satisfiable ', satisfiable
        constraint = choice(satisfiable)
        constraint.flow(objs)

    def replace(self, from_sym, to_sym):
        return OrConstraint([
          con.replace(from_sym, to_sym) for con in self.constraints
        ])

    def produce(self, obj):
        values = set()
        for con in self.constraints:
            v, ok = con.produce(obj)
            if ok:
                values = values.union(v)
        if values:
            return values, True
        else:
            return None, False

    def constrains(self, obj):
        c = True
        for con in self.constraints:
            _, ok = con.produce(obj)
            c = ok and c
        return c

    def __repr__(self): return str(self)

    def __str__(self):
        return "<OrConstraint %s>" % str(self.constraints)

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

    def replace(self, from_sym, to_sym):
        return SingleValueConstraint(
          self.obj.replace(from_sym, to_sym),
          self.value
        )

    def produce(self, obj):
        if self.obj == obj:
            return set([self.value]), True
        else:
            return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<SingleValueConstraint %s, %s>" % (str(self.obj), str(self.value))

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
            print self.obj.value(objs), self.values
            assert self.obj.value(objs) in self.values
        else:
            self.obj.set_value(objs, choice(self.values))

    def replace(self, from_sym, to_sym):
        return MultiValueConstraint(
          self.obj.replace(from_sym, to_sym),
          self.values
        )

    def produce(self, obj):
        if self.obj == obj:
            return set(self.values), True
        else:
            return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<MultiValueConstraint %s, %s>" % (str(self.obj), str(self.values))

class SubsetConstraint(Constraint):

    def __init__(self, obj, values):
        self.obj = obj
        self.values = values

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs).issubset(self.values)
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs).issubset(self.values)
        else:
            self.obj.set_value(objs, set(self.values))

    def replace(self, from_sym, to_sym):
        return SubsetConstraint(
          self.obj.replace(from_sym, to_sym),
          self.values
        )

    def produce(self, obj):
        if self.obj == obj:
            return set(self.values), True
        else:
            return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<SubsetConstraint %s, %s>" % (str(self.obj), str(self.values))

class ContainsConstraint(Constraint):

    def __init__(self, obj, value):
        self.obj = obj
        self.value = value

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.value in self.obj.value(objs)
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.value in self.obj.value(objs)
        else:
            self.obj.set_value(objs, set([self.value]))

    def replace(self, from_sym, to_sym):
        return ContainsConstraint(
          self.obj.replace(from_sym, to_sym),
          self.value
        )

    def produce(self, obj):
        if self.obj == obj:
            return set([self.value]), True
        else:
            return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<ContainsConstraint %s, %s>" % (str(self.obj), str(self.value))


class SupersetConstraint(Constraint):

    def __init__(self, obj, values):
        self.obj = obj
        self.values = values

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs).issuperset(self.values)
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs).issuperset(self.values)
        else:
            self.obj.set_value(objs, set(self.values))

    def replace(self, from_sym, to_sym):
        return SupersetConstraint(
          self.obj.replace(from_sym, to_sym),
          self.values
        )

    def produce(self, obj):
        if self.obj == obj:
            return set(self.values), True
        else:
            return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<SupersetConstraint %s, %s>" % (str(self.obj), str(self.values))

class IsNotConstraint(Constraint):

    def __init__(self, obj, value):
        self.obj = obj
        self.value = value

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs) != self.value
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs) != self.value

    def replace(self, from_sym, to_sym):
        return IsNotConstraint(
          self.obj.replace(from_sym, to_sym),
          self.value
        )

    def produce(self, obj):
        return None, False

    def constrains(self, obj):
        _, ok = self.produce(obj)
        return ok

    def __repr__(self): return str(self)

    def __str__(self):
        return "<IsNotConstraint %s != %s>" % (str(self.obj), str(self.value))
