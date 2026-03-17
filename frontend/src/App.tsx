import './App.css';
import { ReconciliationForm } from './features/reconciliation/ReconciliationForm';
import { ReconciliationPanel } from './features/reconciliation/ReconciliationPanel';
import { DataQualityForm } from './features/data-quality/DataQualityForm';
import { DataQualityPanel } from './features/data-quality/DataQualityPanel';
import { useReconcile, useDataQuality } from './hooks';

function App() {
  const {
    submit: submitReconcile,
    result: reconcileResult,
    loading: reconcileLoading,
    error: reconcileError
  } = useReconcile();

  const {
    submit: submitDataQuality,
    result: dataQualityResult,
    loading: dataQualityLoading,
    error: dataQualityError
  } = useDataQuality();

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
      <main className="flex-1 max-w-7xl mx-auto w-full p-8 space-y-6">
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <div className="space-y-6">
            <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide">
                  Medication Reconciliation
                </h2>
                {reconcileResult && (
                  <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-700 rounded-full">
                    Analysis Complete
                  </span>
                )}
              </div>
              <div className="p-6 space-y-8">
                <div>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Input Data</h3>
                  <ReconciliationForm 
                    onSubmit={submitReconcile} 
                    loading={reconcileLoading} 
                    error={reconcileError}
                  />
                </div>
                
                <div className="border-t border-gray-100 pt-6">
                   <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Analysis Results</h3>
                   <ReconciliationPanel result={reconcileResult} loading={reconcileLoading} />
                </div>
              </div>
            </section>
          </div>

          <div className="space-y-6">
            <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-full">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide">
                  Data Quality Check
                </h2>
                {dataQualityResult && (
                  <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-700 rounded-full">
                    Analysis Complete
                  </span>
                )}
              </div>
              <div className="p-6 space-y-8">
                <div>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Input Data</h3>
                  <DataQualityForm 
                    onSubmit={submitDataQuality} 
                    loading={dataQualityLoading}
                    error={dataQualityError}
                  />
                </div>
                
                <div className="border-t border-gray-100 pt-6">
                   <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Quality Analysis</h3>
                   <DataQualityPanel result={dataQualityResult} loading={dataQualityLoading} />
                </div>
              </div>
            </section>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;
