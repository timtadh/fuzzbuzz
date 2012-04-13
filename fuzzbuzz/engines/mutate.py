#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: John Gunderman
#Email: johngunderman@gmail.com
#For licensing see the LICENSE file in the top level directory.

from ply import yacc

from reg import registration
from astgenerate import ast_generator
from fuzzbuzz.models.symbols import Terminal, NonTerminal
from fuzzbuzz.frontend.lexer import tokens, Lexer
from fuzzbuzz.frontend.ast   import Node

class NoExampleException(Exception):
    pass

@registration.register(
  {'example_list':'examples',
   'lexer':'lexer_class'},
  'Mutates the AST of the given example files s.t. conditions hold')
def mutation_fuzzer(rlexer, grammar, example_list=None, lexer=None):

    if not lexer:
        return None, 'Mutation Fuzzer requires a lexer'
    if not example_list:
        return None, 'Mutation Fuzzer requires at least one example'


    def mutate(ast):
        """Mutate a singular AST and return the resultant AST

        @param ast : the AST which we will mutate
        """
        return ast


    def mutate_all(ast_list):
        """Takes in a list of AST and mutates them, returning a list of each
        AST in mutated form.

        @param ast_list : a list of ASTs to be mutated. See frontent/ast.py
        """
        mutated_list = list()
        for ast in ast_list:
            mutated_list.append(mutate(ast))
        return mutated_list


    ast_list, _ = ast_generator(rlexer, grammar, example_list, lexer);
    mutated_asts = mutate_all(ast_list)
    return mutated_asts, None
