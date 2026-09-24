from app.services import sensitivity_analysis_service
from app.services.sensitivity_analysis_service import (
    calculate_beta,
    calculate_stock_sensitivity,
    align_returns,
    calculate_sensitivity_analysis,
    
)


def test_calculate_beta():
    stock_returns = [
        0.02,
        0.01,
        -0.01,
        0.03,
    ]

    benchmark_returns = [
        0.01,
        0.005,
        -0.005,
        0.015,
    ]

    result = calculate_beta(
        stock_returns=stock_returns,
        benchmark_returns=benchmark_returns,
    )

    assert result is not None

    expected_beta = 2.0

    assert round(result, 6) == round(expected_beta, 6)

def test_calculate_beta_different_lengths():
    stock_returns = [
        0.02,
        0.01,
        -0.01,
    ]

    benchmark_returns = [
        0.01,
        0.005,
    ]

    try:
        calculate_beta(
            stock_returns=stock_returns,
            benchmark_returns=benchmark_returns,
        )
        assert False
    except ValueError as e:
        assert str(e) == (
            "Stock returns and benchmark returns must have "
            "the same length."
        )

def test_calculate_beta_zero_benchmark_variance():
    stock_returns = [
        0.02,
        0.01,
        -0.01,
    ]

    benchmark_returns = [
        0.01,
        0.01,
        0.01,
    ]

    result = calculate_beta(
        stock_returns=stock_returns,
        benchmark_returns=benchmark_returns,
    )

def test_calculate_stock_sensitivity():
    stock_returns = [
        0.02,
        0.01,
        -0.01,
        0.03,
    ]

    benchmark_returns = [
        0.01,
        0.005,
        -0.005,
        0.015,
    ]

    result = calculate_stock_sensitivity(
        stock_returns=stock_returns,
        benchmark_returns=benchmark_returns,
    )

    assert result is not None
    assert round(result["beta"], 6) == 2.0
    assert result["observationCount"] == 4

def test_align_returns():
    stock_data = [
        {
            "date": "2026-01-01",
            "dailyReturn": 0.02,
        },
        {
            "date": "2026-01-02",
            "dailyReturn": 0.01,
        },
        {
            "date": "2026-01-03",
            "dailyReturn": -0.01,
        },
    ]

    benchmark_data = [
        {
            "date": "2026-01-01",
            "dailyReturn": 0.01,
        },
        {
            "date": "2026-01-03",
            "dailyReturn": -0.005,
        },
        {
            "date": "2026-01-04",
            "dailyReturn": 0.015,
        },
    ]

    result = align_returns(
        stock_data=stock_data,
        benchmark_data=benchmark_data,
    )

    assert result["dates"] == [
        "2026-01-01",
        "2026-01-03",
    ]

    assert result["stockReturns"] == [
        0.02,
        -0.01,
    ]

    assert result["benchmarkReturns"] == [
        0.01,
        -0.005,
    ]

def test_calculate_sensitivity_analysis():
    stock_data = [
        {
            "date": "2026-01-01",
            "dailyReturn": 0.02,
        },
        {
            "date": "2026-01-02",
            "dailyReturn": 0.01,
        },
        {
            "date": "2026-01-03",
            "dailyReturn": -0.01,
        },
        {
            "date": "2026-01-04",
            "dailyReturn": 0.03,
        },
    ]

    benchmark_data = [
        {
            "date": "2026-01-01",
            "dailyReturn": 0.01,
        },
        {
            "date": "2026-01-02",
            "dailyReturn": 0.005,
        },
        {
            "date": "2026-01-03",
            "dailyReturn": -0.005,
        },
        {
            "date": "2026-01-04",
            "dailyReturn": 0.015,
        },
    ]

    result = calculate_sensitivity_analysis(
        stock_data=stock_data,
        benchmark_data=benchmark_data,
    )

    assert result is not None
    assert round(result["beta"], 6) == 2.0
    assert result["observationCount"] == 4

    assert result["dates"] == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
    ]

    assert result["stockReturns"] == [
        0.02,
        0.01,
        -0.01,
        0.03,
    ]

    assert result["benchmarkReturns"] == [
        0.01,
        0.005,
        -0.005,
        0.015,
    ]

def test_get_stock_sensitivity(monkeypatch):
    stock_history = {
        "symbol": "BBCA.JK",
        "period": "1y",
        "interval": "1d",
        "data": [
            {
                "date": "2026-01-01",
                "close": 8050,
            },
            {
                "date": "2026-01-02",
                "close": 8211,
            },
            {
                "date": "2026-01-03",
                "close": 8129,
            },
            {
                "date": "2026-01-04",
                "close": 8373,
            },
        ],
    }

    benchmark_history = {
        "symbol": "^JKSE",
        "period": "1y",
        "interval": "1d",
        "data": [
            {
                "date": "2026-01-01",
                "close": 7000,
            },
            {
                "date": "2026-01-02",
                "close": 7035,
            },
            {
                "date": "2026-01-03",
                "close": 7017.5,
            },
            {
                "date": "2026-01-04",
                "close": 7052.5,
            },
        ],
    }

    def mock_get_historical_prices(
        symbol,
        period="1y",
        interval="1d",
    ):
        if symbol == "BBCA.JK":
            return stock_history

        if symbol == "^JKSE":
            return benchmark_history

        return None

    monkeypatch.setattr(
        sensitivity_analysis_service,
        "get_historical_prices",
        mock_get_historical_prices,
    )

    result = sensitivity_analysis_service.get_stock_sensitivity(
        symbol="bbca.jk",
        benchmark_symbol="^jkse",
        period="1y",
        interval="1d",
    )

    assert result is not None
    assert result["observationCount"] == 3
    assert "beta" in result
    assert len(result["dates"]) == 3
    assert len(result["stockReturns"]) == 3
    assert len(result["benchmarkReturns"]) == 3