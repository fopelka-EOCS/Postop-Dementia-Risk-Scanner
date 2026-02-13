import requests
import json  # Line 1: Import the JSON library

# Line 2 & 3: Open the 'Surgical Plan' file and load the data
with open('risk_config.json', 'r') as config_file:
    config = json.load(config_file)

# Now, instead of hard-coding, we pull the lists from the 'config' variable
RISK_MEDS = {med['rxcui']: med for med in config['delirium_risk_meds']}
FRAILTY_ICD10 = {diag['code']: diag for diag in config['frailty_icd10_codes']}
KEYWORDS = ["Dementia", "Confusion", "Mini-Cog", "Frailty", "Fall", "MOCA"]

def run_surgical_risk_dashboard(patient_id):
    base_url = "https://hapi.fhir.org/baseR4"
    total_score = 0
    findings = []

    print(f"--- GENERATING COMPREHENSIVE RISK REPORT: Patient {patient_id} ---")

    # A. AGE CHECK (Demographics)
    p_resp = requests.get(f"{base_url}/Patient/{patient_id}")
    if p_resp.status_code == 200:
        p_data = p_resp.json()
        birth_year = int(p_data.get('birthDate', '1950').split('-')[0])
        age = 2026 - birth_year
        if age > 75:
            total_score += 2
            findings.append(f"DEMOGRAPHIC: Age {age} detected. (+2 points)")

    # B. FRAILTY SCAN (Condition Resource / ICD-10)
    c_resp = requests.get(f"{base_url}/Condition?patient={patient_id}&_format=json")
    c_data = c_resp.json()
    if 'entry' in c_data:
        for entry in c_data['entry']:
            codings = entry['resource'].get('code', {}).get('coding', [])
            for c in codings:
                code_val = c.get('code')
                if code_val in FRAILTY_ICD10:
                    risk = FRAILTY_ICD10[code_val]
                    total_score += risk['weight']
                    findings.append(f"DIAGNOSIS: {risk['name']} ({code_val}). (+{risk['weight']} points)")

    # C. MEDICATION SCAN (MedicationRequest / RxNorm)
    m_resp = requests.get(f"{base_url}/MedicationRequest?patient={patient_id}&_format=json")
    m_data = m_resp.json()
    if 'entry' in m_data:
        for entry in m_data['entry']:
            codings = entry['resource'].get('medicationCodeableConcept', {}).get('coding', [])
            for c in codings:
                if c.get('code') in RISK_MEDS:
                    med = RISK_MEDS[c['code']]
                    total_score += med['weight']
                    findings.append(f"MEDICATION: {med['name']} detected. (+{med['weight']} points)")

    # D. NOTE SCAN (DocumentReference / NLP Keywords)
    n_resp = requests.get(f"{base_url}/DocumentReference?patient={patient_id}&_format=json")
    n_data = n_resp.json()
    if 'entry' in n_data:
        for entry in n_data['entry']:
            desc = entry['resource'].get('description', "")
            for word in KEYWORDS:
                if word.lower() in desc.lower():
                    total_score += 2
                    findings.append(f"CHART NOTE: Mention of '{word}'. (+2 points)")

    # FINAL SUMMARY
    print("\n[ CLINICAL FINDINGS ]")
    if not findings:
        print("- No high-risk elements detected.")
    else:
        for f in findings:
            print(f"- {f}")
    
    print(f"\nTOTAL AGGREGATED RISK SCORE: {total_score}")
    if total_score >= 5:
        print("ALERT: HIGH RISK. Consider Pre-habilitation and Geriatric consult.")
    elif total_score >= 2:
        print("ADVISORY: MODERATE RISK. Close post-op monitoring recommended.")

# EXECUTE
run_surgical_risk_dashboard("example")

