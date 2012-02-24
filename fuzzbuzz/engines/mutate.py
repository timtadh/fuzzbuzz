#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from reg import registration

class NoExampleException(Exception):
    pass

@registration.register(
  {'example_list':'examples'},
  'Mutates the AST of the given example files s.t. conditions hold')
def mutation_fuzzer(rlexer, grammar, example_list=None):

    if not example_list:
        raise NoExampleException

    def generate_examples_ast():
        """Generates an AST for each example provided in `example_list`.
        This AST is parsed according to the grammar in `grammar`.
        On completion, this function returns a list of ASTs, corresponding
        to the examples provided.
        """
        ast_list = list()

        for example in example_list:
            ast_list.append(generate_ast(example))

        return ast_list

    def generate_ast(example):
        """Generates and returns an AST for the provided `example`
        AST generated according to the provided grammar
        On completion, returns an AST object.

        Arguments:
        - `example`: the text to be parsed into an AST
        """
        pass

    def generate_parser():
        """Generate a parser for our `example_list` based on the grammar in
        `grammar`. This is probably going to be very hacky.
        On completion this function returns a `parser` object which can be
        used to generate ASTs for our examples.
        """
        pass

    parser = generate_parser(grammar.start)
    generate_ast(example) # should be generate_ast(example, parser). I'll fix this.
    return output

