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
                "closingPrice": "8250",
            },
            {
                "stockCode": "BBRI",
                "netAmount": "30794040970.00",
                "marketValue": "22590740000.00",
                "unrealizedgainorloss": "-8203300970.00",
                "closingPrice": "4370",
            },
        ],
    }

    monkeypatch.setattr(
        portfolio_analysis_service,
        "get_index_report",
        lambda params=None: expected
    )

    result = portfolio_analysis_service.get_portfolio_analysis(
        date="2026-05-26"
    )

    assert result["totalCostBasis"] == 59565619575.43
    assert result["totalMarketValue"] == 45467990000
    assert result["totalUnrealizedGainLoss"] == -14097629575.43

    assert round(
        result["totalUnrealizedGainLossPercentage"], 2
    ) == -23.67

    assert len(result["stocks"]) == 2

    bbca = result["stocks"][0]
    bbri = result["stocks"][1]

    assert bbca["stockCode"] == "BBCA"
    assert bbca["costBasis"] == 28771578605.43
    assert bbca["marketValue"] == 22877250000
    assert bbca["unrealizedGainLoss"] == -5894328605.43
    assert bbca["closingPrice"] == 8250

    assert bbri["stockCode"] == "BBRI"
    assert bbri["closingPrice"] == 4370

    assert round(bbca["performancePercentage"], 2) == -20.49
    assert round(bbca["portfolioWeight"], 2) == 50.32

    assert len(result["topGainers"]) == 2
    assert len(result["topLosers"]) == 2

    assert result["topGainers"][0]["stockCode"] == "BBCA"
    assert result["topLosers"][0]["stockCode"] == "BBRI"