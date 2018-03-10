from src.mcda.equation.equation import Equation
from src.mcda.analysis.weightlist import WeightList

class AppropriateTravelDistanceEquation(Equation):
    
    def __init__(self):
        self.weight = WeightList.APPROPRIATE_TRAVEL_DISTANCE
    
    def computeCriteriaWithoutWeight(self, values):
        return values.road_networks

    def computeCriteriaWithWeight(self, road_distance):
        return road_distance * self.weight
    
    
    
    
    