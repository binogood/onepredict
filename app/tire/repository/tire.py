from abc import ABCMeta, abstractmethod
from typing import Optional, List

from app.tire.models.tire import Tire
from core.db.session import session


class TireRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_tire(self, value: str, tire_type_id: int) -> Optional[Tire]:
        pass

    async def get_by_tire_id(self, tire_id: int) -> Optional[Tire]:
        pass

    @abstractmethod
    async def save(self, tire: Tire) -> Tire:
        pass


class TireMySQLRepo(TireRepo):
    async def get_by_tire(self, value: str, tire_type_id: int) -> Optional[Tire]:
        return session.query(Tire).filter(
            Tire.value == value,
            Tire.tire_type_id == tire_type_id
        ).first()

    async def get_by_tire_id(self, tire_id: int) -> Optional[Tire]:
        return session.query(Tire.tire_id).filter(Tire.tire_id == tire_id)

    async def save(self, tire: Tire) -> Tire:
        session.add(tire)
        return tire


class TireFakeRepo(TireRepo):
    tires: List = []
    db_tire_id: int = 1

    def __init__(self):
        pass

    async def get_by_tire(self, value: str, tire_type_id: int) -> Optional[Tire]:
        for item_tire in TireFakeRepo.tires:
            if item_tire.value == value and item_tire.tire_type_id == tire_type_id:
                return item_tire

    async def get_by_tire_id(self, tire_id: int) -> Optional[Tire]:
        for item_tire_id in TireFakeRepo.tires:
            if item_tire_id.tire_id == tire_id:
                return item_tire_id

    async def save(self, tire: Tire) -> Tire:
        tire.tire_id = TireFakeRepo.db_tire_id
        TireFakeRepo.db_tire_id += 1
        TireFakeRepo.tires.append(tire)
        print(TireFakeRepo.tires)
        return tire





