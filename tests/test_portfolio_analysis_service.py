from app.services import portfolio_analysis_service


def test_get_portfolio_analysis(monkeypatch):
    expected = {
        "status": "success",
        "message": "Successfully retrieve index report",
        "data": [
            {
                "stockCode": "BBCA",
                "netAmount": "28771578605.43",
                "marketValue": "22877250000.00",
                "unrealizedgainorloss": "-5894328605.43",
            },
            {
                "stockCode": "BBRI",
                "netAmount": "30794040970.00",
                "marketValue": "22590740000.00",
                "unrealizedgainorloss": "-8203300970.00",
            },
        ],
    }

    monkeypatch.setattr(
        portfolio_analysis_service,
        "get_index_report",
        lambda: expected
    )

    result = portfolio_analysis_service.get_portfolio_analysis()

    assert result["totalCostBasis"] == 59565619575.43
    assert result["totalMarketValue"] == 45467990000
    assert result["totalUnrealizedGainLoss"] == -14097629575.43

    assert round(
        result["totalUnrealizedGainLossPercentage"], 2
    ) == -23.67