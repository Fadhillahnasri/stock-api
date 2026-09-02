import yfinance as yf

from app.providers.base_provider import BaseProvider
from app.exceptions.provider_exceptions import (
    ProviderError,
    ProviderTimeoutError,
    ProviderConnectionError
)
from app.utils.logger import logger


class YahooProvider(BaseProvider):

    def get_stock_price(self, symbol: str):

        symbol = symbol.upper()

        try:

            logger.info(
                f"Yahoo Provider - Get Stock Price: {symbol}"
            )

            stock = yf.Ticker(symbol)
            info = stock.info

            if not info:
                return None

            current_price = info.get("currentPrice")
            company_name = info.get("longName")

            if current_price is None or company_name is None:

                logger.warning(
                    f"Yahoo Provider - Invalid Stock: {symbol}"
                )

                return None

            return {
                "symbol": symbol,
                "company_name": company_name,
                "current_price": current_price,
                "high": info.get("dayHigh"),
                "low": info.get("dayLow"),
                "open": info.get("open"),
                "previous_close": info.get("previousClose"),
                "change": info.get("regularMarketChange"),
                "change_percent": info.get(
                    "regularMarketChangePercent"
                ),
                "currency": info.get("currency"),
                "exchange": info.get("exchange"),
                "market_state": info.get("marketState")
            }

        except TimeoutError as e:

            logger.exception(
                f"Yahoo Provider Timeout - Stock {symbol}: {e}"
            )

            raise ProviderTimeoutError(
                "Yahoo Finance request timed out"
            )

        except ConnectionError as e:

            logger.exception(
                f"Yahoo Provider Connection Error - Stock {symbol}: {e}"
            )

            raise ProviderConnectionError(
                "Unable to connect to Yahoo Finance"
            )

        except Exception as e:

            logger.exception(
                f"Yahoo Provider Error - Stock {symbol}: {e}"
            )

            raise ProviderError(
                f"Yahoo Finance error for {symbol}"
            )

    def get_company_profile(self, symbol: str):

        symbol = symbol.upper()
        
        try:
            logger.info(
                f"Yahoo Provider - Get Company Profile: {symbol}"
            )
            stock = yf.Ticker(symbol)
            info = stock.info

            if not info:
                return None

            company_name = info.get("longName")

            if not company_name:
                logger.warning(
                    f"Yahoo Provider - Invalid Company: {symbol}"
                )
                return None

            return {
                "symbol": symbol,
                "company_name": company_name,
                "exchange": info.get("exchange"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "employees": info.get("fullTimeEmployees"),
                "currency": info.get("currency")
            }

        except TimeoutError as e:
            logger.exception(
                f"Yahoo Provider Timeout - Company {symbol}: {e}"
            )
            raise ProviderTimeoutError(
                "Yahoo Finance request timed out"
            )

        except ConnectionError as e:
            logger.exception(
                f"Yahoo Provider Connection Error - Company {symbol}: {e}"
            )
            raise ProviderConnectionError(
                "Unable to connect to Yahoo Finance"
            )

        except Exception as e:
            logger.exception(
                f"Yahoo Provider Error - Company {symbol}: {e}"
            )
            raise ProviderError(
                f"Yahoo Finance error for company {symbol}"
            )