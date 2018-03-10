from src.mcda.equation.equation import Equation
from src.mcda.analysis.weightlist import WeightList

class MaximumCoverageEquation(Equation):
    
    def __init__(self):
        self.weight = WeightList.MAXIMUM_COVERAGE
    
    def computeCriteriaWithoutWeight(self, values):
        return values.population
        #equation -> normalize -> weight

    def computeCriteriaWithWeight(self, population):
        return population * self.weight