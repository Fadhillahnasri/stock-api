import pytest

from app.schemas.error_schema import ErrorResponse


def test_error_response_schema():
    response = ErrorResponse(
        success=False,
        status=502,
        message="Internal API request timed out",
        path="/stock/BBCA.JK"
    )

    assert response.success is False
    assert response.status == 502
    assert response.message == "Internal API request timed out"
    assert response.path == "/stock/BBCA.JK"


def test_error_response_invalid_status():
    with pytest.raises(ValueError):
        ErrorResponse(
            success=False,
            status="invalid",
            message="Something went wrong",
            path="/stock/BBCA.JK"
        )