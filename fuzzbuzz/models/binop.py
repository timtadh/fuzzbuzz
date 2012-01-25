#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attr_types import Set
from value import Value

def BinOp(Value):
  
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def type(self, objs):
        raise Exception

    def value(self, objs):
        raise Exception

def SetOp(BinOp):

    def type(self, objs):
        return Set

def Union(SetOp):

    def value(self, objs):
        a = self.a.value(objs)
        b = self.b.value(objs)
        assert isinstance(a, set)
        assert isinstance(b, set)
        return a | b

def Intersection(SetOp):

    def value(self, objs):
        a = self.a.value(objs)
        b = self.b.value(objs)
        assert isinstance(a, set)
        assert isinstance(b, set)
        return a & b
