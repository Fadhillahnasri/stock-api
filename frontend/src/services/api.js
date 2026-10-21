const API_BASE_URL = 'http://127.0.0.1:8000'

async function apiRequest(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`)

  if (!response.ok) {
    let message = `Request gagal: ${response.status}`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Gunakan pesan default jika response bukan JSON.
    }

    throw new Error(message)
  }

  return response.json()
}

export const api = {
  getHealth: () => apiRequest('/health'),

  getStock: (symbol) =>
    apiRequest(`/stock/${encodeURIComponent(symbol)}`),

  getPortfolioAnalysis: (date) =>
    apiRequest(`/portfolio/analysis?date=${encodeURIComponent(date)}`),

  getHistoricalScenarios: () =>
    apiRequest('/stress-test/scenarios'),

  getHistoricalStressTest: (portfolioDate, scenarioId) =>
    apiRequest(
    `/stress-test/historical/multi-group?portfolioDate=${encodeURIComponent(portfolioDate)}&scenarioId=${encodeURIComponent(scenarioId)}`
  ),

  getCustomStressTest: ({
    portfolioDate,
    startDate,
    endDate,
    targetFx,
    oilShock,
  }) => {
    const params = new URLSearchParams({
      portfolioDate,
      startDate,
      endDate,
      targetFx: String(targetFx),
      oilShock: String(oilShock),
    })

    return apiRequest(`/stress-test/custom?${params.toString()}`)
  },

  getMacroSensitivity: ({ symbol, currency, startDate, endDate }) => {
    const params = new URLSearchParams({
      symbol,
      currency: currency || 'USD',
      startDate,
      endDate,
    })

    return apiRequest(`/macro/sensitivity?${params.toString()}`)
  },

  getOilSensitivity: ({ symbol, startDate, endDate }) => {
    const params = new URLSearchParams({
      symbol,
      startDate,
      endDate,
    })

    return apiRequest(`/macro/oil-price/sensitivity?${params.toString()}`)
  },

  getBiRateSensitivity: ({ symbol, startDate, endDate }) => {
    const params = new URLSearchParams({
      symbol,
      startDate,
      endDate,
    })

    return apiRequest(`/macro/bi-rate/sensitivity?${params.toString()}`)
  },
}

export default api
