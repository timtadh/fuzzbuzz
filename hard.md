This is a Hard Problem
======================

No really. Generating strings of an attribute grammar is at least NP-Hard. I
am still trying to nail down the exact complexity class it belongs to, but it
is fairly straight forward to show it is NP-Hard.

Reduction, 3SAT -> AGSG [Attribute Grammar String Generation]
-------------------------------------------------------------

### Construct a grammar for the 3SAT instance

eg.

    (x1 || x2 || x3) && (x2 || ~x3 || x4) ... (x2 || x3 || x4)

becomes

    SAT -> AndsN ;
    
    AndN -> AndsN-1 AND ClauseN ;
    ...
    And2 -> Ands1 AND Clause2 ;
    And1 -> Clause1 ;

    Clause1 -> '(' x1 OR x2 OR x3 ')' ;
    Clause2 -> '(' x2 OR NOT x3 OR x4 ')' ;
    ...
    ClauseN -> '(' x2 OR x3 OR x4 ')' ;

    x1 -> TRUE
        | FALSE
        ;
    x2 -> TRUE
        | FALSE
        ;
    ...
    xN -> TRUE
        | FALSE
        ;

With attributes which synthesize the values for each clause and with a
condition which asserts that the whole expression is true.

    SAT -> AndsN
           with Condition {
             AndsN.value == True
           }
           ;

    AndN -> AndsN-1 AND ClauseN
             with Action {
                AndsN.value = AndsN-1.value && ClauseN.value
                AndsN.names = {
                  ClauseN.a.name:ClauseN.a.value,
                  ClauseN.b.name:ClauseN.b.value,
                  ClauseN.c.name:ClauseN.c.value
                }
                AndsN.names = AndsN.names | AndsN-1.names
             }
             with Condition {
               (ClauseN.a.name != ClauseN.b.name || ClauseN.a.value == ClauseN.b.value) &&
               (ClauseN.c.name != ClauseN.b.name || ClauseN.c.value == ClauseN.b.value) &&
               (ClauseN.a.name != ClauseN.c.name || ClauseN.a.value == ClauseN.c.value) &&
               (ClauseN.a.name not in AndsN-1.names || ClauseN.a.value == AndsN-1.names[ClauseN.a.name]) &&
               (ClauseN.b.name not in AndsN-1.names || ClauseN.b.value == AndsN-1.names[ClauseN.b.name]) &&
               (ClauseN.c.name not in AndsN-1.names || ClauseN.c.value == AndsN-1.names[ClauseN.c.name])
             }
             ;
    ...
    And2 -> Ands1 AND Clause2
             with Action {
                Ands2.value = Ands1.value && Clause2.value
                Ands2.names = {
                  Clause2.a.name:Clause2.a.value,
                  Clause2.b.name:Clause2.b.value,
                  Clause2.c.name:Clause2.c.value
                }
                Ands2.names = Ands2.names | Ands1.names
             }
             with Condition {
               (Clause2.a.name != Clause2.b.name || Clause2.a.value == Clause2.b.value) &&
               (Clause2.c.name != Clause2.b.name || Clause2.c.value == Clause2.b.value) &&
               (Clause2.a.name != Clause2.c.name || Clause2.a.value == Clause2.c.value) &&
               (Clause2.a.name not in Ands1.names || Clause2.a.value == Ands1.names[Clause2.a.name]) &&
               (Clause2.b.name not in Ands1.names || Clause2.b.value == Ands1.names[Clause2.b.name]) &&
               (Clause2.c.name not in Ands1.names || Clause2.c.value == Ands1.names[Clause2.c.name])
             }
             ;
    And1 -> Clause1
             with Action {
                Ands1.value = Clause1.value
                Ands1.names = {
                  Clause1.a.name:Clause1.a.value,
                  Clause1.b.name:Clause1.b.value,
                  Clause1.c.name:Clause1.c.value
                }
             }
             with Condition {
               (Clause1.a.name != Clause1.b.name || Clause1.a.value == Clause1.b.value) &&
               (Clause1.c.name != Clause1.b.name || Clause1.c.value == Clause1.b.value) &&
               (Clause1.a.name != Clause1.c.name || Clause1.a.value == Clause1.c.value)
             }
             ;

    Clause1 -> '(' x1 OR x2 OR x3 ')'
               with Action {
                 Clause1.value = x1.value || x2.value || x3.value
                 Clause1.a.name = 'x1'
                 Clause1.a.value = x1.value
                 Clause1.b.name = 'x2'
                 Clause1.b.value = x2.value
                 Clause1.c.name = 'x3'
                 Clause1.c.value = x3.value
               }
               ;
    Clause2 -> '(' x2 OR NOT x3 OR x4 ')'
               with Action {
                 Clause2.value = x2.value || !x3.value || x4.value
                 Clause1.a.name = 'x2'
                 Clause1.a.value = x2.value
                 Clause1.b.name = 'x3'
                 Clause1.b.value = x3.value
                 Clause1.c.name = 'x4'
                 Clause1.c.value = x4.value
               }
               ;
    ...
    ClauseN -> '(' x2 OR x3 OR x4 ')'
               with Action {
                 ClauseN.value = x2.value || x3.value || x4.value
                 Clause1.a.name = 'x2'
                 Clause1.a.value = x2.value
                 Clause1.b.name = 'x3'
                 Clause1.b.value = x3.value
                 Clause1.c.name = 'x4'
                 Clause1.c.value = x4.value
               }
               ;

    x1 -> TRUE
          with Action {
            x1.value = True
          }
        | FALSE
          with Action {
            x1.value = False
          }
        ;
    x2 -> TRUE
          with Action {
            x1.value = True
          }
        | False
          with Action {
            x1.value = False
          }
        ;
    ...
    xN -> TRUE
          with Action {
            x1.value = True
          }
        | FALSE
          with Action {
            x1.value = False
          }
        ;

