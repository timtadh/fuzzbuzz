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
        nts = dict()
        for rule in rules:
            nt_rules = nts.get(rule.name, list())
            nt_rules.append(rule)
            nts[rule.name] = nt_rules
        for name, rules in nts.iteritems():
            self.nonterminals[name] = NonTerminal(name, rules)
        for rule in self.rules:
            for i, tup in enumerate(rule.pattern):
                sym, cnt = tup
                if sym in self.nonterminals:
                    rule.pattern[i] = (self.nonterminals[sym], cnt)
                else:
                    terminal = Terminal(sym)
                    rule.pattern[i] = (terminal, cnt)
        self.start = self.nonterminals[self.rules[0].name]
        #for rule in self.rules:
            #print rule.pattern
        #print
        #print self.start
        #print

    def __str__(self):
        return super(Grammar, self).__str__()[:-1] + ' ' + str(self.rules) + '>'
