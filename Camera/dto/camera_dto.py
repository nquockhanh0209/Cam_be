
from Base.BaseDto import BaseDto

from dataclasses import dataclass

@dataclass
class CameraDTO(BaseDto):
   
    activate : bool
    name : bool
    restreamEndpoint : str
    state : str