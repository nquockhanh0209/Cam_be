import abc
from typing import Set

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, joinedload
from typing import List, TypeVar, Generic
from Base.BaseModel import BaseModel
ModelT = TypeVar('ModelT')
class AbstractRepository(abc.ABC):
    def __init__(self, session):
        self.seen = set()  # type: Set[BaseModel]

        self.session = session

    # @abc.abstractmethod
    # def _add(self, model: BaseModel):
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def _get(self, sku) -> BaseModel:
    #     raise NotImplementedError
    
    # @abc.abstractmethod
    # def model_to_entity(cls: ModelT ,dto) -> dict:
        
    #     filtered_data = {key: value for key,
    #                      value in cls.items() if hasattr(dto, key)}
    #     return dto(**filtered_data)

    # @abc.abstractmethod
    # def entity_to_model(cls ,dto: dict) -> ModelT:
        
    #     filtered_model = {key: value for key,
    #                      value in dto.items() if hasattr(cls, key)}
    #     return cls(**filtered_model)
    
    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, model, commit=True):
        self.before_save()
        self.session.add(model)
        if commit:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e

        self.after_save()


    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        self.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        self.session.delete(self)
        if commit:
            self.session.commit()  
    @classmethod
    # Ex: Model.eager('rel1', 'rel2').all()
    def eager(cls, *args):
        cols = [joinedload(arg) for arg in args]
        return cls.query.options(*cols)
    
    # @classmethod
    # def before_bulk_create(cls, iterable, *args, **kwargs):
    #     pass

    # @classmethod
    # def after_bulk_create(cls, model_objs, *args, **kwargs):
    #     pass


    # @classmethod
    
    # Ex: >>> user_dicts = [
    # ...     {'username': 'user1010', 'password_hash': 'some_hash'},
    # ...     {'username': 'user1011', 'password_hash': 'some_hash'},
    # ...     {'username': 'user1012', 'password_hash': 'some_hash'},
    # ...     {'username': 'user1013', 'password_hash': 'some_hash'},
    # ... ]
    # >>> users  = User.bulk_create(user_dicts)
    # def bulk_create(cls, iterable, *args, **kwargs):
    #     cls.before_bulk_create(iterable, *args, **kwargs)
    #     model_objs = []
    #     for data in iterable:
    #         if not isinstance(data, cls):
    #             data = cls(**data)
    #         model_objs.append(data)

    #     self.session.bulk_save_objects(model_objs)
    #     if kwargs.get('commit', True) is True:
    #         self.session.commit()
    #     cls.after_bulk_create(model_objs, *args, **kwargs)
    #     return model_objs


    # @classmethod
    # def bulk_create_or_none(cls, iterable, *args, **kwargs):
    #     try:
    #         return cls.bulk_create(iterable, *args, **kwargs)
    #     except IntegrityError as e:
    #         self.session.rollback()
    #         return None