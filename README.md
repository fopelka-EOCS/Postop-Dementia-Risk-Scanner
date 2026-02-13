# Postop-Dementia-Risk-Scanner
**Objective:** An AI-enhanced SMART on FHIR application to identify high-risk surgical candidates for Postoperative Delirium (POD) and Dementia.

## Overview
As the surgical population ages, the risk of postoperative cognitive decline increases. This tool queries FHIR-based Electronic Health Records (EHR) to flag patients based on:
* **Structured Data:** Age, Medications (Beers Criteria), and Comorbidities.
* **Unstructured Data:** Natural Language Processing (NLP) of H&P notes to extract Mini-Cog scores and Frailty indices.

## Tech Stack
* **Language:** Python 3.x
* **Standard:** HL7 FHIR (R4)
* **API:** SMART on FHIR / CDS Hooks
