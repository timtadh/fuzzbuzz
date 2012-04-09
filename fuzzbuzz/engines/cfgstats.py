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
class CouldNotChooseRule(Exception): pass

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
        tables = ["Table Names CFGStats Accepts:"]
        for tname in valid_tables:
            tables.append(tname + " - " + valid_tables[tname])
        return None, '\n'.join(tables)

    if stat_tables:
        for tname in valid_tables:
            if stat_tables.has_key(tname):
                intersection.append(tname)
        if len(intersection) is 0:
            err = (
              "CFGStats Failure: No known table names were provided\n"
              "Run with -T flag for more information"
            )
            return None, err
    else:
        return None, "CFGStats Failure: No stats tables provided!"


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
        rand = random()
        probdist = dict()

        #we want to build a quick index of probabilities => rules
        for tname in intersection:
            for rule in tables[tname][nonterm.name]:
                prob = tables[tname][nonterm.name][rule]
                if not probdist.has_key(prob): #first time we find a rule with this probability
                    probdist[prob] = {rule}
                else: #we have a key with this probability so we just want to add ourselves to that key's set
                    probdist[prob].add(rule)

        '''
        At this point we want to find out where our random number lies in our probability distribution

             1         2    3
        [-a--|---b-----|-c--|-d--]

        if rand=a, winningKey = 1
        if rand=b, winningKey = 2
        if rand=c, winningKey = 3
        if rand=d, winningKey = 3


        thus we set winningKey = current_key (if rand < current_key
                                           and if current_key < current_winningKey) (because if rand=a, we dont want winningKey to be 2 or 3, for example)
        '''

        winningKey = 2
        for prob in probdist:
            if rand < prob and prob < float(winningKey):
                    winningKey = prob

        if winningKey is 2:
            winningKey = max(probdist)

        ruleStr = probdist[winningKey].pop()
        #so at this point we have a string representing the rule we want, but we need to actually return a RULE (type)

        stringList = list()
        for rule in nonterm.rules:
            toString = str()
            for sym,cnt in rule.pattern:
                if sym.name == "NEWLINE": #temporary workaround for token mismatch between gramstats and fuzzbuzz
                    continue
                elif sym.name == "NUMBER": #temporary workaround for token mismatch between gramstats and fuzzbuzz
                    toString = toString + "INT_VAL"
                else:
                    toString = toString + sym.name
                toString = toString + ":" #temporary workaround for token mismatch between gramstats and fuzzbuzz
            toString = toString[:-1] #there is an extra ":" at the end that we don't want
            stringList.append(toString)

        if ruleStr not in stringList:
            print "Parsed rule could not be matched with grammar rule"
            print "(Attempted to parse " + ruleStr + ")"
            raise CouldNotChooseRule
        else:
            return nonterm.rules[[i for i,x in enumerate(stringList) if x == ruleStr][0]]


    output = list()
    def fuzz(start):
        keyify()
        stack = list()
        stack.append((start, None, 0))

        while stack:
            nonterm, rule, j = stack.pop()
            if rule is None: #otherwise we are continuing from where we left off
                assert j is 0
                rule = choose(nonterm)
            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    stack.append((nonterm, rule, i+1))
                    stack.append((sym, None, 0))
                    break
                if sym.__class__ is Terminal:
                    output.append(rlexer[sym.name]())

    fuzz(grammar.start)
    return output, None
