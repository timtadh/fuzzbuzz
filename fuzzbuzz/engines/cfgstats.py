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
        stack.append((start, None, 0))
        
        while stack:
            nonterm, rule, j = stack.pop()
            #print "POP: "
            #print nonterm
            #print "\n"
            if rule is None: #otherwise we are continuing from where we left off
                assert j is 0
                rule = choice(nonterm.rules)
            #print "CHOSE: "
            #print rule
            #print "\n"
            
            print "rule pattern:\n"
            print rule.pattern
            print "\n"
            print "listed...: \n"
            print list(enumerate(rule.pattern))
            print "\n"
        
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    #fuzz(sym)
                    #print "NONTERMINAL: "
                    #print sym
                    #print "\n"
                    stack.append((nonterm, rule, i+1))
                    stack.append((sym, None, 0))
                    break
                if sym.__class__ is Terminal:
                    #print "TERMINAL: "
                    #print sym
                    #print "\n"
                    output.append(rlexer[sym.name]())
        
    fuzz(grammar.start)
    return output
