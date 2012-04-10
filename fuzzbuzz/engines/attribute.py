#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

import sys, random
import subprocess, functools

from reg import registration
from fuzzbuzz.frontend import parser
from fuzzbuzz.models.symbols import Terminal, NonTerminal
from fuzzbuzz.models.attribute import SymbolObject
from fuzzbuzz.models.constraints import TrueConstraint, SubsetConstraint

def init():
    random.seed()

@registration.register(
  dict(),
  'Generates strings from an attribute grammar st. conditions hold')
def attribute_fuzzer(rlexer, grammar, choice=None):
    if choice is None: choice = random.choice
    init()
    out = list()

    def filter(objs, rules, constraint):
        #print 'filtering', rules
        for rule in rules:
            #print 'is rule unconstrainted?', rule
            if rule.action is None:
                yield rule
            elif rule.action.unconstrained(constraint):
                yield rule

    def choose(nonterm, objs, constraint):
        #print 'choosing ->', nonterm, constraint, objs
        rules = list(filter(objs, nonterm.rules, constraint))
        #print 'allowed rules for', nonterm.name, rules
        rule = choice(rules)
        #print 'chose', rule
        cobjs = rule.mknamespace(objs)
        if rule.action:
            #print 'about to flow constraints'
            new_constraint = rule.action.flow_constraints(cobjs, constraint)
            #print 'xxx', 'new constraint', new_constraint
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
            #print rule, id(objs), rule.condition, display(objs)
            if rule.condition is not None:
                constraint = rule.condition.generate_constraint(objs)
                #print 'xx', 'new constraint', constraint
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    #print 'about to find rule for', rule, sym.name, display(objs)
                    #print '--->', constraint
                    constraint = constraint.replace(
                      (sym.name, cnt),
                      (sym.name, 1)
                    )
                    #print '--->', constraint
                    crule, cobjs, new_constraint = \
                                  choose(sym, objs[(sym.name, cnt)], constraint)
                    #print cobjs, constraint
                    #print 'found rule for', rule, display(objs)
                    stack.append((objs, rule, i+1, sobjs, constraint))
                    stack.append((cobjs, crule, 0, list(), new_constraint))
                    break
                else:
                    so = SymbolObject('Terminal', sym.name, cnt)
                    sobjs.append(so)
                    out.append(functools.partial(so.value, objs))
            else:
                if rule.action is not None:
                    #print 'filling ', rule
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
    #print output
    return output, None

class guided_choice(object):

    def __init__(self, choices):
        self.choices = choices
        self.i = 0

    def __call__(self, rules):
        if self.i >= len(self.choices):
            raise Exception, "Too many rules expanded."
        cur = self.choices[self.i]
        for rule in rules:
            sig = tuple(s.name for s, n in rule.pattern)
            if sig == cur: break
        else:
            raise Exception, "Expected choice not found."
        print rule
        self.i += 1
        return rule

if __name__ == '__main__':
    import os
    import testdata.simple
    from testdata.simple.lexer import rlexer
    with open(
      os.path.join(
        os.path.dirname(testdata.simple.__file__),
        'simple_3.grammar'
      ), 'r') as f:
        s = f.read()
    grammar = parser.parse(s)
    strings, err = attribute_fuzzer(
        rlexer, grammar,
        guided_choice([
          ('Stmts', 'Use'),
          ('Decl',),
          ('VAR', 'NAME', 'EQUAL', 'NUMBER', 'NEWLINE'),
          ('PRINT', 'NAME', 'NEWLINE'),
        ])
    )
    string = ' '.join(strings)
    for line in string.split('\n'):
        print line.strip()