Proposed Grammar For Defining Fuzzer
====================================

Production -> NonTerminal ARROW Bodys SEMI

NonTerminal -> NAME
             | NAME LPAREN NUMBER RPAREN

Bodys -> Bodys PIPE Body
       | Body

Body -> Symbols
      | Symbols ACStmts

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
                | Attr

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