class Classifier:    
    
    optimizer = None
    
    def __init__(self, optimizer):
        self.optimizer = optimizer
        
    def classify(self, index):
        if index >= self.optimizer.SAFE_THRESHOLD:
            return self.optimizer.SAFE_INDEX
        elif index >= self.optimizer.LOW_HAZARD_THRESHOLD:
            return self.optimizer.LOW_HAZARD_INDEX
        elif index >= self.optimizer.MEDIUM_HAZARD_THRESHOLD:
            return self.optimizer.MEDIUM_HAZARD_INDEX
        elif index >= self.optimizer.HIGH_HAZARD_THRESHOLD:
            return self.optimizer.HIGH_HAZARD_INDEX
        else:
            return self.optimizer.UNSAFE_INDEX
        
# =============================================================================
#         if index <= 0:
#             return -1
#           
#         elif index <= optimizer.HIGH_HAZARD_THRESHOLD:
#             return optimizer.HIGH_HAZARD_INDEX  
#         
#         elif index <= optimizer.MEDIUM_HAZARD_THRESHOLD: 
#             return optimizer.MEDIUM_HAZARD_INDEX
#         
#         elif index <= optimizer.LOW_HAZARD_THRESHOLD:
#             return optimizer.LOW_HAZARD_INDEX
#         
#         else:
#             return optimizer.SAFE_INDEX
# =============================================================================
        
    
                
        
        
            
            
    
    