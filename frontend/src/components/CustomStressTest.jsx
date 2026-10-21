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

function formatNumber(value, digits = 2) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '-'

  return number.toLocaleString('id-ID', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
}

export default function CustomStressTest() {
  const [portfolioDate, setPortfolioDate] = useState('2026-09-29')
  const [startDate, setStartDate] = useState('2025-05-21')
  const [endDate, setEndDate] = useState('2026-09-29')
  const [targetFx, setTargetFx] = useState('25000')
  const [oilShock, setOilShock] = useState('-40')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function runSimulation(event) {
    event.preventDefault()

    if (!portfolioDate || !startDate || !endDate || startDate > endDate) {
      setError('Periksa tanggal portofolio dan rentang tanggal analisis.')
      return
    }

    if (!Number.isFinite(Number(targetFx)) || Number(targetFx) <= 0) {
      setError('Target USD/IDR harus berupa angka positif.')
      return
    }

    if (
      !Number.isFinite(Number(oilShock)) ||
      Number(oilShock) < -100
    ) {
      setError('WTI Oil Shock harus berupa angka dan tidak boleh kurang dari -100%.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await api.getCustomStressTest({
        portfolioDate,
        startDate,
        endDate,
        targetFx: Number(targetFx),
        oilShock: Number(oilShock),
      })

      setResult(data)
    } catch (err) {
      setError(err.message || 'Gagal menjalankan simulasi.')
    } finally {
      setLoading(false)
    }
  }

  const scenario = result?.scenario ?? {}
  const portfolio = result?.portfolio ?? {}

  const stocks = portfolio.stocks ?? []

  const estimatedReturn = portfolio.portfolioReturnPercentage
  const coverage = portfolio.coveragePercentage
  const fxShock = scenario.fxShockPercentage
  const oilShockResult = scenario.oilShockPercentage

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h2>Custom Worst-Case Simulator</h2>
          <p>
            Simulasikan dampak perubahan USD/IDR dan harga WTI terhadap portofolio.
          </p>
        </div>
      </div>

      <form className="stress-controls" onSubmit={runSimulation}>
        <label>
          Tanggal Portofolio
          <input
            type="date"
            value={portfolioDate}
            onChange={(event) => setPortfolioDate(event.target.value)}
            required
          />
        </label>

        <label>
          Tanggal Mulai Analisis
          <input
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
            required
          />
        </label>

        <label>
          Tanggal Akhir Analisis
          <input
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
            required
          />
        </label>

        <label>
          Target USD/IDR
          <input
            type="number"
            min="1"
            step="any"
            value={targetFx}
            onChange={(event) => setTargetFx(event.target.value)}
            required
          />
        </label>

        <label>
          WTI Oil Shock (%)
          <input
            type="number"
            min="-100"
            step="any"
            value={oilShock}
            onChange={(event) => setOilShock(event.target.value)}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Menjalankan...' : 'Run Simulation'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {result && (
        <>
          <div className="stock-metrics stress-summary">
            <article className="metric-card">
              <p>FX Shock</p>
              <h3>{formatPercent(fxShock)}</h3>
            </article>

            <article className="metric-card">
              <p>Oil Shock</p>
              <h3>{formatPercent(oilShockResult ?? oilShock)}</h3>
            </article>

            <article className="metric-card">
              <p>Coverage</p>
              <h3>{formatPercent(coverage)}</h3>
            </article>
          </div>

          <div className="stress-return">
            <p>Estimated Portfolio Return</p>
            <h3>{formatPercent(estimatedReturn)}</h3>
          </div>

          {Array.isArray(stocks) && stocks.length > 0 && (
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Stock</th>
                    <th>Weight</th>
                    <th>FX Beta</th>
                    <th>Oil Beta</th>
                    <th>Estimated Return</th>
                  </tr>
                </thead>
                <tbody>
                  {stocks.map((stock, index) => (
                    <tr key={stock.symbol}>
                    <td>{stock.symbol}</td>
                    <td>{formatPercent(stock.weight * 100)}</td>
                    <td>{formatNumber(stock.fxBeta)}</td>
                    <td>{formatNumber(stock.oilBeta)}</td>
                    <td>{formatPercent(stock.estimatedReturnPercentage)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </section>
  )
}