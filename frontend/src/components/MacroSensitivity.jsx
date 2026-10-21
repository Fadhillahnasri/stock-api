import { useEffect, useState } from 'react'
import api from '../services/api'

function MetricCard({ label, value }) {
  return (
    <article className="metric-card">
      <p>{label}</p>
      <h3>{value ?? '-'}</h3>
    </article>
  )
}

function formatNumber(value) {
  const number = Number(value)

  if (!Number.isFinite(number)) return '-'

  return number.toLocaleString('id-ID', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 4,
  })
}

function SensitivityPanel({ title, description, result, loading, error }) {
  const sensitivity = result?.sensitivity

  return (
    <section className="sensitivity-panel">
      <div className="sensitivity-heading">
        <div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
        {loading && <span className="loading-label">Memuat...</span>}
      </div>

      {error && <p className="error-message">{error}</p>}

      {!loading && !error && (
        <>
          <div className="stock-metrics">
            <MetricCard
              label="BETA"
              value={formatNumber(sensitivity?.beta)}
            />
            <MetricCard
              label="CORRELATION"
              value={formatNumber(sensitivity?.correlation)}
            />
            <MetricCard
              label="OBSERVASI"
              value={
                sensitivity?.observations != null
                  ? `${sensitivity.observations} hari`
                  : '-'
              }
            />
          </div>

          <p className="sensitivity-footnote">
            Benchmark: <strong>{result?.macro || title}</strong>
            {' | '}
            {sensitivity?.startDate || '-'}
            {' – '}
            {sensitivity?.endDate || '-'}
          </p>
        </>
      )}
    </section>
  )
}

export default function MacroSensitivity() {
  const [symbol, setSymbol] = useState('BBCA.JK')
  const [startDate, setStartDate] = useState('2025-09-02')
  const [endDate, setEndDate] = useState('2026-09-29')

  const [fxResult, setFxResult] = useState(null)
  const [oilResult, setOilResult] = useState(null)
  const [fxError, setFxError] = useState('')
  const [oilError, setOilError] = useState('')
  const [loading, setLoading] = useState(false)

  async function loadSensitivity() {
    if (!startDate || !endDate || startDate > endDate) {
      setFxError('Pastikan rentang tanggal valid.')
      setOilError('Pastikan rentang tanggal valid.')
      return
    }

    setLoading(true)
    setFxError('')
    setOilError('')
    setFxResult(null)
    setOilResult(null)

    const params = { symbol, startDate, endDate }

    const [fxResponse, oilResponse] = await Promise.allSettled([
      api.getMacroSensitivity({
        ...params,
        currency: 'USD',
      }),
      api.getOilSensitivity(params),
    ])

    if (fxResponse.status === 'fulfilled') {
      setFxResult(fxResponse.value)
    } else {
      setFxError(
        fxResponse.reason?.message || 'Gagal memuat sensitivitas USD/IDR.'
      )
    }

    if (oilResponse.status === 'fulfilled') {
      setOilResult(oilResponse.value)
    } else {
      setOilError(
        oilResponse.reason?.message || 'Gagal memuat sensitivitas WTI.'
      )
    }

    setLoading(false)
  }

  useEffect(() => {
    loadSensitivity()
  }, [])

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h2>Macro Sensitivity</h2>
          <p>
            Analisis hubungan historis return saham dengan perubahan
            USD/IDR dan harga WTI Oil.
          </p>
        </div>
      </div>

      <div className="macro-controls">
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
          />
        </label>

        <label>
          Tanggal akhir
          <input
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
          />
        </label>

        <button onClick={loadSensitivity} disabled={loading}>
          {loading ? 'Memuat...' : 'Analisis'}
        </button>
      </div>

      <SensitivityPanel
        title="USD/IDR Sensitivity"
        description="Sensitivitas historis saham terhadap perubahan kurs USD/IDR."
        result={fxResult}
        loading={loading}
        error={fxError}
      />

      <SensitivityPanel
        title="WTI Oil Price Sensitivity"
        description="Hubungan historis return saham dengan perubahan harga WTI."
        result={oilResult}
        loading={loading}
        error={oilError}
      />
    </section>
  )
}