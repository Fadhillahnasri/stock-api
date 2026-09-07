import logging
import os

# Membuat folder logs jika belum ada
os.makedirs("logs", exist_ok=True)

# Membuat logger aplikasi
logger = logging.getLogger("indonesia_stock_api")
logger.setLevel(logging.INFO)

# Hindari handler terduplikasi
if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Log ke file
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)

    # Log ke CMD
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)