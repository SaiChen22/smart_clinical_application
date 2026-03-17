import { useState } from 'react';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import type { ReconciliationRequest, MedicationSource } from '../../types';

interface ReconciliationFormProps {
  onSubmit: (request: ReconciliationRequest) => Promise<void>;
  loading?: boolean;
  error?: string | null;
}

const DEFAULT_SOURCE: MedicationSource = {
  system: '',
  medication: '',
  last_updated: new Date().toISOString().split('T')[0],
  last_filled: null,
  source_reliability: 'medium',
};

// Metformin example from assessment
const INITIAL_STATE: ReconciliationRequest = {
  patient_context: {
    age: 58,
    conditions: ['type 2 diabetes'],
    recent_labs: { hba1c: 7.1 },
  },
  sources: [
    {
      system: 'Hospital EHR',
      medication: 'Metformin 500mg',
      last_updated: '2024-02-20',
      last_filled: null,
      source_reliability: 'high',
    },
    {
      system: 'Pharmacy',
      medication: 'Metformin 1000mg',
      last_updated: '2024-03-02',
      last_filled: null,
      source_reliability: 'high',
    },
  ],
};

export function ReconciliationForm({ onSubmit, loading = false, error = null }: ReconciliationFormProps) {
  const [formData, setFormData] = useState<ReconciliationRequest>(INITIAL_STATE);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const updatePatientContext = <K extends keyof ReconciliationRequest['patient_context']>(
    field: K,
    value: ReconciliationRequest['patient_context'][K]
  ) => {
    setFormData(prev => ({
      ...prev,
      patient_context: {
        ...prev.patient_context,
        [field]: value,
      },
    }));
  };

  const updateSource = <K extends keyof MedicationSource>(
    index: number,
    field: K,
    value: MedicationSource[K]
  ) => {
    const newSources = [...formData.sources];
    newSources[index] = { ...newSources[index], [field]: value };
    setFormData(prev => ({ ...prev, sources: newSources }));
  };

  const addSource = () => {
    setFormData(prev => ({
      ...prev,
      sources: [...prev.sources, { ...DEFAULT_SOURCE }],
    }));
  };

  const removeSource = (index: number) => {
    setFormData(prev => ({
      ...prev,
      sources: prev.sources.filter((_, i) => i !== index),
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6" data-testid="reconciliation-form">
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4" role="alert">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">
                {error}
              </p>
            </div>
          </div>
        </div>
      )}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Patient Context</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
            <input
              type="number"
              value={formData.patient_context.age}
              onChange={(e) => updatePatientContext('age', parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Conditions (comma separated)</label>
            <input
              type="text"
              value={formData.patient_context.conditions.join(', ')}
              onChange={(e) => updatePatientContext('conditions', e.target.value.split(',').map(c => c.trim()))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div className="flex justify-between items-center mb-4 border-b pb-2">
          <h3 className="text-lg font-semibold text-gray-800">Medication Sources</h3>
          <button
            type="button"
            onClick={addSource}
            className="px-3 py-1 text-sm bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
          >
            + Add Source
          </button>
        </div>
        
        <div className="space-y-4">
          {formData.sources.map((source, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-md border border-gray-200 relative group">
              <button
                type="button"
                onClick={() => removeSource(index)}
                className="absolute top-2 right-2 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                aria-label="Remove source"
              >
                ×
              </button>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">System</label>
                  <input
                    type="text"
                    value={source.system}
                    onChange={(e) => updateSource(index, 'system', e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                    placeholder="e.g. Hospital EHR"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Medication</label>
                  <input
                    type="text"
                    value={source.medication}
                    onChange={(e) => updateSource(index, 'medication', e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                    placeholder="e.g. Metformin 500mg"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Last Updated</label>
                  <input
                    type="date"
                    value={source.last_updated || ''}
                    onChange={(e) => updateSource(index, 'last_updated', e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Reliability</label>
                  <select
                    value={source.source_reliability}
                    onChange={(e) => updateSource(index, 'source_reliability', e.target.value as MedicationSource['source_reliability'])}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end pt-2">
        <button
          type="submit"
          disabled={loading}
          data-testid="reconciliation-submit"
          className={`px-6 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors ${
            loading ? 'opacity-70 cursor-not-allowed' : ''
          }`}
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <LoadingSpinner size="sm" />
              <span>Reconciling...</span>
            </div>
          ) : (
            'Reconcile Medications'
          )}
        </button>
      </div>
    </form>
  );
}
