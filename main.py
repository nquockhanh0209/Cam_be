from sqlalchemy import create_engine, Column, String, Integer,  PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from AIService.ai_service import *
Base = declarative_base()
if __name__ == '__main__':
    
    
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    service_ai = ServiceAI()
    print(service_ai)
    def create_service(engine, name: String, type: AIServiceType, hostName: String, ipAddress: String, macAddress: String, heartbeat: String):
        
        service_ai.create_service(engine, name, type, hostName, ipAddress, macAddress, heartbeat)
    
    name= "NewService"
    type="HUMAN_AI" 
    hostName = "cerberus"
    ipAddress= "192.168.1.212:48080/" 
    macAddress= "a8:a1:59:d5:61:55" 
    heartbeat = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    print("heartbeat", heartbeat)
    
    # create_service(engine,
    #                 api_url,
    #                 name,
    #                 type, 
    #                 hostName,
    #                 ipAddress,
    #                 macAddress,
    #                 heartbeat,
    #                 cameraIds)
    child = Process(target=create_service, args=(engine,
                                                    
                                                    name,
                                                    type, 
                                                    hostName,
                                                    ipAddress,
                                                    macAddress,
                                                    heartbeat,
                                                    ))

    child.start()

    child.join()