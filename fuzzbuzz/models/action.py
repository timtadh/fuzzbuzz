#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import abc, copy, random

import attr_types
import value
import binop
from constraints import *

class AbstractAction(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def unconstrained(self, objs, constraint): pass

    @abc.abstractmethod
    def flow_constraints(self, objs, prior_constraint): pass

    @abc.abstractmethod
    def execute(self, objs): pass

    @abc.abstractmethod
    def fillvalues(self, objs, constraint): pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<AbstractAction>'


class Action(AbstractAction):

    def __init__(self, stmts):
        self.stmts = stmts

    def unconstrained(self, objs, constraint):
        return all(stmt.unconstrained(objs, constraint) for stmt in self.stmts)

    def flow_constraints(self, objs, prior):
        constraints = [stmt.flow_constraints(objs, prior)
                        for stmt in self.stmts]
        constraints = [c for c in constraints
                        if not isinstance(c, TrueConstraint)]
        if any(isinstance(c, FalseConstraint) for c in constraints):
            return FalseConstraint()
        elif len(constraints) > 1:
            return AndConstraint(constraints)
        elif len(constraints) == 1:
            return constraints[0]
        else:
            return TrueConstraint()

    def execute(self, objs):
        for stmt in self.stmts:
            stmt.execute(objs)

    def fillvalues(self, objs, constraint):
        for stmt in self.stmts:
            stmt.fillvalues(objs, constraint)

    def __str__(self):
        return '<Action %s>' % str(self.stmts)

## There are two types of action statements
##  1) Assign statements
##  2) If statements

class Assign(AbstractAction):

    def __init__(self, left, right):
        #print left, right
        self.left = left
        self.right = right

    def unconstrained(self, objs, constraint):
        print objs
        nobjs = copy.deepcopy(objs)
        constraint.flow(nobjs)
        if not self.left.has_value(nobjs): return True
        if self.right.has_value(nobjs):
            print constraint
            print self.left, self.right
            print self.left.value(nobjs), '==', self.right.value(nobjs)
            if (self.left.type(nobjs) == attr_types.Set and
              self.right.type(nobjs) == attr_types.Set
            ):
                return self.right.value(nobjs).issubset(self.left.value(nobjs))
            return self.left.value(nobjs) == self.right.value(nobjs)
        else:
            print '-->', 'reached'
            print constraint
            print self.left, self.right
            print self.left.value(nobjs)
            if hasattr(self.right, 'lookup_chain'):
                print self.right.lookup_chain
            print '------>', self.left.type(nobjs), self.right.writable(self.left.type(nobjs))
            print self.right
            print issubclass(self.right.__class__, binop.BinOp)
            if issubclass(self.right.__class__, binop.BinOp):
                return self.right.satisfiable(nobjs, self.left.value(nobjs))
            return self.right.writable(self.left.type(nobjs))

    def flow_constraints(self, objs, prior):
        values, ok = prior.produce(objs, self.left)
        if not ok:
            return TrueConstraint()
        if self.right.type(objs) == attr_types.Set:
            constraints = [self.right.make_constraint(objs, values, attr_types.Set)]
        else:
            constraints = [
                self.right.make_constraint(objs, value, attr_types.Type(value))
                for value in values
            ]
        if len(constraints) > 1:
            constraint = OrConstraint(constraints)
        elif len(constraints) == 1:
            constraint = constraints[0]
        else:
            constraint = TrueConstraint()
        print
        print '-------------------------------------------'
        print prior
        print values
        print constraint
        print '-------------------------------------------'
        print
        return constraint

    def execute(self, objs):
        left = self.left.has_value(objs)
        right = self.right.has_value(objs)
        if left and right:
            #print self.left
            #if self.right.type(objs) == attr_types.Set:
                #print self.right.values[0].lookup_chain[0].obj.name
            print '----->', self.left.value(objs)
            print '----->', self.right.value(objs)
            assert self.left.value(objs) == self.right.value(objs)
            return
        else:
            assert right
            self.left.set_value(objs, self.right.value(objs))

    def fillvalues(self, objs, constraint):
        print 'filling objs', constraint
        print 'left', self.left
        print 'right', self.right
        print 'produced value for left', constraint.produce(objs, self.left)
        print 'produced value for right', constraint.produce(objs, self.right)
        #print 'before', objs
        #constraint.flow(objs)
        #print 'flowed values', objs
        #print 'filled objs', objs
        #left_values, lok = constraint.produce(objs, self.left)
        right_values, rok = constraint.produce(objs, self.right)

        if self.right.has_value(objs) and self.left.has_value(objs):
            return
        elif self.right.has_value(objs):
            return ## This is only left to right
        elif self.left.has_value(objs):
            print 'left value', self.right.value(objs)
            print 'right values', right_values
            assert rok == False
            self.right.set_value(objs, self.left.value(objs))
        elif rok:
            print self.right.type(objs)
            if self.right.type(objs) == attr_types.Set:
                self.right.set_value(objs, right_values)
            else:
                self.right.set_value(objs, random.choice(tuple(right_values)))

    def __str__(self):
        return '<Assign %s = %s>' % (self.left, self.right)

class If(AbstractAction):

    def __init__(self, condition, then, otherwise=None):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def unconstrained(self, objs, constraint):
        #print 'xxx', objs
        #print 'xxx', self.condition
        #print 'xxx', 'condition applies', self.condition.applies(objs)
        nobjs = dict()
        constraint.flow(nobjs)
        then = self.then.unconstrained(nobjs, constraint)
        otherwise = True
        if self.otherwise is not None:
            otherwise = self.otherwise.unconstrained(nobjs, constraint)

        if not self.condition.applies(objs):
            if then and otherwise: return True
            elif then or otherwise: raise Exception, \
                'Need to pass the condition on as a checked constraint'
            else: return False
        elif self.condition.evaluate(objs):
            return then
        else:
            return otherwise

    def flow_constraints(self, objs, prior): raise Exception, NotImplemented

    def execute(self, objs):
        if self.condition.evaluate(objs):
            self.then.execute(objs)
        elif self.otherwise is not None:
            self.otherwise.execute(objs)

    def fillvalues(self, objs, constraint):
        raise Exception, "Invalid implementation fixme"
        if self.condition.evaluate(objs):
            self.then.fillvalues(objs)
        elif self.otherwise is not None:
            self.otherwise.fillvalues(objs)

    def __str__(self):
        return '<If (%s) then %s else %s>' \
            % (self.condition, self.then, self.otherwise)
