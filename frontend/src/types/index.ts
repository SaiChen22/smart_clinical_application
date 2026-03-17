/**
 * TypeScript type definitions for Clinical Data Reconciliation Engine
 * Mirrors backend Pydantic schemas exactly
 */

// ============================================================================
// Reconciliation Types
// ============================================================================

export interface PatientContext {
  age: number;
  conditions: string[];
  recent_labs: Record<string, number>;
}

export interface MedicationSource {
  system: string;
  medication: string;
  last_updated: string | null;
  last_filled: string | null;
  source_reliability: "high" | "medium" | "low";
}

export interface ReconciliationRequest {
  patient_context: PatientContext;
  sources: MedicationSource[];
}

export interface ReconciliationResponse {
  reconciled_medication: string;
  confidence_score: number;
  reasoning: string;
  recommended_actions: string[];
  clinical_safety_check: "PASSED" | "FAILED" | "WARNING";
}

// ============================================================================
// Data Quality Types
// ============================================================================

export interface Demographics {
  name: string | null;
  dob: string | null;
  gender: string | null;
}

export interface VitalSigns {
  blood_pressure: string | null;
  heart_rate: number | null;
  temperature: number | null;
}

export interface IssueDetected {
  field: string;
  issue: string;
  severity: "low" | "medium" | "high";
}

export interface QualityBreakdown {
  completeness: number;
  accuracy: number;
  timeliness: number;
  clinical_plausibility: number;
}

export interface DataQualityRequest {
  demographics: Demographics;
  medications: string[];
  allergies: string[];
  conditions: string[];
  vital_signs: VitalSigns;
  last_updated: string | null;
}

export interface DataQualityResponse {
  overall_score: number;
  breakdown: QualityBreakdown;
  issues_detected: IssueDetected[];
}

// ============================================================================
// Error Types
// ============================================================================

export interface ApiError {
  detail?: string;
  error?: string;
  message?: string;
  status?: number;
}
