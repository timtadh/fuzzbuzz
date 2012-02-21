#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from attribute import fuzz as attr_fuzz

def stub(rlexer, grammar, stat_tables=None, example_list=None):
    print stat_tables, example_list
    return list()

fuzzers = {
  'attribute_fuzzer':{
    'function':attr_fuzz,
    'description':'Generates strings from an attribute grammar st. conditions hold',
    'requires':dict()
  },
  'stub':{
    'function':stub,
    'description':'A test fuzzer for the engine decl syntax',
    'requires':{'stat_tables':'tables', 'example_list':'examples'}
  }
}
