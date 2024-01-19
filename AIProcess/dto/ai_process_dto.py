from typing import List
from Base.BaseDto import BaseDto
from dataclasses import dataclass

@dataclass
class AIProcessDTO(BaseDto):

    service_id: int
    camera_ids: List[int]