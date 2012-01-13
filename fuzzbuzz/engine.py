#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

from frontend import parser

def main():
    tree, grammar = parser.parse('''
    Stmts -> Stmts Stmt
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
                  Stmts{1}.names = { stmt.decl }
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
          ;
    ''')
    print repr(tree)
    print grammar

if __name__ =='__main__':
    main()
