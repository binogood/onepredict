from pythondi import Provider, configure
from app.user.repository.user import UserRepo, UserMySQLRepo, UserFakeRepo
from app.user.repository.user_car import UserCarRepo, UserCarMySQLRepo, UserCarFakeRepo
from app.tire.repository.tire import TireRepo, TireMySQLRepo, TireFakeRepo
from app.tire.repository.tire_type import TireTypeRepo, TireTypeMySQLRepo, TireTypeFakeRepo
from app.car.repository.car import CarRepo, CarMySQLRepo, CarFakeRepo
from app.car.repository.car_tire import CarTireRepo, CarTireMySQLRepo, CarTireFakeRepo


def init_di():
    provider = Provider()
    provider.bind(UserRepo, UserMySQLRepo)
    provider.bind(UserCarRepo, UserCarMySQLRepo)
    provider.bind(TireRepo, TireMySQLRepo)
    provider.bind(TireTypeRepo, TireTypeMySQLRepo)
    provider.bind(CarRepo, CarMySQLRepo)
    provider.bind(CarTireRepo, CarTireMySQLRepo)
    configure(provider=provider)


def fake_init_di():
    provider = Provider()
    provider.bind(UserRepo, UserFakeRepo)
    provider.bind(UserCarRepo, UserCarFakeRepo)
    provider.bind(TireRepo, TireFakeRepo)
    provider.bind(TireTypeRepo, TireTypeFakeRepo)
    provider.bind(CarRepo, CarFakeRepo)
    provider.bind(CarTireRepo, CarTireFakeRepo)
    configure(provider=provider)