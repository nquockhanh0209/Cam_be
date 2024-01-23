import enum
class AIServiceType(enum.Enum):

    CROWD_AI = 'CROWD_AI'
    HUMAN_AI =  'HUMAN_AI'
    VEHICLE_AI= 'VEHICLE_AI'
    
class AIFlowType(enum.Enum):
    AiFlowDTO = 'AiFlowDTO'
    CROWD = 'CROWD'
    HUMAN =  'HUMAN'
    VEHICLE= 'VEHICLE'
    
class CameraState(enum.Enum):
  
    CONNECTED = 'CONNECTED'
    DISCONNECTED =  'DISCONNECTED'
    CONNECTING= 'CONNECTING'
    
# class ConsumerType(enum.Enum):
  
#     CAMERA_SERVICE = 'SERVICE'
   


