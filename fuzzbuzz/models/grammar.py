#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Grammar(object):

    def __init__(self):
        self.rules = list()

    def addrule(self, rule):
        self.rules.append(rule)
