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
    def unconstrained(self, constraint): pass

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

    def unconstrained(self, constraint):
        return all(stmt.unconstrained(constraint) for stmt in self.stmts)

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

    def unconstrained(self, constraint):
        ## Attempt to discern if the constraints are in conflict with the
        ## action.
        print '->', self
        print '->', constraint
        left_values, has_left = constraint.produce(dict(), self.left)
        right_values, has_right = constraint.produce(dict(), self.right)
        print left_values, right_values
        print has_left, has_right
        if not has_left:
            print True
            return True
        if has_right:
            print left_values & right_value
            return left_values & right_values
        else:
            print 'issubclass(self.right.__class__, binop.BinOp)', issubclass(self.right.__class__, binop.BinOp)
            print 'self.right.__class__ != value.Value', self.right.__class__ != value.Value
            if issubclass(self.right.__class__, binop.BinOp):
                return any(
                  self.right.satisfiable(dict(), lv) for lv in left_values)
            if self.right.__class__ != value.Value:
                print '(self.right.allows(attr_types.Type(lv)) for lv in left_values)', any(
                  self.right.allows(attr_types.Type(lv)) for lv in left_values)
                return any(
                  self.right.allows(attr_types.Type(lv)) for lv in left_values)
            else:
                print self.right.value(dict()), left_values, self.right.value(dict()) in left_values
                return self.right.value(dict()) in left_values

    def flow_constraints(self, objs, prior):
        ## Transform applicable prior constraint into a new constraint.
        values, has = prior.produce(objs, self.left)
        if not has: ## If there is no values for left, it is unconstrained
            return TrueConstraint()
        ## If right is known to be a set give it all the values.
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
        return constraint

    def execute(self, objs):
        ## Executes the action
        ## Eg. it assigns the value in the right to the left
        left = self.left.has_value(objs)
        right = self.right.has_value(objs)
        if left and right:
            assert self.left.value(objs) == self.right.value(objs)
            return
        ## right should always have a value (this will raise unbound
        ## value error if it doesn't)
        self.left.set_value(objs, self.right.value(objs))

    def fillvalues(self, objs, constraint):
        ## Fill values fills in the the right side of the assignment.
        ## It fills it from 2 places.
        ## (1) the left side
        ## (2) the from values produced by the constraint.
        right_values, rok = constraint.produce(objs, self.right)
        if self.right.has_value(objs):
            ##
            return
        elif self.left.has_value(objs):
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
        #raise Exception, "needs to be re-written"
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def unconstrained(self, constraint):
        then = self.then.unconstrained(constraint)
        otherwise = True
        if self.otherwise is not None:
            otherwise = self.otherwise.unconstrained(constraint)
        return then or otherwise

    def flow_constraints(self, objs, prior):
        #raise Exception, "These should be conditioned constraints"
        constraints = list()
        constraints.append(self.then.flow_constraints(objs, prior))
        if self.otherwise is not None:
            constraints.append(self.otherwise.flow_constraints(objs, prior))
        if len(constraints) > 1:
            return OrConstraint(constraints)
        return constraints[0]

    def execute(self, objs):
        if self.condition.evaluate(objs):
            self.then.execute(objs)
        elif self.otherwise is not None:
            self.otherwise.execute(objs)

    def fillvalues(self, objs, constraint):
        if self.condition.evaluate(objs):
            self.then.fillvalues(objs, constraint)
        elif self.otherwise is not None:
            self.otherwise.fillvalues(objs, constraint)

    def __str__(self):
        return '<If (%s) then %s else %s>' \
            % (self.condition, self.then, self.otherwise)
