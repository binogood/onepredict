import datetime

from abc import ABCMeta, abstractmethod
from typing import Optional, List

from app.car.models.car import Car
from core.db.session import session


class CarRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_car_trim(self, trim_id: int) -> Optional[Car]:
        pass

    @abstractmethod
    async def get_by_car_id(self, car_id: int) -> Optional[Car]:
        pass

    @abstractmethod
    async def save(self, car: Car) -> Car:
        pass


class CarMySQLRepo(CarRepo):
    async def get_by_car_trim(self, trim_id: int) -> Optional[Car]:
        return session.query(Car).filter(Car.trim_id == trim_id).first()

    async def get_by_car_id(self, car_id: int) -> Optional[Car]:
        return session.query(Car).filter(Car.car_id == car_id).first()

    async def save(self, car: Car) -> Car:
        session.add(car)
        return car


class CarFakeRepo(CarRepo):
    cars: List = []
    db_car_id = 1
    created_at: datetime = datetime.datetime.now()
    updated_at: datetime = datetime.datetime.now()

    def __init__(self):
        print(CarFakeRepo.cars)

    async def get_by_car_trim(self, trim_id: int) -> Optional[Car]:
        for item_car_trim in CarFakeRepo.cars:
            if item_car_trim.trim_id == trim_id:
                return item_car_trim

    async def get_by_car_id(self, car_id: int) -> Optional[Car]:
        for item_car_id in CarFakeRepo.cars:
            if item_car_id.car_id == car_id:
                return item_car_id

    async def save(self, car: Car) -> Car:
        car.car_id = CarFakeRepo.db_car_id
        car.created_at = CarFakeRepo.created_at
        car.updated_at = CarFakeRepo.updated_at
        CarFakeRepo.db_car_id += 1
        CarFakeRepo.cars.append(car)
        return car