import subprocess
from multiprocessing import Process
from os import getppid
from sqlalchemy import create_engine, Column, String, Integer,  PickleType,Enum, update
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
import requests
import json
import asyncio
from AIProcess.ai_process import ProcessAI
import websockets
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv() 
Base = declarative_base()
wss_url = os.getenv('WSS_URL')
create_cam_url = os.getenv('CREATE_CAM_URL')
update_cam_url = os.getenv('UPDATE_CAM_URL')
create_service_url = os.getenv('CREATE_SERVICE_URL')
class AIServiceType(enum.Enum):

    CROWD_AI = 'CROWD_AI'
    HUMAN_AI =  'HUMAN_AI'
    VEHICLE_AI= 'VEHICLE_AI'

class ServiceAI(Base):
    __tablename__ = "service_ai"

    id = Column(Integer, primary_key=True, nullable=False)
    name= Column(String)
    type= Enum(AIServiceType)
    hostName= Column(String)
    ipAddress= Column(String)
    macAddress= Column(String)
    heartbeat= Column(String)
    state= Column(String)
    cameraIds= Column(PickleType)

   
         
    
    def create_service(self, engine, name: str, type: AIServiceType, hostName: str, ipAddress: str, macAddress: str, heartbeat: str):
        Session = sessionmaker(bind= engine)
        session = Session()
        if not bool(session.query(ServiceAI).filter().first()):
            body = {
                "name": name,
                "type": type,
                "hostName": hostName,
                "ipAddress": ipAddress,
                "macAddress": macAddress,
                "heartbeat": heartbeat,

            }
            
            headers= {
                "Id":"alo",
                "Content-Type": "application/json"
            }
            r = requests.post(url=create_service_url, data=json.dumps(body), headers=headers)
            res = r.json()
    
            self.id= res["id"]
            self.name = res["name"]
            self.type= res["type"]
            self.hostName=res["hostName"]
            self.ipAddress=res["ipAddress"]
            self.heartbeat=res["heartbeat"]
            self.state=res["state"]

            
            service = self
            session.add(service)
            session.commit()
            
            
            
            camCreateParams = {
                "name": "alo4",
                "urlMainstream": "rtsp://alo4.com"
            }
            print("create_cam_url", create_cam_url)
            r = requests.post(url=create_cam_url, params=(camCreateParams), headers=headers)
            print("res",r.json())
            
            camUpdateParams = {
                "id": 3,
                "serviceId": self.id
            }
            
        
            process_ai = ProcessAI()
            process_ai.start(engine, self.id)
            r = requests.patch(url=update_cam_url, params=(camUpdateParams), headers=headers)
               
            self.id = 57   
            async def start_websocket(wss_url: str):
                print("wss_url",wss_url)
                async with websockets.connect(wss_url) as ws:
                    
                    
                    while True:
                        msg = await ws.recv()
                        
                        if json.loads(msg)["dst"] ==str(self.id):
                            print(str(json.loads(msg)["deliveryTag"]))
                            res = {
                                "deliveryTag": str(json.loads(msg)["deliveryTag"])
                            }
                            print(res)
                            await ws.send(json.dumps(res))
            final_wss_url = wss_url + str(self.id)
            asyncio.run(start_websocket(final_wss_url))
        

    
 
# protect the entry point
# if __name__ == '__main__':
    
    
#     engine = create_engine("sqlite:///database.db", echo = True)
#     Base.metadata.create_all(bind= engine)
#     service_ai = ServiceAI()
#     print(service_ai)
#     def create_service(engine, api_url: String, name: String, type: AIServiceType, hostName: String, ipAddress: String, macAddress: String, heartbeat: String, cameraIds: List[int]):
        
#         service_ai.create_service(engine, api_url, name, type, hostName, ipAddress, macAddress, heartbeat, cameraIds)
        
#     api_url= "http://192.168.1.212:48080/api/service"
#     name= "NewService"
#     type="HUMAN_AI" 
#     hostName = "http://192.168.1.212:48080/"
#     ipAddress= "http://192.168.1.212:48080/" 
#     macAddress= "http://192.168.1.212:48080/" 
#     heartbeat = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
#     cameraIds = [1,2,3]
#     print("heartbeat", heartbeat)
    
#     # create_service(engine,
#     #                 api_url,
#     #                 name,
#     #                 type, 
#     #                 hostName,
#     #                 ipAddress,
#     #                 macAddress,
#     #                 heartbeat,
#     #                 cameraIds)
#     child = Process(target=create_service, args=(engine,
#                                                     api_url,
#                                                     name,
#                                                     type, 
#                                                     hostName,
#                                                     ipAddress,
#                                                     macAddress,
#                                                     heartbeat,
#                                                     cameraIds))

#     child.start()

#     child.join()