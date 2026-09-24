from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def get_stock_price(self, symbol: str):
        pass

    @abstractmethod
    def get_company_profile(self, symbol: str):
        pass

    @abstractmethod
    def get_historical_prices(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ):
        pass