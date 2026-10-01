from app.providers.macro_provider import MacroProvider


def test_get_oil_price():
    provider = MacroProvider()

    result = provider.get_oil_price(
        start_date="2025-09-01",
        end_date="2026-09-29"
    )

    assert result is not None
    assert result["indicator"] == "WTI Oil Price"
    assert result["source"] == (
        "U.S. Energy Information Administration"
    )
    assert result["unit"] == "USD/barrel"
    assert len(result["data"]) > 0


def test_get_oil_price_date_filter():
    provider = MacroProvider()

    result = provider.get_oil_price(
        start_date="2026-09-01",
        end_date="2026-09-29"
    )

    assert result is not None

    for item in result["data"]:
        assert "2026-09-01" <= item["date"] <= "2026-09-29"