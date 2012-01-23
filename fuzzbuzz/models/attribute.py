#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value, UnboundValueError, BoundValueError, Unwritable

class AttrChain(Value):

    def __init__(self, lookup_chain):
        self.lookup_chain = lookup_chain
        self.__type = None                          ## TODO TYPES

    def writable(self): return all(x.writable() for x in self.lookup_chain)

    def value(self, objs):
        cobjs = objs
        cvalue = None
        for attr in self.lookup_chain:
            cvalue = attr.value(objs, cobjs)
            cobjs = cvalue
        return cvalue
    
    def set_value(self, objs, value):
        cobjs = objs
        for attr in self.lookup_chain[:-1]:
            #if not attr.has_value(objs, cobjs):
                #attr.set_value(objs, cobjs, dict())
            #print attr.obj.name, objs
            cobjs = attr.value(objs, cobjs)
        last_attr = self.lookup_chain[-1]
        last_attr.set_value(objs, cobjs, value)

class Attribute(Value):

    def __init__(self, obj, call_chain=None):
        self.obj = obj
        self.call_chain = call_chain
        self.__type = None                          ## TODO TYPES

    def writable(self):
        return self.call_chain is None and self.obj.writable()

    def value(self, gobjs, cobjs):
        obj = self.obj.value(cobjs)
        if self.call_chain is not None:
            for params in self.call_chain.value(gobjs):
                assert hasattr(obj, '__call__')
                obj = obj.__call__(*params)
        return obj

    def set_value(self, gobjs, cobjs, value):
        if self.call_chain is not None:
            raise Unwritable, 'Can not write to a function call'
        self.obj.set_value(cobjs, value)
        
class FCall(Value):

    def __init__(self, parameters):
        self.parameters = parameters
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        return [param.value(objs) for param in self.parameters]

class CallChain(Value):

    def __init__(self, calls):
        self.calls = calls
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        return [call.value(objs) for call in self.calls]

class Object(Value):

    def __init__(self, name):
        self.name = name
        self.__type = None                          ## TODO TYPES

    def writable(self): return True

    def value(self, objs):
        if self.name not in objs:
            raise UnboundValueError
        return objs[self.name]

    def set_value(self, objs, value):
        if self.name in objs:
            raise BoundValueError
        objs[self.name] = value

class SymbolObject(Value):

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        if (self.name, self.id) not in objs:
            raise UnboundValueError
        return objs[(self.name, self.id)]
