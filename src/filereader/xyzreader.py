class XYZReader:

    FHM_FILE = 'fhm%syrs'
    LC_FILE ='landcover'
    LE_FILE = 'landelevationnormalized'
    RN_FILE = 'roadnetworkcount'
    RD_FILE = 'road_distance'
    POP_FILE = 'population_distributed_aligned'
    
    fhm005yrs = []
    landcover = []
    landelevation = []
    roadnetworkcount = []
    road_distance = []
    population_distributed_aligned = []
    
    def read(self, fileName):
        holder = []
        try:
            with(open("%s.xyz" % fileName, 'r')) as f:
                for line in f:
                   holder.append(line.split())
                   
            return holder
        except IOError:
            print("Error reading %s" % fileName)
            return None
        
    def __init__(self, sYear):
        #Read 5yr Flood Hazard Map data   
        self.FHM_FILE = self.FHM_FILE % sYear
        self.fhm005yrs = self.read(self.FHM_FILE)
        self.landcover = self.read(self.LC_FILE)
        self.landelevation = self.read(self.LE_FILE)
        self.roadnetworkcount = self.read(self.RN_FILE)
        self.road_distance = self.read(self.RD_FILE)
        self.population_distributed_aligned = self.read(self.POP_FILE)
            
    