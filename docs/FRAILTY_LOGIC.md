# Clinical Logic: Frailty and Sarcopenia

## Objective
To identify "Phenotypic Frailty" using ICD-10 codes stored in the EHR 'Condition' resource.

## Rationale for Weighting
* **R54 (Age-related physical debility):** Assigned Weight: 4. This is the "gold standard" code for clinical frailty.
* **M62.84 (Sarcopenia):** Assigned Weight: 3. Low muscle mass is a direct predictor of post-op complications and cognitive decline.
* **Z91.81 (History of Falling):** Assigned Weight: 2. Falls indicate balance/gait deficits, which are core components of the Frailty Index.

## Data Source
* **FHIR Resource:** `Condition`.
* **Filtering:** The script scans only "active" or "confirmed" diagnoses.
