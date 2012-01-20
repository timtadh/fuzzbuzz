#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import abc

class Executable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def execute(self, objs): pass

class Any(Executable): pass
class All(Executable): pass

