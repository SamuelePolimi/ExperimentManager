import os.path
import csv
import ExpMan.utils.fileUpdater 

class ExperimentSample:
    
    def __init__(self, experiment, test, case, code, num, time_start, time_end, duration, params, var_param, cmd, close, valid, error):
        self.experiment = experiment
        self.test = test
        self.case = case
        self.time_start = time_start
        self.time_end = time_end
        self.duration = duration
        self.params = params
        self.var_param = var_param                                              # Special parameter that deserve to replicate an experiment with different data/seed
        self.cmd = cmd
        self.close = close
        self.valid = valid
        self.error = error
        self.variable = {}
        self.code = code
        self.num = num
        self.path = experiment.folder + "/test" + str(test.number) + "/" + case.label + "/" + code + "/" + str(num)
        
    def addVariableResults(self, name, result):
        if self.close:
            raise Exception("ExperimentSample Already close")
        if name in self.variable:
            raise Exception("Value for the variable already in.")
        if not name in self.experiment.variable:
            raise Exception("Variable not declared in the Experiment - Experiment>>add variable name type_ dim")
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        var_decl = self.experiment.variable[name]
        dim = var_decl.dim
        type_ = var_decl.type_
        
        if (dim==0 or dim=="0") and type_ == "single":
            var_file = open(self.path + "/" + name + ".log","w")
            var_file.write(str(result))
            var_file.close()
            
                
        if (dim==0 or dim=="0") and type_ == "history":
            var_file = open(self.path + "/" + name + ".log","w")
            for res in result[0:-1]:
                var_file.write(str(res) + ",")
            var_file.write(str(result[-1]) + "\n")
            var_file.close()
        
        self.variable[name] = result
        
    def addPlotFunction(self, function, n_dim, lower_shape, higher_shape):
        raise Exception("Not implemented yet")
      
    def closeSample(self):
        #def update(path, line_number, number_param, param):
        ExpMan.utils.fileUpdater.update(self.experiment.folder +"/test" + str(self.test.number) + "/" + self.case.label + "/testParams" + self.code + ".log",self.num,1,"True")
        self.close = True
        
    def load(self):
        for var in self.experiment.variable:
            
            dim = var.dim
            name = var.name
            type_ = var.type_
            
            if os.path.isfile(self.path + "/" + var.name + ".log"):
                
                if (dim==0 or dim=="0") and type_ == "single":
                    var_file = open(self.path + "/" + var.name + ".log","r")
                    val = var_file.readline()
                    val = float(val)
                    self.variable[var.name] = val
                    var_file.close()
                    continue
                
                if (dim==0 or dim=="0") and type_ == "history":
                    var_file = open(self.path + "/" + var.name + ".log","rb")
                    csvFile = csv.reader(var_file)
                    row = csvFile.next()
                    self.variable[name] = []
                    for val in row:
                        self.variable[name].append(val)
                    continue
        
    def getCommandLine(self,mOpt=True):
        """let's see if to keep python or not"""
        """folder = sys.argv[1]
        test = sys.argv[2]
        case = sys.argv[3]
        code = sys.argv[5]
        number = sys.argv[6]"""
        if(mOpt):
            return ["python","-m", self.cmd[0], self.experiment.folder , str(self.test.number), self.case.label,str(self.code), str(self.num), self.var_param] + self.params
        else:
            return ["python", self.cmd[0], self.experiment.folder , str(self.test.number), self.case.label,str(self.code), str(self.num), self.var_param] + self.params
            
        
    
        
    
        
        