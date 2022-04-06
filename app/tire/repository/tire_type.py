from abc import ABCMeta, abstractmethod
from typing import Optional, List

from app.tire.models.tire_type import TireType
from core.db.session import session


class TireTypeRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_tire_type(self, name: str) -> Optional[TireType]:
        pass

    @abstractmethod
    async def save(self, tire_type: TireType) -> TireType:
        pass


class TireTypeMySQLRepo(TireTypeRepo):
    async def get_by_tire_type(self, name: str) -> Optional[TireType]:
        return session.query(TireType).filter(TireType.name == name).first()

    async def save(self, tire_type: TireType) -> TireType:
        session.add(tire_type)
        return tire_type


class TireTypeFakeRepo(TireTypeRepo):
    tire_types: List = []
    db_tire_types_id = 1

    async def get_by_tire_type(self, name: str) -> Optional[TireType]:
        for item_tire_type in TireTypeFakeRepo.tire_types:
            if item_tire_type.name == name:
                return item_tire_type

    async def save(self, tire_type: TireType) -> TireType:
        tire_type.tire_type_id = TireTypeFakeRepo.db_tire_types_id
        TireTypeFakeRepo.db_tire_types_id += 1
        TireTypeFakeRepo.tire_types.append(tire_type)
        print(TireTypeFakeRepo.tire_types)
        return tire_type