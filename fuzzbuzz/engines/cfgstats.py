#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Rafael Lopez
#Email: rafael.lopez.u@gmail.com
#For licensing see the LICENSE file in the top level directory.

from random import seed, choice, randint, random

from reg import registration
from fuzzbuzz.models.symbols import Terminal, NonTerminal

class ListTables(Exception): pass
class NoValidTable(Exception): pass

@registration.register(
  {'stat_tables':'tables', 'list_tables':'table_names_requested'},
  'A fuzzer to produce output based on statistics provided at input')
def cfgstats(rlexer, grammar, stat_tables=None, list_tables=False):
    # grammar.start --> start symbol it is a fuzzbuzz.models.symbols.NonTerminal
    # nonterm.rules --> a list of the possible choices.
    # rule -> list of Terminal and NonTerminal symbols
    # getnextrule(nonterm): random.choice(nonterm.rules)

    #print stat_tables

    valid_tables = {
        'pp' : 'production_probabilities',
        'test' : 'test description'
    }

    intersection = []

    tables = dict()

    if list_tables:
        print "Table Names CFGStats Accepts:\n"
        for tname in valid_tables:
            print tname + " - " + valid_tables[tname]
        raise ListTables

    if stat_tables:
        for tname in valid_tables:
            if stat_tables.has_key(tname):
                intersection.append(tname)
        if len(intersection) is 0:
            print "No table names that CFGStats accepts were provided"
            print "Run with -T flag for more information"
            raise NoValidTable
    else:
        print "CFGStats Warning: No stats tables provided!"


    def keyify():
        for tname in intersection:
            for gramtuple in stat_tables[tname]: #these are all of the productions for a specific table
                assert len(gramtuple) is 3
                if not tables.has_key(tname): # this is a new table
                    tables[tname] = {gramtuple[0] : {gramtuple[1] : float(gramtuple[2])}}
                else:
                    if not tables.get(tname).has_key(gramtuple[0]): # this is simply a new production for the table
                        tables[tname][gramtuple[0]] = {gramtuple[1] : float(gramtuple[2])}
                    else: # adding a new rule to a production
                        tables[tname][gramtuple[0]][gramtuple[1]] = float(gramtuple[2])

    def choose(nonterm):
        #print nonterm.name
        rand = random()
        print rand
        probdist = dict()

        for tname in intersection:
            for rule in tables[tname][nonterm.name]:
                prob = tables[tname][nonterm.name][rule]
                #print rule + " with " + prob
                if not probdist.has_key(prob): #first time we find a rule with this probability
                    probdist[prob] = {rule}
                else: #we have a key with this probability so we just want to add ourselves to that key's set
                    probdist[prob].add(rule)

        #print probdist

        winner = 2

        for prob in probdist:
            print prob
            if rand < prob:
                #print 'we are here'
                if prob < float(winner):
                    #print 'we are now here'
                    winner = prob

        if winner is 2:
            winner = max(probdist)

        #print winner
        #pass
        return probdist[winner].pop()


    output = list()
    def fuzz(start):
        keyify()
        stack = list()
        stack.append((start, None, 0))

        while stack:
            nonterm, rule, j = stack.pop()

            if rule is None: #otherwise we are continuing from where we left off
                assert j is 0
                #rule = choice(nonterm.rules)
                rule = choose(nonterm)
                return
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    stack.append((nonterm, rule, i+1))
                    stack.append((sym, None, 0))
                    break
                if sym.__class__ is Terminal:
                    output.append(rlexer[sym.name]())

    fuzz(grammar.start)
    return output
