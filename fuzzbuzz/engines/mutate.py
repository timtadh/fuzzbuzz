#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: John Gunderman
#Email: johngunderman@gmail.com
#For licensing see the LICENSE file in the top level directory.

import random
from ply import yacc

from reg import registration
from astgenerate import ast_generator
from attribute import attribute_fuzzer
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
        node = select_mutation_subtree(ast)
        mutate_subtree(node)
        return ast

    def select_mutation_subtree(ast):
        """Chooses a subtree from the ast

        @param ast : The ast from which we will choose
        @return : the root node of the subtree
        """
        # There's tons of ways to do this. Current way weights all
        # nodes equally, instead of giving more precedence to
        # nonterminals or higher precedence to larger branches of the
        # tree
        nodes = []
        for node in ast:
            nodes.append(node)

        return random.choice(nodes)

    def mutate_subtree(node):
        """Takes in an ast node (see ast.py) and manipulates it according to `grammar`
        We don't return anything here. The node object will be modified, leading to
        a change in the state of the AST int belongs to

        @param node : the node to be mutated.
        """
        print "Node to be mutated: "
        print node
        print "*******"

        # As with select_mutation_subtree, this function has many potential
        # implementations. A simple on is included for now. In the future,
        # this will become more moduler, and the user will be able to set a
        # function of their choice as the mutator or selector.

        # TODO: please implement me!
        # g = grammar
        # import pdb
        # pdb.set_trace()

        # check if we have a nonterminal or a terminal to mutate
        if node.label in grammar.nonterminals:
            nonterm = grammar.nonterminals[node.label]

            # Choose what to generate. This should eventually be made more complicated,
            # perhaps using Rafael's code.
            rule = random.choice(nonterm.rules)

            for sym, cnt in rule.pattern:
                if hasattr(sym, 'name'):
                    new_node = Node(sym.name)
                    mutate_subtree(new_node)
                    node.addkid(new_node)

        else:
            name = node.label.split(':')[0]
            if name in rlexer:
                value = rlexer[name]()
                new_name = [name, value]
                node.label = ":".join(new_name)
            else:
                print "Something terrible must have happened!"
                print new_name


    def mutate_all(ast_list):
        """Takes in a list of AST and mutates them, returning a list of each
        AST in mutated form.

        @param ast_list : a list of ASTs to be mutated. See frontent/ast.py
        """
        mutated_list = list()
        for ast in ast_list:
            mutated_list.append(ast_to_str(mutate(ast)))
        return mutated_list

    def ast_to_str(ast):
        """Takes an AST and returns the string represented by that AST

        @param ast : the root node of the ast to be transformed into a string
        """
        # Super hacky, but I'll move it to ast.py / fix it up when I have more time
        # (aka it may be a while)
        out = ""
        block = str(ast).split('\n')

        for line in block:
            chunks = line.split(':')
            #  we have a leaf node
            if chunks[0] == '0':
                if chunks[-1] == "\\n":
                    out += "\n"
                else:
                    out += chunks[-1]
                    out += " "

        return out


    ast_list, _ = ast_generator(rlexer, grammar, example_list, lexer);
    mutated_asts = mutate_all(ast_list)
    return mutated_asts, None
