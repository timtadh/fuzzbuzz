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
        #print clazz, allargs
        instance.__init__(*allargs, **kwargs)
        return instance
    instance_creator.func_name = clazz.__name__ + '_creator'
    setattr(instance_creator, 'clazz', clazz)
    for key, value in kwargs.get('register', dict()).iteritems():
        setattr(instance_creator, name, value)
    return instance_creator


#class defer(type):

    #def __call__(cls, *args, **kwargs):
        #print '------', cls, args
        #def instance_creator(*objs):
            #'Makes a new instance of the specified class'
            #allargs = list(objs) + list(args)
            #instance = object.__new__(cls)
            #instance.__init__(*allargs, **kwargs)
            #return instance
        #print 'defer call', cls
        #instance_creator.func_name = cls.__name__ + '_creator'
        #setattr(instance_creator, 'clazz', cls)
        #return instance_creator
    
class Value(object):

    #__metaclass__ = defer
    
    def __new__(cls, *args, **kwargs): return defer(cls, *args, **kwargs)

    def __init__(self, objs, type, value):
        self.__type = type
        self.__value = value
        self.__writable = False
        #delhook = False
        #if not hasattr(self, '__writehook__'):
            #self.__writehook__ = lambda value: None
            #delhook = True
        #self.__writable = True
        #self.value = value
        #self.__writable = False
        #if delhook:
            #del self.__writehook__

    def __set_writable__(self):
        if not issubclass(self.__class__, WritableValue):
            raise RuntimeError, "Only WritableValue's are allowed to become writable"
        self.__writable = True
    
    @property
    def type(self):
        return self.__type

    def hasvalue(self):
        return self.__value is not None
    
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
