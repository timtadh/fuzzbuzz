#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys, functools
from collections import Mapping

class Registration(Mapping):

    types = ['img', 'table']

    def __init__(self):
        self.engines = dict()

    def __iter__(self):
        for k,v in self.engines.iteritems(): yield k,v

    def __getitem__(self, name):
        return self.engines[name]

    def __contains__(self, name):
        return name in self.engines

    def __len__(self, name):
        return len(self.engines)

    def register(self, requires, description):

        def dec(f):
            name = f.func_name
            self.engines.update({
              name : {
                'function':f,
                'description':description,
                'requires':requires
              }
            })
            return f

        return dec


registration = Registration()

