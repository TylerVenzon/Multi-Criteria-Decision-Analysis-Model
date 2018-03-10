from src.mcda.equation.equation import Equation
from src.mcda.analysis.weightlist import WeightList

class LandUseEquation(Equation):
    
    def __init__(self):
        self.weight = WeightList.LAND_COVER
    
    def computeCriteriaWithoutWeight(self, values):
        return values.land_cover

    def computeCriteriaWithWeight(self, land_cover):
        return land_cover * self.weight