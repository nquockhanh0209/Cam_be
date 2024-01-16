import subprocess
from multiprocessing import Process
from os import getppid
from sqlalchemy import create_engine, Column, String, Integer,  PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ProcessAI(Base):
    __tablename__ = "process_ai"
    pid = Column(Integer, primary_key=True, nullable=False)
    service_id = Column(Integer)
    
    def start(self, engine, service_id: int):
        
        Session = sessionmaker(bind= engine)
        session = Session()
        subprocess.run(["./test.sh"]).stdout
        pid = getppid()
        
        self.pid = pid
        self.service_id= service_id
    
        process_id = self
        session.add(process_id)
        session.commit()
    
    

    
 
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