#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import random

rlexer = {
    'T' : (lambda: 'T'),
    'EXP' : (lambda: '^'),
    'LOG' : (lambda: 'log'),
    'SEMI' : (lambda: ';'),
    'PLUS' : (lambda: '+'),
    'DASH' : (lambda: '-'),
    'STAR' : (lambda: '*'),
    'SLASH' : (lambda: '/'),
    'COMMA' : (lambda: ','),
    'LANGLE' : (lambda: '<'),
    'RANGLE' : (lambda: '>'),
    'LPAREN' : (lambda: '('),
    'RPAREN' : (lambda: ')'),
    'LSQUARE' : (lambda: '['),
    'RSQUARE' : (lambda: ']'),
    'NUMBER' : (lambda: str(random.randint(1, 10)*random.random())),
}
