#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import abc

import attr_types
import value
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
    def fillvalues(self, objs): pass

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

    def fillvalues(self, objs):
        for stmt in self.stmts:
            stmt.fillvalues(objs)

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
        nobjs = dict(objs)
        constraint.flow(nobjs)
        if not self.left.has_value(nobjs): return True

        if self.right.has_value(nobjs):
            return self.left.value(nobjs) == self.right.value(nobjs)
        else:
            #print '------>', self.left.type(nobjs), self.right.writable(self.left.type(nobjs))
            #print self.right
            if self.right.writable(self.left.type(nobjs)):
                return True
            else:
                return False

    def flow_constraints(self, objs, prior):
        def constrain(objs, obj, val, prior):
            #print obj, value
            val_value = val.value(objs)
            val_type = val.type(objs)
            #obj_type = obj.type(objs)
            #print val_type, val_value
            if val_type == attr_types.Set:
                if isinstance(obj, value.SetValue):
                    for v in obj.values:
                        print 'x', v
                    raise Exception
                    #return SubsetConstraint(obj, val_value)
                return MultiValueConstraint(obj, val_value)
                #raise Exception, NotImplemented
            elif val_type == attr_types.String:
                raise Exception, NotImplemented
            elif val_type == attr_types.Number:
                raise Exception, NotImplemented
            elif val_type == attr_types.NoneType:
                raise Exception, NotImplemented
            else:
                raise Exception, "Unsupport type"
        nobjs = dict(objs)
        prior.flow(nobjs)
        print '------>', nobjs, prior.obj if hasattr(prior, 'obj') else prior
        if not self.left.has_value(nobjs): return TrueConstraint()

        if self.right.has_value(nobjs):
            if self.left.value(nobjs) == self.right.value(nobjs):
                return TrueConstraint()
            else:
                return FalseConstraint()
        else:
            if self.right.writable(self.left.type(nobjs)):
                print self.right, self.left
                #raise Exception, "Here it get hard my friends!"
                return constrain(objs, self.right, self.left, prior)
            else:
                return FalseConstraint()

    def execute(self, objs):
        left = self.left.has_value(objs)
        right = self.right.has_value(objs)
        if left and right:
            assert self.left.value(objs) == self.right.value(objs)
            return
        else:
            assert right
            self.left.set_value(objs, self.right.value(objs))

    def fillvalues(self, objs):
        if self.right.has_value(objs): return
        if self.left.has_value(objs):
            self.right.set_value(objs, self.left.value(objs))

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
        then = self.then.unconstrained(constraint, nobjs)
        otherwise = True
        if self.otherwise is not None:
            otherwise = self.otherwise.unconstrained(constraint, nobjs)
        
        if not self.condition.applies(objs):
            if then and otherwise: return True
            elif then or otherwise: raise Exception, \
                'Need to pass the condition on as a checked constraint'
            else: return False
        elif self.condition.evaluate(objs):
            return then
        else:
            return otherwise

    def execute(self, objs):
        if self.condition.evaluate(objs):
            self.then.execute(objs)
        elif self.otherwise is not None:
            self.otherwise.execute(objs)

    def fillvalues(self, objs):
        if self.condition.evaluate(objs):
            self.then.fillvalues(objs)
        elif self.otherwise is not None:
            self.otherwise.fillvalues(objs)

    def __str__(self):
        return '<If (%s) then %s else %s>' \
            % (self.condition, self.then, self.otherwise)