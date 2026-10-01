from app.providers.macro_provider import MacroProvider


def test_get_bi_rate():
    provider = MacroProvider()

    result = provider.get_bi_rate(
        start_date="2025-09-01",
        end_date="2026-09-29"
    )

    assert result["indicator"] == "BI-Rate"
    assert result["source"] == "Bank Indonesia"
    assert len(result["data"]) == 14


def test_get_bi_rate_date_filter():
    provider = MacroProvider()

    result = provider.get_bi_rate(
        start_date="2026-05-01",
        end_date="2026-06-30"
    )

    assert len(result["data"]) == 3

    assert result["data"][0]["date"] == "2026-05-20"
    assert result["data"][0]["value"] == 5.25

    assert result["data"][1]["date"] == "2026-06-09"
    assert result["data"][1]["value"] == 5.50

    assert result["data"][2]["date"] == "2026-06-18"
    assert result["data"][2]["value"] == 5.75


def test_get_bi_rate_empty_data():
    provider = MacroProvider()

    result = provider.get_bi_rate(
        start_date="2027-01-01",
        end_date="2027-01-31"
    )

    assert result["data"] == []