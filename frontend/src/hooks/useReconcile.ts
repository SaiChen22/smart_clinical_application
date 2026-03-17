/**
 * Custom hook for medication reconciliation API integration
 * Manages state, loading, and error handling for reconciliation requests
 */

import { useState } from 'react';
import type { ReconciliationRequest, ReconciliationResponse } from '../types';
import { reconcileMedication } from '../lib/api';
import { ApiErrorException } from '../lib/errors';

interface UseReconcileReturn {
  submit: (request: ReconciliationRequest) => Promise<void>;
  result: ReconciliationResponse | null;
  loading: boolean;
  error: string | null;
  reset: () => void;
}

export default function useReconcile(): UseReconcileReturn {
  const [result, setResult] = useState<ReconciliationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (request: ReconciliationRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await reconcileMedication(request);
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
