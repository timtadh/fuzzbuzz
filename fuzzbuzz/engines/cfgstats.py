#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Rafael Lopez
#Email: rafael.lopez.u@gmail.com
#For licensing see the LICENSE file in the top level directory.

from random import seed, choice, randint, random

from reg import registration
from fuzzbuzz.models.symbols import Terminal, NonTerminal

@registration.register(
  {'stat_tables':'tables'},
  'A fuzzer to produce output based on statistics provided at input')
def cfgstats(rlexer, grammar, stat_tables=None):
    # grammar.start --> start symbol it is a fuzzbuzz.models.symbols.NonTerminal
    # nonterm.rules --> a list of the possible choices.
    # rule -> list of Terminal and NonTerminal symbols
    # getnextrule(nonterm): random.choice(nonterm.rules)
    
    output = list()
    def fuzz(nonterm):
        rule = choice(nonterm.rules)
      
        for sym, cnt in rule.pattern:
            if sym.__class__ is NonTerminal:
                fuzz(sym)
            if sym.__class__ is Terminal:
                output.append(rlexer[sym.name]())
    
    fuzz(grammar.start)
    return output
