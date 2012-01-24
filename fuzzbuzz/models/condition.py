#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Condition(object):

    def __init__(self, constraint):
        self.constraint = constraint

    def execute(self, objs):
        self.constraint.execute(objs)
