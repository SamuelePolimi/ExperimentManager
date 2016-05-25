# -*- coding: utf-8 -*-
"""
Performer example

"""

import sys
from ExpMan.core.ExperimentManager import ExperimentManager

def retreiveParams():
    global folder,test,case,code, number
    if len(sys.argv) < 6:
        raise "Number of parameters not sufficient"
    folder = sys.argv[1]
    test = int(sys.argv[2])
    case = sys.argv[3]
    code = sys.argv[4]
    number = int(sys.argv[5])
    
    for arg in sys.argv[6:]:
        s = arg.split("=")    
        name = s[0]
        value = s[1]
        try:
            if "." in value:
                globals()[name] = float(value)
            else:
                globals()[name] = int(value)
        except:
            globals()[name] = str(value)
            
def loadSample():
    global folder, test, case, code, number, expSample
    man = ExperimentManager()
    man.loadExperiment(folder, verbose=False)
    expTest = man.openExperimentTest(test)
    expTest.loadTestCases()
    expCase = expTest.openTestCase(case)
    expCase.loadSamples()
    expSample = expCase.openSample(code, number)
    
retreiveParams()
loadSample()
expSample.addVariableResults("var1",str(n_hidden))


    

    
    
            
    
    
