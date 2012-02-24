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
    def fuzz(start):
        stack = list()
        stack.append(start)
        
        while stack:
            nonterm = stack.pop()
            #print "POP: "
            #print nonterm
            #print "\n"
            rule = choice(nonterm.rules)
            #print "CHOSE: "
            #print rule
            #print "\n"
        
            for sym, cnt in rule.pattern:
                if sym.__class__ is NonTerminal:
                    #fuzz(sym)
                    #print "NONTERMINAL: "
                    #print sym
                    #print "\n"
                    stack.append(sym)
                if sym.__class__ is Terminal:
                    #print "TERMINAL: "
                    #print sym
                    #print "\n"
                    output.append(rlexer[sym.name]())
        
    fuzz(grammar.start)
    return output
