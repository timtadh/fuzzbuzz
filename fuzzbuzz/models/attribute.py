#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value

class AttrChain(Value):

    def __init__(self, lookup_chain):
        self.__type = type
        self.lookup_chain

class Attribute(Value):

    def __init__(self, objs, call_chain):
        self.call_chain = call_chain