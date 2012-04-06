#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

from random import randint

stringifiers = {
    'VAR' : (lambda: 'var'),
    'NAME' : (lambda: ''.join(chr(randint(97, 122)) for x in xrange(1, randint(2,10)))),
    'EQUAL' : (lambda: '='),
    'NUMBER' : (lambda: str(randint(1, 1000))),
    'PRINT' : (lambda: 'print'),
    'NEWLINE' : (lambda: '\n'),
}
