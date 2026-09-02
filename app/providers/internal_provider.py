from app.config import settings
from app.providers.base_provider import BaseProvider
from app.core.http_client import HttpClient
from app.utils.logger import logger
from app.exceptions.provider_exceptions import ProviderError


class InternalProvider(BaseProvider):

    def __init__(self):

        self.client = HttpClient()
        self.base_url = settings.INTERNAL_API_BASE_URL

    def get_stock_price(self, symbol: str):

        symbol = symbol.upper()

        logger.info(
            f"Internal Provider - Get Stock Price: {symbol}"
        )

        raise ProviderError(
            "Internal Provider belum diimplementasikan."
        )

    def get_company_profile(self, symbol: str):

        symbol = symbol.upper()

        logger.info(
            f"Internal Provider - Get Company Profile: {symbol}"
        )

        raise NotImplementedError(
            "Internal Provider belum diimplementasikan."
        )