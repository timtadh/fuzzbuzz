#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: John Gunderman
#Email: johngunderman@gmail.com
#For licensing see the LICENSE file in the top level directory.

from ply import yacc

from reg import registration
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

    lex = lexer()

    if not example_list:
        raise NoExampleException

    def generate_examples_ast(parser, example_list):
        """Generates an AST for each example provided in `example_list`.
        This AST is parsed according to the grammar in `grammar`.

        @param parser : The parser from which the ASTs will be generated from
        @param example_list : A list of example strings to be mutated
        @return list of ASTs, corresponding to the examples provided.
        """
        ast_list = list()

        for example in example_list:
            ast_list.append(generate_ast(example, parser))

        return ast_list

    def generate_ast(example, parser):
        """Generates and returns an AST for the provided `example`
        AST generated according to the provided grammar

        @param example : the text to be parsed into an AST
        @param parser  : the parser from which the ASTs will be generated from
        @return an AST object
        """
        print example
        parser.parse(example, lex)
        return example

    def generate_parser(grammar):
        """Generate a parser for our `example_list` based on the grammar in
        `grammar`. This is probably going to be very hacky.
        On completion this function returns a `parser` object which can be
        used to generate ASTs for our examples.

        @param grammar_start : The start symbol for the grammar we are to
                               generate a parser for
        """
        for sym in grammar.nonterminals.itervalues():
            for rule in sym.ply():
                print rule
                ParserGenerator.add_production(rule)

        return ParserGenerator(lexer.tokens)

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


    parser = generate_parser(grammar)
    ast_list = generate_examples_ast(parser, example_list)
    mutated_asts = mutate_all(ast_list)
    return mutated_asts


class ParserGenerator(object):
    """Generate a yacc (ply) parser for the given input strings
    """

    # production counter
    pcount = 0

    @classmethod
    def add_production(cls, prod_string):
        func = cls.ply_func_for(prod_string)
        prod_name = prod_string.split(' ')[0]
        func_name = 'p_' + prod_name + str(cls.pcount)
        cls.pcount += 1
        setattr(cls, func_name, func)

    @classmethod
    def ply_func_for(cls, docstring):
        """Returns an anonymous function which has the supplied docstring

        @param docstring : the docstring for the returned anonymous function
        @return an anonymous function
        """
        def ply_make_tree(t):
            """Where t is a production generated by ply, give t[0] a new node
            with child nodes t[1..n]

            @param t : (list) where t[0] is the left-hand side of the production
            generated by ply, and t[0..n] is the right-hand side.
            """
            # TODO: figure out what to label things
            label = ''
            n = Node(label)
            for x in xrange(1, len(t)):
                # TODO: figure out what tokens to ignore
                n.addkid(Node(label))
            t[0] = n

        f = lambda s, t : ply_make_tree(t)
        f.__doc__ = docstring
        return f

    def p_error(self, t):
        # TODO: we need a better exception framework
        print "Syntax error in input!"
        print t
        raise Exception

    def __new__(cls, tokens,  **kwargs):
        # get the tokens from the lexer into the scope of our parser.
        setattr(cls, 'tokens', tokens)
        self = super(ParserGenerator, cls).__new__(cls, **kwargs)
        self.yacc = yacc.yacc(module=self,  tabmodule="mutate_parser_tab", **kwargs)
        return self.yacc

