#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Action(object):

    def __init__(self, stmts):
        self.stmts = stmts

    def unconstrained(self, objs):
        return all(stmt.unconstrained(objs) for stmt in self.stmts)

    def execute(self, objs):
        for stmt in self.stmts:
            stmt.execute(objs)

## There are two types of action statements
##  1) Assign statements
##  2) If statements

class Assign(object):

    def __init__(self, left, right):
        #print left, right
        self.left = left
        self.right = right

    def unconstrained(self, objs):
        #print ' '*4, objs
        #print ' '*4, self.left.has_value(objs), '==', self.right.has_value(objs)
        if not self.left.has_value(objs): return True
        
        if self.right.has_value(objs):
            return self.left.value(objs) == self.right.value(objs)
        else:
            if self.right.writable():
                #print self.right.lookup_chain[0].obj.name
                self.right.set_value(objs, self.left.value(objs))
                return True
            else:
                return False

    def execute(self, objs):
        if self.left.has_value(objs):
            assert self.left.value(objs) == self.right.value(objs)
            return
        
        assert self.right.has_value(objs)
        self.left.set_value(objs, self.right.value(objs))
        

class If(object): pass
