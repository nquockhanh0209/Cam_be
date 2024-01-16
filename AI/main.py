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
    
    def __init__(self, 
                pid
                ):
      
        self.pid = pid
def insert_new_pid(engine, pid):
    Session = sessionmaker(bind= engine)
    session = Session()
    process_id = ProcessAI(pid)
    session.add(process_id)
    session.commit()       
def task(engine):
    subprocess.run(["./test.sh"]).stdout

    pid = getppid()
    print(pid)
    insert_new_pid(engine,pid)
    
 
# protect the entry point
if __name__ == '__main__':
    
    engine = create_engine("sqlite:///database.db", echo = True)
    Base.metadata.create_all(bind= engine)

    child = Process(target=task, args=(engine,))

    child.start()

    child.join()