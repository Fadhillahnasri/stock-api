import yfinance as yf


from app.utils.logger import logger

def get_stock_price(symbol: str) -> dict | None:
    """
    Mengambil data harga saham berdasarkan simbol.
    """

    try:

        logger.info(f"Fetching stock data: {symbol}")

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

        logger.exception(f"Error fetching stock {symbol}: {e}")

        return None


def get_multiple_stocks(symbols: list[str]) -> dict:
    """
    Mengambil data beberapa saham sekaligus.
    """

    stocks = []
    failed = []

    for symbol in symbols:

        data = get_stock_price(symbol)

        if data:

            stocks.append(data)

        else:

            failed.append(symbol)

    return {

        "total": len(stocks),

        "failed": failed,

        "data": stocks
    }

def get_company_profile(symbol: str) -> dict | None:
    """
    Mengambil profil perusahaan berdasarkan simbol saham.
    """

    try:

        logger.info(f"Fetching company profile: {symbol}")

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

        logger.exception(f"Error fetching company profile {symbol}: {e}")

        return None