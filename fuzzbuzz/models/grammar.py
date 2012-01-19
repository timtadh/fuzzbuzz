#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import functools

from symbols import NonTerminal, Terminal

class Grammar(object):

    def __init__(self, rules):
        self.rules = rules
        self.nonterminals = dict()
        for rule in rules:
            nt = self.nonterminals.get(rule.name, NonTerminal(rule.name))
            nt.addrule(rule)
            self.nonterminals[rule.name] = nt
        for rule in self.rules:
            for i, tup in enumerate(rule.pattern):
                sym, cnt = tup
                if sym in self.nonterminals:
                    rule.pattern[i] = (self.nonterminals[sym], cnt)
                else:
                    terminal = Terminal(sym)
                    rule.pattern[i] = (terminal, cnt)
        self.start = self.nonterminals[rules[0].name]
        #for rule in self.rules:
            #print rule.pattern
        #print
        #print self.start
        #print

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'
