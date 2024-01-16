from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Thread
import multiprocessing
import requests
import json
Base = declarative_base()

class AIFlow(Base):
    __tablename__ = "ai_flow"

    id = Column(Integer, primary_key=True, nullable=False)
    alert = Column(Boolean)
    apply = Column(Boolean)
    cameraIds = Column(PickleType)
    type = Column(Enum('AiFlowDTO', 'CROWD', 'HUMAN', 'VEHICLE'))
    def __init__(self, 
                id,
                alert,
                apply,
                cameraIds,
                type
                ):
      
        self.id = id
        self.alert = alert
        self.apply = apply
        self.cameraIds =cameraIds
        self.type = type
      
    def __repr__(self):
        return self



    
def load_from_api(engine,api_url):
    headers= {
        "Id":"alo"
    }
    Session = sessionmaker(bind= engine)
    session = Session()
    res = requests.get(url = api_url, headers=headers)
    aiflows = res.json()
 
    print("aiflows", aiflows)
    for aiflow in aiflows:
        print('aiflow["cameraIds"]',aiflow["cameraIds"])
        if not bool(session.query(AIFlow).filter_by(id=aiflow["id"]).first()):
            flow = AIFlow(int(aiflow["id"]),
                        aiflow["alert"],
                        aiflow["apply"],
                        aiflow["cameraIds"],
                        aiflow["type"]
                        )
            session.add(flow)
            session.commit()

        
if __name__ == "__main__":
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    api_url = "http://192.168.1.212:48080/api/aiflows" 
    load_from_api(engine, api_url)
    

