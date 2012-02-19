#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from symbols import NonTerminal
from action import Action
from condition import Condition

class Rule(object):
    '''Represents a grammar rule.'''

    def __init__(self, name, pattern, action, condition):
        '''Constructs a new rule.
        @param name (string) : the name of the rule
        @param pattern (list) : a list of (string, int) pares reprenting the
                                grammar pattern. ex.
                                  A -> B c A d
                                  [('B', 1), ('c', 1), ('A', 2), ('d', 1)]
        @param action (action.Action) : an action or (None)
        @param condition (condition.Condition) : a condition or (None)
        '''
        self.name = name
        self.pattern = pattern
        self.action = action
        self.condition = condition

    def mknamespace(self, objs):
        objs = {(self.name, 1) : objs}
        for sym, cnt in self.pattern:
            if isinstance(sym, NonTerminal):
                objs.update({(sym.name, cnt):  dict()})
        return objs

    def __repr__(self): return str(self)
    def __str__(self):
        return (
            '<Rule "%s -> %s"%s%s%s>'
        ) % (
          self.name,
          ' '.join(sym.name if hasattr(sym, 'name') else sym for sym, cnt in self.pattern),
          ' with action' if self.action is not None else '',
          ' and' if self.action is not None and self.condition is not None else '',
          ' with condition' if self.condition is not None else ''
        )
