from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Thread
import multiprocessing
import requests
import json
Base = declarative_base()
import enum

class AIFlowType(enum.Enum):
    AiFlowDTO = 'AiFlowDTO'
    CROWD = 'CROWD'
    HUMAN =  'HUMAN'
    VEHICLE= 'VEHICLE'
class AIFlow(Base):
    __tablename__ = "ai_flow"

    id = Column(Integer, primary_key=True, nullable=False)
    alert = Column(Boolean)
    apply = Column(Boolean)
    cameraIds = Column(PickleType)
    type = Column(Enum(AIFlowType))
    # def __init__(self, 
    #             id: int,
    #             alert: bool,
    #             apply: bool,
    #             cameraIds: [],
    #             type: AIFlowType
    #             ):
      
    #     self.id = id
    #     self.alert = alert
    #     self.apply = apply
    #     self.cameraIds =cameraIds
    #     self.type = type
   
    
    def load_from_api(self, engine ,api_url: str):
        headers= {
            "Id":"alo"
        }
        Session = sessionmaker(bind= engine)
        session = Session()
        res = requests.get(url = api_url, headers=headers)
        aiflows = res.json()
    
   
        for aiflow in aiflows:
            
            if not bool(session.query(AIFlow).filter_by(id=aiflow["id"]).first()):
                print('aiflow["apply"]', aiflow["apply"])
                
                self.id = int(aiflow["id"]),
                self.alert= aiflow["alert"],
                self.apply= aiflow["apply"],
                self.cameraIds= aiflow["cameraIds"],
                self.type= aiflow["type"]
                            
                flow = self
                session.add(flow)
                session.commit()

        
# if __name__ == "__main__":
#     engine = create_engine("sqlite:///database.db", echo = True)
#     Base.metadata.create_all(bind= engine)
#     api_url = "http://192.168.1.212:48080/api/aiflows" 
#     ai_flow = AIFlow()
#     ai_flow.load_from_api(engine, api_url)
    

