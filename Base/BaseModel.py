import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, joinedload

from sqlalchemy.exc import IntegrityError

from Base.BaseDto import BaseDto
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
   
    def model_to_entity(self,cls: any ,dto) -> dict:
        
        filtered_data = {key: value for key,
                         value in cls.__dict__.items() if hasattr(dto, key)}
        return dto(**filtered_data)


    def entity_to_model(self ,dto: dict, cls) -> any:
        print(cls)
        filtered_model = {key: value for key,
                         value in dto.__dict__.items() if hasattr(cls, key)}
        return cls(**filtered_model)
    

    