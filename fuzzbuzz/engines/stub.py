#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from reg import registration

@registration.register(
  {'stat_tables':'tables', 'example_list':'examples'},
  'A test fuzzer for the engine decl syntax')
def stub(rlexer, grammar, stat_tables=None, example_list=None):
    print stat_tables, example_list
    return list(), None
