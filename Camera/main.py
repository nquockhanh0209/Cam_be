from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, ARRAY,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Thread
import multiprocessing
import requests
import json
Base = declarative_base()

class Camera(Base):
    __tablename__ = "camera"
    id = Column(Integer, primary_key=True, nullable=False)
    activate = Column(Boolean)
    name = Column(String(255))
    restreamEndpoint = Column(String(1020))
    state = Column(Enum('CONNECTED', 'DISCONNECTED', 'CONNECTING'))
    
    # def __init__(self, 
    #             id,
    #             name,
    #             activate,
    #             restreamEndpoint,
    #             state
    #             ):
      
    #     self.id = id
    #     self.name = name
    #     self.activate = activate
    #     self.restreamEndpoint =restreamEndpoint
    #     self.state = state
      
    def __repr__(self):
        return self

    def load_from_api(self,engine,api_url: String):
        headers= {
            "Id":"alo"
        }
        Session = sessionmaker(bind= engine)
        session = Session()
        res = requests.get(url = api_url, headers=headers)
        cameras = res.json()
        print("X-cameras", cameras)
        
        for camera in cameras:
   
            if not bool(session.query(Camera).filter_by(id=camera["id"]).first()):
                self.__init__(int(camera["id"]),
                            camera["name"],
                            camera["activate"],
                            camera["restreamEndpoint"],
                            camera["state"]
                            )
                cam = self
                session.add(cam)
                session.commit()
            
if __name__ == "__main__":
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    api_url = "http://192.168.1.212:48080/api/cameras" 
    camera = Camera()
    camera.load_from_api(engine, api_url)

