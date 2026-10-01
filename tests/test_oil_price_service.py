from app.services.macro_service import get_oil_price


def test_get_oil_price():
    result = get_oil_price(
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


def test_get_oil_price_empty():
    result = get_oil_price(
        start_date="2030-01-01",
        end_date="2030-01-31"
    )

    assert result["data"] == []