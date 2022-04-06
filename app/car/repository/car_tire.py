from abc import ABCMeta, abstractmethod
from typing import Optional, List, Dict

from app.car.models.car_tire import CarTire
from app.car.models.car import Car
from app.tire.models.tire import Tire
from app.tire.repository.tire import TireFakeRepo
from app.car.repository.car import CarFakeRepo
from core.db.session import session
from core.const.const import FRONT



class CarTireRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_car_tire(self, car_id: int, tire_id: int) -> Optional[CarTire]:
        pass

    async def get_by_car_tire_info(self, trim_id: int):
        pass

    @abstractmethod
    async def save(self, car_tire: CarTire) -> CarTire:
        pass


class CarTireMySQLRepo(CarTireRepo):
    async def get_by_car_tire(self, car_id: int, tire_id: int) -> Optional[CarTire]:
        return session.query(CarTire).filter(
                    CarTire.car_id == car_id,
                    CarTire.tire_id == tire_id,
                ).first()

    async def get_by_car_tire_info(self, trim_id: int) -> Dict:
        tire_dict = {}
        tire_list = session.query(Tire.value, Tire.tire_type_id).\
            join(CarTire, CarTire.tire_id == Tire.tire_id).join(Car, Car.car_id == CarTire.car_id).\
            filter(Car.trim_id == trim_id).filter(Car.car_id == CarTire.car_id).all()

        for tire in tire_list:
            if tire[1] == FRONT:
                tire_dict['front'] = tire[0]
            tire_dict['rear'] = tire[0]

        return tire_dict

    async def save(self, car_tire: CarTire) -> CarTire:
        session.add(car_tire)
        return car_tire


class CarTireFakeRepo(CarTireRepo):
    car_tires: List = []
    car_tire_id = 1

    def __init__(self):
        pass

    async def get_by_car_tire(self, car_id: int, tire_id: int) -> Optional[CarTire]:
        for item_car_tire in CarTireFakeRepo.car_tires:
            if item_car_tire.car_id == car_id and item_car_tire.tire_id == tire_id:
                return item_car_tire

    async def get_by_car_tire_info(self, trim_id: int) -> dict:
        car_tire_info = await self._car_tire_list(trim_id=trim_id)
        return car_tire_info

    async def save(self, car_tire: CarTire) -> CarTire:
        car_tire.car_tire_id = CarTireFakeRepo.car_tire_id
        CarTireFakeRepo.car_tire_id += 1
        CarTireFakeRepo.car_tires.append(car_tire)
        print(CarTireFakeRepo.car_tires)
        return car_tire

    async def _car_tire_list(self, trim_id: int):
        _car_info = self._car_info_get(trim_id=trim_id)
        _car_tire_info = self._tire_info_get(car_info=_car_info)
        return _car_tire_info

    def _tire_info_get(self, car_info):
        _tire_info_dict = {}
        for _car_tire in CarTireFakeRepo.car_tires:
            if car_info.car_id == _car_tire.car_id:
                for _tire in TireFakeRepo.tires:
                    if _tire.tire_id == _car_tire.tire_id:
                        if _tire.tire_type_id == FRONT:
                            _tire_info_dict['front'] = _tire.value
                        _tire_info_dict['rear'] = _tire.value

        return _tire_info_dict

    def _car_info_get(self, trim_id: int):
        for car in CarFakeRepo.cars:
            if car.trim_id == trim_id:
                return car


