import './App.css'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Header */}
      <header data-testid="app-header" className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 shadow-lg">
        <h1 className="text-4xl font-bold">Clinical Data Reconciliation Engine</h1>
        <p className="text-purple-100 mt-2">AI-powered clinical data reconciliation and quality assessment</p>
      </header>

      {/* Main content area - two panels */}
      <div className="flex flex-1 gap-4 p-6">
        {/* Left Panel - Medication Reconciliation */}
        <div
          data-testid="reconciliation-panel"
          className="flex-1 bg-gray-50 border border-gray-200 rounded-lg p-6 shadow"
        >
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Medication Reconciliation
          </h2>
          <div className="bg-white p-4 rounded border border-gray-300">
            <p className="text-gray-600">
              Reconciliation panel will display medication records here.
            </p>
          </div>
        </div>

        {/* Right Panel - Data Quality Assessment */}
        <div
          data-testid="data-quality-panel"
          className="flex-1 bg-gray-50 border border-gray-200 rounded-lg p-6 shadow"
        >
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Data Quality Assessment
          </h2>
          <div className="bg-white p-4 rounded border border-gray-300">
            <p className="text-gray-600">
              Data quality metrics and assessment results will appear here.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
