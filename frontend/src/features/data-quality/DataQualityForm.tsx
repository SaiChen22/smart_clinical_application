import { useState, type ChangeEvent, type FormEvent } from 'react';
import type { DataQualityRequest } from '../../types';

interface DataQualityFormProps {
  onSubmit: (request: DataQualityRequest) => void;
  loading?: boolean;
}

const INITIAL_DATA: DataQualityRequest = {
  demographics: { 
    name: 'John Doe', 
    dob: '1975-06-15', 
    gender: 'male' 
  },
  medications: ['Lisinopril 10mg'],
  allergies: ['Penicillin'],
  conditions: ['hypertension'],
  vital_signs: { 
    blood_pressure: '120/80', 
    heart_rate: 72, 
    temperature: 37.0 
  },
  last_updated: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
};

export function DataQualityForm({ onSubmit, loading = false }: DataQualityFormProps) {
  const [formData, setFormData] = useState<DataQualityRequest>(INITIAL_DATA);

  const handleDemographicsChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      demographics: { ...prev.demographics, [name]: value }
    }));
  };

  const handleVitalChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      vital_signs: {
        ...prev.vital_signs,
        [name]: name === 'blood_pressure' ? value : (value === '' ? null : Number(value))
      }
    }));
  };

  const handleListChange = (field: 'medications' | 'allergies' | 'conditions', value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value.split('\n')
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md" data-testid="data-quality-form">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Patient Data Entry</h2>

      {/* Demographics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            type="text"
            name="name"
            value={formData.demographics.name || ''}
            onChange={handleDemographicsChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">DOB</label>
          <input
            type="date"
            name="dob"
            value={formData.demographics.dob || ''}
            onChange={handleDemographicsChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Gender</label>
          <select
            name="gender"
            value={formData.demographics.gender || ''}
            onChange={handleDemographicsChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          >
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      {/* Vitals */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Blood Pressure</label>
          <input
            type="text"
            name="blood_pressure"
            value={formData.vital_signs.blood_pressure || ''}
            onChange={handleVitalChange}
            placeholder="e.g. 120/80"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Heart Rate</label>
          <input
            type="number"
            name="heart_rate"
            value={formData.vital_signs.heart_rate || ''}
            onChange={handleVitalChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Temperature (°C)</label>
          <input
            type="number"
            step="0.1"
            name="temperature"
            value={formData.vital_signs.temperature || ''}
            onChange={handleVitalChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
      </div>

      {/* Lists */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Medications (one per line)</label>
          <textarea
            value={formData.medications.join('\n')}
            onChange={(e) => handleListChange('medications', e.target.value)}
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Allergies (one per line)</label>
          <textarea
            value={formData.allergies.join('\n')}
            onChange={(e) => handleListChange('allergies', e.target.value)}
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Conditions (one per line)</label>
          <textarea
            value={formData.conditions.join('\n')}
            onChange={(e) => handleListChange('conditions', e.target.value)}
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
      </div>

      {/* Last Updated */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Last Updated</label>
        <input
          type="date"
          value={formData.last_updated || ''}
          onChange={(e) => setFormData(prev => ({ ...prev, last_updated: e.target.value }))}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
        />
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          data-testid="data-quality-submit"
          className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
            loading ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
          } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
        >
          {loading ? 'Analyzing...' : 'Analyze Data Quality'}
        </button>
      </div>
    </form>
  );
}
