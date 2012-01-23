#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from nose import tools

from value import Value, SetValue, BoundValueError
from attr_types import *

def test_Value_instantiate():
    objs = dict()
    v = Value('type', 'value')
    assert isinstance(v, Value)
    assert v.type(objs) == 'type'
    assert v.value(objs) == 'value'

def test_Set_instantiate():
    objs = dict()
    v = SetValue([Value(Number, 1),Value(Number, 2),Value(Number, 3)])
    assert isinstance(v, SetValue)
    assert v.type(objs) == Set
    assert v.value(objs) == {1,2,3}
    