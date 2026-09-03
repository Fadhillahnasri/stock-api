import pytest
from app.schemas.company_schema import CompanyData, CompanyResponse


def test_company_response_schema():
    response = CompanyResponse(
        success=True,
        provider="Yahoo Finance",
        data=CompanyData(
            symbol="BBCA.JK",
            company_name="PT Bank Central Asia Tbk",
            exchange="JKT",
            sector="Financial Services",
            industry="Banks - Diversified",
            country="Indonesia",
            website="https://www.bca.co.id",
            employees=28000,
            currency="IDR"
        )
    )

    assert response.success is True
    assert response.provider == "Yahoo Finance"
    assert response.data.symbol == "BBCA.JK"
    assert response.data.company_name == "PT Bank Central Asia Tbk"
    assert response.data.country == "Indonesia"
    assert response.data.currency == "IDR"


def test_company_response_invalid_employees():
    with pytest.raises(ValueError):
        CompanyResponse(
            success=True,
            provider="Yahoo Finance",
            data=CompanyData(
                symbol="BBCA.JK",
                company_name="PT Bank Central Asia Tbk",
                exchange="JKT",
                sector="Financial Services",
                industry="Banks - Diversified",
                country="Indonesia",
                website="https://www.bca.co.id",
                employees="invalid",
                currency="IDR"
            )
        )