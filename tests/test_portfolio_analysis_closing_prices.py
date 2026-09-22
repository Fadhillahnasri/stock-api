from app.services import portfolio_analysis_service


def test_get_all_closing_prices(monkeypatch):
    responses = {
        1: {
            "totalPage": 2,
            "data": [
                {
                    "stockCode": "BBCA",
                    "stockName": "Bank Central Asia Tbk",
                    "closingPrice": 8250,
                }
            ],
        },
        2: {
            "totalPage": 2,
            "data": [
                {
                    "stockCode": "BBRI",
                    "stockName": "Bank Rakyat Indonesia Tbk",
                    "closingPrice": 4370,
                }
            ],
        },
    }

    def mock_get_closing_prices(params=None):
        return responses[params["page"]]

    monkeypatch.setattr(
        portfolio_analysis_service,
        "get_closing_prices",
        mock_get_closing_prices,
    )

    result = portfolio_analysis_service.get_all_closing_prices(
        date="2026-05-26"
    )

    assert len(result) == 2
    assert result[0]["stockCode"] == "BBCA"
    assert result[1]["stockCode"] == "BBRI"