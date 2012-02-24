#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attr_types import *
from constraints import *
from value import Value, UnboundValueError, BoundValueError, Unwritable

class AttrChain(Value):

    def __init__(self, lookup_chain):
        self.lookup_chain = lookup_chain

    def __repr__(self): return str(self)

    def __str__(self):
        return "<AttrChain %s>" % str(self.lookup_chain)

    def writable(self, type):
        return all(x.writable(type) for x in self.lookup_chain)

    def replace(self, from_sym, to_sym):
        return AttrChain([
            attr.replace(from_sym, to_sym) for attr in self.lookup_chain
        ])

    def type(self, objs):
        cobjs = objs
        for attr in self.lookup_chain[:-1]:
            cobjs = attr.value(objs, cobjs)
        last_attr = self.lookup_chain[-1]
        return last_attr.type(objs, cobjs)

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
            if not attr.has_value(objs, cobjs):
                attr.set_value(objs, cobjs, dict())
            cobjs = attr.value(objs, cobjs)
        last_attr = self.lookup_chain[-1]
        last_attr.set_value(objs, cobjs, value)

    def make_constraint(self, objs, value, type):
        if type == Set:
            #print 'making a multi value constraint', self.type(objs)
            return OrConstraint([
              MultiValueConstraint(self, tuple(value)),
              SubsetConstraint(self, tuple(value)),
            ])
        else:
            return SingleValueConstraint(self, value)

class Attribute(Value):

    def __init__(self, obj, call_chain=None):
        self.obj = obj
        self.call_chain = call_chain

    def __repr__(self): return str(self)

    def __str__(self):
        return "<Attribute %s>" % str(self.obj)

    def writable(self, type):
        return self.call_chain is None and self.obj.writable(type)

    def replace(self, from_sym, to_sym):
        return Attribute(
          self.obj.replace(from_sym, to_sym),
          self.call_chain.replace(from_sym, to_sym)
            if self.call_chain is not None
              else self.call_chain
        )

    def type(self, gobjs, cobjs):
        #obj = self.obj.value(cobjs)
        otype = self.obj.type(cobjs)
        if self.call_chain is not None:
            raise Exception, NotImplemented
            #for params in self.call_chain.value(gobjs):
                #assert hasattr(obj, '__call__')
                #obj = obj.__call__(*params)
        return otype

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

    def replace(self, from_sym, to_sym):
        raise Exception, NotImplemented

    def value(self, objs):
        return [param.value(objs) for param in self.parameters]

class CallChain(Value):

    def __init__(self, calls):
        self.calls = calls
        self.__type = None                          ## TODO TYPES

    def replace(self, from_sym, to_sym):
        raise Exception, NotImplemented

    def value(self, objs):
        return [call.value(objs) for call in self.calls]

class Object(Value):

    def __init__(self, name):
        self.name = name
        #self.__type = None                          ## TODO TYPES

    def __repr__(self): return str(self)

    def __str__(self):
        return "<Object %s>" % str(self.name)

    def writable(self, type):
        return True

    def replace(self, from_sym, to_sym):
        return self

    def type(self, objs):
        if self.name not in objs:
            raise UnboundValueError
        obj = objs[self.name]
        if isinstance(obj, NoneType): return NoneType
        elif isinstance(obj, set): return Set
        elif isinstance(obj, int): return Number
        elif isinstance(obj, str): return String
        elif isinstance(obj, dict): return Namespace
        else: raise RuntimeError

    def value(self, objs):
        if self.name not in objs:
            raise UnboundValueError
        return objs[self.name]

    def set_value(self, objs, value):
        if self.name in objs:
            raise BoundValueError
        objs[self.name] = value

    def make_constraint(self, value):
        raise Exception, NotImplemented
        pass

class SymbolObject(Value):

    def __init__(self, symtype, name, id):
        self.name = name
        self.id = id
        self.symtype = symtype
        if symtype == 'Terminal':
            self.__type = String
        else:
            self.__type = Namespace

    def __repr__(self): return str(self)

    def __str__(self):
        return "<SymbolObject (%s, %s)>" % (str(self.name), str(self.id))

    def writable(self, type):
        return issubclass(type, self.type(None))

    def replace(self, from_sym, to_sym):
        if self.name == from_sym[0] and self.id == self.id:
            return SymbolObject(self.symtype, *to_sym)
        return self

    def make_value(self, objs, rlexer):
        assert self.__type == String
        assert self.name in rlexer
        value = rlexer[self.name]()
        self.set_value(objs, value)
        return value

    def value(self, objs):
        key = (self.name, self.id)
        if key not in objs:
            raise UnboundValueError
        return objs[key]

    def set_value(self, objs, value):
        key = (self.name, self.id)
        if key in objs:
            raise BoundValueError
        objs[key] = value
