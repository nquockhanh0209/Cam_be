from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, ARRAY,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from AIProcess.ai_process import ProcessAI
import requests
import json
import asyncio
import os
import websockets
Base = declarative_base()
wss_url = os.getenv('WSS_URL')
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
    def create_or_update_cam(self, engine, id, activate, name, restreamEndpoint, state):
        Session = sessionmaker(bind= engine)
        session = Session()
        if not bool(session.query(Camera).filter_by(id=id).first()):
            
            self.id = id
            self.activate = activate
            self.name = name
            self.restreamEndpoint = restreamEndpoint
            self.state = state
            session.add(self)
            session.commit()
        # else:
            
        #     session.query(Camera).filter_by(id=id).update({Camera.activate:activate,
        #                                                   Camera.name:name,
        #                                                   Camera.restreamEndpoint:restreamEndpoint,
        #                                                   Camera.state:state,
        #                                                   }, synchronize_session = False)         
    def load_from_api(self,engine):
        
        api_url = "http://192.168.1.212:48080/api/cameras" 
        headers= {
            "Id":"alo"
        }
        
        res = requests.get(url = api_url, headers=headers)
        cameras = res.json()
        print("X-cameras", cameras)
        
        for camera in cameras:
            
            
            self.create_or_update_cam(engine, int(camera["id"]), camera["activate"], camera["name"], camera["restreamEndpoint"], camera["state"])
            print('camera["serviceIds"]', camera["serviceIds"])
            for service_id in camera["serviceIds"]:
                process_ai = ProcessAI()
                
                print(123456, service_id, " ", camera["id"])
                process_ai.update_cam(engine, service_id, camera["id"])
    def update_or_create_cam_wss(self, engine, ai_service_id):
        
        async def start_websocket(wss_url: str):
            print("wss_url",wss_url)
            async with websockets.connect(wss_url) as ws: 
                while True:
                    msg = await ws.recv()
                    print
                    data = json.loads(json.loads(msg)["data"])
                    print(data)
                    
                    self.create_or_update_cam(engine, int(data["id"]), data["activate"], data["name"], data["restreamEndpoint"], data["state"])
                    
                    res = {
                        "deliveryTag": str(json.loads(msg)["deliveryTag"])
                    }
                    print(res)
                    
                    print(await ws.send(json.dumps(json.loads(msg))))
        final_wss_url = wss_url + str(ai_service_id)
        asyncio.run(start_websocket(final_wss_url)) 
        
# if __name__ == "__main__":
#     engine = create_engine("sqlite:///database.db", echo = True)
#     Base.metadata.create_all(bind= engine)
#     api_url = "http://192.168.1.212:48080/api/cameras" 
#     camera = Camera()
#     camera.load_from_api(engine, api_url)

