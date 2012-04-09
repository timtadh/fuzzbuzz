FuzzBuzz
========

By Tim Henderson (tim.tadh@gmail.com)

What?
-----

An `attribute grammar` fuzzer. It generates new tests cases from an s-attributed
grammar.

### Is it good?

I think you are asking the wrong questions.

### How do I use it?

I will get back to you when there is something to use?

Attribute Grammars
------------------

A context sensitive version of the context free grammar. They were invented by
Don Knuth in 1968 to enable exact specification of the semantics of
programming langauges. The semantics are difficult to specify with syntax alone
even when using a Type 1 or Type 0 grammar in the Chompsky heirarchy. Diffcult
in the sense the descriptions are long, formal, uninformatative and tedious to
specify. Attribute grammars solve this by adding actions and conditions to each
production.

#### A simple example. (Use before declaration)

Consider the following grammar:

    Stmts -> Stmts Stmt
          | Stmt

    Stmt -> VAR NAME EQUAL NUMBER
          | PRINT NAME


    VAR = "var", PRINT = "print", EQUAL = "=", NAME = "[A-Za-z][A-Za-z0-9_]*",
    NUMBER = "[0-9]+"

This grammar defines a language which looks something like this:

    var foo = 12
    print foo

According to the syntax defined in the above CFG the following string is in the
language:

    print baz
    var baz = 12

However, this string violates the semantics of this simple language -- variables
must be declared before they can be used. To restrict the strings allowed in the
language to those in which variables are declared and not used we use the
following attributed grammar. An attribute grammar expands context free grammars
to include attributes, actions and conditions. Attributes, variables attached to
grammar symbols hold values assigned by actions. Conditions only allow a grammar
rule to apply if the condition evaluates to true. Conditions generally make use
of the values of attributes which were assigned by previous actions.


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

### Learning More

There is an excellent free book available called [Syntax and Semantics of
Programming Languages](http://www.divms.uiowa.edu/~slonnegr/plf/Book/).
Chapter 3
[Attribute Grammars](http://www.divms.uiowa.edu/~slonnegr/plf/Book/Chapter3.pdf)
is a great introduction to the subject. Ullman et. all (in the illustrious
"Dragon Book") provide an overview of the practical use of attribute grammars in
 syntax directed translation. While a good background, does not provide as much
insight as *Syntax and Semantics* does.

Fuzzing with Attributes
-----------------------

### Why Fuzz With Attribute Grammars

Why use attribute grammars to specify the grammar? Aren't context free grammars
or "block structured" grammars sufficient? For simple languages, a context free
grammar may be suffiecient however many languages have context sensitive
elements. Consider the language defined in the "Attribute Grammars" section, it
demonstrates the "Declare Before Use" constraint on variable names. These
constraints are semantic in nature not syntactic. Real-world protocols often
have similar constraints (for instance length fields, and hash fields).
Attribute grammars allow us to model such constraints with accuracy.

### Mechanics of the Fuzzing Process

TODO :-)

