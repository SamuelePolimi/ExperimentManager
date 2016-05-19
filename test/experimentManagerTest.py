import unittest
import os
from core.ExperimentManager import ExperimentManager

class ExperimentManagerTest(unittest.TestCase):
    
    def checkCreateTest(self):
        manager = ExperimentManager()
        manager.createExperiment("experiment/experiment1", "Experiment1", "Test Experiment type 1")
        self.assertTrue(os.path.exists("experiment/experiment1"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/general.txt"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/experimentsTest.log"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/experimentsTag.log"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/experimentsComment.log"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/experimentsPostComment.log"))
        self.assertTrue(os.path.isfile("experiment/experiment1" + "/experimentsParams.log"))
        
        manager.newExperimentTest("Samuele",["prova","prova1"],["param1=alfa","param2=beta"],"prova esperimento")
        
        self.assertTrue(manager.n_experiments == 1)
        self.assertTrue(len(manager.log) == 1)
        self.assertTrue(len(manager.log[0].parameters) == 2)
        self.assertTrue(len(manager.log[0].tags) == 2)
        self.assertTrue(manager.log[0].number == 0)
        
        manager.newExperimentTest("Samuele",["prova","prova1","prova3"],["param1=alfa"],"prova esperimento")
        
        self.assertTrue(manager.n_experiments == 2)
        self.assertTrue(len(manager.log) == 2)
        self.assertTrue(len(manager.log[0].parameters) == 2)
        self.assertTrue(len(manager.log[0].tags) == 2)
        self.assertTrue(manager.log[0].number == 0)
        
        print manager.log[1]
        self.assertTrue(len(manager.log[1].parameters) == 1)
        self.assertTrue(len(manager.log[1].tags) == 3)
        self.assertTrue(manager.log[1].number == 1)
        
        
    def loadTest(self):
        manager = ExperimentManager()
        manager.loadExperiment("experiment/experiment1")
        
        self.assertTrue(manager.n_experiments == 2)
        self.assertTrue(len(manager.log) == 2)
        self.assertTrue(len(manager.log[0].parameters) == 2)
        self.assertTrue(len(manager.log[0].tags) == 2)
        self.assertTrue(manager.log[0].number == 0)
        
        self.assertTrue(len(manager.log[1].parameters) == 1)
        self.assertTrue(len(manager.log[1].tags) == 3)
        self.assertTrue(manager.log[1].number == 1)
        
        manager.printExperiment()
        
    def addCase(self):
        
        manager = ExperimentManager()
        manager.loadExperiment("experiment/experiment1")
        
        test = manager.openExperimentTest(1)
        test.addTestCase("mlp","finalPendulum",["regressor=mlp"],"Normal mlp")
        
        self.assertTrue( "mlp" in test.testCase)
        self.assertTrue(len(test.testCase["mlp"].params)==1, str(test.testCase["mlp"].params))
        self.assertTrue(test.testCase["mlp"].cmd == "finalPendulum")

        #def addTestCase(self, name, cmd, params, comment, verbose=True):

    def loadCase(self):

        manager = ExperimentManager()
        manager.loadExperiment("experiment/experiment1")
        
        test = manager.openExperimentTest(1)
        test.loadTestCases()
        
        self.assertTrue( "mlp" in test.testCase)
        self.assertTrue(len(test.testCase["mlp"].params)==1, str(test.testCase["mlp"].params))
        self.assertTrue(test.testCase["mlp"].cmd == "finalPendulum")
        
        
    def addCoding(self):
        manager = ExperimentManager()
        manager.loadExperiment("experiment/experiment1")
        manager.addCoding("n_neuron=10","small")
        self.assertTrue(manager.code(["n_neuron=10"])=="small")
        self.assertTrue(manager.decode(["small"])[0]=="n_neuron=10")
        #self.assertRaises(manager.addCoding("n_neuron=100","small"))
        #self.assertRaises(manager.addCoding("n_neuron=10","medium"))
        
    def afterAddCoding(self):
        manager = ExperimentManager()
        manager.loadExperiment("experiment/experiment1")
        self.assertTrue(manager.code(["n_neuron=10"])=="small")
        self.assertTrue(manager.decode(["small"])[0]=="n_neuron=10")
        #self.assertRaises(manager.addCoding("n_neuron=100","small"))
        #self.assertRaises(manager.addCoding("n_neuron=10","medium"))
        
    def test(self):
        
        self.checkCreateTest()
        self.loadTest()
        self.addCase()
        self.loadCase()
        self.addCoding()
        self.afterAddCoding()