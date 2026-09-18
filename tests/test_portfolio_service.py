from app.services import portfolio_service


def test_get_portfolios(monkeypatch):
    expected = {"status": "success", "data": []}

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_portfolios",
        lambda: expected
    )

    result = portfolio_service.get_portfolios()

    assert result == expected


def test_get_stocks(monkeypatch):
    expected = {"status": "success", "data": []}

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_stocks",
        lambda: expected
    )

    result = portfolio_service.get_stocks()

    assert result == expected


def test_get_closing_prices(monkeypatch):
    expected = {"status": "success", "data": []}
    params = {
        "page": 1,
        "limit": 20
    }

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_closing_prices",
        lambda params=None: expected
    )

    result = portfolio_service.get_closing_prices(params=params)

    assert result == expected


def test_get_index_prices(monkeypatch):
    expected = {"status": "success", "data": []}
    params = {
        "page": 1,
        "limit": 20
    }

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_index_prices",
        lambda params=None: expected
    )

    result = portfolio_service.get_index_prices(params=params)

    assert result == expected


def test_get_index_report(monkeypatch):
    expected = {"status": "success", "data": []}
    params = {
        "date": "2026-09-14"
    }

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_index_report",
        lambda params=None: expected
    )

    result = portfolio_service.get_index_report(params=params)

    assert result == expected


def test_get_trading_report(monkeypatch):
    expected = {"status": "success", "data": []}
    params = {
        "date": "2026-09-14"
    }

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_trading_report",
        lambda params=None: expected
    )

    result = portfolio_service.get_trading_report(params=params)

    assert result == expected


def test_get_transactions(monkeypatch):
    expected = {"status": "success", "data": []}
    params = {
        "page": 1,
        "limit": 20
    }

    monkeypatch.setattr(
        portfolio_service.provider,
        "get_transactions",
        lambda params=None: expected
    )

    result = portfolio_service.get_transactions(params=params)

    assert result == expected