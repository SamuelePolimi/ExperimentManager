import csv
import os
import numpy as np
import ExpMan.utils.samplePlotter as plotter

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
        self.path = self.experiment.folder +"/test" + str(self.test.number) + "/" + self.label
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
                    sam = ExperimentSample(self.experiment, self.test, self,code, num, time_start, time_end, duration, params, var_param, cmd, closed, valid, error)
                    sam.load()
                    self.samples[code].append(sam)
                else:
                    sam = ExperimentSample(self.experiment, self.test, self,code,0, time_start, time_end, duration, params, var_param, cmd, closed, valid, error)
                    sam.load()
                    self.samples[code] = [sam]
                #def __init__(self, experiment, test, case, time_start, time_end, duration, params, var_param, cmd):
                
            testParam.close()
            testCommand.close()
            
            
        
    def getListOfCommandSamples(self):
        ret = []
        for sample_code in self.samples:
            for sample in self.samples[sample_code]:
                ret.append(sample.getCommandLine())
        return ret
    
    def getMean(self, code, var_name):
        if not var_name in self.experiment.variable:
            raise Exception("Variable not declared in the Experiment - Experiment>>add variable name type_ dim")
        
        var_decl = self.experiment.variable[var_name]
        dim = var_decl.dim
        type_ = var_decl.type_
        
        
        if (dim==0 or dim=="0") and type_ == "history":
            samples = []
            for sample in self.samples[code]:
                samples.append(sample.variable[var_name].tolist())
            samples_mat = np.array(samples)
            return np.mean(samples_mat, axis=0)
        
    def plotVariable(self, code, var_name):
        res = self.getMean(code, var_name)
        res_std = self.getStd(code, var_name)
        var_decl = self.experiment.variable[var_name]
        dim = var_decl.dim
        type_ = var_decl.type_
        if (dim==0 or dim=="0") and type_ == "history":
            plotter.oneDimPlot(res.tolist(),self.path + "/" + var_name + ".jpg",var_name,"n_iteration", var_name, (np.min(res-res_std)*1.1,np.max(res+res_std)*1.1), std=res_std)
        
    def getStd(self, code, var_name):
        if not var_name in self.experiment.variable:
            raise Exception("Variable not declared in the Experiment - Experiment>>add variable name type_ dim")
            
        var_decl = self.experiment.variable[var_name]
        dim = var_decl.dim
        type_ = var_decl.type_
        
        if (dim==0 or dim=="0") and type_ == "history":
            samples = []
            for sample in self.samples[code]:
                samples.append(sample.variable[var_name])
            samples_mat = np.array(samples)
            return np.std(samples_mat, axis=0)
            
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