import csv
import os
from ExpMan.core.ExperimentSample import ExperimentSample

class ExperimentCase:

    def __init__(self, experiment, test, label, cmd, time, params, comment, close, valid):
        self.experiment = experiment
        self.test = test
        self.label = label
        self.time = time
        self.params = params
        self.comment = comment
        self.cmd = cmd
        self.close = close
        self.valid = valid
        self.samples = {}
        #TODO: implement
        #self.controlVariable
        
        
    def loadSamples(self):
        self.samples = {}
        #testCoded = open(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/testCoded.log","rb")
        #csvCode = csv.reader(testCoded)
        csvCode =  [ x for x in os.listdir(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label) if not "." in  x]
        #for each code_case
        for  code in csvCode:
            """try:
                code_next = csvCode.next()
            except:
                break"""
            
            #code is the actual code .. there will be a folder with that name
            """code = code_next[0]
            if len(code_next) > 1:
                for c in code_next[1:]:
                    code += "_" + c"""
                
            testParam = open(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/testParams" + code + ".log","rb")
            csvParam = csv.reader(testParam)
            
            testCommand = open(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/testCommands" + code + ".log","rb")
            
            #for each coded test
            while True:
                try:
                    param_next = csvParam.next()
                except:
                    break
                
                var_param = param_next[0]                                           # Param for generate different test
                closed = param_next[1]=="True"
                valid = param_next[2]=="True"
                error = param_next[3]=="True"
                time_start = param_next[4]
                time_end = param_next[5]
                duration = param_next[6]
                
                cmd = testCommand.readline()[0:-1].split(",")                
                #TODO: set params
                params = self.experiment.decode(code)
                
                #TODO: add closed and error
                if code in self.samples:
                    num = len(self.samples[code])
                    self.samples[code].append(ExperimentSample(self.experiment, self.test, self,code, num, time_start, time_end, duration, params, var_param, cmd, closed, valid, error))
                else:
                    self.samples[code] = [ExperimentSample(self.experiment, self.test, self,code,0, time_start, time_end, duration, params, var_param, cmd, closed, valid, error)]
                #def __init__(self, experiment, test, case, time_start, time_end, duration, params, var_param, cmd):
                
            testParam.close()
            testCommand.close()
            
        
    def getListOfCommandSamples(self):
        ret = []
        for sample_code in self.samples:
            for sample in self.samples[sample_code]:
                ret.append(sample.getCommandLine())
        return ret
        
    """All params here should be codificable
        var_param is the param wich make difference from a sample to another one (could be a dataset, or a random seed..)
        for example:
        params = ["n_neurons=10","n_layer=2"] 
        var_param = ["randomWeights1.txt"]        
    """
    def addSample(self, params, var_param):
        
        code = self.experiment.code(params)
        all_params =   self.params + params + [var_param]
        
        command = self.cmd +","
        for par in all_params[0:-1]:
            command += par + ","
        command += all_params[-1]
        
        
        if code in self.samples:
            num = len(self.samples[code])
            self.samples[code].append(ExperimentSample(self.experiment, self.test, self,code,num, "", "", "", params, var_param, command, False, True, False))
        else:
            self.samples[code] = [ExperimentSample(self.experiment, self.test, self,code,0, "", "", "", params, var_param, command, False, True, False)]
        #TODO: create dir code
        if not os.path.exists(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/" + code):
            os.makedirs(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/" + code)
        #TODO: retreive params from upper parts
            
        testParam = open(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/testParams" + code + ".log","a")
            
        testCommand = open(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label + "/testCommands" + code + ".log","a")
        
        #TODO: check
        testParam.write(var_param + "," +
                        str(False) + "," +
                        str(True) + "," + 
                        str(False) + "," +
                        "," +
                        "," + 
                        "\n")
        
        
        testCommand.write(command + "\n")
        
    
    def openSample(self, code, number):
        #TODO: check if is loaded
        return self.samples[code][int(number)]