#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import collections

def build_tree(gen):
    stack = list()
    root = None
    for children, sym in gen:
        if not sym.value: node = Node(sym.sym)
        else: node = Node(sym.value)
        if not root: root = node

        if stack:
            stack[-1]['node'].addkid(node)
            stack[-1]['children'] -= 1
            if stack[-1]['children'] <= 0:
                stack.pop()
        if children:
            stack.append({'node':node, 'children':children})
    return root

class Node(object):

    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else list()

    def addkid(self, node, before=False):
        if before:  self.children.insert(0, node)
        else:   self.children.append(node)
        return self

    def get(self, label):
        if self.label == label: return self
        for c in self.children:
            if label in c: return c.get(label)

    def iter(self):
        queue = collections.deque()
        queue.append(self)
        while len(queue) > 0:
            n = queue.popleft()
            for c in n.children: queue.append(c)
            yield n

    def __contains__(self, b):
        if isinstance(b, str) and self.label == b: return 1
        elif not isinstance(b, str) and self.label == b.label: return 1
        elif (isinstance(b, str) and self.label != b) or self.label != b.label:
            return sum(b in c for c in self.children)
        raise TypeError, "Object %s is not of type str or Node" % repr(b)

    def __eq__(self, b):
        if b is None: return False
        if not isinstance(b, Node):
            raise TypeError, "Must compare against type Node"
        return self.label == b.label

    def __ne__(self, b):
        return not self.__eq__(b)

    def __repr__(self):
        return super(Node, self).__repr__()[:-1] + " %s>" % str(self.label)

    def __str__(self):
        def string(s):
            if isinstance(s, Node): return str(s)
            return '0:%s' % str(s)
        s = "%d:%s" % (len(self.children), str(self.label))
        s = '\n'.join([s]+[string(c) for c in self.children])
        return s

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

