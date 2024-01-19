from sqlalchemy import create_engine, Table, Column, String, Integer,  PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only
from AIService.repository.ai_service_repository import ServiceAIRepository
from AIService.dto.ai_service_dto import AIServiceDTO
from Camera.model.camera_model import CameraModel
from Camera.repository.camera_repository import CameraRepository
from sqlalchemy import MetaData
from datetime import datetime, timezone
import subprocess
from multiprocessing import Process
from sqlalchemy.orm import sessionmaker
from AIService.model.ai_service_model import ServiceAIModel
from alembic.migration import MigrationContext
from alembic.operations import Operations
Base = declarative_base()
def upgrade(engine):
    mc = MigrationContext.configure(engine.connect())

    # Creation operations object
    ops = Operations(mc)
    ops.alter_column('process_ai', 'pid', new_column_name='id')
def drop_table(table_name, engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)


# def create_table(table_name, engine):
#     metadata = MetaData()
#     metadata.reflect(bind=engine)
#     # table = metadata.tables[table_name]
#     if table is not None:
#         Base.metadata.create(engine, [table], checkfirst=True)

def start_ai_service():
    Session = sessionmaker(bind= engine)
    session = Session()   
    # service_ai = ServiceAIRepository[ServiceAIModel](session)
    service_ai = ServiceAIRepository(session)
    

    
     
    # session.query(ServiceAIModel).delete()
    # session.commit()
    def create_service( ai_service_dto: AIServiceDTO):
        
        service_ai.create_service( ai_service_dto)
    # name= "NewService"
    # type="HUMAN_AI" 
    # hostName = "cerberus"
    # ipAddress= "192.168.1.212:48080/" 
    # macAddress= "a8:a1:59:d5:61:55" 
    # heartbeat = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    ai_service_dto = AIServiceDTO(0, 
                                  "NewService", 
                                  "HUMAN_AI", 
                                  "cerberus",
                                  "192.168.1.212:48080/" ,
                                  "a8:a1:59:d5:61:55" ,
                                  datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
                                  "CONNECTED",
                                  [])

    thread = Process(target=create_service, args=( ai_service_dto,))

    thread.start()

    thread.join()
def start_update_or_create_cam_wss():
    Session = sessionmaker(bind= engine)
    session = Session()
    def update_or_create_cam_wss():

        ai_service_ids = session.query(ServiceAIModel.id).all()

        
        for ai_service_id in ai_service_ids:
            
            
            # camera_repo = CameraRepository[CameraModel](session)
            camera_repo = CameraRepository(session)
            
            
            camera_repo.update_or_create_cam_wss(ai_service_id[0])
    thread = Process(target=update_or_create_cam_wss)

    thread.start()

    thread.join()
def get_cam_data():
    Session = sessionmaker(bind= engine)
    session = Session()
    def load_from_api():
        camera = CameraRepository(session)
        # camera = CameraRepository[CameraModel](session)
        
        camera.load_from_api()
    thread = Process(target=load_from_api)

    thread.start()

    thread.join()
if __name__ == '__main__':
    
    
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    
    # drop_table('service_ai', engine)
    # ServiceAIModel.__table__.create(engine)
    start_ai_service()
    get_cam_data()
    start_update_or_create_cam_wss()
    # upgrade(engine)
    
    
    
    