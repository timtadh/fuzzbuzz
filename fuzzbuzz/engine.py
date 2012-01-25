#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

import subprocess, functools
from random import seed, choice, randint, random

from frontend import parser
from models.symbols import Terminal, NonTerminal
from models.attribute import SymbolObject

def dot(name, dotty):
    dot = name + '.dot'
    png = name + '.png'

    f = open(dot, 'w')
    f.write(dotty)
    f.close()

    p = subprocess.Popen(['dot', '-Tpng', '-o', png], stdin=subprocess.PIPE)
    p.stdin.write(dotty + '\0')
    p.stdin.close()
    p.wait()

def init():
    seed()

def fuzz(grammar):
    out = list()

    def filter(objs, rules):
        for rule in rules:
            #print rule.action.unconstrained
            if rule.action is None:
                yield rule
            elif rule.action.unconstrained(rule.mknamespace(objs)):
                yield rule

    def choose(nonterm, objs):
        rules = list(filter(objs, nonterm.rules))
        print 'allowed rules for', nonterm.name, rules
        rule = choice(rules)
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
        trule, tobjs = choose(start, dict())
        #print cobjs, id(cobjs)
        stack.append((tobjs, trule, 0, list()))
        while stack:
            objs, rule, j, sobs = stack.pop()
            if rule.condition is not None:
                #print nonterm.value
                rule.condition.flow(objs)
            nextfuzz = list()
            #print rule.name, j, objs
            print rule, id(objs), display(objs)
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    #objs[(sym.name, cnt)] = objs.get[(sym.name, cnt)]
                    crule, cobjs = choose(sym, objs[(sym.name, cnt)])
                    #print rule.name, cobjs, id(cobjs)
                    #new_objs[(rule.name, 1)] = objs
                    stack.append((objs, rule, i+1, sobs))
                    stack.append((cobjs, crule, 0, list()))
                    break
                else:
                    #if (sym.name, cnt) not in objs:
                        #objs[(sym.name, cnt)] = sym.mkvalue()
                    so = SymbolObject('Terminal', sym.name, cnt)
                    sobs.append((so, sym.mkvalue))
                    #yield objs[(sym.name, cnt)]
                    out.append(functools.partial(so.value, objs))
                    #terminal = sym.mkvalue()
                    #yield terminal
                    #objs[] = terminal
            else:
                if rule.action is not None:
                    rule.action.fillvalues(objs)
                for so, mkval in sobs:
                    if not so.has_value(objs): so.set_value(objs, mkval())
                display(objs)
                print objs
                if rule.action is not None:
                    rule.action.execute(objs)
        print trule.name, display(tobjs)
    fuzz(grammar.start)
    return list(sym() for sym in out)

def main():
    init()
    Terminal.stringifiers = {
        'VAR' : (lambda: 'var'),
        'NAME' : (lambda: ''.join(chr(randint(97, 122)) for x in xrange(1, randint(2,10)))),
        'EQUAL' : (lambda: '='),
        'NUMBER' : (lambda: str(randint(1, 1000))),
        'PRINT' : (lambda: 'print'),
        'NEWLINE' : (lambda: '\n'),
    }
    tree, grammar = parser.parse('''
    /*
    As -> As NEWLINE A
        | A
        ;
    A -> VAR B NUMBER  ;
    B -> EQUAL ;
    */
    Stmts ->  Stmts NEWLINE Stmt
                with Action {
                  if (Stmt.decl is None) {
                    Stmts{1}.names = Stmts{2}.names
                  }
                  else {
                    Stmts{1}.names = Stmts{2}.names | { Stmt.decl }
                  }
                }
                with Condition {
                  // Stmt.decl is None &&
                  Stmt.uses in Stmts{2}.names
                }
             | Stmt
                with Action {
                  Stmts{1}.names = { Stmt.decl }
                }
                with Condition {
                  Stmt.uses is None
                }
              ;

    Stmt -> VAR NAME EQUAL NUMBER
            with Action {
              Stmt.decl = NAME
              Stmt.uses = None
            }
          | PRINT NAME
            with Action {
              Stmt.decl = None
              Stmt.uses = NAME
            }
          ;
    ''')
    strings = fuzz(grammar)
    print strings
    print ' '.join(strings)
    dot('test', tree.dotty())
    #print tree.dotty()
    #print repr(tree)
    #print grammar

if __name__ =='__main__':
    main()
