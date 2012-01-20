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

    #def fuzz(start):
    out = list()
    def fuzzR(nonterm):
        rule = choice(nonterm.rules)
        nextfuzz = list()
        for sym, cnt in rule.pattern:
            if sym.clazz is NonTerminal:
                fuzzR(sym())
            else:
                terminal = sym()
                terminal.mkvalue()
                out.append(terminal)
        
    
    out = list()
    def fuzz(start):
        stack = list()
        no_continue = (lambda:None)
        def make_continue(rule, i, next_continue):
            def continuef():
                stack.append((rule, i, next_continue))
            return continuef

        stack.append((choice(start.rules), 0, no_continue))
        while stack:
            rule, j, continuef = stack.pop()
            nextfuzz = list()
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.clazz is NonTerminal:
                    stack.append((choice(sym().rules),0,make_continue(rule,i+1,continuef)))
                    break
                else:
                    terminal = sym()
                    terminal.mkvalue()
                    out.append(terminal)
            else:
                continuef()
            #if i+1 == len(rule.pattern):
                #print rule, out
        ##stack = list()
        ##stack.append(start)
        #while stack:
            #nonterm = stack.pop()
            #rule = choice(nonterm.rules)
            #for sym, cnt in rule.pattern:
                #if sym.clazz is NonTerminal:
                    #stack.append(sym())
                #else:
                    #terminal = sym()
                    #terminal.mkvalue()
                    #yield terminal
    fuzz(grammar.start())
    return list(sym.value for sym in out)

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
    As -> As NEWLINE A
        | A
        ;
    A -> VAR B NUMBER  ;
    B -> EQUAL ;
    /*Stmts -> Stmts NEWLINE Stmt
                with Action {
                  if (Stmt.decl is not None) {
                    Stmts{1}.names = Stmts{2}.names | { stmt.decl }
                  }
                  else {
                    Stmts{1}.names = Stmts{2}.names
                  }
                }
                with Condition {
                  (Stmt.uses is not None && Stmt.uses in Stmts{2}.names) ||
                  (Stmt.decl is not None && Stmt.decl not in Stmts{2}.names)
                }
             | Stmt
                with Action {
                  Stmts{1}.names.games.thames.james = { stmt.decl }
                }
                with Condition {
                  Stmt.uses is None
                }
              ;

    Stmt -> VAR NAME EQUAL NUMBER
            with Action {
              Stmt.decl = NAME.value
              Stmt.uses = None
            }
          | PRINT NAME
            with Action {
              Stmt.decl = None
              Stmt.uses = NAME.value
            }
          ; */
    ''')
    dot('test', tree.dotty())
    #print tree.dotty()
    #print repr(tree)
    #print grammar
    print ' '.join(fuzz(grammar))

if __name__ =='__main__':
    main()
