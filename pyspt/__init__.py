# -*- coding: utf-8 -*-
"""
Python Signal Processing Toolbox

Python toolbox to visualize, analyze and manipulate digital signal. The primary 
focus is on a higher level of abstraction rather than performance aspects or 
even real time capability. 

@author: mguski@alaska.edu


"""

"""
TODOs:
 - apply python naming: ClassNames, function_names, CONSTANT_VALUES, modules, packages (PEP8 Style Guide for Python)
 
"""
 
print("callin PySPT.pyspt.__init__")



# import modules into pyspt namespace
from . import init_logging 
from .Signal import Signal
from .other_functions import *
from . import dsp
