import pytest
from app.schemas.health_schema import HealthResponse


def test_health_response_schema():
    response = HealthResponse(
        status="healthy",
        message="API is running"
    )

    assert response.status == "healthy"
    assert response.message == "API is running"


def test_health_response_invalid_status():
    with pytest.raises(ValueError):
        HealthResponse(
            status=123,
            message="API is running"
        )