from abc import abstractmethod, ABC

from domain.asset.asset import Asset
from domain.user.user import User


class AssetPersistenceInterface(ABC):


    @abstractmethod
    def get_all(self, new_user: User) -> list[Asset]:
        pass



    @abstractmethod
    def add(self, user, units):
        pass

    @abstractmethod
    def get_for_user(self, u):
        pass

    @abstractmethod
    def add_to_user(self, user, asset):
        pass