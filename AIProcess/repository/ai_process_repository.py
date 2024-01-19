import subprocess
from multiprocessing import Process
from os import getppid
from sqlalchemy import create_engine, Column, String, Integer,  PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Base.BaseRepository import AbstractRepository
from AIProcess.dto.ai_process_dto import AIProcessDTO
from AIProcess.model.ai_process_model import ProcessAIModel


class ProcessAIRepository(AbstractRepository):
    # def model_to_entity(self,model: ProcessAIModel) -> AIProcessDTO:
        

    #     return AIProcessDTO(
    #         id=model.id,
    #         service_id=model.service_id,
    #         camera_ids = model.camera_ids   
    #     )

    # def entity_to_model(self,dto: AIProcessDTO, existing=None) -> ProcessAIModel:
        

    #     return ProcessAIModel(
    #         id=dto.id,
    #         service_id=dto.service_id,
    #         camera_ids = dto.camera_ids  
    #     )
    def start(self, service_id: int):
        
        
        subprocess.run(["./test.sh"]).stdout
        pid = getppid()
        ai_process_model = ProcessAIModel()
        ai_process = ai_process_model.entity_to_model(AIProcessDTO(pid, service_id, []), ProcessAIModel,)
        self.save(ai_process)
        

    def update_cam(self, service_id: int, camera_id: int):
        print("ProcessAIModel", ProcessAIModel)
        if bool(self.session.query(ProcessAIModel).filter_by(service_id = service_id).first()):
            
            service = self.session.query(ProcessAIModel).filter_by(service_id = service_id).first()
            # .update({ProcessAI.camera_ids: ProcessAI.camera_ids + camera_id})
                       
            if service.camera_ids != None:
                
                new_cam_ids = service.camera_ids
                new_cam_ids.append(camera_id)
                service.camera_ids = new_cam_ids
                self.session.commit()
    
            else:
                new_cam_ids = [camera_id]
                service.camera_ids = new_cam_ids
                self.session.commit()
    
 
# # protect the entry point
# if __name__ == '__main__':
    
#     engine = create_engine("sqlite:///database.db", echo = True)
#     Base.metadata.create_all(bind= engine)
#     def start_process(engine,id):
#         process_ai = ProcessAI()
#         process_ai.start(engine,id)
#     child = Process(target=start_process, args=(engine,12,))

#     child.start()

#     child.join()