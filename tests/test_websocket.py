from fastapi.testclient import TestClient
from app.main import app
from app.services import stock_service

client = TestClient(app)


def test_websocket_valid_stock(monkeypatch):
    def mock_get_stock_price(symbol):
        return {
            "symbol": "BBCA.JK",
            "company_name": "PT Bank Central Asia Tbk",
            "current_price": 9000,
            "high": 9100,
            "low": 8900,
            "open": 8950,
            "previous_close": 8950,
            "change": 50,
            "change_percent": 0.56
        }

    monkeypatch.setattr(
        stock_service,
        "get_stock_price",
        mock_get_stock_price
    )

    with client.websocket_connect("/ws/BBCA.JK") as websocket:
        response = websocket.receive_json()

        assert response["success"] is True
        assert response["provider"] == "yahoo"
        assert response["data"]["symbol"] == "BBCA.JK"
        assert response["data"]["company_name"]
        assert response["data"]["current_price"] is not None


def test_websocket_invalid_stock(monkeypatch):
    def mock_get_stock_price(symbol):
        return None

    monkeypatch.setattr(
        stock_service,
        "get_stock_price",
        mock_get_stock_price
    )

    with client.websocket_connect("/ws/ABC123.JK") as websocket:
        response = websocket.receive_json()

        assert response["success"] is False
        assert response["message"] == "Stock 'ABC123.JK' not found."