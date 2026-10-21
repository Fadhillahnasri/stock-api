import { useEffect, useState } from 'react'
import api from '../services/api'

const DEFAULT_START = '2025-01-01'
const DEFAULT_END = '2026-09-29'

function formatRate(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  return `${number.toLocaleString('id-ID', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}%`
}

function formatBps(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  const prefix = number > 0 ? '+' : ''
  return `${prefix}${number.toLocaleString('id-ID')} bps`
}

function formatReturn(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  const prefix = number > 0 ? '+' : ''
  return `${prefix}${number.toLocaleString('id-ID', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}%`
}

function MetricCard({ label, value }) {
  return (
    <article className="metric-card">
      <p>{label}</p>
      <h3>{value}</h3>
    </article>
  )
}

export default function BIRateSensitivity() {
  const [symbol, setSymbol] = useState('BBCA.JK')
  const [startDate, setStartDate] = useState(DEFAULT_START)
  const [endDate, setEndDate] = useState(DEFAULT_END)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function loadEvents(event) {
    event?.preventDefault()

    if (!startDate || !endDate || startDate > endDate) {
      setError('Periksa kembali rentang tanggal yang dipilih.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await api.getBiRateSensitivity({
        symbol,
        startDate,
        endDate,
      })

      setResult(data)
    } catch (err) {
      setError(err.message || 'Gagal memuat BI-Rate Event Sensitivity.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadEvents()
  }, [])

  const events = Array.isArray(result?.events) ? result.events : []
  const latestEvent = events[events.length - 1]

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h2>BI-Rate Event Sensitivity</h2>
          <p>
            Return saham di sekitar tanggal perubahan suku bunga BI.
          </p>
        </div>
      </div>

      <form className="macro-controls" onSubmit={loadEvents}>
        <label>
          Saham
          <select
            value={symbol}
            onChange={(event) => setSymbol(event.target.value)}
          >
            <option value="BBCA.JK">BBCA — Bank Central Asia</option>
            <option value="BBRI.JK">BBRI — Bank Rakyat Indonesia</option>
            <option value="BMRI.JK">BMRI — Bank Mandiri</option>
            <option value="BBNI.JK">BBNI — Bank Negara Indonesia</option>
            <option value="TLKM.JK">TLKM — Telkom Indonesia</option>
            <option value="ASII.JK">ASII — Astra International</option>
            <option value="ANTM.JK">ANTM — Aneka Tambang</option>
          </select>
        </label>

        <label>
          Tanggal mulai
          <input
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
            required
          />
        </label>

        <label>
          Tanggal akhir
          <input
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Memuat...' : 'Tampilkan'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {loading && <p className="loading-label">Memuat data BI-Rate...</p>}

      {!loading && !error && result && (
        <>
          <div className="stock-metrics">
            <MetricCard
              label="EVENTS"
              value={`${result.observations ?? events.length} event`}
            />
            <MetricCard
              label="PERUBAHAN TERAKHIR"
              value={
                latestEvent ? formatBps(latestEvent.changeBps) : '-'
              }
            />
            <MetricCard
              label="BI-RATE TERAKHIR"
              value={
                latestEvent ? formatRate(latestEvent.currentRate) : '-'
              }
            />
          </div>

          {events.length > 0 ? (
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Tanggal</th>
                    <th>BI-Rate Sebelum</th>
                    <th>BI-Rate Sesudah</th>
                    <th>Perubahan</th>
                    <th>Return Saham</th>
                  </tr>
                </thead>

                <tbody>
                  {events.map((item, index) => {
                    const stockReturn = item.stockReturnPercentage

                    return (
                      <tr key={`${item.date}-${index}`}>
                        <td>{item.date}</td>
                        <td>{formatRate(item.previousRate)}</td>
                        <td>{formatRate(item.currentRate)}</td>
                        <td>{formatBps(item.changeBps)}</td>
                        <td
                          className={
                            stockReturn > 0
                              ? 'return-positive'
                              : stockReturn < 0
                                ? 'return-negative'
                                : ''
                          }
                        >
                          {stockReturn == null
                            ? '-'
                            : formatReturn(stockReturn)}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Tidak ada event BI-Rate pada rentang tanggal tersebut.</p>
          )}
        </>
      )}
    </section>
  )
}