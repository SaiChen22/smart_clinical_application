/**
 * API client for Clinical Data Reconciliation Engine
 * Uses native fetch API with typed responses
 */

import type {
  ReconciliationRequest,
  ReconciliationResponse,
  DataQualityRequest,
  DataQualityResponse,
  ApiError,
} from "../types";
import { ApiErrorException } from "./errors";

// ============================================================================
// Configuration
// ============================================================================

const API_BASE_URL = ""; // Empty for dev - Vite proxy handles /api routing
const API_KEY = import.meta.env.VITE_API_KEY || "development-key";

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Parse API error response and throw typed error
 */
async function handleErrorResponse(response: Response): Promise<never> {
  let errorData: ApiError;

  try {
    errorData = await response.json();
  } catch {
    errorData = { message: response.statusText };
  }

  const detail =
    errorData.detail || errorData.error || errorData.message || "Unknown error";
  throw new ApiErrorException(response.status, detail);
}

/**
 * Fetch wrapper with headers and error handling
 */
async function fetchApi<T>(
  endpoint: string,
  method: "GET" | "POST" = "POST",
  body?: unknown
): Promise<T> {
  const url = `${API_BASE_URL}/api${endpoint}`;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
  };

  const fetchOptions: RequestInit = {
    method,
    headers,
  };

  if (body) {
    fetchOptions.body = JSON.stringify(body);
  }

  const response = await fetch(url, fetchOptions);

  if (!response.ok) {
    await handleErrorResponse(response);
  }

  return response.json() as Promise<T>;
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Reconcile medications from multiple sources
 * @param request Reconciliation request with patient context and medication sources
 * @returns Reconciled medication information
 */
export async function reconcileMedication(
  request: ReconciliationRequest
): Promise<ReconciliationResponse> {
  return fetchApi<ReconciliationResponse>(
    "/reconciliation/reconcile",
    "POST",
    request
  );
}

/**
 * Validate data quality for patient records
 * @param request Data quality request with demographics and clinical data
 * @returns Data quality assessment with scores and issues
 */
export async function validateDataQuality(
  request: DataQualityRequest
): Promise<DataQualityResponse> {
  return fetchApi<DataQualityResponse>(
    "/data-quality/validate",
    "POST",
    request
  );
}

/**
 * Check API health status
 * @returns Health check response
 */
export async function checkHealth(): Promise<{ status: string }> {
  return fetchApi<{ status: string }>("/health", "GET");
}
