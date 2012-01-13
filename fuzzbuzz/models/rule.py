#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Rule(object):

    def __init__(self, name, pattern, action, condition):
        self.name = name
        self.pattern = pattern
        self.action = action
        self.condition = condition

    def __repr__(self): return str(self)
    def __str__(self):
        return (
            '<Rule "%s -> %s"%s%s%s>'
        ) % (
          self.name,
          ' '.join(sym[0] for sym in self.pattern),
          ' with action' if self.action is not None else '',
          ' and' if self.action is not None and self.condition is not None else '',
          ' with condition' if self.condition is not None else ''
        )

def mkrules(node):
    def sym_name(node): return node.children[0]
    def sym_num(node): return node.children[1]
    rules = list()
    name = sym_name(node.children[0])
    bodys = node.children[1]
    #print name
    for body in bodys.children:
        pattern = body.children[0]
        pattern = [(sym_name(sym), sym_num(sym)) for sym in pattern.children]
        action = None
        condition = None
        if len(body.children) == 2:
            for ACStmt in body.children[1].children:
                type = ACStmt.label
                if type == 'Action':
                    action = ACStmt
                elif type == 'Condition':
                    condition = ACStmt
                else:
                    raise Exception, 'Unexpected type %s' % (type,)
        rules.append(Rule(name, pattern, action, condition))
    #print productions
    #print
    return rules