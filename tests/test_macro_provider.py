from app.providers.macro_provider import MacroProvider


def test_get_exchange_rate():
    provider = MacroProvider()

    result = provider.get_exchange_rate(
        currency="USD",
        start_date="2026-09-28",
        end_date="2026-09-29"
    )

    assert result["currency"] == "USD"

    assert len(result["data"]) == 2

    assert result["data"][0]["date"] == "2026-09-28"
    assert result["data"][0]["value"] == 17965.0

    assert result["data"][1]["date"] == "2026-09-29"
    assert result["data"][1]["value"] == 17998.0


def test_get_exchange_rate_date_filter():
    provider = MacroProvider()

    result = provider.get_exchange_rate(
        currency="USD",
        start_date="2026-09-29",
        end_date="2026-09-29"
    )

    assert len(result["data"]) == 1

    assert result["data"][0]["date"] == "2026-09-29"
    assert result["data"][0]["value"] == 17998.0


def test_get_exchange_rate_empty_data():
    provider = MacroProvider()

    result = provider.get_exchange_rate(
        currency="USD",
        start_date="2026-10-01",
        end_date="2026-10-05"
    )

    assert result["currency"] == "USD"
    assert result["data"] == []