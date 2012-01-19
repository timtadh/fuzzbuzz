#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Action(object):

    def __init__(self, node):
        pass
        #self.node = node
        #print node
        #print
        #print

## There are two types of action statements
##  1) Assign statements
##  2) If statements

class Assign(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        

class If(object): pass
