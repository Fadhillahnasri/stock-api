from app.utils.logger import logger

from app.services.historical_analysis_service import calculate_historical_returns
from app.services.macro_sensitivity_service import calculate_macro_sensitivity
from app.services.macro_service import get_exchange_rate, get_oil_price
from app.services.oil_price_sensitivity_service import calculate_oil_price_sensitivity


def calculate_fx_shock(current_fx: float, target_fx: float = 25000):
    """
    Menghitung shock USD/IDR berdasarkan target exchange rate.
    Contoh:
    current_fx = 17998
    target_fx = 25000
    """
    if current_fx <= 0:
        raise ValueError("Current FX harus lebih besar dari 0.")

    shock = (target_fx / current_fx) - 1

    return shock



def calculate_oil_shock(shock_percentage: float):
    """
    Mengembalikan shock harga minyak dalam bentuk desimal.

    Contoh:
    -30% -> -0.30
    -40% -> -0.40
    """
    if not -100 <= shock_percentage <= 100:
        raise ValueError(
            "Oil shock harus berada di antara -100 dan 100 persen."
        )

    return shock_percentage / 100



def calculate_stock_stress_impact(
    fx_beta: float,
    fx_shock: float,
    oil_beta: float,
    oil_shock: float,
):
    """
    Menghitung estimasi dampak stress test terhadap return saham.

    Model:
    Estimated Impact =
        (FX Beta × FX Shock)
        +
        (Oil Beta × Oil Shock)
    """

    fx_impact = fx_beta * fx_shock
    oil_impact = oil_beta * oil_shock

    total_impact = fx_impact + oil_impact

    return {
        "fxImpact": fx_impact,
        "oilImpact": oil_impact,
        "estimatedReturn": total_impact,
        "estimatedReturnPercentage": total_impact * 100,
    }


def calculate_portfolio_stress_impact(
    portfolio_stocks: list,
    fx_shock: float,
    oil_shock: float,
):
    """
    Menghitung estimasi dampak custom stress test
    terhadap seluruh portfolio.

    portfolio_stocks diharapkan memiliki:
    - symbol
    - weight
    - fxBeta
    - oilBeta
    """

    logger.info("Custom Stress Test - Calculate Portfolio Impact")

    if not portfolio_stocks:
        return None

    stock_results = []
    portfolio_impact = 0
    total_weight = 0

    for stock in portfolio_stocks:
        weight = float(stock.get("weight", 0))
        fx_beta = stock.get("fxBeta")
        oil_beta = stock.get("oilBeta")

        if fx_beta is None or oil_beta is None:
            continue

        impact = calculate_stock_stress_impact(
            fx_beta=float(fx_beta),
            fx_shock=fx_shock,
            oil_beta=float(oil_beta),
            oil_shock=oil_shock,
        )

        weighted_impact = weight * impact["estimatedReturn"]

        portfolio_impact += weighted_impact
        total_weight += weight

        stock_results.append({
            "symbol": stock.get("symbol"),
            "weight": weight,
            "fxBeta": float(fx_beta),
            "oilBeta": float(oil_beta),
            "fxImpact": impact["fxImpact"],
            "oilImpact": impact["oilImpact"],
            "estimatedReturn": impact["estimatedReturn"],
            "estimatedReturnPercentage": impact["estimatedReturnPercentage"],
            "weightedImpact": weighted_impact,
        })

    return {
        "portfolioReturn": portfolio_impact,
        "portfolioReturnPercentage": portfolio_impact * 100,
        "totalWeight": total_weight,
        "stocks": stock_results,
    }

