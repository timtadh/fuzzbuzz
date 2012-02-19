#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

import subprocess, functools
from random import seed, choice, randint, random

from fuzzbuzz.frontend import parser
from fuzzbuzz.models.symbols import Terminal, NonTerminal
from fuzzbuzz.models.attribute import SymbolObject
from fuzzbuzz.models.condition import TrueConstraint

def init():
    seed()

def fuzz(grammar):
    init()
    out = list()

    def filter(objs, rules, constraint):
        #print objs
        for rule in rules:
            #print rule.action.unconstrained
            #print constraint
            if rule.action is None:
                yield rule
            elif rule.action.unconstrained(constraint, rule.mknamespace(objs)):
                yield rule

    def choose(nonterm, objs, constraint):
        rules = list(filter(objs, nonterm.rules, constraint))
        #print 'allowed rules for', nonterm.name, rules
        rule = choice(rules)
        #print 'chose', rule
        cobjs = rule.mknamespace(objs)
        return rule, cobjs

    def display(d, i=0):
        print
        for key, value in d.iteritems():
            print ' '*(i+1), key,
            if isinstance(value, dict):
                display(value, i+3)
            else:
                print value
        return ''
  
    def fuzz(start):
        stack = list()
        trule, tobjs = choose(start, dict(), TrueConstraint())
        #print cobjs, id(cobjs)
        stack.append((tobjs, trule, 0, list(), TrueConstraint()))
        while stack:
            objs, rule, j, sobjs, constraint = stack.pop()
            #print rule, id(objs), rule.condition, display(objs)
            if rule.condition is not None:
                ## TODO: Condtion flows return several canidate object sets
                ##       based on the Any operator. This needs to be integrated
                ##       into this engine. Right now it works because the All
                ##       operator mutates the given object space. Mutation
                ##       should be considered to deprecated behavior.
                #print '->', rule.condition.flow(objs) ## Needs to be reflowed to update
                                          ## conditions which rely on earlier Nonterminals
                constraint = rule.condition.generate_constraint(objs)
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    crule, cobjs = choose(sym, objs[(sym.name, cnt)], constraint)
                    stack.append((objs, rule, i+1, sobjs, constraint))
                    stack.append((cobjs, crule, 0, list(), TrueConstraint()))
                    break
                else:
                    so = SymbolObject('Terminal', sym.name, cnt)
                    sobjs.append(so)
                    out.append(functools.partial(so.value, objs))
            else:
                if rule.action is not None:
                    rule.action.fillvalues(objs)
                for so in sobjs:
                    if not so.has_value(objs): so.make_value(objs)
                #display(objs)
                #print objs
                if rule.action is not None:
                    rule.action.execute(objs)
                #print [sym() for sym in out]
        #print trule.name, display(tobjs)
    fuzz(grammar.start)
    return list(sym() for sym in out)

def main():
    
    tree, grammar = parser.parse()
    strings = fuzz(grammar)
    string = ' '.join(strings)
    for line in string.split('\n'):
        print line.strip()

if __name__ =='__main__':
    main()

