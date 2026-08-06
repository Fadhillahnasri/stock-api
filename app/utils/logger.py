import logging
import os

# Membuat folder logs jika belum ada
os.makedirs("logs", exist_ok=True)

# Konfigurasi logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)