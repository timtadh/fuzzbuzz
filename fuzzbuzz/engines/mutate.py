#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from reg import registration

@registration.register(
  {'example_list':'examples'},
  'Mutates the AST of the given example files s.t. conditions hold')
def mutation_fuzzer(rlexer, grammar, example_list=None):
    print example_list

    
