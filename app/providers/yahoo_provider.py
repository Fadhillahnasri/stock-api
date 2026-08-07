import yfinance as yf

from app.providers.base_provider import BaseProvider
from app.utils.logger import logger


class YahooProvider(BaseProvider):

    def get_stock_price(self, symbol: str):

        try:
            symbol = symbol.upper()

            logger.info(
                f"Yahoo Provider - Get Stock Price: {symbol}"
            )

            stock = yf.Ticker(symbol)
            info = stock.info

            if not info:
                return None

            return {
                "symbol": symbol,
                "company_name": info.get("longName"),
                "current_price": info.get("currentPrice"),
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

        except Exception as e:

            logger.exception(
                f"Yahoo Provider Error - Stock {symbol}: {e}"
            )

            return None

    def get_company_profile(self, symbol: str):

        try:
            symbol = symbol.upper()

            logger.info(
                f"Yahoo Provider - Get Company Profile: {symbol}"
            )

            stock = yf.Ticker(symbol)
            info = stock.info

            if not info:
                return None

            return {
                "symbol": symbol,
                "company_name": info.get("longName"),
                "exchange": info.get("exchange"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "employees": info.get("fullTimeEmployees"),
                "currency": info.get("currency")
            }

        except Exception as e:

            logger.exception(
                f"Yahoo Provider Error - Company {symbol}: {e}"
            )

            return None