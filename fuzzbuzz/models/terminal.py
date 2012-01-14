#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Terminal(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self): return str(self)
    def __str__(self): return '<Term %s>' % self.name
