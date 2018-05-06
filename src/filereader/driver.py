import math
import pandas as pd
import numpy as np 
import sys
from pyproj import Proj, transform

from src.classifier.classifier import Classifier
from src.mcda.analysis.optimizer import Optimizer
from src.mcda.analysis.weightlist import WeightList
from src.filereader.xyzreader import XYZReader
from src.filereader.xyzparser import XYZParser

class Driver:
    ###########################################################################
    # CONSTANTS ###############################################################
    ###########################################################################
    
    # default values for the ideal configuration of the area's suitability
    #DEFAULT_VALUES = [[3, 3, 3, 171, 334.5, 0.0002175], # VERY HIGH SUITABILITY
    #                  [3, 3, 2, 114, 334.5, 0.000145],  # HIGH SUITABILITY
    #                  [2, 2, 2, 57, 446, 0.000145],     # LOW SUITABILITY
    #                  [2, 2, 1, 57, 446, 0.0000725]]    # VERY LOW SUITABILITY
    
    DEFAULT_VALUES = [[3, 3, 3, 3, 2, 3], # VERY HIGH SUITABILITY
                      [3, 3, 2, 2, 2, 2],  # HIGH SUITABILITY
                      [2, 2, 2, 1, 1, 2],     # LOW SUITABILITY
                      [2, 2, 1, 1, 1, 1]]    # VERY LOW SUITABILITY
    
    NON_PEOPLE_BASED = [3,3,1,1,1]
    PEOPLE_BASED = [2,2,3,3,3]
    DEFAULT_WEIGHTS = [3, 1, 2, 2, 2]
    
    YEAR_TO_GENERATE = "005"

    ideal_values = DEFAULT_VALUES
    
    def generate(year=YEAR_TO_GENERATE, ideal_values=DEFAULT_VALUES, weights=DEFAULT_WEIGHTS):
        MESSAGE_ERROR_READ = "Error reading one or more files"
        MESSAGE_ERROR_UNKNOWN = "Unknown exception occured during file parsing"
        MESSAGE_SUCCESS = "Finished generating output"
    
        #######################################################################
        # CONSTNT INITIALIZATION ##############################################
        #######################################################################
        
        # indices for accessing values in input list
        COORD_INDEX = 0
        FH_INDEX = 1
        LE_INDEX = 2
        LC_INDEX = 3
        RNC_INDEX = 4
        ATDT_INDEX = 5
        MC_INDEX = 6
        
        # indices for accessing values in equation list
        SAFETY_EQ_INDEX = 0
        LC_EQ_INDEX = 1
        A_EQ_INDEX = 2
        AT_EQ_INDEX = 3
        MC_EQ_INDEX = 4
        
        #######################################################################
        # FILE READING ########################################################
        #######################################################################
    
        try:
            print("Starting File Reading")
            maps = XYZReader(year)
        except IOError:
            print("Error reading one or more files. Aborting whole process")
            return MESSAGE_ERROR_READ
        except Exception as e:
            print("Unknown exception occured during file reading. Here's the trace:")
            print(e)
            return MESSAGE_ERROR_UNKNOWN
            
        #######################################################################
        # FILE PARSING ########################################################
        #######################################################################
    
        try:
            print("Starting File Parsing")
            parser = XYZParser()
            FHMx, FHMy, FHMz = parser.parse(maps.fhm005yrs, int)
            LEx, LEy, LEz = parser.parse(maps.landelevation, int)
            LCx, LCy, LCz = parser.parse(maps.landcover, int)
            RNCx, RNCy, RNCz = parser.parse(maps.roadnetworkcount, int)
            RDx,RDy, RDz = parser.parse(maps.road_distance, int)
            PDAx, PDAy, PDAz = parser.parse(maps.population_distributed_aligned, float)
        except Exception as e:
            print("Unknown exception occured during file parsing. Here's the trace:")
            print(e)
            return MESSAGE_ERROR_UNKNOWN
        
        #######################################################################
        # DATASET PREPRATION ##################################################
        #######################################################################
    
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
            return MESSAGE_ERROR_UNKNOWN
        
        #######################################################################
        # DATASET MERGING #####################################################
        #######################################################################
    
        data = []
        # allData = []
        try:
            print("Starting Dataset Merging")
            dFH = pd.DataFrame(FH, columns=['coord', 'fh'])
            dLE = pd.DataFrame(LE, columns=['coord', 'le'])
            dLC = pd.DataFrame(LC, columns=['coord', 'lc'])
            dRNC = pd.DataFrame(RNC, columns=['coord', 'rnc'])
            dATDT = pd.DataFrame(ATDT, columns=['coord', 'atdt'])
            dMC = pd.DataFrame(MC, columns=['coord', 'mc'])
            
            data = dFH.merge( dLE.merge( dLC.merge( dRNC.merge( dATDT.merge(dMC), 
            how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord'), how='outer', on='coord')
            # allData = data
            data = data.values.tolist()
    
        except Exception as e:
            print("Unknown exception occured during dataset merging. Here's the trace:")
            print(e)
            return MESSAGE_ERROR_UNKNOWN
        
        
        #######################################################################
        # WEIGHTLIST CUSTOMIZATION ############################################
        #######################################################################     
        print("Starting WeightList Customization")
        WeightList.SAFETY = weights[SAFETY_EQ_INDEX]
        WeightList.LAND_COVER = weights[LC_EQ_INDEX]
        WeightList.ACCESSIBILITY = weights[A_EQ_INDEX]
        WeightList.APPROPRIATE_TRAVEL_DISTANCE = weights[AT_EQ_INDEX]
        WeightList.MAXIMUM_COVERAGE = weights[MC_EQ_INDEX]
        
        #######################################################################
        # OPTIMIZATION ########################################################
        #######################################################################        
        print("Starting Model Computation and Classification")
        
        xyz = "mcdamap%syrs" % year
        xyzfilename = xyz + ".xyz"
        analysisfilename = "alldata" + xyz + ".csv"
        
        f = open(xyzfilename,"w+")
        fwrite = f.write
        
        ad = open(analysisfilename, "w+")
        adwrite = ad.write
        
        rn = [row[4] for row in data]
        rd = [row[5] for row in data]
        pp = [row[6] for row in data]
        
        optimizer = Optimizer(rn,rd, pp, ideal_values)
        classifier = Classifier(optimizer)
        
        suitability = []
        classification = []
        toAppend = []
        
        isnan = math.isnan
        suitability_append = suitability.append
        classification_append = classification.append
        toAppend_append = toAppend.append
        
        computeSuitability = optimizer.computeSuitabilityScore
        for i in range(len(data)):
            toCheck = data[i]
            # coord = toCheck[COORD_INDEX]
            nodeArray = [float(toCheck[FH_INDEX]), float(toCheck[LE_INDEX]), float(toCheck[LC_INDEX]), float(toCheck[RNC_INDEX]), float(toCheck[ATDT_INDEX]), float(toCheck[MC_INDEX])]
            score = computeSuitability(*nodeArray)
            
            if isnan(score):
                score = 0
                classificationScore = 0
            elif np.sum(nodeArray) == 0: 
                score = 0 
                classificationScore = 0
            else:
                classificationScore = classifier.classify(score)
                suitability_append([toCheck[COORD_INDEX], score])
                classification_append([toCheck[COORD_INDEX], classificationScore])
                toAppend_append( [toCheck[COORD_INDEX], score, classificationScore] )            
                
                fwrite("%s %d\n" % (toCheck[COORD_INDEX], classificationScore))
            
                inProj = Proj(init='epsg:32651')
                outProj = Proj(init='epsg:4326')
                coordinates = transform(inProj, outProj, *list(map(int, toCheck[COORD_INDEX].split(" "))))
                adwrite("%f,%f,%f,%f,%f,%f,%f,%f,%d,%d\n" % ( *coordinates,
                                                *nodeArray, 
                                                score,
                                                classificationScore))
                
        print("Finished generating output")
            
        f.close
        ad.close
        
        return MESSAGE_SUCCESS
    
    message = generate()
    print(message)
    sys.exit