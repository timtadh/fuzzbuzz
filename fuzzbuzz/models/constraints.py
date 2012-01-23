#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from executable import Executable

class Constraint(Executable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

class Is(Constraint):

    def execute(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.a.value == self.b.value(objs)
        elif a_hasvalue:
            print 'set b to', self.a.value(objs)
            pass
        elif b_hasvalue:
            print 'set a to', self.b.value(objs)
            pass
        else:
            print self.b(objs).value
            print 'no values'
            pass # nothing should need to be done here
