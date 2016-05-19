class ExperimentSample:
    
    def __init__(self, experiment, test, case, time_start, time_end, duration, params, var_param, cmd):
        self.experiment = experiment
        self.test = test
        self.case = case
        self.time_start = time_start
        self.time_end = time_end
        self.duration = duration
        self.params = params
        self.var_param = var_param                                              # Special parameter that deserve to replicate an experiment with different data/seed
        self.cmd = cmd
        
        
    
        
        