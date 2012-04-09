#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from ply import lex
from ply.lex import Token

reserved = dict(
    (word.lower(), word) for word in (
      'LOG',
    )
)

tokens = reserved.values() + [
    'NUMBER', 'PLUS', 'DASH', 'STAR', 'SLASH', 'LPAREN', 'RPAREN', 'LSQUARE',
    'RSQUARE', 'LANGLE', 'RANGLE', 'COMMA', 'SEMI', 'EXP', 'T'
]

# Common Regex Parts

D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?(' + D + ')+'


## Normally PLY works at the module level. I perfer having it encapsulated as
## a class. Thus the strange construction of this class in the new method allows
## PLY to do its magic.
class Lexer(object):

    def __new__(cls, **kwargs):
        self = super(Lexer, cls).__new__(cls, **kwargs)
        self.lexer = lex.lex(object=self, **kwargs)
        return self.lexer

    tokens = tokens

    'LPAREN', 'RPAREN', 'LSQUARE',
    'RSQUARE', 'LANGLE', 'RANGLE', 'COMMA', 'SEMI', 'EXP'
    t_T = r'T'
    t_EXP = r'\^'
    t_PLUS = r'\+'
    t_DASH = r'-'
    t_STAR = r'\*'
    t_SEMI = r';'
    t_SLASH = r'/'
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LANGLE = r'\<'
    t_RANGLE = r'\>'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'


    name = '(' + L + ')((' + L + ')|(' + D + '))*'
    @Token(name)
    def t_NAME(self, token):
        if token.value in reserved:
            token.type = reserved[token.value]
            return token
        return None

    const_float = '(' + D + ')+\.?(' + D + ')*(' + E + ')?'
    @Token(const_float)
    def t_CONST_FLOAT(self, token):
        token.type = 'NUMBER'
        token.value = float(token.value)
        return token

    @Token(r'\n+')
    def t_newline(self, t):
        #t.type = 'NEWLINE'
        t.lexer.lineno += t.value.count("\n")
        return None

    @Token(r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)')
    def t_COMMENT(self, token):
        #print token.lexer.lineno, len(token.value.split('\n')), token.value.split('\n')
        lines = len(token.value.split('\n')) - 1
        if lines < 0: lines = 0
        token.lexer.lineno += lines

    # Ignored characters
    t_ignore = " \t"

    def t_error(self, t):
        raise Exception, "Illegal character '%s'" % t
        t.lexer.skip(1)

if __name__ == '__main__':
    lexer = Lexer()
    lexer.input('''
        var r = 10
        print r
    ''')
    print [x for x in lexer]
