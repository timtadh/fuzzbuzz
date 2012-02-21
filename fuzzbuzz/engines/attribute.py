#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

import subprocess, functools
from random import seed, choice, randint, random

from reg import registration
from fuzzbuzz.frontend import parser
from fuzzbuzz.models.symbols import Terminal, NonTerminal
from fuzzbuzz.models.attribute import SymbolObject
from fuzzbuzz.models.constraints import TrueConstraint, SubsetConstraint

def init():
    seed()

@registration.register(
  dict(),
  'Generates strings from an attribute grammar st. conditions hold')
def attribute_fuzzer(rlexer, grammar):
    init()
    out = list()

    def filter(objs, rules, constraint):
        #print objs
        print 'filtering', rules
        for rule in rules:
            #print rule.action.unconstrained
            #print constraint
            print rule.action
            if rule.action is None:
                yield rule
            elif rule.action.unconstrained(rule.mknamespace(objs), constraint):
                yield rule

    def choose(nonterm, objs, constraint):
        #print 'choosing ->', nonterm, constraint, objs
        #print constraint.values if isinstance(constraint, SubsetConstraint) else constraint
        rules = list(filter(objs, nonterm.rules, constraint))
        print 'allowed rules for', nonterm.name, rules
        rule = choice(rules)
        #print 'chose', rule, objs
        cobjs = rule.mknamespace(objs)
        print 'chose', rule, cobjs
        if rule.action:
            new_constraint = rule.action.flow_constraints(cobjs, constraint)
            print 'xxx', 'new constraint', new_constraint
        else:
            new_constraint = TrueConstraint()
        return rule, cobjs, new_constraint

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
        trule, tobjs, first_constraint = choose(start, dict(), TrueConstraint())
        #print cobjs, id(cobjs)
        stack.append((tobjs, trule, 0, list(), first_constraint))
        while stack:
            objs, rule, j, sobjs, constraint = stack.pop()
            print rule, id(objs), rule.condition, display(objs)
            if rule.condition is not None:
                constraint = rule.condition.generate_constraint(objs)
                #print 'xx', 'new constraint', constraint
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    print 'about to find rule for', rule, display(objs)
                    crule, cobjs, new_constraint = \
                                  choose(sym, objs[(sym.name, cnt)], constraint)
                    #print cobjs, constraint
                    print 'found rule for', rule, display(objs)
                    stack.append((objs, rule, i+1, sobjs, constraint))
                    stack.append((cobjs, crule, 0, list(), new_constraint))
                    break
                else:
                    so = SymbolObject('Terminal', sym.name, cnt)
                    sobjs.append(so)
                    out.append(functools.partial(so.value, objs))
            else:
                if rule.action is not None:
                    rule.action.fillvalues(objs, constraint)
                for so in sobjs:
                    if not so.has_value(objs): so.make_value(objs, rlexer)
                #display(objs)
                #print objs
                if rule.action is not None:
                    rule.action.execute(objs)
                #print [sym() for sym in out]
        #print trule.name, display(tobjs)
    fuzz(grammar.start)
    output = list(sym() for sym in out)
    return output
