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
        'cp' : 'conditional_probabilities',
    }

    intersection = []

    tables = dict()
    lookBack = int()

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

    def getLookback():
        if stat_tables.has_key("cp"):
            return int(stat_tables["cp"][0][0])
        else:
            return None


    def initialize_tables():
        for tname in intersection:
            if tname == "pp":
                for gramtuple in stat_tables[tname]:
                    #these are all of the productions for a specific table
                    assert len(gramtuple) is 3
                    if not tables.has_key(tname): # this is a new table
                        tables[tname] = {gramtuple[0] :
                                            {gramtuple[1] :
                                                float(gramtuple[2])
                                            }
                                        }
                    else:
                        if not tables.get(tname).has_key(gramtuple[0]):
                            # this is simply a new production for the table
                            tables[tname][gramtuple[0]] = {gramtuple[1] :
                                                            float(gramtuple[2])
                                                          }
                        else: # adding a new rule to a production
                            tables[tname][gramtuple[0]][gramtuple[1]] = float(gramtuple[2])
            elif tname == "cp":
                #tables[tname][nonterminal][prevTuple][rule] = prob
                for gramtuple in stat_tables[tname]:
                    #these are all of the productions for a specific table
                    lookBack = int(gramtuple[0])
                    assert len(gramtuple) is lookBack + 3
                    production = gramtuple[1]

                    #prudction = nonterminal => rule
                    nonterminal = production.split("=>")[0].strip() #LHS of =>
                    rule = production.split("=>")[1].strip() #RHS of =>

                    prevTuple = tuple(gramtuple[x+2] for x in range(lookBack))
                    prob = gramtuple[lookBack + 2]
                    if not tables.has_key(tname): # this is a new table
                        tables[tname] = {nonterminal :
                                            {prevTuple :
                                                {rule : float(prob)}
                                            }
                                        }

                    else:
                        if not tables.get(tname).has_key(nonterminal):
                            # this is simply a new nonterminal for the table
                            tables[tname][nonterminal] = {prevTuple :
                                                            {rule : float(prob)}
                                                         }
                        else:
                            if not tables.get(tname).get(nonterminal).has_key(prevTuple):
                            #this is a new prevTuple for a nonterminal we have
                                tables[tname][nonterminal][prevTuple] = {rule : float(prob)}
                            else:
                                tables[tname][nonterminal][prevTuple][rule] = float(prob)
        return

    def log_as_prev(lookBack, prev, label):
        retVal = tuple(prev[x+1] for x in range(lookBack-1)) + (label,)
        return retVal

    '''
    This function takes a string representation of a Rule Object and returns
    the corresponding object.

    We do this by taking all of the rule objects for a specific nonterminal
    and converting them into NT:NT:NT format strings (gramstat format?)

    Then we can compare strings to strings.
    '''
    def getRulefromString(nonterm, ruleStr):
        stringList = list()
        for rule in nonterm.rules:
            toString = str()
            for sym,cnt in rule.pattern:
                if sym.name == "NEWLINE":
                    continue
                else:
                    toString = toString + sym.name
                toString = toString + ":"
            toString = toString[:-1] #remove extra ":" at the end
            stringList.append(toString)

        if ruleStr not in stringList:
            print "Parsed rule could not be matched with grammar rule"
            print "(Attempted to parse " + ruleStr + ")"
            raise CouldNotChooseRule
        else:
            return nonterm.rules[[i for i,x in enumerate(stringList) if x == ruleStr][0]]

    def choose(nonterm, prevTuple=None):
        rand = random()
        probdist = dict()

        #we want to build a quick index of probabilities => rules
        for tname in intersection:
            if tname == "pp":
                for rule in tables[tname][nonterm.name]:
                    prob = tables[tname][nonterm.name][rule]
                    if not probdist.has_key(prob): #first time we find a rule with this probability
                        probdist[prob] = [rule]
                    else: #we have a key with this probability so we just want to add ourselves to that key's set
                        probdist[prob].add(rule)
            elif tname == "cp":
                #print nonterm.name
                #print prevTuple
                if not tables[tname][nonterm.name].has_key(prevTuple):
                    return choice(nonterm.rules) # maybe (probably?) do do something smarter in the future
                else:
                    for rule in tables[tname][nonterm.name][prevTuple]:
                        prob = tables[tname][nonterm.name][prevTuple][rule]
                        if not probdist.has_key(prob): #first time we find a rule with this probability
                            probdist[prob] = [rule]
                        else: #we have a key with this probability so we just want to add ourselves to that key's set
                            probdist[prob].append(rule)

        '''
        At this point we want to find out where our random number lies in our probability distribution

             1         2    3
        [-a--|---b-----|-c--|-d--]

        if rand=a, winningKey = 1
        if rand=b, winningKey = 2
        if rand=c, winningKey = 3
        if rand=d, winningKey = 3


        thus we set:

        winningKey = current_key (if rand < current_key
                                    and if current_key < current_winningKey)

        (because if rand=a, we dont want winningKey to be 2 or 3, for example)
        '''

        winningKey = 2
        for prob in probdist:
            if rand < prob and prob < float(winningKey):
                    winningKey = prob

        if winningKey is 2:
            winningKey = max(probdist)


        ruleStr = probdist[winningKey].pop()
        chosen_rule = getRulefromString(nonterm, ruleStr)

        return chosen_rule


    output = list()
    def fuzz(start):
        initialize_tables()
        lookBack = getLookback()
        if lookBack:
            prev = tuple('None' for x in range(lookBack))
            prevStack = list() #stack of previous prevTuples
            #the Boolean in each prevStack tuple tells us if we need to pop
            initStack = (tuple('None' for x in range(lookBack)), False)
            prevStack.append(initStack)
        stack = list()
        stack.append((start, None, 0))

        while stack:
            if lookBack:
                prev = prevStack[len(prevStack)-1][0]
                requirePop = prevStack[len(prevStack)-1][1]
                prevAsTuple = tuple(prev[x] for x in range(lookBack))

                if requirePop:
                    prevStack.pop()

            nonterm, rule, j = stack.pop()
            if rule is None: #otherwise we are continuing from where we left off
                assert j is 0
                if not lookBack:
                    rule = choose(nonterm)
                else:
                    rule = choose(nonterm, prev)
                    prevAsTuple = log_as_prev(lookBack, prevAsTuple, nonterm.name) #set myself as the last visited nonterm
                    if len(rule.pattern) > 1:
                        prevStack.append((prevAsTuple, False))
                    else:
                        prevStack.append((prevAsTuple, True))
                        '''
                                        ~~ Why True above? ~~

                        If there is only one nonterminal in this rule then we
                        want to log it as a previous but then pop it from the
                        stack.

                        This way, rules that have >1 nonterminals will keep
                        their "prev" relative to what it was originally.

                        For example, with NT:NT2:NT3, when we get to NT2, we
                        dont want previous to include the previous from when we
                        went down NT's productions.
                        '''



            for i, (sym, cnt) in list(enumerate(rule.pattern))[j:]:
                if sym.__class__ is NonTerminal:
                    stack.append((nonterm, rule, i+1))
                    stack.append((sym, None, 0))
                    break
                if sym.__class__ is Terminal:
                    output.append(rlexer[sym.name]())

    fuzz(grammar.start)

    return output, None