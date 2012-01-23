#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from nose import tools

from value import UnboundValueError
from attribute import *
from attr_types import *

def test_Object_instantiate():
    objs = {'test':1}
    v = Object('test')
    assert isinstance(v, Object)
    assert v.value(objs) == 1

def test_Object_has_value():
    objs = {'test':1}
    v = Object('test')
    assert v.has_value(objs)

def test_Object_has_novalue():
    objs = {'test':None}
    v = Object('test')
    assert not v.has_value(objs)

def test_Object_has_value_uninstantiatable():
    objs = {'asdf':None}
    v = Object('test')
    assert not v.has_value(objs)

def test_SymbolObject_instantiate():
    objs = {('test', 12):1}
    v = SymbolObject('test', 12)
    assert isinstance(v, SymbolObject)
    assert v.value(objs) == 1

def test_FCall_instantiate():
    objs = {'test':1}
    v = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    assert isinstance(v, FCall)
    assert v.value(objs) == [1,2,3]

def test_CallChain_instantiate():
    objs = {'test':1}
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    v = CallChain([fc1, fc2, fc3])
    assert isinstance(v, CallChain)
    assert v.value(objs) == [[1,2,3],[4,5],[6,7]]

def test_Attribute_instantiate():
    def f(a,b,c):
        def g(d,e):
            def h(f, g):
                return a*b*c + d*e + f*g
            return h
        return g
    gobjs, cobjs = {'test':1}, {'f':f}
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    cc = CallChain([fc1, fc2, fc3])
    obj = Object('f')
    v = Attribute(obj, cc)
    assert isinstance(v, Attribute)
    assert v.value(gobjs, cobjs) == 1*2*3 + 4*5 + 6*7

def test_AttrChain_instantiate():
    A = dict()
    def reflect():
        return A
    def f(a,b,c):
        def g(d,e):
            def h(f, g):
                return a*b*c + d*e + f*g
            return h
        return g
    A.update({'reflect':reflect, 'f':f})
    objs = {'test':1, 'f':None, ('a',1):A}
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    cc = CallChain([fc1, fc2, fc3])
    obj = Object('f')
    sym = SymbolObject('a', 1)
    a1 = Attribute(sym)
    a2 = Attribute(Object('reflect'), CallChain([FCall([])]))
    a3 = Attribute(obj, cc)
    v = AttrChain([a1,a2,a3])
    assert isinstance(v, AttrChain)
    assert v.value(objs) == 1*2*3 + 4*5 + 6*7
