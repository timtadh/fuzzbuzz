#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import collections, math

def build_tree(gen):
    stack = list()
    root = None
    for children, sym in gen:
        node = Node(sym)
        if not root:
            root = node
        if stack:
            stack[-1]['node'].addkid(node)
            stack[-1]['children'] -= 1
            if stack[-1]['children'] <= 0:
                stack.pop()
        if children:
            stack.append({'node':node, 'children':children})
    if stack:
        raise SyntaxError, 'Malformed input'
    return root

class Node(object):

    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else list()

    def addkid(self, node, before=False):
        if before:  self.children.insert(0, node)
        else:   self.children.append(node)
        return self

    def __iter__(self):
        queue = collections.deque()
        queue.append(self)
        while len(queue) > 0:
            n = queue.popleft()
            for c in n.children: queue.append(c)
            yield n

    def __repr__(self):
        return super(Node, self).__repr__()[:-1] + " %s>" % str(self.label)

    def __str__(self):
        def leaf(node):
            if hasattr(node, 'children'):
                return not bool(len(node.children))
            else:
                return False
        def walk(node):
            stack = list()
            stack.append((node, 0))
            while stack:
                n, j = stack.pop()
                if j == 0: yield len(n.children), n
                for i, kid in list(enumerate(n.children))[j:]:
                    if leaf(kid):
                        yield 0, kid
                    else:
                        stack.append((n, i+1))
                        stack.append((kid, 0))
                        break
        def string(nkids,node):
            if isinstance(node, Node): return '%d:%s' % (nkids, node.label)
            return ('%d:%s' % (nkids, node)).replace('\n', '\\n')
        return '\n'.join(string(d,n) for d,n in walk(self))

    def dotty(self):
        def string(s):
            if isinstance(s, Node): return str(s.label)
            return str(s)
        node = '%(name)s [shape=rect, label="%(label)s"];'
        leaf = '%(name)s [shape=rect, label="%(label)s" style="filled" fillcolor="#dddddd"];'
        edge = '%s -> %s;'
        nodes = list()
        edges = list()

        i = 0
        queue = collections.deque()
        queue.append((i, self))
        i += 1
        while len(queue) > 0:
            c, n = queue.popleft()
            name = 'n%d' % c
            label = string(n)
            if not hasattr(n, 'children'): nodes.append(leaf % locals())
            elif not n.children: nodes.append(leaf % locals())
            else: nodes.append(node % locals())
            if not hasattr(n, 'children'): continue
            for c in n.children:
                edges.append(edge % (name, ('n%d' % i)))
                queue.append((i, c))
                i += 1
        return 'digraph G {\n' + '\n'.join(nodes) + '\n' + '\n'.join(edges) + '\n}\n'
