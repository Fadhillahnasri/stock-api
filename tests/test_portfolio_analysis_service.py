from app.services import portfolio_analysis_service


def test_get_portfolio_analysis(monkeypatch):
    expected = {
        "status": "success",
        "message": "Successfully retrieve index report",
        "data": [
            {
                "stockCode": "BBCA",
                "marketValue": "22101750000",
                "unrealizedgainorloss": "-6669828605.43",
            },
            {
                "stockCode": "BBRI",
                "marketValue": "21850060000",
                "unrealizedgainorloss": "-8943980970.00",
            },
        ],
    }

    monkeypatch.setattr(
        portfolio_analysis_service,
        "get_index_report",
        lambda: expected
    )

    result = portfolio_analysis_service.get_portfolio_analysis()

    assert result["totalMarketValue"] == 43951810000
    assert result["totalUnrealizedGainLoss"] == -15613809575.43