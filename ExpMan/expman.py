#!/usr/bin/python
from ExpMan.core.ExperimentManager import ExperimentManager
import readline

readline.read_history_file(".history")
manager_obj = ExperimentManager()

actual = "start"

actualOut = ">"

obj = {"start":manager_obj, "manager":manager_obj}
help_ = {}
cmd = {}

def checkIsParam(param, throw=False):
    if not "=" in param:
        if throw:
            raise Exception("Param must be in the shape <name>=<value>")
        else:
            print "Param must be in the shape <name>=<value>"
            return False
    if "," in param:
        if throw:
            raise Exception("Param must not contain commas or underscores")
        else:
            print "Param must not contain commas or underscores"
            return False
    return True
    
def getParamList():
    print "Insert one parameter per line; type exit for exit"
    params_ = []
    param = ""
    while True:
        param = raw_input (">> ")
        if param == "exit":
            break
        if not checkIsParam(param):
            continue
        params_.append(param)
    if len(params_)==0:
        params_.append("None")
    return params_

def getTagList():
    print "Insert one tag per line; type exit for exit"
    tags = []
    tag = ""
    while True:
        tag = raw_input (">> ")
        if tag == "exit":
            break
        tags.append(tag)
    if len(tags)==0:
        tags_.append("None")
    return tags
    
def getComment():
    print "Insert a comment and type then Enter."
    comment = raw_input (">> ")
    return comment

    
#-----------------------------------------------------------------------------
# Method section
#-----------------------------------------------------------------------------
def createExperiment(params):
    global actual, actualOut
    if actual!="start":
        raise Exception("Not in the right context")
    if len(params)<2:
        raise Exception("Incorrect number of parameters")
    manager_obj.createExperiment(params[0], params[1], "None")
    actualOut = params[1] + ">"
    actual = "manager"
    

def loadExperiment(params):
    global actual, actualOut
    if actual!="start":
        raise Exception("Not in the right context")
    if len(params)==0:
        manager_obj.loadExperiment("")
    else:
        manager_obj.loadExperiment(params[0])
    actual = "manager"
    actualOut = manager_obj.name + ">"
   
def newTest(params):
    global actual, actualOut,obj
    if actual!="manager":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    
    params = getParamList()
    tags = getTagList()
    comment = getComment()
    
    test = manager_obj.newExperimentTest(params[0], tags, params,comment)
    
    actualOut = manager_obj.name + ">test" + str(test.number) + ">"
    actual = "test"
    obj["test"] = test

