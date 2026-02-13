import requests
import json

# 1. LOAD YOUR CLINICAL CONFIG
with open('risk_config.json') as f:
    config = json.load(f)

BASE_URL = config['fhir_endpoints']['sandbox']

def get_delirium_risk(patient_id):
    print(f"--- Starting Risk Scan for Patient: {patient_id} ---")
    risk_score = 0
    flags = []

    # 2. FETCH PATIENT DATA (Demographics)
    p_resp = requests.get(f"{BASE_URL}/Patient/{patient_id}")
    patient = p_resp.json()
    
    # Simple Age Logic
    birth_year = int(patient.get('birthDate', '1900').split('-')[0])
    age = 2026 - birth_year # Using current year
    if age >= config['high_risk_thresholds']['age']:
        risk_score += 5
        flags.append(f"Age Risk: Patient is {age}")

    # 3. FETCH MEDICATIONS (RxNorm Check)
    m_resp = requests.get(f"{BASE_URL}/MedicationRequest?patient={patient_id}&status=active")
    med_bundle = m_resp.json()
    
    if 'entry' in med_bundle:
        for entry in med_bundle['entry']:
            resource = entry['resource']
            # Look for the RxNorm code in the medication coding
            codings = resource.get('medicationCodeableConcept', {}).get('coding', [])
            for c in codings:
                code = c.get('code')
                # Cross-reference with our config list
                for risk_med in config['delirium_risk_meds']:
                    if code == risk_med['rxcui']:
                        risk_score += risk_med['weight']
                        flags.append(f"Med Alert: {risk_med['name']} (Weight: {risk_med['weight']})")

    # 4. FINAL ASSESSMENT
    print(f"TOTAL RISK SCORE: {risk_score}")
    for f in flags:
        print(f" - {f}")
    
    if risk_score > 7:
        print("RESULT: HIGH RISK. Recommend Geriatric Anesthesia Protocol.")
    else:
        print("RESULT: Standard Risk Monitoring.")

# TEST RUN: Use a common sandbox ID like 'example' or '2543713'
get_delirium_risk("example")
