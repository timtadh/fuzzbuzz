#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

import argparse
import subprocess, functools
from random import seed, choice, randint, random

from frontend import parser
from models.symbols import Terminal, NonTerminal
from models.attribute import SymbolObject
from models.condition import TrueConstraint

def init():
    seed()

def fuzz(grammar):
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


def read_input_grammar():
    """Read in the input grammar from a file.
    If the contents exist, return them as a string.

    TODO: let the user specify what file to load.
    """
    contents = open("../example_grammar").read()
    return contents


def parse_arguments():
    parser = argparse.ArgumentParser(description='FuzzBuzz: An attribute grammar fuzzer (Read the README)')
    parser.add_argument('string', metavar='grammar_input_file', type=str,
                        help='The grammar for which we will fuzz')

    args = parser.parse_args()
    return args


def main():
    init()
    args = parse_arguments()
    input_grammar = read_input_grammar()
    SymbolObject.stringifiers = {
        'VAR' : (lambda: 'var'),
        'NAME' : (lambda: ''.join(chr(randint(97, 122)) for x in xrange(1, randint(2,10)))),
        'EQUAL' : (lambda: '='),
        'NUMBER' : (lambda: str(randint(1, 1000))),
        'PRINT' : (lambda: 'print'),
        'NEWLINE' : (lambda: '\n'),
    }
    tree, grammar = parser.parse(input_grammar)
    strings = fuzz(grammar)
    string = ' '.join(strings)
    for line in string.split('\n'):
        print line.strip()

if __name__ =='__main__':
    main()

