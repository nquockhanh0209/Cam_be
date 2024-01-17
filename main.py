from sqlalchemy import create_engine, Column, String, Integer,  PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only
from AIService.ai_service import *
from Camera.camera import Camera
from sqlalchemy import MetaData
Base = declarative_base()

def drop_table(table_name, engine):
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)


def start_ai_service():
    service_ai = ServiceAI()
    print(service_ai)
    Session = sessionmaker(bind= engine)
    session = Session()
        
    ai_service_ids = session.query(ServiceAI).delete()
    session.commit()
    def create_service(engine, name: str, type: AIServiceType, hostName: str, ipAddress: str, macAddress: str, heartbeat: str):
        
        service_ai.create_service(engine, name, type, hostName, ipAddress, macAddress, heartbeat)
    
    name= "NewService"
    type="HUMAN_AI" 
    hostName = "cerberus"
    ipAddress= "192.168.1.212:48080/" 
    macAddress= "a8:a1:59:d5:61:55" 
    heartbeat = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


    thread = Process(target=create_service, args=(engine,
                                                    
                                                    name,
                                                    type, 
                                                    hostName,
                                                    ipAddress,
                                                    macAddress,
                                                    heartbeat,
                                                    ))

    thread.start()

    thread.join()
def start_update_or_create_cam_wss():
    
    def update_or_create_cam_wss(engine):
        fields = ['id']
        Session = sessionmaker(bind= engine)
        session = Session()
        
        ai_service_ids = session.query(ServiceAI.id).all()
        session.commit()
        print("ai_service_ids",ai_service_ids)
        for ai_service_id in ai_service_ids:
            print(ai_service_id[0])
            
            camera = Camera()
            camera.update_or_create_cam_wss(engine, ai_service_id[0])
    thread = Process(target=update_or_create_cam_wss, args=(engine,))

    thread.start()

    thread.join()
def get_cam_data():
    def load_from_api(engine):
        camera = Camera()
        camera.load_from_api(engine,)
    thread = Process(target=load_from_api, args=(engine,))

    thread.start()

    thread.join()
if __name__ == '__main__':
    
    
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    
    # drop_table('process_ai', engine)
    
    # start_ai_service()
    get_cam_data()
    # start_update_or_create_cam_wss()
    
    
    
    