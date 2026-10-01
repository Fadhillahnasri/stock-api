import csv
from pathlib import Path

from app.utils.logger import logger
from app.exceptions.provider_exceptions import ProviderError


class MacroProvider:

    def __init__(self):
        self.data_file = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "macro"
            / "usd_idr_jisdor.csv"
        )

    def get_exchange_rate(
        self,
        currency: str,
        start_date: str,
        end_date: str
    ):
        currency = currency.strip().upper()

        logger.info(
            f"Macro Provider - Get Exchange Rate: "
            f"{currency}, {start_date} to {end_date}"
        )

        if currency != "USD":
            raise ProviderError(
                f"Macro data untuk currency '{currency}' belum tersedia."
            )

        try:
            data = []

            with open(
                self.data_file,
                mode="r",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    date = row["date"]

                    if start_date <= date <= end_date:
                        data.append({
                            "date": date,
                            "value": float(row["value"])
                        })

            return {
                "currency": currency,
                "data": data
            }

        except FileNotFoundError as e:
            logger.exception(
                f"Macro Provider - Data file not found: "
                f"{self.data_file}"
            )

            raise ProviderError(
                "File data JISDOR tidak ditemukan."
            ) from e

        except Exception as e:
            logger.exception(
                f"Macro Provider - Error reading data: {e}"
            )

            raise ProviderError(
                "Gagal membaca data JISDOR."
            ) from e
        
    def get_oil_price(
        self,
        start_date: str,
        end_date: str
    ):
        logger.info(
            f"Macro Provider - Get Oil Price: "
            f"{start_date} to {end_date}"
        )

        oil_file = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "macro"
            / "oil_price_wti.csv"
        )

        try:
            data = []

            with open(oil_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    date = row["date"]

                    if start_date <= date <= end_date:
                        data.append({
                            "date": date,
                            "value": float(row["value"])
                        })

            return {
                "indicator": "WTI Oil Price",
                "source": "U.S. Energy Information Administration",
                "unit": "USD/barrel",
                "data": data
            }

        except FileNotFoundError as e:
            logger.exception(
                f"Macro Provider - Oil Price file not found: {oil_file}"
            )
            raise ProviderError(
                "File data WTI Oil Price tidak ditemukan."
            ) from e

        except Exception as e:
            logger.exception(
                f"Macro Provider - Error reading Oil Price data: {e}"
            )
            raise ProviderError(
                "Gagal membaca data WTI Oil Price."
            ) from e
    

    def get_bi_rate(self, start_date: str, end_date: str):
        logger.info(
            f"Macro Provider - Get BI-Rate: {start_date} to {end_date}"
        )

        try:
            data = []

            bi_rate_file = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "macro"
                / "bi_rate.csv"
            )

            with open(bi_rate_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    date = row["date"]

                    if start_date <= date <= end_date:
                        data.append({
                            "date": date,
                            "value": float(row["value"])
                        })

            return {
                "indicator": "BI-Rate",
                "source": "Bank Indonesia",
                "data": data
            }

        except FileNotFoundError as e:
            logger.exception(
                f"Macro Provider - BI-Rate file not found: {bi_rate_file}"
            )
            raise ProviderError(
                "File data BI-Rate tidak ditemukan."
            ) from e

        except Exception as e:
            logger.exception(
                f"Macro Provider - Error reading BI-Rate data: {e}"
            )
            raise ProviderError(
                "Gagal membaca data BI-Rate."
            ) from e

    def get_bi_rate(self, start_date: str, end_date: str):
        logger.info(
            f"Macro Provider - Get BI-Rate: {start_date} to {end_date}"
        )

        bi_rate_file = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "macro"
            / "bi_rate.csv"
        )

        try:
            data = []

            with open(bi_rate_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    date = row["date"]

                    if start_date <= date <= end_date:
                        data.append({
                            "date": date,
                            "value": float(row["value"])
                        })

            return {
                "indicator": "BI-Rate",
                "source": "Bank Indonesia",
                "data": data
            }

        except FileNotFoundError as e:
            logger.exception(
                f"Macro Provider - BI-Rate file not found: {bi_rate_file}"
            )
            raise ProviderError(
                "File data BI-Rate tidak ditemukan."
            ) from e

        except Exception as e:
            logger.exception(
                f"Macro Provider - Error reading BI-Rate data: {e}"
            )
            raise ProviderError(
                "Gagal membaca data BI-Rate."
            ) from e