from Base.BaseModel import BaseModel, Base
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, ARRAY,Enum, update

from ENUM.enum import CameraState
class CameraModel(BaseModel, Base):
    __tablename__ = "camera"

    activate = Column(Boolean)
    name = Column(String(255))
    restreamEndpoint = Column(String(1020))
    state =  Column(Enum(CameraState))
    
