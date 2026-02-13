# System Architecture: PostOp-Dementia-Risk-Scanner

## 1. Data Layer (The Inputs)
* **FHIR Patient Resource**: Used for age-based risk calculation.
* **FHIR MedicationRequest**: Scanned against RxNorm CUI library for anticholinergic/sedative burden.
* **FHIR DocumentReference**: NLP-lite keyword scanning of clinical note metadata (H&Ps, Consults).

## 2. Logic Layer (The Engine)
* **Decoupled Configuration**: All clinical thresholds (Age > 75, Risk Weights) are stored in `risk_config.json` to allow clinical updates without code changes.
* **Aggregated Scoring**: 
    - Age > 75: +2
    - High-Risk Med: +2 to +3 per med
    - Clinical Note Keyword: +2 per mention

## 3. Presentation Layer (The Dashboard)
* **Terminal/Console Output**: Current v1.0 provides a text-based surgical risk report.
* **Future State**: SMART on FHIR web interface for real-time EHR integration.
