import os
import csv
import time
import datetime

from core.ExperimentCase import ExperimentCase

class ExperimentTest(object):
    
    def __init__(self, experiment, number, time, user, tags, parameters, comment, close, postComment, valid):
        self.experiment = experiment
        self.number = number
        self.time = time
        self.tags = tags
        self.parameters = parameters
        self.comment = comment
        self.close = close
        self.user = user
        self.valid = valid
        self.testCase = {}
        #TODO: implement
        #self.controlVariable
    
    def initialize(self):
        if os.path.isfile(self.experiment.folder + "/test" + str(self.number) + "/testCases.log"):
            raise "Folder already in use."
        open(self.experiment.folder + "/test" + str(self.number) + "/testCases.log").close()
        open(self.experiment.folder + "/test" + str(self.number) + "/params.log").close()
        open(self.experiment.folder + "/test" + str(self.number) + "/comments.log").close()
        open(self.experiment.folder + "/test" + str(self.number) + "/generalResults.log").close()
        
    def loadTestCases(self):
        
        testCases = open(self.experiment.folder + "/test" + str(self.number) + "/testCases.log", "rb")
        csvCases = csv.reader(testCases,delimiter=",")
        
        testParams = open(self.experiment.folder + "/test" + str(self.number) + "/testParams.log", "rb")
        csvParams = csv.reader(testParams,delimiter=",")
            
        testComments = open(self.experiment.folder + "/test" + str(self.number) + "/testComments.log", "r")
        
        while True:
            try:
                csvCases_next = csvCases.next()
            except:
                break
            
        
            csvParams_next = csvParams.next()
            
            name = csvCases_next[0]
            time_init = csvCases_next[1]
            cmd = csvCases_next[2]
            close = csvCases_next[3]
            valid = csvCases_next[4]
            
            params = []
            for param in csvParams_next:
                params.append(param)
                
            comment = testComments.readline()[0:-1]
            
            testCase = ExperimentCase(self.experiment, self, name, cmd, time_init, params, comment ,close,valid)
            #def __init__(self, experiment, test, label, cmd, time, params, comment, close, valid):
            self.testCase[name] = testCase
        
        testCases.close()
        testParams.close()
        testComments.close()
            
    #TODO: what to do if the case is not Valid?!
    def openTestCase(self,name):
        return self.testCase[name]
        
    def addTestCase(self, name, cmd, params, comment):
        #def __init__(self, experiment, test, label, cmd, time, params, comment, close, valid):
        
        loc_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        if name in self.testCase:
            raise "TestCase already exist in this Test"
        
        testCases = open(self.experiment.folder + "/test" + str(self.number) + "/testCases.log", "a")
        testCases.write(name + "," + str(loc_time) + "," + cmd + "," + str(False) + "," + str(True) + "\n")
        testCases.close()
        
        testComments = open(self.experiment.folder + "/test" + str(self.number) + "/testComments.log", "a")
        testComments.write(comment + "\n")
        testComments.close()
        
        testParams = open(self.experiment.folder + "/test" + str(self.number) + "/testParams.log", "a")
        for param in params[0:-1]:
            testParams.write(params + ",")
        testParams.write(params[-1] + "\n")
        testComments.close()
        
        if not os.path.exists(self.experiment.folder + "/test" + str(self.number) + "/" + name):
            os.makedirs(self.experiment.folder+ "/test" + str(self.number)+ "/" + name)
        else:
            #TODO: uncomment raise
            pass
            #raise "Impossible to overwrite a Case experiment"
            
        self.testCase[name] = ExperimentCase(self.experiment, self, name, cmd, loc_time, params, comment, False, True)
        
        #TODO: be verbose :)
        
    def close(self, results):
        raise "Not implemented yet"
        
    def modifyComment(self, comment):
        raise "Not implemented yet"
		
    def modifyPostComment(self, postComment):
        raise "Not implemented yet"
    
    def reload_(self, comment):
        raise "Not implemented yet"
    
    def addTag(self, tag):
        raise "Not implemented yet"
    
    def removeTag(self, tag):
        raise "Not implemented yet"
        
    def unvalidate(self):
        raise "Not implemented yet"
        
    def __str__(self):
        return ("N" + str(self.number) + ": " +  self.user + " " + self.time + " "
                    +  self.comment + " closed:" + str(self.close) + (""  if self.valid else " valid:False")
                    + "\n\t params: " + str(self.parameters)
                    )
        
        
    