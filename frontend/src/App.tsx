import { useState } from 'react';
import './App.css';
import { ReconciliationForm } from './features/reconciliation/ReconciliationForm';
import { ReconciliationPanel } from './features/reconciliation/ReconciliationPanel';
import type { ReconciliationRequest, ReconciliationResponse } from './types';

function App() {
  const [reconciliationResult, setReconciliationResult] = useState<ReconciliationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleReconciliationSubmit = async (_request: ReconciliationRequest) => {
    setLoading(true);
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock response based on the Metformin example
    const mockResponse: ReconciliationResponse = {
      reconciled_medication: "Metformin 1000mg extended-release",
      confidence_score: 0.92,
      reasoning: "Both sources agree on Metformin usage. Pharmacy fill data (1000mg) is more recent (2024-03-02) than Hospital EHR (500mg, 2024-02-20), suggesting a dosage increase. Patient condition (Type 2 Diabetes) supports this medication.",
      recommended_actions: [
        "Update current medication list to Metformin 1000mg",
        "Verify dosage increase with patient",
        "Schedule follow-up HbA1c in 3 months"
      ],
      clinical_safety_check: "PASSED"
    };

    setReconciliationResult(mockResponse);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 font-sans text-gray-900">
      {/* Header */}
      <header data-testid="app-header" className="bg-white border-b border-gray-200 px-8 py-4 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">
              C
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 leading-tight">Clinical Data Reconciliation</h1>
              <p className="text-xs text-gray-500 font-medium">AI-Powered Engine</p>
            </div>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>v1.0.0</span>
            <div className="w-8 h-8 rounded-full bg-gray-200"></div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full p-8 gap-8 grid grid-cols-12">
        
        {/* Left Column: Input Form (4 cols) */}
        <div className="col-span-12 lg:col-span-5 space-y-6">
          <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
              <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide">
                1. Input Data
              </h2>
            </div>
            <div className="p-6">
              <ReconciliationForm onSubmit={handleReconciliationSubmit} loading={loading} />
            </div>
          </section>
        </div>

        {/* Right Column: Results (8 cols) */}
        <div className="col-span-12 lg:col-span-7 space-y-6">
           <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-full">
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide">
                2. AI Analysis & Reconciliation
              </h2>
              {reconciliationResult && (
                <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-700 rounded-full">
                  Analysis Complete
                </span>
              )}
            </div>
            <div className="p-6">
              <ReconciliationPanel result={reconciliationResult} />
            </div>
          </section>
        </div>

      </main>
    </div>
  )
}

export default App
