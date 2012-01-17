#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attr_types import Set, String

def defer(clazz, *args, **kwargs):
    def instance_creator(objs):
        'Makes a new instance of the specified class'
        instance = object.__new__(clazz)
        instance.__init__(objs, *args, **kwargs)
        return instance
    return instance_creator

class Value(object):

    def __new__(cls, *args, **kwargs): return defer(cls, *args, **kwargs)

    def __init__(self, objs, type, value):
        self.__type = type
        self.__value = value
    
    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

class SetValue(Value):

    def __init__(self, objs, values):
        value = set(val(objs).value for val in values)
        super(SetValue, self).__init__(objs, Set, value)

if __name__ == '__main__':
    import attribute
    print attribute.Attribute('a')('b')
    print SetValue([Value(String, 'a'), Value(String, 'b'), Value(String, 'c')])(None).value
