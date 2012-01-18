#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Terminal(object):

    stringifiers = None

    def __new__(cls, *args, **kwargs):
        def create():
            self = super(Terminal, cls).__new__(cls)
            self.__init__(*args, **kwargs)
            return self
        return create

    def __init__(self, name):
        assert self.stringifiers is not None
        self.name = name
        self.__value = None

    @property
    def value(self):
        if self.__value is None:
            raise RuntimeError, (
              'Tried to deref the value of a Terminal which does not yet know'
              '  its value.'
            )
        return self.__value

    def mkvalue(self):
        if self.__value is not None:
            raise RuntimeError, (
              'Tried to make a new value for a terminal, %s, who already has '
              'one.'
            ) % (self.name)
        # defers to user supplied function for each terminal type.
        self.__value = self.stringifiers[self.name]()
        return self.__value

    def setvalue(self, value):
        if self.__value is not None:
            raise RuntimeError, (
              'Tried to set a value for a terminal who already has one.'
            )

    def __repr__(self): return str(self)
    def __str__(self): return '<Term %s>' % self.name

class NonTerminal(object):

    def __init__(self, name):
        self.rules = list()
        self.name = name

    def addrule(self, rule):
        self.rules.append(rule)

    def __repr__(self): return str(self)
    def __str__(self):
        return (
          '<NonTerm' + ' ' + self.rules[0].name + ' -> ' +
          ' | '.join(
            ' '.join(sym.name for sym, cnt in rule.pattern)
            for rule in self.rules
          ) + '>'
        )
