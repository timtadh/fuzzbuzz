#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attribute import *
from attr_types import *

def test_Object_instantiate():
    creator = Object('test')
    v = creator({'test':1})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, Object)
    #assert v.type == 'type'
    assert v.value == 1

def test_SymbolObject_instantiate():
    creator = SymbolObject('test', 12)
    v = creator({('test', 12):1})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, SymbolObject)
    #assert v.type == 'type'
    assert v.value == 1

def test_FCall_instantiate():
    creator = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    v = creator({'test':1})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, FCall)
    #assert v.type == 'type'
    assert v.value == [1,2,3]

def test_CallChain_instantiate():
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    creator = CallChain([fc1, fc2, fc3])
    v = creator({'test':1})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, CallChain)
    #assert v.type == 'type'
    assert v.value == [[1,2,3],[4,5],[6,7]]

def test_Attribute_instantiate():
    def f(a,b,c):
        def g(d,e):
            def h(f, g):
                return a*b*c + d*e + f*g
            return h
        return g
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    cc = CallChain([fc1, fc2, fc3])
    obj = Object('f')
    creator = Attribute(obj, cc)
    v = creator({'test':1}, {'f':f})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, Attribute)
    #assert v.type == 'type'
    assert v.value == 1*2*3 + 4*5 + 6*7

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
    fc1 = FCall([Object('test'),Value(Number, 2),Value(Number, 3)])
    fc2 = FCall([Value(Number, 4),Value(Number, 5)])
    fc3 = FCall([Value(Number, 6),Value(Number, 7)])
    cc = CallChain([fc1, fc2, fc3])
    obj = Object('f')
    sym = SymbolObject('a', 1)
    a1 = Attribute(sym)
    a2 = Attribute(Object('reflect'), CallChain([FCall([])]))
    a3 = Attribute(obj, cc)
    creator = AttrChain([a1,a2,a3])
    v = creator({'test':1, 'f':None, ('a',1):A})
    assert hasattr(creator, 'func_name')
    assert isinstance(v, AttrChain)
    #assert v.type == 'type'
    assert v.value == 1*2*3 + 4*5 + 6*7
