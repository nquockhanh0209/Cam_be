from ENUM.enum import AIFlowType

from typing import List
from Base.BaseDto import BaseDto
from dataclasses import dataclass

@dataclass
class AIFlowDTO(BaseDto):

    alert = bool
    apply = bool
    cameraIds = List[int]
    type = AIFlowType