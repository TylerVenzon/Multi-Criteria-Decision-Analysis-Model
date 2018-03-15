from src.mcda.analysis.optimizer import Optimizer


class Classifier:
    

    
    @staticmethod
    def classify(index):
        
        optimizer = Optimizer()
        
        if index >= optimizer.SAFE_THRESHOLD:
            return optimizer.SAFE_INDEX
        elif index >= optimizer.LOW_HAZARD_THRESHOLD:
            return optimizer.LOW_HAZARD_INDEX
        elif index >= optimizer.MEDIUM_HAZARD_THRESHOLD:
            return optimizer.MEDIUM_HAZARD_INDEX
        elif index >= optimizer.HIGH_HAZARD_THRESHOLD:
            return optimizer.HIGH_HAZARD_INDEX
        else:
            return optimizer.UNSAFE_INDEX
        
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
        
    
                
        
        
            
            
    
    