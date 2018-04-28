from src.mcda.implementation.accessibilityequation import AccessibilityEquation
from src.mcda.implementation.appropriatetraveldistanceequation import AppropriateTravelDistanceEquation
from src.mcda.implementation.landusequation import LandUseEquation
from src.mcda.implementation.maximumcoveragequation import MaximumCoverageEquation
from src.mcda.implementation.safetyequation import SafetyEquation

import numpy as np




class Optimizer:
    
    SAFE_INDEX = 5
    LOW_HAZARD_INDEX = 4
    MEDIUM_HAZARD_INDEX = 3
    HIGH_HAZARD_INDEX = 2
    UNSAFE_INDEX = 1
    
    SAFE_THRESHOLD = 3
    LOW_HAZARD_THRESHOLD = 2
    MEDIUM_HAZARD_THRESHOLD = 1
    HIGH_HAZARD_THRESHOLD = 0
    UNSAFE_THRESHOLD = -1
    
    safeValues = []
    lowHazardValues = []
    mediumHazardValues = []
    highHazardValues = []
    
    safeEquationResults = []
    lowHazardEquationResults = []
    mediumHazardEquationResults = []
    highHazardEquationResults = []
    
    DIVISIONS = 3
    
    ROAD_NETWORK_BIN = []
    ROAD_DISTANCE_BIN = []
    POP_PERCENTAGE_BIN = []
    
    def __init__(self, roadNetwork, roadDistance, popPercentage):
        #Values of factors according to the table 
        #self.safeValues = [2, 3, 2, 8, 30, .20]       
        #self.lowHazardValues = [1, 2, 1, 5, 30, .10]
        #self.mediumHazardValues = [1, 2, 1, 2, 60, .10]
        #self.highHazardValues = [1, 2, 1, 1, 60, .5]
        
        #SafeValue:
        #flood hazard level >= 2; E1
        #land elevation > 2; E1
        #land cover >= 2; E2
        #road networks >= 8; E3
        #time <= 30 minutes
        #population >= 20%
        
        #get the equal interval differences based on min-max values of each map.
        roadNetwork = list(map(float, roadNetwork))
        roadDistance = list(map(float, roadDistance))
        popPercentage = list(map(float, popPercentage))

        self.ROAD_NETWORK_BIN,self.ROAD_DISTANCE_BIN,self.POP_PERCENTAGE_BIN = \
            self.getBinsOf(roadNetwork, roadDistance, popPercentage, self.DIVISIONS)
    
        '''
        Ideal setup of each evacuation center. Basis for a score that will be 
        used for checking other possible ideal evacuation areas. 
        
        '''
        # TODO: make this so that it is easy to change.
        self.safeValues = [3, 3, 3, 171, 334.5, 0.0002175]       
        self.lowHazardValues = [3, 3, 2, 114, 334.5, 0.000145]
        self.mediumHazardValues = [2, 2, 2, 57, 446, 0.000145]
        self.highHazardValues = [2, 2, 1, 57, 446, 0.0000725]
        
        self.safeValues = self.prepValues(self.safeValues)
        self.lowHazardValues = self.prepValues(self.lowHazardValues)
        self.mediumHazardValues = self.prepValues(self.mediumHazardValues)
        self.highHazardValues = self.prepValues(self.highHazardValues)
        
        self.safeEquationResults = self.computeEquations(self.safeValues)
        self.lowHazardEquationResults = self.computeEquations(self.lowHazardValues)
        self.mediumHazardEquationResults = self.computeEquations(self.mediumHazardValues)
        self.highHazardEquationResults = self.computeEquations(self.highHazardValues)
                       
        self.SAFE_THRESHOLD = self.computeScore(self.safeEquationResults)
        self.LOW_HAZARD_THRESHOLD = self.computeScore(self.lowHazardEquationResults)
        self.MEDIUM_HAZARD_THRESHOLD = self.computeScore(self.mediumHazardEquationResults)
        self.HIGH_HAZARD_THRESHOLD = self.computeScore(self.highHazardEquationResults)

    def prepValues(self, listValues):
        listValues[3] = self.binValue(listValues[3], self.ROAD_NETWORK_BIN, False)
        listValues[4] = self.binValue(listValues[4], self.ROAD_DISTANCE_BIN, True)
        listValues[5] = self.binValue(listValues[5], self.POP_PERCENTAGE_BIN, False)
        return listValues
    
    def getBinsOf(self, rn, rd, pop, divisions=DIVISIONS):
        return  self.getBins(rn, divisions), \
                self.getBins(rd, divisions), \
                self.getBins(pop, divisions)
    
    def getBins(self, myList, divisions):
        divisions = divisions + 2
        binned = np.linspace(min(myList), max(myList), divisions, endpoint=True)
        return list(binned[1:])
    
    def binValue(self, value, binList, isReversed):
        if np.isnan(value) == False:    
            for i in range(len(binList)):
                if value <= binList[i]:
                    #return (len(binList)*isReversed) + (-1*isReversed * i) + (1*notReversed)
                    if isReversed == True:
                        return len(binList)-i
                    else:
                        return (i+1)
            return 0;
        return -1;
            
    def computeEquations(self, nodeValues):
        accessibilityEquation = AccessibilityEquation()
        appropriateTravelDistanceEquation = AppropriateTravelDistanceEquation()
        landUseEquation = LandUseEquation()
        maximumCoverageEquation = MaximumCoverageEquation()
        safetyEquation = SafetyEquation()
        
        equationResults = []
        appendResults = equationResults.append
        
        appendResults(safetyEquation.computeCriteriaWithWeight(nodeValues[0], nodeValues[1]))
        appendResults(landUseEquation.computeCriteriaWithWeight(nodeValues[2]))
        appendResults(accessibilityEquation.computeCriteriaWithWeight(nodeValues[3]))
        appendResults(appropriateTravelDistanceEquation.computeCriteriaWithWeight(nodeValues[4]))
        appendResults(maximumCoverageEquation.computeCriteriaWithWeight(nodeValues[5]))
        
        return equationResults 

    @staticmethod 
    def computeScore(values): 
        return np.sum(values)
    
    @staticmethod
    def computeOptimalThresholdValues():
        return
        #SafeValue:
        #flood hazard level >= 2; E1
        #land elevation > 2; E1
        #land cover >= 2; E2
        #road networks >= 8; E3
        #time <= 30 minutes
        #population >= 20%
        
        #LowHazardValue:
        #flood hazard level >= 1; E1
        #land elevation > 1; E1
        #land cover >= 1; E2
        #road networks 5 <= value <= 7; E3
        #time <= 30 minutes
        #population >= 10%
        
        #MediumHazardValue:
        #flood hazard level >= 1; E1
        #land elevation > 1; E1
        #land cover >= 0; E2
        #road networks 2 <= value <= 4; E3
        #time <= 60 minutes
        #population >= 10%
        
        #HighHazardValue:
        #flood hazard level >= 1; E1
        #land elevation > 1 ; E1
        #land cover >= 0; E2
        #road networks <= 1; E3
        #time <= 60 minutes
        #population >= 5%

        #thresholdValuesDict['HIGH_HAZARD_INDEX'] = 4;
        #thresholdValuesDict['MEDIUM_HAZARD_INDEX'] = 6;
        #thresholdValuesDict['LOW_HAZARD_INDEX'] = 13;
        #thresholdValuesDict['SAFE_INDEX'] = 18;
        
        #BASIS FOR DISCRETIZATION

        #PLOT FREQUENCY OF EXISTING EQUATIONS THEN EVALUATE FROM THERE