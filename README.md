# Indonesia Stock API

REST API dan WebSocket service untuk mengambil dan memantau data saham Indonesia secara near real-time.

Project ini dibangun menggunakan **FastAPI** dengan pendekatan provider-based architecture, sehingga sumber data saham dapat diganti atau dikembangkan tanpa mengubah struktur utama aplikasi.

Saat ini project menggunakan **Yahoo Finance** melalui library `yfinance` sebagai provider utama. Arsitektur juga sudah disiapkan untuk integrasi **Internal API** pada tahap berikutnya.

---

## Features

* REST API untuk mengambil data satu saham
* REST API untuk mengambil beberapa saham sekaligus
* REST API untuk mengambil profil perusahaan
* WebSocket untuk monitoring harga saham secara berkala
* Health check endpoint
* Provider-based architecture
* Centralized exception handling
* Request logging dan application logging
* Pydantic response validation
* HTTP client dengan timeout dan connection error handling
* Unit dan integration testing menggunakan Pytest
* Konfigurasi melalui environment variables
* Swagger API documentation

---

## Tech Stack

* **Python**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **Pydantic Settings**
* **yfinance**
* **HTTPX**
* **Jinja2**
* **WebSocket**
* **Pytest**

---

## Project Structure

```text
stock-api/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── websocket.py
│   │
│   ├── core/
│   │   └── http_client.py
│   │
│   ├── exceptions/
│   │   ├── handlers.py
│   │   └── provider_exceptions.py
│   │
│   ├── middleware/
│   │   └── logging_middleware.py
│   │
│   ├── providers/
│   │   ├── base_provider.py
│   │   ├── internal_provider.py
│   │   ├── provider_factory.py
│   │   └── yahoo_provider.py
│   │
│   ├── schemas/
│   │   ├── company_schema.py
│   │   ├── error_schema.py
│   │   ├── health_schema.py
│   │   ├── multiple_stock_schema.py
│   │   └── stock_schema.py
│   │
│   ├── services/
│   │   └── stock_service.py
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   ├── config.py
│   └── main.py
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── test_company_schema.py
│   ├── test_error_schema.py
│   ├── test_health.py
│   ├── test_health_schema.py
│   ├── test_http_client.py
│   ├── test_multiple_stock_schema.py
│   ├── test_stock_schema.py
│   ├── test_stock_service.py
│   ├── test_websocket.py
│   └── test_yahoo_provider.py
│
├── logs/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Architecture

Project menggunakan beberapa layer utama:

```text
Client
  │
  ▼
API Routes
  │
  ▼
Service Layer
  │
  ▼
Provider Factory
  │
  ├── YahooProvider
  │
  └── InternalProvider
          │
          ▼
      Internal API
```

### API Layer

Menangani request dari client melalui REST API dan WebSocket.

### Service Layer

Menjadi penghubung antara API layer dan provider. Service tidak bergantung langsung pada sumber data tertentu.

### Provider Layer

Menangani komunikasi dengan sumber data.

Provider yang tersedia:

* `YahooProvider` — provider yang saat ini digunakan
* `InternalProvider` — placeholder untuk integrasi Internal API

### Schema Layer

Menggunakan Pydantic untuk memastikan struktur response API sesuai dengan schema yang telah ditentukan.

### Exception Handling

Error dari API maupun provider ditangani secara terpusat sehingga response error memiliki format yang konsisten.

---

## Installation

### 1. Clone repository

```bash
git clone <repository-url>
cd stock-api
```

### 2. Create virtual environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Environment Configuration

Buat file `.env` berdasarkan `.env.example`.

```env
APP_NAME=Indonesia Stock API
APP_VERSION=1.0.0

PROVIDER=yahoo

REQUEST_TIMEOUT=10
LOG_LEVEL=INFO
STOCK_UPDATE_INTERVAL=5

