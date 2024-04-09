#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logs.logger import *

Logger.init("127.0.0.1", verbose=True, saveToFile=False)


####Setup the exception handler
from logs.utils.exceptions import ExceptionConfigurator, DEBUG_VERBOSE, DEBUG_TELEPLOT, DEBUG_NONE

ExceptionConfigurator.current_debug_level = DEBUG_VERBOSE