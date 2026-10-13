from app.services.portfolio_service import (
    get_index_report,
    get_trading_report,
    get_mi_report,
)
from app.utils.logger import logger


def _fetch_all_pages(fetch_function, params: dict) -> list:
    """Mengambil seluruh halaman data dari endpoint laporan."""
    all_data = []
    page = 1

    while True:
        request_params = {
            **params,
            "page": page,
            "limit": 100,
        }

        response = fetch_function(params=request_params)

        if not isinstance(response, dict):
            raise ValueError(
                "Format respons laporan tidak valid."
            )

        data = response.get("data", [])

        if not isinstance(data, list):
            raise ValueError(
                "Field 'data' pada respons bukan list."
            )

        all_data.extend(data)

        total_pages = int(response.get("totalPage", 1) or 1)

        if page >= total_pages:
            break

        page += 1

    return all_data


def _normalize_stocks(rows: list) -> list:
    """Menyeragamkan format posisi saham untuk stress test."""
    stocks = []

    for row in rows:
        stock_code = row.get("stockCode")

        if not stock_code:
            continue

        market_value = float(row.get("marketValue") or 0)

        if market_value <= 0:
            continue

        stocks.append({
            "stockCode": str(stock_code).strip().upper(),
            "marketValue": market_value,
        })

    return stocks


def get_stress_test_portfolios(date: str) -> dict:
    """
    Mengambil posisi saham untuk masing-masing kelompok investasi.

    SBN belum termasuk karena sumber datanya belum teridentifikasi.
    """
    logger.info(
        f"Stress Test Portfolio - Fetch all groups: date={date}"
    )

    index_rows = _fetch_all_pages(
        get_index_report,
        {"date": date},
    )

    trading_rows = _fetch_all_pages(
        get_trading_report,
        {"date": date},
    )

    schroder_rows = _fetch_all_pages(
        get_mi_report,
        {
            "date": date,
            "dealerCode": "SCH",
        },
    )

    bnp_rows = _fetch_all_pages(
        get_mi_report,
        {
            "date": date,
            "dealerCode": "BNP",
        },
    )

    groups = {
        "sahamIndeks": _normalize_stocks(index_rows),
        "sahamTrading": _normalize_stocks(trading_rows),
        "sahamFMSchroder": _normalize_stocks(schroder_rows),
        "sahamFMBNPParibas": _normalize_stocks(bnp_rows),
    }

    for group_name, stocks in groups.items():
        logger.info(
            f"Stress Test Portfolio - {group_name}: "
            f"{len(stocks)} positions"
        )

    return {
        "date": date,
        "groups": groups,
        "includedGroups": list(groups.keys()),
        "excludedGroups": [
            "sbnHTM",
            "sbnTrading",
        ],
    }