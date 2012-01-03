Proposed Grammar For Defining Fuzzer
====================================

    Productions -> Productions Production
                 | Production

    Production -> Symbol ARROW Bodys SEMI

    Bodys -> Bodys PIPE Body
           | Body

    Body -> Symbols
          | Symbols ACStmts

    Symbols -> Symbols Symbol
             | Symbol

    Symbol -> NAME
            | NAME LCURLY NUMBER RCURLY

    ACStmts -> ACStmts ACStmt
             | ACStmt

    ACStmt -> WITH ACTION COLON ActionStmts
            | WITH CONDITION COLON OrExpr

    OrExpr -> OrExpr OR AndExpr
             | AndExpr

    AndExpr -> AndExpr AND NotExpr
             | NotExpr

    NotExpr -> NOT BooleanExpr
             | BooleanExpr

    BooleanExpr -> Expr
                 | CmpExpr
                 | LPAREN OrExpr RPAREN

    CmpExpr -> Expr CmpOp Expr

    CmpOp -> EQEQ
           | NQ
           | LANGLE
           | LE
           | RANGLE
           | GE
           | IN
           | NOT IN
           | SUPERSET
           | SUBSET
           | PROPER SUPERSET
           | PROPER SUBSET

    ActionStmts -> ActionStmts ActionStmt
                | ActionStmt

    ActionStmt -> NAME EQUAL Expr
                | IF LPAREN OrExpr RPAREN LCURLY ActionStmts RCURLY
                | IF LPAREN OrExpr RPAREN LCURLY ActionStmts RCURLY ELSE LCURLY ActionStmts RCURLY

    Expr -> AddSub

    AddSub -> AddSub PLUS MulDiv
            | AddSub DASH MulDiv
            | MulDiv

    MulDiv -> MulDiv STAR Atomic
            | MulDiv SLASH Atomic
            | Atomic

    Atomic -> Value
            | LPAREN Expr RPAREN

    Value -> NUMBER
           | STRING
           | AttributeValue

    AttributeValue -> AttributeValue DOT Attr
                    | NAME LCURLY NUMBER RCURLY
                    | NAME Call
                    | NAME

    Attr -> NAME
          | NAME Call

    Call -> Call Call_
          | Call_

    Call_ -> Fcall
           | Dcall

    Fcall -> LPAREN RPAREN
           | LPAREN ParameterList RPAREN

    Dcall ->  LSQUARE Value RSQUARE

    ParameterList -> ParameterList COMMA Value
                   | Value

Tokens
======

    ACTION = 'action'
    CONDITION = 'condition'
    ELSE = 'else'
    IF = 'if'
    IN = 'in'
    NOT = 'not'
    PROPER = 'proper'
    SUBSET = 'subset'
    SUPERSET = 'superset'
    WITH = 'with'
    
    ARROW = '->'
    AND = '&&'
    COLON = ':'
    COMMA = ','
    DASH = '-'
    DOT = '.'
    EQEQ = '=='
    EQUAL = '='
    GE = '>='
    LANGLE = '<'
    LCURLY = '{'
    LE = '<='
    LPAREN = '('
    LSQUARE = '['
    NQ = '!='
    OR = '||'
    PIPE = '|'
    PLUS = '+'
    RANGLE = '>'
    RCURLY = '}'
    RPAREN = ')'
    RSQUARE = ']'
    SEMI = ';'
    SLASH = '/'
    STAR = '*'
    
    NAME = [a-zA-Z_][a-zA-Z0-9_]*'?
    NUMBER = [0-9]+
    STRING = "([^"\\]|\\.)*"