def run_custom_stress_test(
    portfolio_stocks: list,
    current_fx: float,
    fx_betas: dict,
    oil_betas: dict,
    target_fx: float = 25000,
    oil_shock_percentage: float = -40,
):
    """
    Menjalankan custom worst-case stress test
    menggunakan sensitivity historis USD/IDR dan WTI.

    Input portfolio mengikuti struktur get_portfolio_analysis():
    - stockCode
    - portfolioWeight

    Model:
    Estimated Stock Return =
        (FX Beta × FX Shock)
        +
        (Oil Beta × Oil Shock)
    """

    logger.info("Custom Stress Test - Run Scenario")

    fx_shock = calculate_fx_shock(
        current_fx=current_fx,
        target_fx=target_fx,
    )

    oil_shock = calculate_oil_shock(
        oil_shock_percentage
    )

    stocks = []
    missing_stocks = []


    for stock in portfolio_stocks:
        symbol = stock.get("stockCode")

        # portfolioWeight dari portfolio analysis
        # menggunakan satuan persen (0-100).
        if not symbol:
            continue

        try:
            portfolio_weight = float(stock.get("portfolioWeight", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Nilai bobot tidak valid untuk saham {symbol}."
            ) from exc

        if not 0 <= portfolio_weight <= 100:
            raise ValueError(
                f"Nilai bobot saham {symbol} harus berada "
                "di antara 0 dan 100 persen."
            )

        # Custom stress test menggunakan desimal (0-1).
        weight = portfolio_weight / 100


        fx_beta = fx_betas.get(symbol)
        oil_beta = oil_betas.get(symbol)

        if fx_beta is None or oil_beta is None:
            logger.warning(
                f"Custom Stress Test - Sensitivity tidak tersedia: {symbol}"
            )

            missing_stocks.append({
                "symbol": symbol,
                "weight": weight,
                "reason": "Sensitivity USD/IDR atau WTI tidak tersedia."
            })

            continue

        stocks.append({
            "symbol": symbol,
            "weight": weight,
            "fxBeta": float(fx_beta),
            "oilBeta": float(oil_beta),
        })

    portfolio_result = calculate_portfolio_stress_impact(
        portfolio_stocks=stocks,
        fx_shock=fx_shock,
        oil_shock=oil_shock,
    )

    if portfolio_result is None:
        return None

    coverage_percentage = (
        portfolio_result["totalWeight"] * 100
    )

    return {
            "scenario": {
                "targetFx": target_fx,
                "currentFx": current_fx,
                "fxShock": fx_shock,
                "fxShockPercentage": fx_shock * 100,
                "oilShock": oil_shock,
                "oilShockPercentage": oil_shock_percentage,
            },
            "portfolio": {
                **portfolio_result,
                "coveragePercentage": coverage_percentage,
                "missingStocks": missing_stocks,
            },
        }

def get_stock_macro_betas(
    symbol: str,
    start_date: str,
    end_date: str,
):
    logger.info(
        f"Custom Stress Test - Get Macro Betas: {symbol}"
    )

    yahoo_symbol = symbol.strip().upper()

    if "." not in yahoo_symbol:
        yahoo_symbol = f"{yahoo_symbol}.JK"

    stock_data = calculate_historical_returns(
        symbol=yahoo_symbol,
        period="max",
        interval="1d"
    )

    if not stock_data or not stock_data.get("data"):
        return None


    # =========================
    # USD/IDR
    # =========================

    fx_data = get_exchange_rate(
        currency="USD",
        start_date=start_date,
        end_date=end_date
    )

    if not fx_data or not fx_data.get("data"):
        return None

    fx_sensitivity = calculate_macro_sensitivity(
        stock_data=stock_data["data"],
        macro_data=fx_data["data"]
    )

    if fx_sensitivity is None:
        return None

    # =========================
    # WTI Oil Price
    # =========================

    oil_data = get_oil_price(
        start_date=start_date,
        end_date=end_date
    )

    if not oil_data or not oil_data.get("data"):
        return None

    oil_sensitivity = calculate_oil_price_sensitivity(
        stock_data=stock_data["data"],
        oil_data=oil_data["data"]
    )

    if oil_sensitivity is None:
        return None

    return {
        "symbol": symbol.upper(),
        "fxBeta": fx_sensitivity["beta"],
        "fxCorrelation": fx_sensitivity["correlation"],
        "oilBeta": oil_sensitivity["beta"],
        "oilCorrelation": oil_sensitivity["correlation"],
    }
