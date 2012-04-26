#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## We have to import all of our fuzzer modules otherwise they don't get
## registered. There is no way to work around this because the initialization
## code doesn't get run unless it is imported.
import attribute, mutate, cfgstats, stub, astgenerate
del attribute, mutate, cfgstats, stub

## Make registration available at the package level.
from reg import registration
