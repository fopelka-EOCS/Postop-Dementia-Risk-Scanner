import requests

# 1. SETUP: Clinical Standards & Risk Weights
RISK_MEDS = {
    "3498": {"name": "Diphenhydramine", "weight": 3},
    "6470": {"name": "Lorazepam", "weight": 2},
    "3322": {"name": "Diazepam", "weight": 3}
}
KEYWORDS = ["Dementia", "Confusion", "Mini-Cog", "Frailty", "Fall", "MOCA"]

def run_surgical_risk_dashboard(patient_id):
    base_url = "https://hapi.fhir.org/baseR4"
    total_score = 0
    findings = []

    print(f"--- GENERATING SURGICAL RISK REPORT: Patient {patient_id} ---")

    # A. PATIENT AGE CHECK
    p_resp = requests.get(f"{base_url}/Patient/{patient_id}")
    p_data = p_resp.json()
    birth_year = int(p_data.get('birthDate', '1900').split('-')[0])
    age = 2026 - birth_year
    if age > 75:
        total_score += 2
        findings.append(f"AGE RISK: Patient is {age} (>75). (+2 points)")

    # B. MEDICATION SCAN (Structured Data)
    m_resp = requests.get(f"{base_url}/MedicationRequest?patient={patient_id}&_format=json")
    m_data = m_resp.json()
    if 'entry' in m_data:
        for entry in m_data['entry']:
            codings = entry['resource'].get('medicationCodeableConcept', {}).get('coding', [])
            for c in codings:
                if c['code'] in RISK_MEDS:
                    med = RISK_MEDS[c['code']]
                    total_score += med['weight']
                    findings.append(f"MED RISK: {med['name']} detected. (+{med['weight']} points)")

    # C. NOTE SCAN (Unstructured Data)
    n_resp = requests.get(f"{base_url}/DocumentReference?patient={patient_id}&_format=json")
    n_data = n_resp.json()
    if 'entry' in n_data:
        for entry in n_data['entry']:
            desc = entry['resource'].get('description', "")
            for word in KEYWORDS:
                if word.lower() in desc.lower():
                    total_score += 2
                    findings.append(f"CLINICAL NOTE FLAG: Mention of '{word}' in chart. (+2 points)")

    # D. FINAL ASSESSMENT
    print("\n[ RESULTS ]")
    for f in findings:
        print(f"- {f}")
    
    print(f"\nAGGREGATED RISK SCORE: {total_score}")
    if total_score >= 5:
        print("RECOMMENDATION: HIGH RISK. Initiate Delirium Prevention Bundle.")
    elif total_score >= 2:
        print("RECOMMENDATION: MODERATE RISK. Monitor baseline cognition.")
    else:
        print("RECOMMENDATION: LOW RISK.")

# RUN FOR PETER
run_surgical_risk_dashboard("example")
