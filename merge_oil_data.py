
import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OLD_FILE = ROOT / "data" / "macro" / "oil_price_wti.csv"
NEW_FILE = ROOT / "wti_fred.csv"
OUTPUT_FILE = ROOT / "data" / "macro" / "oil_price_wti_merged.csv"

# Baca data WTI lama
prices = {}

with OLD_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        day = row["date"].strip()
        value = row["value"].strip()

        if day and value:
            prices[day] = float(value)

# Baca data historis EIA.
# Lewati metadata sebelum header CSV yang sebenarnya.
with NEW_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    for row in reader:
        if row and row[0].strip() == "Day":
            break
    else:
        raise ValueError("Header 'Day' tidak ditemukan di file sumber.")

    for row in reader:
        if len(row) < 2:
            continue

        raw_date = row[0].strip()
        raw_value = row[1].strip()

        if not raw_date or not raw_value or raw_value == ".":
            continue

        try:
            day = datetime.strptime(raw_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            value = float(raw_value)
        except ValueError:
            continue

        # Data historis hanya melengkapi tanggal yang belum tersedia.
        if day not in prices:
            prices[day] = value

# Simpan ke file baru, jangan menimpa file sumber.
with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "value"])

    for day in sorted(prices):
        writer.writerow([day, prices[day]])

target_count = sum(
    1 for day in prices
    if "2025-05-21" <= day <= "2025-08-21"
)

print(f"File hasil: {OUTPUT_FILE}")
print(f"Jumlah observasi: {len(prices)}")
print(f"Tanggal awal: {min(prices)}")
print(f"Tanggal akhir: {max(prices)}")
print(f"Data untuk Mei-Agustus 2025: {target_count}")
