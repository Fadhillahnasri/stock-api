import { useState } from 'react'
import api from '../services/api'

function formatMoney(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(number)
}

function formatPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  return `${number.toLocaleString('id-ID', {
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

function StockRanking({ title, stocks, positive }) {
  return (
    <div className="ranking-card">
      <h3>{title}</h3>

      {!stocks?.length ? (
        <p>Data tidak tersedia.</p>
      ) : (
        <div className="ranking-list">
          {stocks.map((stock) => (
            <div className="ranking-row" key={stock.stockCode}>
              <strong>{stock.stockCode}</strong>
              <span className={positive ? 'return-positive' : 'return-negative'}>
                {formatPercent(stock.performancePercentage)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function PortfolioAnalysis() {
  const [date, setDate] = useState('2026-09-29')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function loadPortfolio(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await api.getPortfolioAnalysis(date)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Gagal memuat analisis portofolio.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading portfolio-heading">
        <div>
          <h2>Portfolio Analysis</h2>
          <p>Analisis portofolio berdasarkan tanggal.</p>
        </div>

        <form className="portfolio-date-form" onSubmit={loadPortfolio}>
          <label htmlFor="portfolio-analysis-date">Tanggal</label>
          <input
            id="portfolio-analysis-date"
            type="date"
            value={date}
            onChange={(event) => setDate(event.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Memuat...' : 'Tampilkan'}
          </button>
        </form>
      </div>

      {error && <p className="error-message">{error}</p>}
      {loading && <p className="loading-label">Memuat analisis portofolio...</p>}

      {result && (
        <>
          <div className="stock-metrics portfolio-metrics">
            <MetricCard
              label="Total Cost Basis"
              value={formatMoney(result.totalCostBasis)}
            />
            <MetricCard
              label="Total Market Value"
              value={formatMoney(result.totalMarketValue)}
            />
            <MetricCard
              label="Unrealized Gain/Loss"
              value={formatMoney(result.totalUnrealizedGainLoss)}
            />
            <MetricCard
              label="Performance"
              value={formatPercent(result.totalUnrealizedGainLossPercentage)}
            />
          </div>

          <div className="ranking-grid">
            <StockRanking
              title="📈 Top Gainers"
              stocks={result.topGainers}
              positive
            />
            <StockRanking
              title="📉 Top Losers"
              stocks={result.topLosers}
              positive={false}
            />
          </div>
        </>
      )}
    </section>
  )
}