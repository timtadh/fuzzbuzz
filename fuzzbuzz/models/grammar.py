#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from nonterminal import NonTerminal

class Grammar(object):

    def __init__(self, rules):
        self.rules = rules
        self.symbols = dict()
        for rule in rules:
            nt = self.symbols.get(rule.name, NonTerminal(rule.name))
            nt.addrule(rule)
            self.symbols[rule.name] = nt
        #print self.symbols
        for rule in self.rules:
            for i, tup in enumerate(rule.pattern):
                sym, cnt = tup
                if sym not in self.symbols: continue
                rule.pattern[i] = (self.symbols[sym], cnt)
        for rule in self.rules:
            print rule.pattern
        print
        print

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'

class Terminal(object):

    def __init__(self, name, id):
        self.name = name

