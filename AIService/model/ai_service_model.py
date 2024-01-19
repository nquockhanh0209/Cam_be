
from Base.BaseModel import BaseModel, Base
from sqlalchemy import PickleType, Column, String,Enum

from ENUM.enum import AIServiceType
class ServiceAIModel(BaseModel, Base):
    __tablename__ = "service_ai"

    # id = Column(Integer, primary_key=True, nullable=False)
    name= Column(String)
    type= Column(Enum(AIServiceType))
    hostName= Column(String)
    ipAddress= Column(String)
    macAddress= Column(String)
    heartbeat= Column(String)
    state= Column(String)
    cameraIds= Column(PickleType)
