Expression Grammar
==================

The following specification is defines the LL(1) grammar used in the parser. The
grammar is appropriate for a non-backtracking recursive descent parser.

### Tokens

    NUMBER  = /[0-9]+\.?[0-9]*/
    PLUS    = '+'
    DASH    = '-'
    STAR    = '*'
    SLASH   = '/'
    EXP     = '^'
    LPAREN  = '('
    RPAREN  = ')'
    LSQUARE = '['
    RSQUARE = ']'
    LANGLE  = '<'
    RANGLE  = '>'
    COMMA   = ','
    SEMI    = ';'
    T       = 'T'
    LOG     = 'log'

### LL(1) Grammar

NB: `e` indicates the Empty string.

    Expr : Term Expr_
    Expr_ : PLUS Term Expr_
    Expr_ : DASH Term Expr_
    Expr_ : e
    Term : Exp Term_
    Term_ : STAR Exp Term_
    Term_ : SLASH Exp Term_
    Term_ : e
    Exp : Unary Exp_
    Exp_ : EXP Unary Exp_
    Exp_ : e
    Unary : DASH PostUnary
    Unary : PostUnary
    PostUnary : Factor T
    PostUnary : Factor
    Factor : Value
    Factor : LPAREN Expr RPAREN
    Value : Atom
    Value : Log
    Value : LSQUARE Matrix RSQUARE
    Value : LANGLE Vector RANGLE
    Atom : NUMBER
    Log : LOG LPAREN Expr COMMA Expr RPAREN
    Matrix : Vector Matrix_
    Matrix_ : SEMI Vector Matrix_
    Matrix_ : e
    Vector : Expr Vector_
    Vector_ : COMMA Expr Vector_
    Vector_ : e
