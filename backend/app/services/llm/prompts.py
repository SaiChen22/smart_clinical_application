# Why this system prompt is structured this way:
# 1) It frames the model as a clinical reconciliation assistant to bias toward
#    medically relevant reasoning.
# 2) It explicitly requires valid JSON only, preventing prose wrappers that
#    break parsers.
# 3) It anchors expected keys to the API response model so outputs stay aligned
#    with schema validation.
RECONCILIATION_SYSTEM_PROMPT = """
You are a clinical pharmacist AI assistant focused on medication reconciliation.
Prioritize patient safety, consistency across source systems, and practical next steps.

Return ONLY valid JSON (no markdown, no code fences, no extra commentary) with keys:
- reconciled_medication: string
- confidence_score: number between 0.0 and 1.0
- reasoning: string
- recommended_actions: array of strings
- clinical_safety_check: one of ["PASSED", "FAILED", "WARNING"]
""".strip()


# Why this user prompt format is used:
# 1) We present patient context first to ensure recommendations are clinically grounded.
# 2) Source-by-source bullet formatting reduces ambiguity in cross-system comparison.
# 3) A direct final instruction reiterates schema expectations to reduce malformed output.
RECONCILIATION_USER_PROMPT_TEMPLATE = """
Patient context:
- Age: {age}
- Active conditions: {conditions}
- Recent labs: {recent_labs}

Medication source records (reconcile conflicts and choose best canonical medication):
{sources}

Produce a single reconciled result in strict JSON with the required keys.
""".strip()


# Why this system prompt is structured this way:
# 1) It asks for scored dimensions that map exactly to QualityBreakdown.
# 2) It mandates integer ranges (0-100) to align with schema constraints.
# 3) It requires explicit issue objects so the UI can render actionable findings.
DATA_QUALITY_SYSTEM_PROMPT = """
You are a healthcare data quality analyst.
Assess record quality across completeness, accuracy, timeliness, and clinical plausibility.

Return ONLY valid JSON with keys:
- overall_score: integer 0-100
- breakdown: object with integer keys {completeness, accuracy, timeliness, clinical_plausibility}
- issues_detected: array of objects with keys {field, issue, severity}

For severity, use only: "low", "medium", "high".
""".strip()


# Why this user prompt format is used:
# 1) Flattened, explicit field presentation avoids missing sparse EHR attributes.
# 2) Section grouping mirrors quality dimensions to guide structured scoring.
# 3) Final instruction asks for conservative uncertainty handling to avoid overconfidence.
DATA_QUALITY_USER_PROMPT_TEMPLATE = """
Evaluate this patient dataset:

Demographics:
- Name: {name}
- DOB: {dob}
- Gender: {gender}

Clinical lists:
- Medications: {medications}
- Allergies: {allergies}
- Conditions: {conditions}

Vital signs:
- Blood pressure: {blood_pressure}
- Heart rate: {heart_rate}
- Temperature: {temperature}

Metadata:
- Last updated: {last_updated}

Return strict JSON only. Be conservative if information is incomplete or implausible.
""".strip()
