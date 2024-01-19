from Base.BaseModel import BaseModel, Base
from sqlalchemy import PickleType, Column,  Integer

class ProcessAIModel(BaseModel, Base):
    __tablename__ = "process_ai"
    # id = Column(Integer, primary_key=True, nullable=False)
    service_id = Column(Integer)
    camera_ids = Column(PickleType)