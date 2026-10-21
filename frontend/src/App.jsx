import './App.css'
import StockRealtime from './components/StockRealtime'
import MacroSensitivity from './components/MacroSensitivity'
import CustomStressTest from './components/CustomStressTest'
import BIRateSensitivity from './components/BIRateSensitivity'
import PortfolioAnalysis from './components/PortfolioAnalysis'
import HistoricalStressTest from './components/HistoricalStressTest'

function App() {
  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Portfolio Risk Dashboard</h1>
          <p>Dashboard Manajemen Risiko Portofolio</p>
        </div>
        <span className="status">React Frontend</span>
      </header>

      <main className="dashboard">
        <section className="welcome">
          <h2>Portfolio Overview</h2>
          <p>
            Pantau harga saham real-time, sensitivitas makroekonomi,
            performa portofolio, dan hasil stress test.
          </p>
        </section>

        <StockRealtime />

        <MacroSensitivity />

        <CustomStressTest />

        <BIRateSensitivity />

        <PortfolioAnalysis />

        <HistoricalStressTest />

      </main>
    </div>
  )
}

export default App
