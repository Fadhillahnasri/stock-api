import pytest

from app.services.custom_stress_test_service import (
    calculate_fx_shock,
    calculate_oil_shock,
    calculate_stock_stress_impact,
    calculate_portfolio_stress_impact,
    run_custom_stress_test,
    get_stock_macro_betas,
)



def calculate_fx_shock(current_fx: float, target_fx: float = 25000):
    """
    Menghitung shock USD/IDR berdasarkan target exchange rate.
    Contoh:
    current_fx = 17998
    target_fx = 25000
    """
    if current_fx <= 0:
        raise ValueError("Current FX harus lebih besar dari 0.")

    if target_fx <= 0:
        raise ValueError("Target FX harus lebih besar dari 0.")

    shock = (target_fx / current_fx) - 1

    return shock


@pytest.mark.parametrize("target_fx", [0, -1])
def test_calculate_fx_shock_rejects_invalid_target(target_fx):
    with pytest.raises(ValueError, match="Target FX"):
        calculate_fx_shock(
            current_fx=17998,
            target_fx=target_fx,
        )

def test_calculate_oil_shock():
    shock = calculate_oil_shock(-40)

    assert shock == -0.40


@pytest.mark.parametrize("shock_percentage", [-100.1, 100.1])
def test_calculate_oil_shock_rejects_invalid_percentage(shock_percentage):
    with pytest.raises(ValueError, match="Oil shock"):
        calculate_oil_shock(shock_percentage)



def test_calculate_stock_stress_impact():
    result = calculate_stock_stress_impact(
        fx_beta=-2.0,
        fx_shock=0.10,
        oil_beta=-0.05,
        oil_shock=-0.40,
    )

    assert result["fxImpact"] == pytest.approx(-0.20)
    assert result["oilImpact"] == pytest.approx(0.02)
    assert result["estimatedReturn"] == pytest.approx(-0.18)
    assert result["estimatedReturnPercentage"] == pytest.approx(-18.0)


def test_calculate_portfolio_stress_impact():
    portfolio = [
        {
            "symbol": "BBCA.JK",
            "weight": 0.60,
            "fxBeta": -2.0,
            "oilBeta": -0.05,
        },
        {
            "symbol": "BBRI.JK",
            "weight": 0.40,
            "fxBeta": -1.5,
            "oilBeta": -0.03,
        },
    ]

    result = calculate_portfolio_stress_impact(
        portfolio_stocks=portfolio,
        fx_shock=0.10,
        oil_shock=-0.40,
    )

    assert result["totalWeight"] == 1.0
    assert len(result["stocks"]) == 2
    assert result["portfolioReturn"] < 0

def test_run_custom_stress_test():
    portfolio = [
        {
            "stockCode": "BBCA.JK",
            "portfolioWeight": 60,
        },
        {
            "stockCode": "BBRI.JK",
            "portfolioWeight": 40,
        },
    ]

    fx_betas = {
        "BBCA.JK": -2.0,
        "BBRI.JK": -1.5,
    }

    oil_betas = {
        "BBCA.JK": -0.05,
        "BBRI.JK": -0.03,
    }

    result = run_custom_stress_test(
        portfolio_stocks=portfolio,
        current_fx=17998,
        fx_betas=fx_betas,
        oil_betas=oil_betas,
        target_fx=25000,
        oil_shock_percentage=-40,
    )

    assert result is not None

    assert result["scenario"]["targetFx"] == 25000
    assert result["scenario"]["currentFx"] == 17998
    assert result["scenario"]["oilShockPercentage"] == -40

    assert result["portfolio"]["totalWeight"] == pytest.approx(1.0)
    assert len(result["portfolio"]["stocks"]) == 2

    assert result["portfolio"]["portfolioReturn"] < 0
    assert result["portfolio"]["portfolioReturnPercentage"] < 0


def test_get_stock_macro_betas(monkeypatch):
    stock_data = {
        "symbol": "BBCA.JK",
        "data": [
            {
                "date": "2026-09-01",
                "dailyReturn": 0.01,
            },
            {
                "date": "2026-09-02",
                "dailyReturn": -0.02,
            },
        ],
    }

    fx_data = {
        "indicator": "USD/IDR",
        "source": "Bank Indonesia",
        "data": [
            {
                "date": "2026-09-01",
                "value": 17000,
            },
            {
                "date": "2026-09-02",
                "value": 17100,
            },
        ],
    }

    oil_data = {
        "indicator": "WTI Oil Price",
        "source": "U.S. Energy Information Administration",
        "data": [
            {
                "date": "2026-09-01",
                "value": 90,
            },
            {
                "date": "2026-09-02",
                "value": 88,
            },
        ],
    }

    fx_sensitivity = {
        "beta": -2.20,
        "correlation": -0.28,
    }

    oil_sensitivity = {
        "beta": -0.04,
        "correlation": -0.07,
    }

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_historical_returns",
        lambda symbol, period, interval: stock_data,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.get_exchange_rate",
        lambda currency, start_date, end_date: fx_data,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.get_oil_price",
        lambda start_date, end_date: oil_data,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_macro_sensitivity",
        lambda stock_data, macro_data: fx_sensitivity,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_oil_price_sensitivity",
        lambda stock_data, oil_data: oil_sensitivity,
    )

    result = get_stock_macro_betas(
        symbol="BBCA.JK",
        start_date="2026-09-01",
        end_date="2026-09-29",
    )

    assert result is not None

    assert result["symbol"] == "BBCA.JK"

    assert result["fxBeta"] == pytest.approx(-2.20)
    assert result["fxCorrelation"] == pytest.approx(-0.28)

    assert result["oilBeta"] == pytest.approx(-0.04)
    assert result["oilCorrelation"] == pytest.approx(-0.07)

