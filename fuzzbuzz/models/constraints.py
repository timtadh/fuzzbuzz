#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from executable import Executable
from 

class Constraint(Executable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

class Is(Constraint):

    def execute(self, objs):
        a = self.a(objs)
        b = self.b(objs)
