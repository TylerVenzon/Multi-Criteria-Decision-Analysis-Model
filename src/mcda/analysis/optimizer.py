from src.mcda.implementation.accessibilityequation import AccessibilityEquation
from src.mcda.implementation.appropriatetraveldistanceequation import AppropriateTravelDistanceEquation
from src.mcda.implementation.landusequation import LandUseEquation
from src.mcda.implementation.maximumcoveragequation import MaximumCoverageEquation
from src.mcda.implementation.safetyequation import SafetyEquation





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
    
    def __init__(self):
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
        
        #x y z, 
        self.safeValues = [3, 3, 3, 171, 334.5, 0.0002175]       
        self.lowHazardValues = [3, 3, 2, 114, 334.5, 0.000145]
        self.mediumHazardValues = [2, 2, 2, 57, 446, 0.000145]
        self.highHazardValues = [2, 2, 1, 57, 446, 0.0000725]
        
        self.safeValues[3] = self.binRoadNetwork(self.safeValues[3])
        self.safeValues[4] = self.binRoadDistance(self.safeValues[4])
        self.safeValues[5] = self.binPopPercentage(self.safeValues[5])
        
        self.lowHazardValues[3] = self.binRoadNetwork(self.lowHazardValues[3])
        self.lowHazardValues[4] = self.binRoadDistance(self.lowHazardValues[4])
        self.lowHazardValues[5] = self.binPopPercentage(self.lowHazardValues[5])

        self.mediumHazardValues[3] = self.binRoadNetwork(self.mediumHazardValues[3])
        self.mediumHazardValues[4] = self.binRoadDistance(self.mediumHazardValues[4])
        self.mediumHazardValues[5] = self.binPopPercentage(self.mediumHazardValues[5])        

        self.highHazardValues[3] = self.binRoadNetwork(self.highHazardValues[3])
        self.highHazardValues[4] = self.binRoadDistance(self.highHazardValues[4])
        self.highHazardValues[5] = self.binPopPercentage(self.highHazardValues[5]) 
        
        
        #print("VALUES")
        #print(self.safeValues)
        #print(self.lowHazardValues)
        #print(self.mediumHazardValues)
        #print(self.highHazardValues) 
        
        
        self.safeEquationResults = self.computeEquations(self.safeValues)
        self.lowHazardEquationResults = self.computeEquations(self.lowHazardValues)
        self.mediumHazardEquationResults = self.computeEquations(self.mediumHazardValues)
        self.highHazardEquationResults = self.computeEquations(self.highHazardValues)


        #print("RESULTS")
        #print(self.safeEquationResults)
        #print(self.lowHazardEquationResults)
        #print(self.mediumHazardEquationResults)
        #print(self.highHazardEquationResults)         

                       
        self.SAFE_THRESHOLD = self.computeScore(self.safeEquationResults)
        self.LOW_HAZARD_THRESHOLD = self.computeScore(self.lowHazardEquationResults)
        self.MEDIUM_HAZARD_THRESHOLD = self.computeScore(self.mediumHazardEquationResults)
        self.HIGH_HAZARD_THRESHOLD = self.computeScore(self.highHazardEquationResults)
        
        
        #print("THRESHOLDS")
        #print(self.SAFE_THRESHOLD)
        #print(self.LOW_HAZARD_THRESHOLD)
        #print(self.MEDIUM_HAZARD_THRESHOLD)
        #print(self.HIGH_HAZARD_THRESHOLD)


    @staticmethod
    def computeEquations(nodeValues):
        accessibilityEquation = AccessibilityEquation()
        appropriateTravelDistanceEquation = AppropriateTravelDistanceEquation()
        landUseEquation = LandUseEquation()
        maximumCoverageEquation = MaximumCoverageEquation()
        safetyEquation = SafetyEquation()
        
        equationResults = []
        
        equationResults.append(safetyEquation.computeCriteriaWithWeight(nodeValues[0], nodeValues[1]))
        equationResults.append(landUseEquation.computeCriteriaWithWeight(nodeValues[2]))
        equationResults.append(accessibilityEquation.computeCriteriaWithWeight(nodeValues[3]))
        equationResults.append(appropriateTravelDistanceEquation.computeCriteriaWithWeight(nodeValues[4]))
        equationResults.append(maximumCoverageEquation.computeCriteriaWithWeight(nodeValues[5]))
        
        return equationResults 
        
        
    @staticmethod
    def binRoadNetwork(value):
        if value <= 57:
            return 1
        elif value <= 114:
            return 2
        elif value <= 171:
            return 3
        elif value > 171:
            return 4
        else:
            return 0
        
    @staticmethod          
    def binRoadDistance(value):
        if value <= 111.5:
            return 4
        elif value <= 223:
            return 3
        elif value <= 334.5:
            return 2
        elif value > 334.5:
            return 1
        else:
            return 0
    
    @staticmethod    
    def binPopPercentage(value):
        if value <= 0.0000725:
            return 1
        elif value <= 0.000145:
            return 2
        elif value <= 0.0002175:
            return 3
        elif value > 0.0002175:
            return 4
        else:
            return 0
            
    @staticmethod
    def computeScore(values):
        total = 0;
        for i in range(len(values)):
            total += values[i]
        
        return total

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