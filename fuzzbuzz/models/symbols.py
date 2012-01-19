#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attr_types import String, Namespace
from value import Value, WritableValue

def make_accessable(name, pos):
    def dec(cls):
        def maker(clazz, *args, **kwargs):
            print clazz, args
            defer = cls.__new__(clazz, *args, **kwargs)
            setattr(defer, name, args[pos])
            return defer
        return maker
    return dec

class Terminal(WritableValue):

    stringifiers = None

    def __init__(self, name):
        assert self.stringifiers is not None
        self.name = name
        super(Terminal, self).__init__(None, String, None)

    def __writehook__(self, value):
        pass
    
    def mkvalue(self):
        if self.value is not None:
            raise RuntimeError, (
              'Tried to make a new value for a terminal, %s, who already has '
              'one.'
            ) % (self.name)
        # defers to user supplied function for each terminal type.
        self.value = self.stringifiers[self.name]()
        return self.value

    def __repr__(self): return str(self)
    def __str__(self): return '<Term %s>' % self.name



class NonTerminal(Value):


    #def __new__(cls, *args, **kwargs):
        #rules = list()
        #def addrule(rule):
            #rules.append(rule)
        #args = list(args) + [rules]
        #defer = super(NonTerminal, cls).__new__(cls, *args, **kwargs)
        #setattr(defer, 'addrule', addrule)
        #return defer
        
    
    def __init__(self, name, rules):
        #print 'Called Nonterminal init', self.__class__.__name__
        self.name = name
        self.rules = rules
        super(NonTerminal, self).__init__(None, Namespace, dict())

    #def addrule(self, rule):
        #self.rules.append(rule)

    def __repr__(self): return str(self)
    def __str__(self):
        return (
          '<NonTerm' + ' ' + self.rules[0].name + ' -> ' +
          ' | '.join(
            ' '.join(sym.name for sym, cnt in rule.pattern)
            for rule in self.rules
          ) + '>'
        )
