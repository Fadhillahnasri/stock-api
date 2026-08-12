from app.providers.base_provider import BaseProvider
from app.providers.yahoo_provider import YahooProvider
from app.providers.internal_provider import InternalProvider


def get_provider(provider_name: str) -> BaseProvider:

    provider_name = provider_name.lower()

    if provider_name == "yahoo":
        return YahooProvider()

    if provider_name == "internal":
        return InternalProvider()

    raise ValueError(
        f"Unknown provider: {provider_name}"
    )