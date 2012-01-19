#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from nose import tools

from value import Value, SetValue, WritableValue
from attr_types import *

def test_Value_instantiate():
    creator = Value('type', 'value')
    v = creator(None)
    assert hasattr(creator, 'func_name')
    assert isinstance(v, Value)
    assert v.type == 'type'
    assert v.value == 'value'

@tools.raises(RuntimeError)
def test_Value_attempt_write():
    creator = Value('type', None)
    v = creator(None)
    v.__writehook__ = lambda value: value
    assert v.value == None
    v.value = 'value'

def test_Set_instantiate():
    creator = SetValue([Value(Number, 1),Value(Number, 2),Value(Number, 3)])
    v = creator(None)
    assert hasattr(creator, 'func_name')
    assert isinstance(v, SetValue)
    assert v.type == Set
    assert v.value == {1,2,3}

def test_WritableValue_instantiate():
    creator = WritableValue('type', 'value')
    v = creator(None)
    assert hasattr(creator, 'func_name')
    assert isinstance(v, WritableValue)
    assert v.type == 'type'
    assert v.value == 'value'

def test_WritableValue_write():
    creator = WritableValue('type', None)
    v = creator(None)
    v.__writehook__ = lambda value: value
    assert v.value == None
    v.value = 'value'
    assert v.value == 'value'
    
@tools.raises(RuntimeError)
def test_WritableValue_2_writes():
    creator = WritableValue('type', None)
    v = creator(None)
    v.__writehook__ = lambda value: value
    assert v.value == None
    v.value = 'value'
    assert v.value == 'value'
    v.value = 'value2'
    