def createCase(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
    if len(params)<2:
        raise Exception("Incorrect number of parameters")
    test = obj["test"]
    #TODO: param[1] to check
    params_ = getParamList()
    comment = getComment()
    
    case = test.addTestCase(params[0], params[1], params_, comment)
    #addTestCase(self, name, cmd, params, comment)
    
    actualOut = manager_obj.name + ">test" + str(test.number) + ">" +  params[0] + ">"
    actual = "case"
    obj["case"] = case
    
def openCase(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    test = obj["test"]
    
    case = test.openTestCase(params[0])
    case.loadSamples()
    #addTestCase(self, name, cmd, params, comment)
    
    actualOut = manager_obj.name + ">test" + str(test.number) + ">" +  params[0] + ">"
    actual = "case"
    obj["case"] = case
    
def openTest(params):
    global actual, actualOut,obj
    if actual!="manager":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    manager = obj["manager"]
    
    test = manager.openExperimentTest(int(params[0]))
    test.loadTestCases()
    
    actualOut = manager_obj.name + ">test" + str(test.number) + ">"
    actual = "test"
    obj["test"] = test
        

def showLast(params):
    global actual, actualOut,obj
    if actual!="manager":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    manager = obj["manager"]
    n = len(manager.validLog) - int(params[0])
    if n< 0 or int(params[0])<=0: 
        n = 0
    test = manager.validLog[n:]
    
    for t in test:
        print t.shortInfo()
        print "-"*50
        
def createSample(params):
    global actual, actualOut,obj
    if actual!="case":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    case = obj["case"]
    params_ = getParamList()
    case.addSample(params_, params[0])
    
    print "Sample added"
    
def plotVar(params):
    global actual, actualOut,obj
    if actual!="case":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    case = obj["case"]
    case.plotVariable(params[0], params[1])
    
def plotTestVar(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
    if len(params)<1:
        raise Exception("Incorrect number of parameters")
    case = obj["test"]
    case.plotVariable(params[0], params[1])
    
def testInfo(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
    print(obj["test"])
    
def addCoding(params):
    global actual, actualOut,obj
    if actual!="manager":
        raise Exception("Not in the right context")
    if len(params)<2:
        raise Exception("Incorrect number of parameters")
    checkIsParam(params[0],throw=True)
    obj["manager"].addCoding(params[0], params[1])
    #addCoding(param, code)
    
    print "Coding inserted"

def addVariable(params):
    global actual, actualOut,obj
    if actual!="manager":
        raise Exception("Not in the right context")
    if len(params)<3:
        raise Exception("Incorrect number of parameters")
        #TODO: check on params[0]
    obj["manager"].addVariable(params[0], params[1], params[2])
    #addVariable(self, type_, dim, name)
    
    print "Variable inserted"
    
def execute(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
    if len(params)<2:
        raise Exception("Incorrect number of parameters")
        #TODO: check on params[0]
    print "Executing.."
    obj["test"].execute(int(params[0]), float(params[1]))
    #execute(n_thread, refresh_time)

    
def unvalidate(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
        #TODO: check on params[0]
    obj["test"].unvalidate()
    print("Test not valid anymore")
    #execute(n_thread, refresh_time)
    
def postComment(params):
    global actual, actualOut,obj
    if actual!="test":
        raise Exception("Not in the right context")
        #TODO: check on params[0]
    comment = raw_input("Insert the comment: ")
    obj["test"].modifyPostComment(comment)
    #execute(n_thread, refresh_time)
    
cmd["start"] = {"create":createExperiment, "load":loadExperiment}
cmd["manager"] = {"newtest":newTest, "opentest":openTest, "showlast":showLast, "addcoding":addCoding, "addvariable":addVariable}
cmd["test"] = {"newcase":createCase, "opencase":openCase, "execute":execute,"plotvar":plotTestVar, "info":testInfo, "unvalidate":unvalidate, "postcomment":postComment}
cmd["case"] = {"newsample":createSample,"plotvar":plotVar}

#------------------------------------------------------------------------------
# Help section
#------------------------------------------------------------------------------

help_["start"] = {
"create":"""create <folder> <name>
<folder>: where to instantiate the new Experiment folder
<name>: name of the experiment""",
"load":"""load <folder>
<folder> where to retreive the Experiment"""
}
help_["manager"] = {
"newtest":"""newtest <user>
<user> the name of who is performing the test""",
"opentest":"""opentest <number>
<number> the reference number of the test""",
"showlast":"""showlast <number>
<number> show the last <number>^th of test made. If <number> = 0, it will be shown all the test made.""",
"addcoding":"""addcoding <param> <code>
<param> parameter and value in the shape <param_name>=<value_name>
<code> a new code for this parameter""",
"addvariable":"""addVariable <type> <dim> <name>
<type> 'history': means that the value changes during the performing of the test
       'single': means that the value is only one
<dim> 0: a single point
      1: 1D function
      2: 2D function
<name> name of the variable"""
}
help_["test"] = {
"newcase":"""newcase <name> <cmd>
<name> name of the test-case
<cmd> name of the program that runs it""",
"opencase":"""opencase <name>
<name> name of the test-case""", 
"execute":"""execute <thread-number> <refresh-time>
<thread-number> number of thread to run (better to set = nCORE)
<refresh-time> time in seconds to check if is possible to run a new test. A good value could be between 0.1 and 0.5""",
"plotvar":"""plotvar <code> <var_name>
<code> code of the sample set
<var_name> name of the variable you want to plot""",
"info":"""info
get the test's info""",
"unvalidate":"""unvalidate
makes the test not visible anymore (but you can always recover it)""",
"postcomment":"""postcomment
give a comment after the results of the test"""}
help_["case"] = {
"newsample":"""newsample <param>
<param> The param that vary for this sample. Param is in the shape <name>=<value>""",
"plotvar":"""plotvar <code> <var_name>
<code> code of the sample set
<var_name> name of the variable you want to plot"""}
help_["general"] = {
"help":"""help [<command>]
<command> It will show how to use that command.
If no parameter is passed, then it will show the list of possible commands inserted the current context.""",
"exit":"It will return to the command line.",
 "up":"""It will go to the upper mode Eg:
 Exp1>test0>up
 Exp1>"""
 }

print """ExpMan 1.0.0
Type help to discover which command you can prompt.
"""

while True:
    readline.write_history_file(".history")
    comand = raw_input(actualOut)
    cmds_ = comand.split(" ")
    cmds = [x for x in cmds_ if x !=""]
    
    if(len(cmds)==0):
        continue
    if cmds[0]=="exit":
        break
    if cmds[0]=="help":
        if(len(cmds)>1):
            if cmds[1] in help_[actual]:
                print help_[actual][cmds[1]]
            elif cmds[1] in help_["general"]:
                print help_["general"][cmds[1]]
            else:
                print "Command name not found"
        else:
            for h in help_[actual]:
                print h
            for h in help_["general"]:
                print h
        continue
    
    if cmds[0]=="up":
        if actual=="manager":
            actual="start"
            actualOut = ">"
        elif actual=="test":
            actual="manager"
            actualOut = obj["manager"].name + ">"
        elif actual=="case":
            actual="test"
            actualOut = obj["manager"].name + ">test" + str(obj["test"].number) + ">"
        continue
    if not cmds[0] in cmd[actual]:
        print "Unknown command. For more details type help"
        continue
    try:
        cmd[actual][cmds[0]](cmds[1:])
    except Exception as inst:
        print inst.args[0]