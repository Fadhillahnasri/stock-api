from app.core.http_client import HttpClient

client = HttpClient()


def fetch_stock(symbol: str):
    raise NotImplementedError(
        "Internal Provider belum diimplementasikan."
    )


def fetch_company(symbol: str):
    raise NotImplementedError(
        "Internal Provider belum diimplementasikan."
    )