This translation from 3SAT to AGSG is clearly poly time. O(|C| + |V|) where
C = the clauses in 3SAT and V = the variables.

### Show a solution for 3SAT --> creates a parsable string for AGSG

In a solution for 3SAT all names (x1, x2, ... xN) always have exactly one value
(True or False) assigned to them. The condition on each "AndX" production
[And1, And2 ...] states that each name always has the same value. That is
once xN has recieved a value (True or False) all other instances of xN must
have the same value. Therefore, all conditions are the AndX clauses are
satisfied by any solution to 3SAT by the definition of a 3SAT solution.

The actions on each variable production (x1, x2, ... xN) produce a value,
eg. `x1.value`, either equal to True or False. The actions on each clause
production (Clause1, Clause2, ... ClauseN) combine the values of the variables
in that clause together. They combine them in the same way they are combined
in the equivalent clause in 3SAT by construction.

Finally the chain of And productions (And1, And2, ... AndN) combine the
values synthesized by the clauses (`Clause1.value`, `Clause2.value`, ...
`ClauseN.value`). Into a final value `AndN.value` via:

    And1.value = Clause1.value
    And2.value = And1.value && Clause2.value
    And3.value = And2.value && Clause3.value
    ...
    AndN.value = AndN-1.value && ClauseN.value

which can be reduced to 1 expression with algebraic substitution as:

    AndN.value = Clause1.value && Clause2.value && ... && ClauseN.value

Which synthesizes the same value which the 3SAT problem specifies. Once again
by construction.

Therefore, if a variable assignment satisfies 3SAT then it must also synthesize
a value of `True` on `AndN.value` resulting in a parsable expression.

### Show a string generated by the grammar --> is a solution for 3SAT

In the above proof, we showed that the attributes on the grammar compute the
same answer as algebraically evaulating the 3SAT expression. Since (once again
by the above proof) there is a unique variable assignment in the generated
string this string must evaluate to True. If it didn't it could not have been
generated by the grammar. Therefore, the string generated corresponds to a
unique variable assignment in 3SAT which causes the expression to evaluate to
True.

