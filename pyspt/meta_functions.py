# -*- coding: utf-8 -*-
"""
Meta functions i.e. for text manupulation.

Created on Sun Nov 27 18:18:19 2016

@author: mguski
"""
import numpy as np

# meta functions
def num2string(value, numberFormat=":.2f"):
    """ Formater function to retun string with SI unit prefixes (kilo, Mega,...) """
    # TODO: extend for inputs: list, array,
    
    if np.isinf(value) or np.isnan(value) or value == 0:
        return str(value)
        
    try:
        unitPrefixes = 'afpnµm kMGTPE'
        prefixIdx = np.floor(np.log10(np.absolute(value)) / 3)
        prefix = unitPrefixes[int(prefixIdx)+6]
        multiplyFactor = 10 ** (-prefixIdx*3)
    
        if np.mod(value*multiplyFactor, 1) == 0:
            strTemplate = '{:.0f}{}'
        else:
            strTemplate = '{' + numberFormat + '}{}'
        outputStr = strTemplate.format(np.round(value*multiplyFactor*1.0e12)/1.0e12, prefix )
        return outputStr
    except:
        print("met_function.num2string: error for input value: {}".format(value))
        return 'num2string error'