#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value

class AttrChain(Value):

    def __init__(self, lookup_chain):
        #self.__type = None
        pass

class Attribute(Value):

    def __init__(self, objs, obj, call_chain=None):
        #self.__type = None
        if call_chain is not None:
            assert hasattr(obj, '__call__')
            for call in call_chain:
                print call
            value = None
            raise Exception
        else:
            value = obj
