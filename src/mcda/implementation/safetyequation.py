from src.mcda.equation.equation import Equation
from src.mcda.analysis.weightlist import WeightList

class SafetyEquation(Equation):
    
    def __init__(self):
        self.weight = WeightList.SAFETY
    
    def computeCriteriaWithoutWeight(self, flood_hazard_level, land_elevation):
        result = (3 * flood_hazard_level + land_elevation)/4
        return result
    
    def computeCriteriaWithWeight(self, flood_hazard_level, land_elevation):
        result = (3 * flood_hazard_level + land_elevation)/4
        result *= self.weight
        return result
    
    
    