def test_custom_stress_test_missing_stocks():
    portfolio = [
        {
            "stockCode": "BBCA.JK",
            "portfolioWeight": 60,
        },
        {
            "stockCode": "BBRI.JK",
            "portfolioWeight": 40,
        },
    ]

    fx_betas = {
        "BBCA.JK": -2.0,
    }

    oil_betas = {
        "BBCA.JK": -0.05,
    }

    result = run_custom_stress_test(
        portfolio_stocks=portfolio,
        current_fx=17998,
        fx_betas=fx_betas,
        oil_betas=oil_betas,
        target_fx=25000,
        oil_shock_percentage=-40,
    )

    assert result is not None

    assert result["portfolio"]["totalWeight"] == pytest.approx(0.60)
    assert result["portfolio"]["coveragePercentage"] == pytest.approx(60.0)

    assert len(result["portfolio"]["missingStocks"]) == 1
    assert result["portfolio"]["missingStocks"][0]["symbol"] == "BBRI.JK"
    assert result["portfolio"]["missingStocks"][0]["weight"] == pytest.approx(0.40)

    assert result["portfolio"]["portfolioReturn"] == pytest.approx(
        result["portfolio"]["stocks"][0]["weight"]
        * result["portfolio"]["stocks"][0]["estimatedReturn"]
    )

    assert result["portfolio"]["portfolioReturnPercentage"] == pytest.approx(
        result["portfolio"]["portfolioReturn"] * 100
    )

def test_get_stock_macro_betas_normalizes_indonesia_symbol(monkeypatch):
    captured = {}

    stock_data = {
        "symbol": "BBRI.JK",
        "data": [
            {
                "date": "2026-09-01",
                "dailyReturn": 0.01,
            },
            {
                "date": "2026-09-02",
                "dailyReturn": -0.02,
            },
        ],
    }

    fx_data = {
        "indicator": "USD/IDR",
        "source": "Bank Indonesia",
        "data": [
            {
                "date": "2026-09-01",
                "value": 17000,
            },
            {
                "date": "2026-09-02",
                "value": 17100,
            },
        ],
    }

    oil_data = {
        "indicator": "WTI Oil Price",
        "source": "U.S. Energy Information Administration",
        "data": [
            {
                "date": "2026-09-01",
                "value": 90,
            },
            {
                "date": "2026-09-02",
                "value": 88,
            },
        ],
    }

    def mock_historical_returns(symbol, period, interval):
        captured["symbol"] = symbol
        return stock_data

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_historical_returns",
        mock_historical_returns,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.get_exchange_rate",
        lambda currency, start_date, end_date: fx_data,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.get_oil_price",
        lambda start_date, end_date: oil_data,
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_macro_sensitivity",
        lambda stock_data, macro_data: {
            "beta": -2.0,
            "correlation": -0.28,
        },
    )

    monkeypatch.setattr(
        "app.services.custom_stress_test_service.calculate_oil_price_sensitivity",
        lambda stock_data, oil_data: {
            "beta": -0.04,
            "correlation": -0.07,
        },
    )

    result = get_stock_macro_betas(
        symbol="BBRI",
        start_date="2026-09-01",
        end_date="2026-09-29",
    )

    assert result is not None
    assert captured["symbol"] == "BBRI.JK"
    assert result["symbol"] == "BBRI"
    assert result["fxBeta"] == pytest.approx(-2.0)
    assert result["oilBeta"] == pytest.approx(-0.04)


@pytest.mark.parametrize("weight", [-10, 110])
def test_run_custom_stress_test_rejects_invalid_weight(weight):
    portfolio = [
        {
            "stockCode": "BBCA.JK",
            "portfolioWeight": weight,
        },
    ]

    with pytest.raises(ValueError, match="bobot"):
        run_custom_stress_test(
            portfolio_stocks=portfolio,
            current_fx=17998,
            fx_betas={"BBCA.JK": -2.0},
            oil_betas={"BBCA.JK": -0.05},
            target_fx=25000,
            oil_shock_percentage=-40,
        )
