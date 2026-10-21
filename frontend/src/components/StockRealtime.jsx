import { useEffect, useRef, useState } from 'react'
import { connectStockWebSocket } from '../services/websocket'

const STOCKS = [
  { symbol: 'BBCA.JK', name: 'Bank Central Asia' },
  { symbol: 'BBRI.JK', name: 'Bank Rakyat Indonesia' },
  { symbol: 'BMRI.JK', name: 'Bank Mandiri' },
  { symbol: 'BBNI.JK', name: 'Bank Negara Indonesia' },
  { symbol: 'TLKM.JK', name: 'Telkom Indonesia' },
  { symbol: 'ASII.JK', name: 'Astra International' },
  { symbol: 'ANTM.JK', name: 'Aneka Tambang' },
  { symbol: 'GOTO.JK', name: 'GoTo Gojek Tokopedia' },
]

function formatPrice(value) {
  const number = Number(value)

  if (!Number.isFinite(number)) return '-'

  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 2,
  }).format(number)
}

function formatTimestamp(value) {
  if (!value) return '-'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)

  return date.toLocaleString('id-ID')
}

function findValue(data, keys) {
  for (const key of keys) {
    if (data?.[key] !== undefined && data[key] !== null) {
      return data[key]
    }
  }

  return undefined
}

export default function StockRealtime() {
  const [symbol, setSymbol] = useState('BBCA.JK')
  const [status, setStatus] = useState('disconnected')
  const [stockData, setStockData] = useState(null)
  const [error, setError] = useState('')
  const connectionRef = useRef(null)

  useEffect(() => {
    return () => {
      connectionRef.current?.disconnect()
      connectionRef.current = null
    }
  }, [])

  function handleConnect() {
    connectionRef.current?.disconnect()
    connectionRef.current = null

    setStockData(null)
    setError('')
    setStatus('connecting')

    try {
      connectionRef.current = connectStockWebSocket(symbol, {
        onStatus: (nextStatus) => {
          setStatus(nextStatus)

          if (nextStatus === 'connected') {
            setError('')
          }
        },
        onMessage: (data) => {
          const stock = data?.data ?? data

          setStockData((previous) => ({
            ...previous,
            ...stock,
            currentPrice:
              findValue(stock, ['current_price', 'currentPrice', 'price']) ??
              previous?.currentPrice,
            high:
              findValue(stock, ['high', 'day_high', 'dayHigh']) ??
              previous?.high,
            low:
              findValue(stock, ['low', 'day_low', 'dayLow']) ??
              previous?.low,
            updatedAt:
              findValue(stock, [
                'timestamp',
                'updated_at',
                'updatedAt',
                'time',
              ]) ?? new Date().toISOString(),
          }))
        },
        onError: (message) => setError(message),
      })
    } catch (err) {
      setStatus('error')
      setError(err.message || 'Gagal membuat koneksi WebSocket.')
    }
  }

  function handleDisconnect() {
    connectionRef.current?.disconnect()
    connectionRef.current = null
    setStatus('disconnected')
  }

  const connected = status === 'connected'
  const busy = status === 'connecting'

  return (
    <section className="panel stock-panel">
      <div className="panel-heading">
        <div>
          <h2>Real-time Stock Dashboard</h2>
          <p>Pemantauan harga saham melalui WebSocket</p>
        </div>

        <span className={`connection-status ${status}`}>
          {status === 'connected'
            ? 'Terhubung'
            : status === 'connecting'
              ? 'Menghubungkan...'
              : status === 'error'
                ? 'Error'
                : 'Terputus'}
        </span>
      </div>

      <div className="stock-controls">
        <label>
          Pilih Saham
          <select
            value={symbol}
            onChange={(event) => {
              setSymbol(event.target.value)
              setStockData(null)
              setError('')
              connectionRef.current?.disconnect()
              connectionRef.current = null
              setStatus('disconnected')
            }}
          >
            {STOCKS.map((stock) => (
              <option key={stock.symbol} value={stock.symbol}>
                {stock.symbol} — {stock.name}
              </option>
            ))}
          </select>
        </label>

        <div className="stock-actions">
          <button onClick={handleConnect} disabled={connected || busy}>
            {busy ? 'Menghubungkan...' : 'Hubungkan'}
          </button>

          <button
            className="secondary-button"
            onClick={handleDisconnect}
            disabled={status === 'disconnected'}
          >
            Putuskan
          </button>
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="stock-metrics">
        <article className="metric-card">
          <p>Harga Saat Ini</p>
          <h3>{formatPrice(stockData?.currentPrice)}</h3>
        </article>

        <article className="metric-card">
          <p>Harga Tertinggi</p>
          <h3>
            {formatPrice(
              findValue(stockData, ['high', 'day_high', 'dayHigh']),
            )}
          </h3>
        </article>

        <article className="metric-card">
          <p>Harga Terendah</p>
          <h3>
            {formatPrice(
              findValue(stockData, ['low', 'day_low', 'dayLow']),
            )}
          </h3>
        </article>
      </div>

      <p className="stock-timestamp">
        Pembaruan terakhir:{' '}
        {formatTimestamp(stockData?.updatedAt)}
      </p>
    </section>
  )
}