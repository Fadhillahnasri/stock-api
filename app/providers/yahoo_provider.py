import yfinance as yf

from app.utils.logger import logger


def fetch_stock(symbol: str) -> dict | None:
    """
    Mengambil data harga saham dari Yahoo Finance.
    """

    try:

        logger.info(f"Yahoo Provider - Fetch Stock: {symbol}")

        stock = yf.Ticker(symbol.upper())
        info = stock.info

        if not info:
            return None

        return {
            "symbol": symbol.upper(),
            "company_name": info.get("longName"),
            "current_price": info.get("currentPrice"),
            "high": info.get("dayHigh"),
            "low": info.get("dayLow"),
            "open": info.get("open"),
            "previous_close": info.get("previousClose"),
            "change": info.get("regularMarketChange"),
            "change_percent": info.get("regularMarketChangePercent")
        }

    except Exception as e:

        logger.exception(e)

        return None


def fetch_company(symbol: str) -> dict | None:
    """
    Mengambil profil perusahaan dari Yahoo Finance.
    """

    try:

        logger.info(f"Yahoo Provider - Fetch Company: {symbol}")

        stock = yf.Ticker(symbol.upper())
        info = stock.info

        if not info:
            return None

        return {

            "symbol": symbol.upper(),
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "currency": info.get("currency")
        }

    except Exception as e:

        logger.exception(e)

        return None