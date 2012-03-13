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

    def __eq__(self, o):
        if not isinstance(o, AttrChain): return False
        return all(
          a == b
          for a,b in zip(self.lookup_chain, o.lookup_chain)
        )

    def replace(self, from_sym, to_sym):
        return AttrChain([
            attr.replace(from_sym, to_sym) for attr in self.lookup_chain
        ])

    def allows(self, type):
        last_attr = self.lookup_chain[-1]
        return last_attr.allows(type)

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

    def __eq__(self, o):
        if not isinstance(o, Attribute): return False
        return self.obj == o.obj and self.call_chain == o.call_chain

    def writable(self, type):
        return self.call_chain is None and self.obj.writable(type)

    def replace(self, from_sym, to_sym):
        return Attribute(
          self.obj.replace(from_sym, to_sym),
          self.call_chain.replace(from_sym, to_sym)
            if self.call_chain is not None
              else self.call_chain
        )

    def allows(self, type):
        assert self.call_chain is None
        return self.obj.allows(type)

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
        raise Exception, 'Not allowing FCalls at the moment'
        ## Reasons, a lot of stuff is not implemented
        ## right now I assume the object is "writable if it is not a instance
        ## of the base class.
        self.parameters = parameters
        self.__type = None                          ## TODO TYPES

    def __eq__(self, o):
        raise Exception, NotImplemented

    def replace(self, from_sym, to_sym):
        raise Exception, NotImplemented

    def value(self, objs):
        return [param.value(objs) for param in self.parameters]

class CallChain(Value):

    def __init__(self, calls):
        raise Exception, 'Not allowing call chains at the moment'
        ## Reasons, a lot of stuff is not implemented
        ## right now I assume the object is "writable if it is not a instance
        ## of the base class.
        self.calls = calls
        self.__type = None                          ## TODO TYPES

    def __eq__(self, o):
        raise Exception, NotImplemented

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

    def __eq__(self, o):
        if not isinstance(o, Object): return False
        return self.name == o.name

    def allows(self, type):
        return True

    def replace(self, from_sym, to_sym):
        return self

    def type(self, objs):
        if self.name not in objs:
            return UnknownType
        obj = objs[self.name]
        return Type(obj)

    def value(self, objs):
        if self.name not in objs:
            raise UnboundValueError
        return objs[self.name]

    def set_value(self, objs, value):
        if self.name in objs:
            raise BoundValueError
        objs[self.name] = value

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

    def __eq__(self, o):
        #print 'SymbolObject.__eq__', self, o
        #print self.name, o.name, self.id, o.id, self.symtype, o.symtype
        #print self.name == o.name and self.id == o.id and self.symtype == o.symtype
        if not isinstance(o, SymbolObject): return False
        return (
          self.name == o.name and self.id == o.id and self.symtype == o.symtype
        )

    def replace(self, from_sym, to_sym):
        if self.name == from_sym[0] and self.id == self.id:
            return SymbolObject(self.symtype, *to_sym)
        return self

    def allows(self, type):
        return not issubclass(type, NoneType)

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
