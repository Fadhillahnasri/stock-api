from app.providers.base_provider import BaseProvider
from app.providers.yahoo_provider import YahooProvider


def get_provider(provider_name: str) -> BaseProvider:

    provider_name = provider_name.lower()

    if provider_name == "yahoo":
        return YahooProvider()

    raise ValueError(
        f"Unknown provider: {provider_name}"
    )