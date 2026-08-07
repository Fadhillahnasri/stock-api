from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def get_stock_price(self, symbol: str):
        pass

    @abstractmethod
    def get_company_profile(self, symbol: str):
        pass