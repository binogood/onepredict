from abc import ABCMeta, abstractmethod
from typing import Optional

from app.user.models.user_car import UserCar
from app.user.repository.user import UserFakeRepo
from app.car.repository.car import CarFakeRepo

from core.db.session import session


class UserCarRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_user_car(self, car_id: int, user_id: int) -> Optional[UserCar]:
        pass

    @abstractmethod
    async def save(self, user_car: UserCar) -> UserCar:
        pass


class UserCarMySQLRepo(UserCarRepo):
    async def get_by_user_car(self, car_id: int, user_id: int) -> Optional[UserCar]:
        return session.query(UserCar).filter(
                    UserCar.user_id == user_id,
                    UserCar.car_id == car_id
                ).first()

    async def save(self, user_car: UserCar) -> UserCar:
        session.add(user_car)
        return user_car


class UserCarFakeRepo(UserCarRepo):
    user_cars = []
    user_car_id = 1

    def __init__(self):
        pass

    async def get_by_user_car(self, car_id: int, user_id: int) -> Optional[UserCar]:
        for item_user_car in UserCarFakeRepo.user_cars:
            if item_user_car.car_id == car_id and item_user_car.user_id == user_id:
                return item_user_car

    async def save(self, user_car: UserCar) -> UserCar:
        user_car.user_car_id = UserCarFakeRepo.user_car_id
        UserCarFakeRepo.user_car_id += 1
        UserCarFakeRepo.user_cars.append(user_car)
        print(UserCarFakeRepo.user_cars)
        return user_car