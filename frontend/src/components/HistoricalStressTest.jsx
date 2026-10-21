
import { useEffect, useState } from 'react'
import { api } from '../services/api'

const formatRupiah = (value) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(Number(value) || 0)

const formatPercent = (value) =>
  `${(Number(value) || 0).toFixed(2)}%`

const formatLabel = (value) =>
  String(value || '').replace(/_/g, ' ')

function HistoricalStressTest() {
  const [scenarios, setScenarios] = useState([])
  const [portfolioDate, setPortfolioDate] = useState('2026-09-29')
  const [scenarioId, setScenarioId] = useState('')
  const [result, setResult] = useState(null)
  const [selectedGroup, setSelectedGroup] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadScenarios() {
      try {
        const data = await api.getHistoricalScenarios()
        const list = Array.isArray(data)
          ? data
          : data.scenarios || []

        setScenarios(list)

        if (list.length > 0) {
          setScenarioId(String(list[0].id))
        }
      } catch (err) {
        setError(err.message || 'Gagal mengambil daftar skenario.')
      }
    }

    loadScenarios()
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await api.getHistoricalStressTest(
        portfolioDate,
        scenarioId,
      )

      setResult(data)

      const groupNames = Object.keys(data.groups || {})
      setSelectedGroup((current) =>
        groupNames.includes(current) ? current : groupNames[0] || '',
      )
    } catch (err) {
      setError(err.message || 'Gagal menjalankan stress test.')
    } finally {
      setLoading(false)
    }
  }

  const groupNames = Object.keys(result?.groups || {})
  const group = result?.groups?.[selectedGroup]
  const stocks = group?.stocks || []

  return (
    <section className="panel historical-stress-panel">
      <div className="panel-heading">
        <div>
          <h2>Historical Stress Test</h2>
          <p>
            Simulasikan dampak skenario historis terhadap kelompok
            portofolio saham.
          </p>
        </div>
      </div>

      <form className="stress-controls" onSubmit={handleSubmit}>
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
          Skenario Historis
          <select
            value={scenarioId}
            onChange={(event) => setScenarioId(event.target.value)}
            required
          >
            <option value="">Pilih skenario</option>
            {scenarios.map((scenario) => (
              <option key={scenario.id} value={scenario.id}>
                {scenario.name || scenario.id}
              </option>
            ))}
          </select>
        </label>

        <button type="submit" disabled={loading || !scenarioId}>
          {loading ? 'Menghitung...' : 'Jalankan Stress Test'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {result && (
        <>
          <div className="historical-scenario-info">
            <h3>{result.scenario?.name || scenarioId}</h3>
            <p>{result.scenario?.description}</p>
            <p>
              Periode: {result.scenario?.startDate || '-'} sampai{' '}
              {result.scenario?.endDate || '-'}
            </p>
            {result.scenario?.source && (
              <p>Sumber: {result.scenario.source}</p>
            )}
          </div>

          <div className="historical-group-selector">
            <label htmlFor="historical-group">Kelompok Portofolio</label>
            <select
              id="historical-group"
              value={selectedGroup}
              onChange={(event) => setSelectedGroup(event.target.value)}
            >
              {groupNames.map((name) => (
                <option key={name} value={name}>
                  {formatLabel(name)}
                </option>
              ))}
            </select>
          </div>

          {group && (
            <>
              <div className="stress-summary">
                <div className="stress-metric">
                  <span>Nilai Pasar Portofolio</span>
                  <strong>{formatRupiah(group.marketValue)}</strong>
                </div>
                <div className="stress-metric">
                  <span>Nilai Pasar Tercakup</span>
                  <strong>{formatRupiah(group.coveredMarketValue)}</strong>
                </div>
                <div className="stress-metric">
                  <span>Coverage</span>
                  <strong>
                    {formatPercent(group.coveragePercentage)}
                  </strong>
                </div>
                <div className="stress-metric">
                  <span>Estimasi Return</span>
                  <strong
                    className={
                      Number(group.portfolioReturnPercentage) >= 0
                        ? 'return-positive'
                        : 'return-negative'
                    }
                  >
                    {formatPercent(group.portfolioReturnPercentage)}
                  </strong>
                </div>
                <div className="stress-metric">
                  <span>Estimasi Dampak</span>
                  <strong>{formatRupiah(group.estimatedImpact)}</strong>
                </div>
                <div className="stress-metric">
                  <span>Nilai Setelah Stress (Aset Tercakup)</span>
                  <strong>
                    {formatRupiah(group.portfolioValueAfterCoveredAssets)}
                  </strong>
                </div>
              </div>

              {group.status !== 'complete' && (
                <p className="stress-warning">
                  Status: {formatLabel(group.status)}.
                  {group.missingStocks?.length > 0 &&
                    ` Data return tidak tersedia untuk: ${group.missingStocks.join(', ')}.`}
                </p>
              )}

              {group.message && <p>{group.message}</p>}

              {stocks.length > 0 && (
                <div className="table-wrapper">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Kode Saham</th>
                        <th>Bobot Portofolio</th>
                        <th>Return Skenario</th>
                        <th>Kontribusi Return</th>
                      </tr>
                    </thead>
                    <tbody>
                      {stocks.map((stock, index) => (
                        <tr
                          key={`${stock.stockCode || stock.code || 'stock'}-${index}`}
                        >
                          <td>{stock.stockCode || stock.code || '-'}</td>
                          <td>
                            {formatPercent(stock.portfolioWeight)}
                          </td>
                          <td>
                            {formatPercent(
                              stock.scenarioReturnPercentage ??
                                stock.returnPercentage ??
                                stock.stockReturnPercentage,
                            )}
                          </td>
                          <td>
                        {formatPercent(
                            stock.contributionPercentage
                        )}
                        </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </>
      )}
    </section>
  )
}

export default HistoricalStressTest
