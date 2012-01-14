#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from nonterminal import NonTerminal
from terminal import Terminal

class Grammar(object):

    def __init__(self, rules):
        self.start = rules[0].name
        self.rules = rules
        self.nonterminals = dict()
        self.terminals = dict()
        for rule in rules:
            nt = self.nonterminals.get(rule.name, NonTerminal(rule.name))
            nt.addrule(rule)
            self.nonterminals[rule.name] = nt
        #print self.symbols
        for rule in self.rules:
            for i, tup in enumerate(rule.pattern):
                sym, cnt = tup
                if sym in self.nonterminals:
                    rule.pattern[i] = (self.nonterminals[sym], cnt)
                else:
                    terminal = self.terminals.get(sym, Terminal(sym))
                    rule.pattern[i] = (terminal, cnt)
                    self.terminals[sym] = terminal
        for rule in self.rules:
            print rule.pattern
        print
        print self.start
        print

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'
