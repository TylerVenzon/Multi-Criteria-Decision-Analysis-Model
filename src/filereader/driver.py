import math
import pandas as pd
import numpy as np 
import sys

from src.classifier.classifier import Classifier
from src.filereader.xyzreader import XYZReader
from src.mcda.analysis.optimizer import Optimizer
from src.filereader.xyzparser import XYZParser

class Driver:
    YEAR_TO_GENERATE = "005"
    
    COORD_INDEX = 0
    FH_INDEX = 1
    LE_INDEX = 2
    LC_INDEX = 3
    RNC_INDEX = 4
    ATDT_INDEX = 5
    MC_INDEX = 6
        
    def computeSuitabilityScore(fhscore, lescore, lcscore, rnscore, atdtscore, mcscore):
        optimizer = Optimizer()
        rnscore = optimizer.binRoadNetwork(rnscore)
        atdtscore = optimizer.binRoadDistance(atdtscore)
        mcscore = optimizer.binPopPercentage(mcscore)
            
        nodeArray = [fhscore, lescore, lcscore, rnscore, atdtscore, mcscore]
        equationResults = optimizer.computeEquations(nodeArray)
        score = optimizer.computeScore(equationResults)
        return score
        

    
    #FileReading
    try:
        print("Starting File Reading")
        maps = XYZReader(YEAR_TO_GENERATE)
    except IOError:
        print("Error reading one files. Aborting whole process")
        sys.exit()
    except Exception as e:
        print("Unknown exception occured during file reading. Here's the trace:")
        print(e)
        sys.exit()
        
    #File Parsing    
    try:
        print("Starting File Parsing")
        parser = XYZParser()
        FHMx, FHMy, FHMz = parser.parse(maps.fhm005yrs, int)
        LCx, LCy, LCz = parser.parse(maps.landcover, int)
        LEx, LEy, LEz = parser.parse(maps.landcover, int)
        RNCx, RNCy, RNCz = parser.parse(maps.roadnetworkcount, int)
        RDx,RDy, RDz = parser.parse(maps.road_distance, int)
        PDAx, PDAy, PDAz = parser.parse(maps.population_distributed_aligned, float)
    except Exception as e:
        print("Unknown exception occured during file parsing. Here's the trace:")
        print(e)
        sys.exit()
    
    #Dataset Preparation
    try:
        print("Starting Dataset Preparation")
        FH = np.array(parser.prepForMapping(FHMx, FHMy, FHMz))
        LE = np.array(parser.prepForMapping(LEx, LEy, LEz))
        LC = np.array(parser.prepForMapping(LCx, LCy, LCz))
        RNC = np.array(parser.prepForMapping(RNCx, RNCy, RNCz))
        ATDT = np.array(parser.prepForMapping(RDx, RDy, RDz))
        MC = np.array(parser.prepForMapping(PDAx, PDAy, PDAz))
    except Exception as e:
        print("Unknown exception occured during dataset preparation. Here's the trace:")
        print(e)
        sys.exit()
    
    #Dataset Merging
    try:
        print("Starting Dataset Merging")
        dFH = pd.DataFrame(FH, columns=['coord', 'fh'])
        dLE = pd.DataFrame(LE, columns=['coord', 'le'])
        dLC = pd.DataFrame(LC, columns=['coord', 'lc'])
        dRNC = pd.DataFrame(RNC, columns=['coord', 'rnc'])
        dATDT = pd.DataFrame(ATDT, columns=['coord', 'atdt'])
        dMC = pd.DataFrame(MC, columns=['coord', 'mc'])
    except Exception as e:
        print("Unknown exception occured during dataset merging. Here's the trace:")
        print(e)
        sys.exit()
    
    data = dFH.merge( dLE.merge( dLC.merge( dRNC.merge( dATDT.merge(dMC), 
            how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord')
    allData = data
    data = data.values.tolist()
    
    
    XYZ_OUTPUT = "mcdamap%syrs" % YEAR_TO_GENERATE
    XYZ_OUTPUT_FILE = XYZ_OUTPUT + ".xyz"
    ANALYSIS_OUTPUT_FILE = "alldata" + XYZ_OUTPUT + ".csv"
    

    f = open(XYZ_OUTPUT_FILE,"w+")
    ad = open(ANALYSIS_OUTPUT_FILE, "w+")
    
    suitability = []
    classification = []
    toAppend = []
    
    #Optimization
    print("Starting Optimization")
    for i in range(len(data)):
        coord = data[i][COORD_INDEX]
        score = computeSuitabilityScore(float(data[i][FH_INDEX]), 
                                        float(data[i][LE_INDEX]),
                                        float(data[i][LC_INDEX]),
                                        float(data[i][RNC_INDEX]),
                                        float(data[i][ATDT_INDEX]),
                                        float(data[i][MC_INDEX]))
        
        if math.isnan(score):
            score = 0
            classificationScore = 0
        elif float(data[i][FH_INDEX])+float(data[i][LE_INDEX])+float(data[i][LC_INDEX])+float(data[i][RNC_INDEX])+float(data[i][ATDT_INDEX])+float(data[i][MC_INDEX]) == 0: 
            score = 0 
            classificationScore = 0
        else:
            classificationScore = Classifier.classify(score)
            suitability.append([data[i][COORD_INDEX], score])
            classification.append([data[i][COORD_INDEX], classificationScore])
            
            toAppend.append( [data[i][COORD_INDEX], score, classificationScore] )            
            
            f.write("%s %d\n" % (data[i][COORD_INDEX], classificationScore))
            ad.write("%s %f %f %f %f %f %f %d %d\n" % (data[i][COORD_INDEX],
                                            float(data[i][FH_INDEX]), 
                                            float(data[i][LE_INDEX]),
                                            float(data[i][LC_INDEX]),
                                            float(data[i][RNC_INDEX]),
                                            float(data[i][ATDT_INDEX]),
                                            float(data[i][MC_INDEX]), 
                                            score,
                                            classificationScore))
            
    print("Finished generating output")
        
    f.close
    ad.close