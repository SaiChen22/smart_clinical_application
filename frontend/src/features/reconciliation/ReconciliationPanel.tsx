import { useState } from 'react';
import type { ReconciliationResponse } from '../../types';
import { ConfidenceBar } from '../../components/ConfidenceBar';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { ErrorMessage } from '../../components/ErrorMessage';

interface ReconciliationPanelProps {
  result: ReconciliationResponse | null;
  loading?: boolean;
  error?: string | null;
}

export function ReconciliationPanel({ result, loading = false, error = null }: ReconciliationPanelProps) {
  const [status, setStatus] = useState<'pending' | 'approved' | 'rejected'>('pending');

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (loading) {
    return <LoadingSpinner message="Reconciling medications..." />;
  }

  if (!result) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200 p-12">
        <div className="text-center">
          <p>Submit a medication reconciliation request to see results</p>
        </div>
      </div>
    );
  }

  const getSafetyBadgeColor = (check: string) => {
    switch (check) {
      case 'PASSED': return 'bg-green-100 text-green-800 border-green-200';
      case 'WARNING': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'FAILED': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSafetyIcon = (check: string) => {
    switch (check) {
      case 'PASSED': return (
        <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      );
      case 'WARNING': return (
        <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      );
      case 'FAILED': return (
        <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      );
      default: return null;
    }
  };

  return (
    <div className="space-y-6 animate-fade-in" data-testid="reconciliation-result">
      {/* Header Result */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div className="flex justify-between items-start mb-4">
          <div>
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Reconciled Medication</span>
            <h2 className="text-2xl font-bold text-gray-900 mt-1">{result.reconciled_medication}</h2>
          </div>
          <div className={`px-3 py-1 rounded-full flex items-center text-sm font-medium border ${getSafetyBadgeColor(result.clinical_safety_check)}`} data-testid="safety-check">
            {getSafetyIcon(result.clinical_safety_check)}
            {result.clinical_safety_check}
          </div>
        </div>

        <div className="mb-6">
          <ConfidenceBar score={result.confidence_score} />
        </div>

        <div className="prose prose-sm max-w-none">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Clinical Reasoning</h4>
          <p className="text-gray-600 bg-gray-50 p-3 rounded-md border border-gray-100 leading-relaxed">
            {result.reasoning}
          </p>
        </div>
      </div>

      {/* Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wider">Recommended Actions</h3>
        <ul className="space-y-2">
          {result.recommended_actions.map((action, idx) => (
            <li key={idx} className="flex items-start">
              <svg className="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-gray-700">{action}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Approval Flow */}
      <div className="flex gap-4 pt-2">
        <button
          onClick={() => setStatus(status === 'approved' ? 'pending' : 'approved')}
          className={`flex-1 py-3 px-4 rounded-md font-medium shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 flex items-center justify-center ${
            status === 'approved'
              ? 'bg-green-600 text-white hover:bg-green-700'
              : 'bg-white text-green-700 border border-green-300 hover:bg-green-50'
          }`}
        >
          {status === 'approved' ? (
            <>
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>
              Approved
            </>
          ) : 'Approve Recommendation'}
        </button>
        
        <button
          onClick={() => setStatus(status === 'rejected' ? 'pending' : 'rejected')}
          className={`flex-1 py-3 px-4 rounded-md font-medium shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 flex items-center justify-center ${
            status === 'rejected'
              ? 'bg-red-600 text-white hover:bg-red-700'
              : 'bg-white text-red-700 border border-red-300 hover:bg-red-50'
          }`}
        >
          {status === 'rejected' ? (
             <>
             <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
             Rejected
           </>
          ) : 'Reject'}
        </button>
      </div>
    </div>
  );
}
