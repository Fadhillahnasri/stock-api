
import yfinance as yf

symbols = ["DEWA.JK", "BRMS.JK", "BKSL.JK"]

for symbol in symbols:
    print(f"\n=== {symbol} ===")

    df = yf.Ticker(symbol).history(
        period="max",
        interval="1d",
        auto_adjust=False
    )

    if df.empty:
        print("Data kosong")
        continue

    print("Rentang tanggal:", df.index.min(), "-", df.index.max())
    print("Jumlah data:", len(df))
    print("Close unik:", df["Close"].nunique())
    print("High unik:", df["High"].nunique())
    print("Low unik:", df["Low"].nunique())
    print("Total volume:", df["Volume"].sum())
    print("Jumlah hari volume nol:", (df["Volume"] == 0).sum())

    print("\n10 data terakhir:")
    print(df[["Open", "High", "Low", "Close", "Volume"]].tail(10))
