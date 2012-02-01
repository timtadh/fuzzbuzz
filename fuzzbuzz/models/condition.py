#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from random import choice

from attr_types import Set

class Condition(object):

    def __init__(self, constraint):
        self.constraint = constraint

    def flow(self, objs):
        self.constraint.flow(objs)

class Any(Condition):

    def __init__(self, *options):
        self.options = options

    def applies(self, objs):
        return all(opt.applies(objs) for opt in self.options)

    def evaluate(self, objs):
        return any(opt.evaluate(objs) for opt in self.options)
        
    def flow(self, objs):
        choices = list()
        for opt in self.options:
            #print opt.applies(objs),
            #if opt.applies(objs): print opt.evaluate(objs)
            #else: print
            if opt.applies(objs) and not opt.evaluate(objs): continue
            for choice in opt.flow(dict(objs)):
                choices.append(choice)
        return choices

class All(Condition):

    def __init__(self, *requirements):
        self.requirements = requirements

    def applies(self, objs):
        return all(req.applies(objs) for req in self.requirements)
    
    def evaluate(self, objs):
        return all(req.evaluate(objs) for req in self.requirements)

    def flow(self, objs):
        choices = list()
        for req in self.requirements:
            for choice in req.flow(objs):
                choices.append(choice)
        return choices
        
class Constraint(Condition):

    def __init__(self, a, b):
        self.a = a
        self.b = b

class Is(Constraint):

    def applies(self, objs):
        return self.a.has_value(objs) and self.b.has_value(objs)

    def evaluate(self, objs):
        return self.a.value(objs) == self.b.value(objs)

    def flow(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.a.value(objs) == self.b.value(objs)
        elif a_hasvalue:
            #print 'set b to', self.a.value(objs)
            self.b.set_value(objs, self.a.value(objs))
        elif b_hasvalue:
            #print 'set a to', self.b.value(objs)
            #print self.b.value(objs)
            self.a.set_value(objs, self.b.value(objs))
        else:
            #print self.b(objs).value
            #print 'no values'
            pass # nothing should need to be done here
        return [objs]


class In(Constraint):

    def applies(self, objs):
        return self.a.has_value(objs) and self.b.has_value(objs)

    def evaluate(self, objs):
        return self.a.value(objs) in self.b.value(objs)

    def flow(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.b.type(objs) == Set
            #print self.a.value(objs), self.b.value(objs)
            assert self.a.value(objs) in self.b.value(objs)
        elif a_hasvalue:
            raise Exception, 'Need to think about how to do this correctly'
        elif b_hasvalue:
            assert self.b.type(objs) == Set
            value = choice(tuple(self.b.value(objs)))
            print '----->', value
            self.a.set_value(objs, value)
        else:
            #print self.b(objs).value
            #print 'no values'
            pass # nothing should need to be done here
        return [objs]
