import os
import csv
import time
import datetime

from core.ExperimentTest import ExperimentTest

class ExperimentManager(object):

    def __init__(self):
        self.folder = None
        """self.log is a list of TestExperiment in this shape
        {number: , date-time:, author:, comment:, tag:[tag1, tag2 ..], done:False}
        """
        self.name = None
        self.info = None
        self.log = None
        self.n_experiments = None
        self.coder = {}
        self.decoder = {}
        
    """Create a new Experiment"""
    #TODO: remember to check if we are over writing something
    #TODO: remember to be verbose
    def createExperiment(self, folder, name, info,verbose=True):
        if not os.path.exists(folder):
            os.makedirs(folder)
        fout = open(folder + "/general.txt","w")
        fout.write(name +"\n")
        fout.write(info)
        fout.close()
        fout = open(folder + "/experimentsTest.log","w")
        fout.close()
        fout = open(folder + "/experimentsTag.log","w")
        fout.close()
        fout = open(folder + "/experimentsComment.log","w")
        fout.close()
        fout = open(folder + "/experimentsPostComment.log","w")
        fout.close()
        fout = open(folder + "/experimentsResults.log","w")
        fout.close()
        fout = open(folder + "/experimentsParams.log","w")
        fout.close()
        fout = open(folder + "/experimentsVariables.log","w")
        fout.close()
        fout = open(folder + "/experimentsCoding.log","w")
        fout.close()
        self.n_experiments = 0
        self.folder = folder
        self.name = name
        self.info = info
        self.log = []
        self.coder = {}
        self.decoder = {}
        
    """
    Load all the experiments
    """
    def loadExperiment(self, folder, verbose=True):
        if not os.path.isfile(folder + "/general.txt"):
            raise "Not a valid Experiment - general.txt missing"
        if not os.path.isfile(folder + "/experimentsTest.log"):
            raise "Not a valid Experiment - experimentsTest.log missing"  
        fin = open(folder + "/general.txt","r")
        linesIn = fin.readlines()
        fin.close()
        
        if len(linesIn) < 2:
            raise "Not a valid Experiment - general.txt not valid"
            
        self.name = linesIn[0]
        
        self.info = ""
        for row in linesIn[1:-1]:
            self.info += row
            
        if verbose:
            print("-"*10)
            print("Experiment: " +  self.name)
            print("Info: " +  self.info)
            print("-"*10)
            
        experimentsTest =  open(folder + "/experimentsTest.log", 'rb')
        experimentsParams = open(folder + "/experimentsParams.log", 'rb')
        experimentsResults = open(folder + "/experimentsResults.log", 'rb')
        experimentsTag = open(folder + "/experimentsTag.log", 'rb')
        experimentsComment = open(folder + "/experimentsComments.log", 'r')
        experimentsPostComment = open(folder + "/experimentsPostComments.log", 'r')
        
        csvTest = csv.reader(experimentsTest, delimiter=',')
        csvParams = csv.reader(experimentsParams, delimiter=',')
        csvResults = csv.reader(experimentsResults, delimiter=',')
        csvTag = csv.reader(experimentsTag, delimiter=',')
        
        #TODO: Check if the last line is empty, so -1 it is okay.     
        
        #assert len(csvTest)==len(csvParams) and len(csvParams)==len(csvResults) and len(csvResults)==len(csvTag), "File inconsistency between test, params, results, and tags"
        self.folder = folder
        self.n_experiments = 0
        self.log = []
        while True: 
            
            try:
                csvTest_next = csvTest.next()
                self.n_experiments += 1
            except:
                break
            
            csvParam_next = csvParams.next()
            csvResults_next = csvResults.next()
            csvTag_next = csvTag.next()
            
            assert len(csvTest_next)==4, "Error at line " + str(self.n_experiments) + " of experimentsTest.txt - " + str(csvTest_next)
            
            
            time = csvTest_next[0]
            user = csvTest_next[1]
            close = csvTest_next[2]
            valid = csvTest_next[3]
            
            tags = []
            for tag in csvTag_next:
                tags.append(tag)
            parameters = []
            for param in csvParam_next:
                parameters.append(param)
            comment = experimentsComment.readline()[0:-1]                       #Exclude the carriege return
            postComment = experimentsPostComment.readline()[0:-1]               #Exclude the carriege return 
            
            self.log.append(ExperimentTest(self, self.n_experiments-1, time, user, tags, parameters, comment, close, postComment, valid))
            
        experimentsTest.close()
        experimentsParams.close()
        experimentsComment.close()
        experimentsPostComment.close()
        experimentsTag.close()
        
        # ---------------------------------------------------------------------
        # Load variables section
        # ---------------------------------------------------------------------
        
        experimentsVariables = open(folder + "/experimentsVariables.log", 'rb')
        csvVariables = csv.reader(experimentsVariables)
        
        for variable in csvVariables:
            type_ = variable[0]
            dim = variable[1]
            name = variable[2]
            #TODO: implement variables
            
        # ---------------------------------------------------------------------
        # Load params coding section
        # ---------------------------------------------------------------------
            
        experimentsCoding = open(folder + "/experimentsCoding.log", 'rb')
        csvCoding = csv.reader(experimentsCoding)
        
        for coding in csvCoding:
            param = coding[0]
            code = coding[1]
            self.coder[param] = code
            self.decoder[code] = param
        
        if verbose:
            print("Number of ExperimentsTest loaded: " + str(self.n_experiments))
            print("-"*10)
            
            
    def addCoding(self, param, code):
        if '_' in code:
            raise "Code shouln't contain '_' character"
        experimentsCoding = open(self.folder + "/experimentsCoding.log", 'w')
        if(not param in self.coder and not code in self.decoder):
            experimentsCoding.write(param + "," + str(code) + "\n")
        else:
            raise "Param or code already present"
        self.coder[param] = code
        self.decoder[code] = param
        experimentsCoding.close()
        
        
    def addVariable(self, type_, dim, name):
        raise "Not Implemented yet"
    """newExperimentTest creates a new test. We can define parameters in common to all the testCases. 
    We can write a comment to explain something. Comment should be of one line
    """
    def newExperimentTest(self,user, tags, parameters, comment, verbose=True):
        
        assert self.name!=None, "No experiment loaded"
        assert user!=None and tags!=None and parameters!=None and comment!=None, "Set all parameters please" 
        assert not "\n" in comment, "Comment should be of one line only" 
        loc_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        ret = ExperimentTest(self, self.n_experiments, loc_time, user, tags, parameters, comment, False, "", True)
        
        experimentsTest =  open(self.folder + "/experimentsTest.log", 'a')
        experimentsParams = open(self.folder + "/experimentsParams.log", 'a')
        experimentsResults = open(self.folder + "/experimentsResults.log", 'a')
        experimentsTag = open(self.folder + "/experimentsTag.log", 'a')
        experimentsComment = open(self.folder + "/experimentsComments.log", 'a')
        experimentsPostComment = open(self.folder + "/experimentsPostComments.log", 'a')
        
        experimentsTest.write(str(ret.time) +"," + ret.user + "," + str(ret.close) + "," + str(ret.valid) + "\n")
        
        for param in parameters[0:-1]:
            experimentsParams.write(param + ",")
        experimentsParams.write(parameters[-1] + "\n")
        
        experimentsResults.write("None\n")
        
        for tag in tags[0:-1]:
            experimentsTag.write(tag + ",")
        experimentsTag.write(tags[-1] + "\n")
        
        experimentsComment.write(comment+"\n")
        
        experimentsPostComment.write("None\n")
        
        experimentsTest.close()
        experimentsParams.close()
        experimentsResults.close()
        experimentsTag.close()
        experimentsComment.close()
        experimentsPostComment.close()
        
        if not os.path.exists(self.folder + "/test" + str(self.n_experiments)):
            os.makedirs(self.folder+ "/test" + str(self.n_experiments))
            
        self.log.append(ret)
        
        self.n_experiments += 1
        #TODO: be verbose :)
            
        return ret
        
    #TODO: what to do is it is not valid?!
    def openExperimentTest(self, id_):
        return self.log[id_]
        
    def getFolder(self):
        return self.folder
        
    #TODO: do a nice print function (or better... a __str__)
    def printExperiment(self):
        for exp in self.log[0:1]:
            print exp
    
    """This function take the codificable params, and tranform it in a code
    """     
    def code(self, params):
        ret = ""
        for p in params[0,-1]:
            try:
                ret += self.coder[p] + "_"
            except:
                raise "Parameter not coded"
        try:
            ret += self.coder[params[-1]] 
        except:
            raise "Parameter not coded"
        return ret
        
    """This function take the code and transform it in params
    """     
    def decode(self, code):
        ret = []
        codes = code.split('_')
        for c in codes:
            try:
                ret.append(self.decoder[c])
            except:
                raise "Code not parametrizable"
        return ret