#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from symbols import NonTerminal
from action import Action
from condition import Condition

class Rule(object):

    def __init__(self, name, pattern, action, condition):
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
        #print [object.__repr__(x[0]()) if not hasattr(x[0], 'name') else x[0].name for x in self.pattern]
        return (
            '<Rule "%s -> %s"%s%s%s>'
        ) % (
          self.name,
          ' '.join(sym.name if hasattr(sym, 'name') else sym for sym, cnt in self.pattern),
          ' with action' if self.action is not None else '',
          ' and' if self.action is not None and self.condition is not None else '',
          ' with condition' if self.condition is not None else ''
        )
