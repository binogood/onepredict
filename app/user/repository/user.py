import datetime

from abc import ABCMeta, abstractmethod
from typing import Optional, List

from app.user.models.user import User
from core.db.session import session


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass


class UserMySQLRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return session.query(User).filter(User.user_id == user_id).first()

    async def get_by_name(self, name: str) -> Optional[User]:
        return session.query(User).filter(User.name == name).first()

    async def save(self, user: User) -> User:
        session.add(user)
        return user


class UserFakeRepo(UserRepo):
    users: List = []
    db_user_id: int = 1
    created_at: datetime = datetime.datetime.now()
    updated_at: datetime = datetime.datetime.now()

    def __init__(self):
        pass

    async def get_by_id(self, user_id: int) -> Optional[User]:
        for item_id in UserFakeRepo.users:
            if item_id.user_id == user_id:
                return item_id

    async def get_by_name(self, name: str) -> Optional[User]:
        for item_name in UserFakeRepo.users:
            if item_name.name == name:
                return item_name

    async def save(self, user: User) -> User:
        user.is_admin = True
        user.user_id = UserFakeRepo.db_user_id
        user.created_at = UserFakeRepo.created_at
        user.updated_at = UserFakeRepo.updated_at
        UserFakeRepo.db_user_id += 1
        UserFakeRepo.users.append(user)
        print(UserFakeRepo.users)
        return user
