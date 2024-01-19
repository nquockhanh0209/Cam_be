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
from AIProcess.model.ai_process_model import ProcessAIModel
from AIProcess.repository.ai_process_repository import ProcessAIRepository
from AIService.dto.ai_service_dto import AIServiceDTO
from AIService.model.ai_service_model import ServiceAIModel

from Base.BaseRepository import AbstractRepository
from Camera.model.camera_model import CameraModel
from Camera.repository.camera_repository import CameraRepository


import os
from dotenv import load_dotenv


load_dotenv() 

wss_url = os.getenv('WSS_URL')
create_cam_url = os.getenv('CREATE_CAM_URL')
update_cam_url = os.getenv('UPDATE_CAM_URL')
create_service_url = os.getenv('CREATE_SERVICE_URL')


class ServiceAIRepository(AbstractRepository):
  

    # def model_to_entity(model: ServiceAIModel) -> AIServiceDTO:
        

    #     return AIServiceDTO(
    #         id=model.id,
    #         name=model.name,
    #         type=model.type,
    #         hostName=model.hostName,
    #         ipAddress=model.ipAddress,
    #         macAddress=model.macAddress,
    #         heartbeat=model.heartbeat,
    #         state=model.state,
    #         cameraIds=model.cameraIds
    #     )

    # def entity_to_model(dto: AIServiceDTO, existing=None) -> ServiceAIModel:
        

    #     return ServiceAIModel(
    #         id=dto.id,
    #         name=dto.name,
    #         type=dto.type,
    #         hostName=dto.hostName,
    #         ipAddress=dto.ipAddress,
    #         macAddress=dto.macAddress,
    #         heartbeat=dto.heartbeat,
    #         state=dto.state,
    #         cameraIds=dto.cameraIds
    #     )
         
    
    def create_service(self, ai_dto: AIServiceDTO):
       
        if not bool(self.session.query(ServiceAIModel).filter().first()):
            body = {
                "name": ai_dto.name,
                "type": ai_dto.type,
                "hostName": ai_dto.hostName,
                "ipAddress": ai_dto.ipAddress,
                "macAddress": ai_dto.macAddress,
                "heartbeat": ai_dto.heartbeat,

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
            # ai_dto = AIServiceDTO(res["id"], 
            #                res["name"], 
            #                res["type"], 
            #                res["hostName"],
            #                res["ipAddress"],
            #                res["heartbeat"],
            #                res["state"])
            # service_ai_model =
            new_ai_service = ServiceAIModel()
            print(new_ai_service)
            ai_service = new_ai_service.entity_to_model(AIServiceDTO(
                res["id"],
                res["name"],
                res["type"],
                res["hostName"],
                res["ipAddress"],
                res["macAddress"],
                
                res["heartbeat"],
                res["state"],
                None
            ), ServiceAIModel)
            
            
            # ai_service =ServiceAIModel(AIServiceDTO(
            #     res["id"],
            #     res["name"],
            #     res["type"],
            #     res["hostName"],
            #     res["ipAddress"],
            #     res["macAddress"],
                
            #     res["heartbeat"],
            #     res["state"],
            #     None
            # )) 
            self.save(ai_service)
            
            
            
            camCreateParams = {
                "name": "alo19",
                "urlMainstream": "rtsp://alo19.com"
            }
            print("create_cam_url", create_cam_url)
            r = requests.post(url=create_cam_url, params=(camCreateParams), headers=headers)
            print("res",r.json())
            
            camUpdateParams = {
                "id": 2,
                "serviceId": self.id
            }
            
        
            # process_ai = ProcessAIRepository[ProcessAIModel](self.session)
            process_ai = ProcessAIRepository(self.session)
            
            process_ai.start( self.id)
            
            r = requests.patch(url=update_cam_url, params=(camUpdateParams), headers=headers)
            print(r.json())
            # camera = CameraRepository[CameraModel](self.session)
            camera = CameraRepository(self.session)
            
            camera.update_or_create_cam_wss( self.id)
        

    
 
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