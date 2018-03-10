from src.mcda.equation.equation import Equation
from src.mcda.analysis.weightlist import WeightList

class AccessibilityEquation(Equation):
    
    def __init__(self):
        self.weight = WeightList.ACCESSIBILITY
    
    
    def computeCriteriaWithoutWeight(self, values):
        return values.road_networks

    def computeCriteriaWithWeight(self, road_networks):
        return road_networks * self.weight