/**
 * Custom hook for data quality validation API integration
 * Manages state, loading, and error handling for data quality requests
 */

import { useState } from 'react';
import type { DataQualityRequest, DataQualityResponse } from '../types';
import { validateDataQuality } from '../lib/api';
import { ApiErrorException } from '../lib/errors';

interface UseDataQualityReturn {
  submit: (request: DataQualityRequest) => Promise<void>;
  result: DataQualityResponse | null;
  loading: boolean;
  error: string | null;
  reset: () => void;
}

export default function useDataQuality(): UseDataQualityReturn {
  const [result, setResult] = useState<DataQualityResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (request: DataQualityRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await validateDataQuality(request);
      setResult(response);
    } catch (err) {
      if (err instanceof ApiErrorException) {
        setError(`API Error (${err.status}): ${err.detail}`);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Unknown error occurred');
      }
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
    setLoading(false);
  };

  return { submit, result, loading, error, reset };
}
