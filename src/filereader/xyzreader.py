
class XYZReader:

    fhm005yrs = []
    landcover = []
    landelevation = []
    roadnetworkcount = []
    road_distance = []
    population_distributed_aligned = []
    
    
    def __init__(self):
        #Read 5yr Flood Hazard Map data    
        with open('fhm005yrs.xyz', 'r') as f:
                    
            for line in f:
                #Split line separating elements through spaces
                self.fhm005yrs.append(line.split())
                
            
            #print(self.fhm005yrs[0])
            
        
        #Read Land Cover Map data
        with open('landcover.xyz', 'r') as f:
                    
            for line in f:
                #Split line separating elements through spaces
                self.landcover.append(line.split())
            
            
            #print(self.landcover[0])
          
        #Read Land Elevation Map data
        with open('landelevationnormalized.xyz', 'r') as f:
                    
            for line in f:
                self.landelevation.append(line.split())
            
            
            #print(self.landelevation[0])
        
        #Read Road Network Count Map data
        with open('roadnetworkcount.xyz', 'r') as f:
                    
            for line in f:
                self.roadnetworkcount.append(line.split())
            
            
            #print(self.roadnetworkcount[0])
            
        #Appropriate Road Distance    
        with open('road_distance.xyz', 'r') as f:
        
            for line in f:
                self.road_distance.append(line.split())
            
            
            #print(self.road_distance[0])
            
            
        #Population 
        with open('population_distributed_aligned.xyz', 'r') as f:
        
            for line in f:
                self.population_distributed_aligned.append(line.split())
            
            
            #print(self.population_distributed_aligned[0])
        #print(len(self.roadnetworkcount))
            
            
    