from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, ARRAY,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from AIProcess.model.ai_process_model import ProcessAIModel
from AIProcess.repository.ai_process_repository import ProcessAIRepository
import requests
import json
import asyncio
import os
import websockets
from Base.BaseRepository import AbstractRepository

from ENUM.enum import CameraState
from Camera.dto.camera_dto import CameraDTO
from Camera.model.camera_model import CameraModel

wss_url = os.getenv('WSS_URL')
Base = declarative_base()
class CameraRepository(AbstractRepository):
 
    # def model_to_entity(self,model: CameraModel) -> CameraDTO:
        

    #     return CameraDTO(
    #         id=model.id,
    #         activate = model.activate,
    #         name=model.name,
    #         restreamEndpoint=model.restreamEndpoint,
    #         state=model.state
    #     )

    # def entity_to_model(self,dto: CameraDTO, existing=None) -> CameraModel:
    #     print(" hghg dto", dto)

    #     return CameraModel(
    #         id=dto.id,
    #         activate = dto.activate,
    #         name=dto.name,
    #         restreamEndpoint=dto.restreamEndpoint,
    #         state=dto.state
    #     )
    def update(self,cameraDto: CameraDTO):
        self.session.query(CameraModel).filter_by(id=cameraDto.id).update({CameraModel.activate:cameraDto.activate,
                                                          CameraModel.name:cameraDto.name,
                                                          CameraModel.restreamEndpoint:cameraDto.restreamEndpoint,
                                                          CameraModel.state:cameraDto.state,
                                                          })
        super().update( cameraDto)
    def create_or_update_cam(self, cameraDto: CameraDTO):
        
        

        if not bool(self.session.query(CameraModel).filter_by(id=cameraDto.id).first()):
            
            camera_model = CameraModel().entity_to_model(cameraDto,CameraModel,)
            self.save(camera_model)
        else:
            
            self.update(cameraDto)     
    def load_from_api(self):
        
        api_url = "http://192.168.1.212:48080/api/cameras" 
        headers= {
            "Id":"alo"
        }
        
        res = requests.get(url = api_url, headers=headers)
        cameras = res.json()
        print("X-cameras", cameras)
        
        for camera in cameras:
            
            
            self.create_or_update_cam(CameraDTO( int(camera["id"]), camera["activate"], camera["name"], camera["restreamEndpoint"], camera["state"]))
            print('camera["serviceIds"]', camera["serviceIds"])
            for service_id in camera["serviceIds"]:
                process_ai = ProcessAIRepository(self.session)
                # process_ai = ProcessAIRepository[ProcessAIModel](self.session)
                
                
                print(123456, service_id, " ", camera["id"])
                process_ai.update_cam( service_id, camera["id"])
    def update_or_create_cam_wss(self, ai_service_id):
        
        async def start_websocket(wss_url: str):
            print("wss_url",wss_url)
            async with websockets.connect(wss_url) as ws: 
                while True:
                    msg = await ws.recv()
                   
                    data = json.loads(json.loads(msg)["data"])
                    print(data)
                    
                    self.create_or_update_cam(CameraDTO(int(data["id"]), data["activate"], data["name"], data["restreamEndpoint"], data["state"]))
                    
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
#     camera = CameraRepository()
#     camera.load_from_api(engine, api_url)

