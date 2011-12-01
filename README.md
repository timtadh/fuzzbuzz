FuzzBuzz
========

By Tim Henderson (tim.tadh@gmail.com)

What?
-----

An `attribute grammar` fuzzer. It generates new tests cases from an s-attributed
grammar. 

Attribute Grammars
------------------

A context sensitive version of the context free grammar. They were invented by
Don Knuth in 1968 to enable exact specification of the semantics of
programming langauges. The semantics are difficult to specify with syntax alone
even when using a Type 1 or Type 0 grammar in the Chompsky heirarchy. Diffcult
in the sense the descriptions are long, formal, uninformatative and tedious to
specify. Attribute grammars solve this by adding actions and conditions to each
production.

### A simple example. (Use before declaration)

This grammar only parses examples which declare names before they use names. 

    Stmts -> Stmts(2) Stmt
             Action:
                if Stmt.decl is not None:
                    Stmts.names = Stmts(2).names | { stmt.decl }
                else:
                    Stmts.names = Stmts(2).names
             with Condition:
                (Stmt.uses is not None && Stmt.uses in Stmts(2).names) ||
                (Stmt.decl is not None && Stmt.decl not in Stmts(2).names)
           | Stmt
             Action:
                if Stmt.Decl is not None:
                    Stmts.names = { stmt.decl }
                else:
                    Stsms.names = {}
             with Condition:
                Stmt.uses is None
  

    Stmt -> VAR NAME EQUAL NUMBER
            Action:
                Stmt.decl = NAME.value
                Stmt.uses = None
          | PRINT NAME
            Action:
                Stmt.decl = None
                Stmt.uses = NAME.value

    VAR = "var", PRINT = "print", EQUAL = "=", NAME = "[A-Za-z][A-Za-z0-9_]*",
    NUMBER = "[0-9]+"
