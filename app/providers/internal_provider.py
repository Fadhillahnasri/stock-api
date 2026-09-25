from fastapi import params

from app.config import settings
from app.providers.base_provider import BaseProvider
from app.core.http_client import HttpClient
from app.utils.logger import logger
from app.exceptions.provider_exceptions import ProviderError


class InternalProvider(BaseProvider):

    def __init__(self):
        self.client = HttpClient()
        self.base_url = settings.INTERNAL_API_BASE_URL

    def _get(self, path: str, params: dict | None = None):
        if not self.base_url:
            raise ProviderError(
                "Internal API Base URL belum dikonfigurasi."
            )

        if not settings.INTERNAL_API_TOKEN:
            raise ProviderError(
                "Internal API Token belum dikonfigurasi."
            )

        url = f"{self.base_url}{path}"


        logger.info(f"Internal API GET - {url}")

        response = self.client.get(
            url,
            params=params,
    
        )

        return response.json()

    def get_portfolios(self):
        return self._get("/api/portfolios")

    def get_stocks(self, params: dict | None = None):
        return self._get("/api/stocks", params=params)

    def get_closing_prices(self, params: dict | None = None):
        return self._get("/api/closing-prices", params=params)

    def get_index_prices(self, params: dict | None = None):
        return self._get("/api/index-prices", params=params)

    def get_index_report(self, params: dict | None = None):
        return self._get("/api/report/index", params=params)

    def get_trading_report(self, params: dict | None = None):
        return self._get("/api/report/trading", params=params)

    def get_transactions(self, params: dict | None = None):
        return self._get("/api/transactions", params=params)

    def get_stock_price(self, symbol: str):
        raise ProviderError(
            "Internal Provider get_stock_price belum diimplementasikan."
        )

    def get_company_profile(self, symbol: str):
        raise ProviderError(
            "Internal Provider get_company_profile belum diimplementasikan."
        )

    def get_historical_prices(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ):
        raise ProviderError(
            "Internal Provider get_historical_prices belum diimplementasikan."
        )