import csv
from core.ExperimentSample import ExperimentSample

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
        testCoded = open(self.experiment.folder +"/test" + self.test.number + "/" + self.label + "/testCoded.log","rb")
        csvCode = csv.reader(testCoded)
        
        #for each code_case
        while True:
            try:
                code_next = csvCode.next()
            except:
                break
            
            #code is the actual code .. there will be a folder with that name
            code = code_next[0]
            for c in csvCode:
                code += "_" + c
                
            testParam = open(self.experiment.folder +"/test" + self.test.number + "/" + self.label + "/testParams" + code + ".log","rb")
            csvParam = csv.reader(testParam)
            
            testCommand = open(self.experiment.folder +"/test" + self.test.number + "/" + self.label + "/testCommands" + code + ".log","rb")
            
            #for each coded test
            while True:
                try:
                    param_next = csvParam.next()
                except:
                    break
                
                var_param = param_next[0]                                           # Param for generate different test
                closed = param_next[1]
                valid = param_next[2]
                error = param_next[3]
                time_start = param_next[4]
                time_end = param_next[5]
                duration = param_next[6]
                
                cmd = testCommand.readline()[0:-1]
                
                #TODO: set params
                params = []
                
                samples[code].append(ExperimentSample(self.experiment, self.test, self, time_start, time_end, duration, params, var_param, cmd))
                #def __init__(self, experiment, test, case, time_start, time_end, duration, params, var_param, cmd):
                
            
                
            
            
        
        
        
        pass
        
    def executeSample(self, id_):
        raise "Not Implemented yet"
        
    def executeSamlpes(self):
        raise "Not Implemented yet"
        
    def paramCoding(self):
        raise "Not Implemented yet"
        
    """All params here should be codificable
        var_param is the param wich make difference from a sample to another one (could be a dataset, or a random seed..)
        for example:
        params = ["n_neurons=10","n_layer=2"] 
        var_param = ["randomWeights1.txt"]        
    """
    def addSample(self, params, var_param):
        
        raise "Not Implemented yet"
    
        
    