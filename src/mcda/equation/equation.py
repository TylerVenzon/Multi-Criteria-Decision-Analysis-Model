import abc

class Equation:
    
    _metaclass_= abc.ABCMeta
    
    weight = 0
    result = 0
    
    def __init__(self):
        self.result = -999
        self.weight = -999
    
    #    May not be needed. instance.weight
    def getWeight(self):
        return self.weight
    
    def setWeight(self, newWeight):
        self.weight = newWeight
    
    
    @abc.abstractmethod
    def computeCriteriaWithoutWeight(self, values):
        return

    def computeCriteria(self, values):
        self.result = self.computeCriteriaWithoutWeight(self, values) * self.weight
        return self.result
    
    def getResult(self):
        return self.result
    