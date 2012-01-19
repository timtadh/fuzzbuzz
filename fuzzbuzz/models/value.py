#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import functools

from attr_types import Set, String

def defer(clazz, *args, **kwargs):
    def instance_creator(*objs):
        'Makes a new instance of the specified class'
        allargs = list(objs) + list(args)
        instance = object.__new__(clazz)
        instance.__init__(*allargs, **kwargs)
        return instance
    instance_creator.func_name = clazz.__name__ + '_creator'
    return instance_creator

class Value(object):

    def __new__(cls, *args, **kwargs): return defer(cls, *args, **kwargs)

    def __init__(self, objs, type, value):
        self.__type = type
        self.__value = value
        self.__writable = False

    def __set_writable__(self):
        if self.__class__.__name__ != 'WritableValue':
            raise RuntimeError, "Only WritableValue's are allowed to become writable"
        self.__writable = True
    
    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.__writable:
            raise RuntimeError, \
            "%s does not support setting the value" % (self.__class__.__name__)
        if self.value is not None:
            raise RuntimeError, \
            "%s already has a value" % (self.__class__.__name__)
        self.__value = value
        self.__writehook__(value)

class WritableValue(Value):

    def __init__(self, *args, **kwargs):
        super(WritableValue, self).__init__(*args, **kwargs)
        self.__set_writable__()
          
class SetValue(Value):

    def __init__(self, objs, values):
        value = set(val(objs).value for val in values)
        super(SetValue, self).__init__(objs, Set, value)

if __name__ == '__main__':
    import attribute
    print attribute.Attribute('a')('b')
    print SetValue([Value(String, 'a'), Value(String, 'b'), Value(String, 'c')])(None).value
