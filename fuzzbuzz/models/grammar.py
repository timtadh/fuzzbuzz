#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Grammar(object):

    def __init__(self, rules):
        self.rules = rules
        self.symbols = dict()
        for rule in rules:
            nt = self.symbols.get(rule.name, NonTerminal(rule.name))
            nt.addrule(rule)
            self.symbols[rule.name] = nt
        print self.symbols

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'

class NonTerminal(object):

    def __init__(self, name):
        self.rules = list()
        self.name = name

    def addrule(self, rule):
        self.rules.append(rule)

    def __repr__(self): return str(self)
    def __str__(self):
        return super(NonTerminal, self).__repr__()[:-1] + ' ' + str(self.rules) + '>'
