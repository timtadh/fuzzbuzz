#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attr_types import String, Namespace
from value import Value, WritableValue

class Terminal(WritableValue):

    stringifiers = None

    def __init__(self, objs, name):
        assert self.stringifiers is not None
        self.name = name
        super(Terminal, self).__init__(objs, String, None)

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

    def __init__(self, name):
        self.rules = list()
        self.name = name
        super(NonTerminal, Namespace, dict())

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
