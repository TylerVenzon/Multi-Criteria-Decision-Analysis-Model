import math
import pandas as pd
import numpy as np 

from src.classifier.classifier import Classifier
from src.filereader.xyzreader import XYZReader
from src.mcda.analysis.optimizer import Optimizer

class Driver:
        maps = XYZReader()
        
        
        
        
        
        #print(len(maps.roadnetworkcount))
        #classifier = Classifier()
        
        
        RNCx = [row[0]for row in maps.roadnetworkcount]
        RNCx = list(map(float, RNCx))
        RNCx = np.array(RNCx).astype(int)
        
    
        RNCy = [row[1]for row in maps.roadnetworkcount]
        RNCy = list(map(float, RNCy))
        RNCy = np.array(RNCy).astype(int)

        
        RNCz = [row[2]for row in maps.roadnetworkcount]
        RNCz = list(map(int, RNCz))
        
                
        RDx = [row[0]for row in maps.road_distance]
        RDx = list(map(float, RDx))
        RDx = np.array(RDx).astype(int)

        
        RDy = [row[1]for row in maps.road_distance]
        RDy = list(map(float, RDy))
        RDy = np.array(RDy).astype(int)

        
        RDz = [row[2]for row in maps.road_distance]
        RDz = list(map(int, RDz))
        
    
        PDAx = [row[0]for row in maps.population_distributed_aligned]
        PDAx = list(map(float, PDAx))
        PDAx = np.array(PDAx).astype(int)

        
        PDAy = [row[1]for row in maps.population_distributed_aligned]
        PDAy = list(map(float, PDAy))
        PDAy = np.array(PDAy).astype(int)
        
        
        PDAz = [row[2]for row in maps.population_distributed_aligned]
        PDAz = list(map(float, PDAz))
        
        
        FHM005x = [row[0]for row in maps.fhm005yrs]
        FHM005x = list(map(float, FHM005x))
        FHM005x = np.array(FHM005x).astype(int)

        FHM005y = [row[1]for row in maps.fhm005yrs]
        FHM005y = list(map(float, FHM005y))
        FHM005y = np.array(FHM005y).astype(int)

        FHM005z = [row[2]for row in maps.fhm005yrs]
        FHM005z = list(map(int, FHM005z))
        
        
        LCx = [row[0]for row in maps.landcover]
        LCx = list(map(float, LCx))
        LCx = np.array(LCx).astype(int)


        LCy = [row[1]for row in maps.landcover]
        LCy = list(map(float, LCy))
        LCy = np.array(LCy).astype(int)
                
        
        LCz = [row[2]for row in maps.landcover]
        LCz = list(map(int, LCz))
        
        
        LEx = [row[0]for row in maps.landelevation]
        LEx = list(map(float, LEx))
        LEx = np.array(LEx).astype(int)

        
        LEy = [row[1]for row in maps.landelevation]
        LEy = list(map(float, LEy))
        LEy = np.array(LEy).astype(int)


        LEz = [row[2]for row in maps.landelevation]
        LEz = list(map(int, LEz))
            
        
        # your code here
        

        
        
        def computeSuitabilityScore(fhscore, lescore, lcscore, rnscore, atdtscore, mcscore):
            optimizer = Optimizer()
            rnscore = optimizer.binRoadNetwork(rnscore)
            atdtscore = optimizer.binRoadDistance(atdtscore)
            mcscore = optimizer.binPopPercentage(mcscore)
            
            nodeArray = [fhscore, lescore, lcscore, rnscore, atdtscore, mcscore]
            equationResults = optimizer.computeEquations(nodeArray)
            score = optimizer.computeScore(equationResults)
            return score
        
         
        suitability = []
        classification = []
        
        rowStart = 0
        rowEnd = 414732
        print("Start")
        
        f = open("mcdamap_5yr.xyz","w+")
        ad = open("alldatamcda_5yr.csv", "w+")
        #gets the whole list (containing the x, y, and z coordinates) and prepares them for the model
        def prepForMapping(xCol, yCol, zCol):
            data = []
            for i in range (len(xCol)):
                merged = str(str(xCol[i]) + " " + str(yCol[i]))
                data.append([merged, zCol[i]])
                
            return data    
            
        #print(LE)
        #print(FH)
        FH = np.array(prepForMapping(FHM005x, FHM005y, FHM005z))
        LE = np.array(prepForMapping(LEx, LEy, LEz))
        LC = np.array(prepForMapping(LCx, LCy, LCz))
        RNC = np.array(prepForMapping(RNCx, RNCy, RNCz))
        ATDT = np.array(prepForMapping(RDx, RDy, RDz))
        MC = np.array(prepForMapping(PDAx, PDAy, PDAz))
        
        dFH = pd.DataFrame(FH, columns=['coord', 'fh'])
        dLE = pd.DataFrame(LE, columns=['coord', 'le'])
        dLC = pd.DataFrame(LC, columns=['coord', 'lc'])
        dRNC = pd.DataFrame(RNC, columns=['coord', 'rnc'])
        dATDT = pd.DataFrame(ATDT, columns=['coord', 'atdt'])
        dMC = pd.DataFrame(MC, columns=['coord', 'mc'])
        
        COORD_INDEX = 0
        FH_INDEX = 1
        LE_INDEX = 2
        LC_INDEX = 3
        RNC_INDEX = 4
        ATDT_INDEX = 5
        MC_INDEX = 6
        
        data = dFH.merge( dLE.merge( dLC.merge( dRNC.merge( dATDT.merge(dMC), 
                how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord')
        allData = data
        data = data.values.tolist()
        
        toAppend = []
        
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
            
            if i >= 70000 and i < 70500:
                print(i, data[i][COORD_INDEX], score, classificationScore)            
        print("End")
        
        f.close
        ad.close
        
        #print("MAX")        
        #print("max road count", max(RNCz))
        #print("max road distance", max(RDz))
        #print("max pop percentage", max(PDAz))
        #print("MIN")        
        #print("min road count", min(RNCz))
        #print("min road distance", min(RDz))
        #print("min pop percentage", min(PDAz))
        

        
        
    
            
        
            
            
       
        
        
        
        
        
#        print("Z " , len(RNCz))
#        print(max(RNCz))
        

                