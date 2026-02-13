Project: Post-Op Dementia Risk Scanner (v1.0-Alpha)

The Problem: As the surgical population ages, postoperative delirium (POD) and cognitive decline (POCD) remain under-identified, leading to increased LOS, costs, and patient morbidity.

The Solution: A FHIR-native, AI-assisted risk stratification engine that monitors EHR data in real-time. By aggregating structured data (RxNorm, ICD-10) and unstructured clinical notes (NLP keywords), the tool identifies high-risk elderly patients before they enter the OR.

Core Architecture:

Interoperability: Built on HL7 FHIR (R4) standards to ensure "plug-and-play" capability across major EHRs.

Decoupled Logic: Clinical risk weights (Beers Criteria, Frailty Index) are stored in JSON, allowing surgeons to update clinical logic without altering code.

Traceability: Provides a transparent "Finding Report" to justify risk scores for clinical decision support.
