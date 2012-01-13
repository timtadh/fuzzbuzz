#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Grammar(object):

    def __init__(self, rules):
        self.rules = rules

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'

class NonTerminal(object):

    def __init__(self, rules):
        pass
