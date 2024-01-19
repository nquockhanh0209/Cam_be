from ENUM.enum import AIServiceType
from typing import List
from Base.BaseDto import BaseDto
from dataclasses import dataclass

@dataclass
class AIServiceDTO(BaseDto):

    name: str
    type: str
    hostName: str
    ipAddress: str
    macAddress: str
    heartbeat: str
    state: str
    cameraIds: List[int]
    
