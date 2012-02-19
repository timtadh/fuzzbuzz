#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from ply import yacc

from lexer import tokens, Lexer
from ast import Node
from fuzzbuzz import models
from fuzzbuzz.models.grammar import Grammar
from fuzzbuzz.models.rule import mkrules
from fuzzbuzz.models import action, attr_types, value, attribute, binop

## If you are confused about the syntax in this file I recommend reading the
## documentation on the PLY website to see how this compiler compiler's syntax
## works.
class Parser(object):

    tokens = tokens
    precedence = (
        #('left', 'LCURLY'),
        ('left', 'RPAREN'),
    )

    def __new__(cls, **kwargs):
        ## Does magic to allow PLY to do its thing.
        self = super(Parser, cls).__new__(cls, **kwargs)
        self.table = dict()
        self.loc = list()
        self.yacc = yacc.yacc(module=self,  tabmodule="sl_parser_tab", **kwargs)
        return self.yacc

    def get_table(self):
        c = self.table
        for s in self.loc:
            c = self.table[c]
        return c

    def p_Start(self, t):
        'Start : Productions'
        t[0] = Grammar(t[1]['rules'])

    def p_Productions1(self, t):
        'Productions : Productions Production'
        node = t[1]['node'].addkid(t[2]['node'])
        rules = t[1]['rules'] + t[2]['rules']
        t[0] = {'node':node, 'rules':rules}


    def p_Productions2(self, t):
        'Productions : Production'
        node = Node('Productions').addkid(t[1]['node'])
        t[0] = {'node':node, 'rules':t[1]['rules']}

    def p_Production(self, t):
        'Production : Symbol ARROW Bodys SEMI'
        t[1].addkid(1)
        node = (
          Node('Production')
            .addkid(t[1])
            .addkid(Node('Bodys', children=t[3]['nodes']))
        )
        for body in t[3]['nodes']:
            names = {t[1].children[0]:2}
            for kid in body.children[0].children:
                count = names.get(kid.children[0], 1)
                kid.addkid(count)
                names[kid.children[0]] = count + 1
        t[0] = {'node':node, 'rules':mkrules(node, t[3]['objs'])}

    def p_Bodys1(self, t):
        'Bodys : Bodys PIPE Body'
        t[0] = {
          'nodes':t[1]['nodes']+[t[3]['node']],
          'objs':t[1]['objs']+[t[3]['objs']]
        }

    def p_Bodys2(self, t):
        'Bodys : Body'
        t[0] = {'nodes':[t[1]['node']], 'objs':[t[1]['objs']]}

    def p_Body1(self, t):
        'Body : Symbols'
        t[0] = {'node':Node('Body').addkid(t[1]), 'objs':None}

    def p_Body2(self, t):
        'Body : Symbols ACStmts'
        t[0] = {'node':Node('Body').addkid(t[1]),
                'objs':t[2]}

    def p_Symbols1(self, t):
        'Symbols : Symbols Symbol'
        t[0] = t[1].addkid(t[2])

    def p_Symbols2(self, t):
        'Symbols : Symbol'
        t[0] = Node('Symbols').addkid(t[1])

    def p_Symbol1(self, t):
        'Symbol : NAME'
        t[0] = Node('NonTerminal').addkid(t[1])

    def p_Symbol2(self, t):
        'Symbol : TERMINAL'
        t[0] = Node('Terminal').addkid(t[1])

    def p_ACStmts1(self, t):
        'ACStmts : ACStmts ACStmt'
        t[0] = t[1]+[t[2]]

    def p_ACStmts2(self, t):
        'ACStmts : ACStmt'
        t[0] = [t[1]]

    def p_ACStmt1(self, t):
        'ACStmt : WITH ACTION LCURLY ActionStmts RCURLY'
        t[0] = action.Action(t[4])

    def p_ACStmt2(self, t):
        'ACStmt : WITH CONDITION LCURLY OrExpr RCURLY'
        t[0] = t[4]

    def p_OrExpr1(self, t):
        'OrExpr : OrExpr OR AndExpr'
        t[0] = models.condition.Any(t[1], t[3])

    def p_OrExpr2(self, t):
        'OrExpr : AndExpr'
        t[0] = t[1]

    def p_AndExpr1(self, t):
        'AndExpr : AndExpr AND NotExpr'
        t[0] = models.condition.All(t[1], t[3])
    
    def p_AndExpr2(self, t):
        'AndExpr : NotExpr'
        t[0] = t[1]

    def p_NotExpr1(self, t):
        'NotExpr : BANG BooleanExpr'
        t[0] = Node('Not').addkid(t[2])
        raise Exception, "Not operator not yet implemented"

    def p_NotExpr2(self, t):
        'NotExpr : BooleanExpr'
        t[0] = t[1]

    def p_BooleanExpr1(self, t):
        'BooleanExpr : Expr'
        t[0] = Node('BooleanCast').addkid(t[1])
        raise Exception, "Boolean Casts not yet implemented"

    def p_BooleanExpr2(self, t):
        'BooleanExpr : CmpExpr'
        t[0] = t[1]

    def p_BooleanExpr3(self, t):
        'BooleanExpr : LPAREN OrExpr RPAREN'
        t[0] = t[2]

    def p_CmpExpr(self, t):
        'CmpExpr : Expr CmpOp Expr'
        t[0] = (
          {
            'is':models.condition.Is,
            'in':models.condition.In
          }
          .get(t[2].label, lambda x,y: None)
        )(t[1], t[3])

    def p_CmpOp1(self, t):
        '''CmpOp : EQEQ
                 | NQ
                 | LANGLE
                 | LE
                 | RANGLE
                 | GE
                 | IN
                 | IS
                 | SUPERSET
                 | SUBSET'''
        t[0] = Node(t[1])

    def p_CmpOp2(self, t):
        '''CmpOp : PROPER SUPERSET
                 | PROPER SUBSET
                 | NOT IN
                 | IS NOT'''
        t[0] = Node(t[1] + ' ' + t[2])

    def p_ActionStmts1(self, t):
        'ActionStmts : ActionStmts ActionStmt'
        t[0] = t[1] + [t[2]]

    def p_ActionStmts2(self, t):
        'ActionStmts : ActionStmt'
        t[0] = [t[1]]

    def p_ActionStmt1(self, t):
        'ActionStmt : AttributeValue EQUAL Expr'
        #t[0] = Node('Assign').addkid(t[1]).addkid(t[3])
        #print t[1], t[3]
        t[0] = action.Assign(attribute.AttrChain(t[1]), t[3])

    def p_ActionStmt2(self, t):
        'ActionStmt : IF LPAREN OrExpr RPAREN LCURLY ActionStmts RCURLY'
        #t[0] = Node('If').addkid(t[3]).addkid(t[6])
        t[0] = action.If(t[3], action.Action(t[6]))

    def p_ActionStmt3(self, t):
        'ActionStmt : IF LPAREN OrExpr RPAREN LCURLY ActionStmts RCURLY ELSE LCURLY ActionStmts RCURLY'
        t[0] = action.If(t[3], action.Action(t[6]), action.Action(t[10]))

    def p_Expr(self, t):
        'Expr : SetOps'
        t[0] = t[1]

    def p_SetOps1(self, t):
        'SetOps : SetOps PIPE AddSub'
        t[0] = binop.Union(t[1], t[3])

    def p_SetOps2(self, t):
        'SetOps : SetOps AMPERSTAND AddSub'
        t[0] = binop.Intersection(t[1], t[3])

    def p_SetOps2(self, t):
        'SetOps : SetOps TILDE AddSub'
        t[0] = binop.Difference(t[1], t[3])

    def p_SetOps3(self, t):
        'SetOps : AddSub'
        t[0] = t[1]

    def p_AddSub1(self, t):
        'AddSub : AddSub PLUS MulDiv'
        t[0] = binop.Add(t[1], t[3])

    def p_AddSub2(self, t):
        'AddSub : AddSub DASH MulDiv'
        t[0] = binop.Sub(t[1], t[3])

    def p_AddSub3(self, t):
        'AddSub : MulDiv'
        t[0] = t[1]

    def p_MulDiv1(self, t):
        'MulDiv : MulDiv STAR Atomic'
        t[0] = binop.Mul(t[1], t[3])

    def p_MulDiv2(self, t):
        'MulDiv : MulDiv SLASH Atomic'
        t[0] = binop.Slash(t[1], t[3])

    def p_MulDiv3(self, t):
        'MulDiv : Atomic'
        t[0] = t[1]

    def p_Atomic1(self, t):
        'Atomic : Value'
        t[0] = t[1]

    def p_Atomic2(self, t):
        'Atomic : LPAREN Expr RPAREN'
        t[0] = t[2]

    def p_Value1(self, t):
        'Value : NUMBER'
        t[0] = value.Value(attr_types.Number, attr_types.Number(t[1]))

    def p_Value2(self, t):
        'Value : STRING'
        t[0] = value.Value(attr_types.String, attr_types.String(t[1][1:-1]))

    def p_Value3(self, t):
        'Value : NONE'
        t[0] = value.Value(attr_types.NoneType, attr_types.NoneType())

    def p_Value4(self, t):
        'Value : SetLiteral'
        t[0] = value.SetValue(t[1].children)

    def p_Value5(self, t):
        'Value : AttributeValue'
        t[0] = attribute.AttrChain(t[1])

    def p_AttributeValue(self, t):
        'AttributeValue : SymbolObject AttributeValue_'
        t[0] = [t[1]] + t[2]

    def p_AttributeValue_1(self, t):
        'AttributeValue_ : DOT Attr AttributeValue_'
        #print t[2](dict(), {'james':'james', 'thames':'thames', 'games':'games', 'names':'names', 'decl':'decl', 'uses':'uses', 'value':'value'}).value
        t[0] = [t[2]] + t[3]

    def p_AttributeValue_2(self, t):
        'AttributeValue_ : '
        t[0] = list()

    def p_SymbolObject1(self, t):
        'SymbolObject : Symbol'
        t[0] = attribute.Attribute(
          attribute.SymbolObject(t[1].label, t[1].children[0], 1))

    def p_SymbolObject2(self, t):
        'SymbolObject : Symbol LCURLY NUMBER RCURLY'
        t[0] = attribute.Attribute(
          attribute.SymbolObject(t[1].label, t[1].children[0], t[3]))

    def p_Attr1(self, t):
        'Attr : NAME'
        t[0] = attribute.Attribute(attribute.Object(t[1]))

    def p_Attr2(self, t):
        'Attr : NAME Call'
        t[0] = attribute.Attribute(attribute.Object(t[1]), attribute.CallChain(t[2].children))

    def p_Call1(self, t):
        'Call : Call Call_'
        t[0] = t[1].addkid(t[2])

    def p_Call2(self, t):
        'Call : Call_'
        t[0] = Node('CallChain').addkid(t[1])

    def p_Call_1(self, t):
        'Call_ : Fcall'
        t[0] = attribute.FCall(t[1])
        #t[0] = Node('Fcall', children=t[1])

    def p_Fcall1(self, t):
        'Fcall : LPAREN RPAREN'
        t[0] = list()

    def p_Fcall2(self, t):
        'Fcall : LPAREN ParameterList RPAREN'
        #print t[2]
        t[0] = t[2]

    def p_ParameterList1(self, t):
        'ParameterList : ParameterList COMMA Value'
        t[0] = t[1] + [t[3]]

    def p_ParameterList2(self, t):
        'ParameterList : Value'
        t[0] = [t[1]]

    def p_SetLiteral1(self, t):
        'SetLiteral : LCURLY ParameterList RCURLY'
        t[0] = Node('SetLiteral', children=t[2])

    def p_SetLiteral2(self, t):
        'SetLiteral : LCURLY RCURLY'
        t[0] = Node('SetLiteral')

    def p_error(self, t):
        raise SyntaxError, "Syntax error at '%s', %s.%s" % (t,t.lineno,t.lexpos)

def parse(string):
    return Parser().parse(string, lexer=Lexer())
