from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_portfolio_index_prices():
    response = client.get("/portfolio/index-prices")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "data" in data


def test_portfolio_index_report():
    response = client.get(
        "/portfolio/index-report?date=2026-09-14"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "data" in data


def test_portfolio_trading_report():
    response = client.get(
        "/portfolio/trading-report"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "summary" in data
    assert "dealerSummaries" in data
    assert "data" in data

def test_portfolio_closing_prices():
    response = client.get("/portfolio/closing-prices")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "page" in data
    assert "limit" in data
    assert "totalPage" in data
    assert "totalData" in data
    assert "data" in data

    assert len(data["data"]) > 0
    assert "stockCode" in data["data"][0]
    assert "stockName" in data["data"][0]
    assert "closingPrice" in data["data"][0]

def test_portfolio_stocks():
    response = client.get("/portfolio/stocks")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "page" in data
    assert "limit" in data
    assert "totalPage" in data
    assert "totalData" in data
    assert "data" in data

    assert len(data["data"]) > 0
    assert "id" in data["data"][0]
    assert "code" in data["data"][0]
    assert "name" in data["data"][0]
    assert "sector" in data["data"][0]
    assert "subSector" in data["data"][0]

def test_portfolio_portfolios():
    response = client.get("/portfolio/portfolios")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "data" in data

    assert len(data["data"]) > 0
    assert "code" in data["data"][0]
    assert "name" in data["data"][0]
    assert "category" in data["data"][0]
    assert "isActive" in data["data"][0]