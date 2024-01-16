import subprocess
from multiprocessing import Process
from os import getppid
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean, PickleType,Enum, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class ProcessAI(Base):
    __tablename__ = "process_ai"
    pid = Column(Integer, primary_key=True, nullable=False)
    
    # def __init__(self):
      
    #     self.pid = pid
   
         
    def start(self, engine):
        subprocess.run(["./test.sh"]).stdout
        self.pid = getppid()
        print(self.pid)
        Session = sessionmaker(bind= engine)
        session = Session()
        process_id = self
        session.add(process_id)
        session.commit()
      

    
 
# protect the entry point
if __name__ == '__main__':
    
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)
    def start_process(engine):
        process_ai = ProcessAI()
        process_ai.start(engine)
    child = Process(target=start_process, args=(engine,))

    child.start()

    child.join()