INTERNAL_API_BASE_URL=
```

### Configuration

| Variable                | Description               | Default               |
| ----------------------- | ------------------------- | --------------------- |
| `APP_NAME`              | Nama aplikasi             | `Indonesia Stock API` |
| `APP_VERSION`           | Versi aplikasi            | `1.0.0`               |
| `PROVIDER`              | Provider data saham       | `yahoo`               |
| `REQUEST_TIMEOUT`       | Timeout request           | `10`                  |
| `LOG_LEVEL`             | Level logging             | `INFO`                |
| `STOCK_UPDATE_INTERVAL` | Interval update WebSocket | `5`                   |
| `INTERNAL_API_BASE_URL` | Base URL Internal API     | -                     |

> Jangan commit file `.env` ke repository. Gunakan `.env.example` sebagai template konfigurasi.

---

## Running the Application

Jalankan aplikasi menggunakan Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

Server akan berjalan pada:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI menyediakan dokumentasi API secara otomatis.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## REST API Endpoints

### Home

```http
GET /
```

Menampilkan informasi dasar aplikasi.

Example response:

```json
{
  "application": "Indonesia Stock API",
  "status": "running",
  "provider": "Yahoo Finance",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

---

### Health Check

```http
GET /health
```

Digunakan untuk memastikan API berjalan dengan normal.

Example response:

```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

### Get Single Stock

```http
GET /stock/{symbol}
```

Mengambil data satu saham berdasarkan simbol.

Example:

```http
GET /stock/BBCA.JK
```

Example response:

```json
{
  "success": true,
  "provider": "Yahoo Finance",
  "data": {
    "symbol": "BBCA.JK",
    "company_name": "Bank Central Asia Tbk.",
    "current_price": 9000,
    "high": 9050,
    "low": 8900,
    "open": 8950,
    "previous_close": 8900,
    "change": 100,
    "change_percent": 1.12,
    "currency": "IDR",
    "exchange": "JKT",
    "market_state": "REGULAR"
  }
}
```

Nilai pada response dapat berubah mengikuti data dari provider.

---

### Get Multiple Stocks

```http
GET /stocks?symbols={symbols}
```

Mengambil data beberapa saham dalam satu request.

Example:

```http
GET /stocks?symbols=BBCA.JK,BBRI.JK,BMRI.JK
```

Response menyediakan:

* jumlah saham yang berhasil diambil
* daftar saham yang gagal diambil
* data masing-masing saham

---

### Get Company Profile

```http
GET /company/{symbol}
```

Mengambil informasi profil perusahaan berdasarkan simbol saham.

Example:

```http
GET /company/BBCA.JK
```

Informasi yang tersedia antara lain:

* Symbol
* Company name
* Exchange
* Sector
* Industry
* Country
* Website
* Employees
* Currency

---

## WebSocket

WebSocket digunakan untuk mendapatkan update data saham secara berkala.

Endpoint:

```text
/ws/{symbol}
```

Example:

```text
ws://127.0.0.1:8000/ws/BBCA.JK
```

Client akan menerima data secara berkala berdasarkan konfigurasi:

```env
STOCK_UPDATE_INTERVAL=5
```

Artinya server melakukan update data setiap 5 detik.

Example response:

```json
{
  "success": true,
  "provider": "Yahoo Finance",
  "data": {
    "symbol": "BBCA.JK",
    "company_name": "Bank Central Asia Tbk.",
    "current_price": 9000
  }
}
```

---

## Error Handling

API menggunakan centralized exception handling untuk menjaga response error tetap konsisten.

### 404 — Data Not Found

Contoh:

```json
{
  "success": false,
  "status": 404,
  "message": "Stock 'ABC123.JK' not found.",
  "path": "/stock/ABC123.JK"
}
```

### 422 — Validation Error

Digunakan ketika request tidak memenuhi parameter yang dibutuhkan oleh endpoint.

### 502 — Provider Error

Digunakan ketika terjadi masalah pada provider eksternal.

Contoh:

```json
{
  "success": false,
  "status": 502,
  "message": "Yahoo Finance error for BBCA.JK",
  "path": "/stock/BBCA.JK"
}
```

### 500 — Internal Server Error

Digunakan untuk error internal yang tidak tertangani secara spesifik.

---

## Testing

Project menggunakan **Pytest** untuk melakukan automated testing.

Jalankan seluruh test:

```bash
python -m pytest
```

Testing mencakup:

* Health endpoint
* Home endpoint
* Single stock endpoint
* Multiple stock endpoint
* Company endpoint
* Error handling
* Internal provider behavior
* Yahoo provider
* Service layer
* WebSocket
* Pydantic schemas
* HTTP client

Test provider eksternal menggunakan mocking sehingga sebagian besar unit test tidak bergantung pada koneksi langsung ke Yahoo Finance.

---

## Provider System

Provider system dibuat agar sumber data dapat diganti tanpa mengubah API dan service layer.

Provider ditentukan melalui environment variable:

```env
PROVIDER=yahoo
```

Factory kemudian memilih provider yang sesuai.

Saat ini tersedia:

```text
YahooProvider
InternalProvider
```

`InternalProvider` telah disiapkan sebagai struktur awal untuk integrasi Internal API.

Detail endpoint dan kontrak Internal API akan mengikuti spesifikasi yang diberikan pada tahap integrasi berikutnya.

---

## Logging

Application logging digunakan untuk mencatat aktivitas API dan error.

Contoh aktivitas yang dicatat:

```text
REST Request - Health Check
REST Request - Stock: BBCA.JK
Yahoo Provider - Get Stock Price: BBCA.JK
WebSocket Connected - Stock: BBCA.JK
WebSocket Data Sent - Stock: BBCA.JK
```

Log aplikasi disimpan pada:

```text
logs/app.log
```

Directory `logs/` tidak disimpan ke repository.

---

## Current Provider

Provider utama saat ini:

```text
Yahoo Finance
```

Data saham diperoleh melalui library:

```text
yfinance
```

Project menggunakan simbol saham Yahoo Finance, misalnya:

```text
BBCA.JK
BBRI.JK
BMRI.JK
```

---

## Future Development

Pengembangan berikutnya dapat mencakup:

* Integrasi Internal API
* Penyesuaian Internal Provider berdasarkan API contract
* Penggunaan database internal apabila telah tersedia
* Peningkatan monitoring dan observability
* Peningkatan dashboard
* Performance optimization
* Deployment production

---

## Notes

Project ini masih dalam tahap pengembangan. Implementasi `InternalProvider` saat ini belum terhubung ke Internal API karena endpoint dan API contract akan mengikuti spesifikasi yang diberikan pada tahap integrasi.

Yahoo Finance digunakan sebagai provider sementara untuk pengembangan dan pengujian API.
