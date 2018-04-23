import numpy as np

# -*- coding: utf-8 -*-
class XYZParser:
    
    @staticmethod
    def parse(raw_xyz, datatype):
        colx = [row[0]for row in raw_xyz]
        colx = list(map(float, colx))
        colx = np.array(colx).astype(int)
        
        coly = [row[1]for row in raw_xyz]
        coly = list(map(float, coly))
        coly = np.array(coly).astype(int)

        colz = [row[2]for row in raw_xyz]
        colz = list(map(datatype, colz))
        
        return (colx, coly, colz)
    
    @staticmethod
    def prepForMapping(xCol, yCol, zCol):
        data = []
        for i in range (len(xCol)):
            merged = str(str(xCol[i]) + " " + str(yCol[i]))
            data.append([merged, zCol[i]])
            
        return data    