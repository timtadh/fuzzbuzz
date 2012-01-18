#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value, SetValue
from attr_types import *

def test_Value_instantiate():
    creator = Value('type', 'value')
    v = creator(None)
    assert hasattr(creator, 'func_name')
    assert isinstance(v, Value)
    assert v.type == 'type'
    assert v.value == 'value'

def test_Set_instantiate():
    creator = SetValue([Value(Number, 1),Value(Number, 2),Value(Number, 3)])
    v = creator(None)
    assert hasattr(creator, 'func_name')
    assert isinstance(v, Value)
    assert v.type == Set
    assert v.value == {1,2,3}
    