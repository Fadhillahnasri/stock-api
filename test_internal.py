from app.services.portfolio_service import get_transactions


def test_get_transactions():
    result = get_transactions()

    assert result is not None