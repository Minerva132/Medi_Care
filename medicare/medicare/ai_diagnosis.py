# AI Diagnosis Module
# This module provides AI-powered diagnosis based on patient symptoms

import random
from decimal import Decimal

# Common symptoms mapping
SYMPTOMS = [
    "Fever", "Cough", "Headache", "Fatigue", "Nausea", "Vomiting",
    "Diarrhea", "Abdominal Pain", "Chest Pain", "Shortness of Breath",
    "Dizziness", "Sore Throat", "Runny Nose", "Body Aches", "Chills",
    "Loss of Appetite", "Joint Pain", "Muscle Pain", "Rash", "Swelling",
    "Back Pain", "Neck Pain", "Ear Pain", "Eye Pain", "Confusion",
    "Anxiety", "Depression", "Insomnia", "Weight Loss", "Weight Gain",
    "Excessive Thirst", "Frequent Urination", "Blurred Vision", "Numbness",
    "Tingling", "Weakness", "Tremors", "Seizures", "Memory Loss", "Bleeding"
]

# Treatment recommendations based on symptoms
DIAGNOSIS_DATABASE = {
    "respiratory": {
        "symptoms": ["Cough", "Shortness of Breath", "Chest Pain", "Sore Throat", "Runny Nose"],
        "treatment": "Respiratory Infection Treatment",
        "description": "You may have a respiratory infection. Treatment includes antibiotics, inhalers, and rest.",
        "base_cost": 350.00,
        "medications": ["Antibiotics", "Cough Syrup", "Inhaler"],
        "follow_up": "7-10 days"
    },
    "flu": {
        "symptoms": ["Fever", "Body Aches", "Fatigue", "Chills", "Headache"],
        "treatment": "Influenza Treatment",
        "description": "You likely have the flu. Treatment includes antiviral medications, rest, and hydration.",
        "base_cost": 250.00,
        "medications": ["Antiviral Medication", "Fever Reducer", "Pain Reliever"],
        "follow_up": "5-7 days"
    },
    "gastro": {
        "symptoms": ["Nausea", "Vomiting", "Diarrhea", "Abdominal Pain", "Loss of Appetite"],
        "treatment": "Gastrointestinal Treatment",
        "description": "You may have a gastrointestinal infection. Treatment includes anti-nausea medication and hydration.",
        "base_cost": 200.00,
        "medications": ["Anti-nausea", "Electrolyte Solution", "Probiotics"],
        "follow_up": "3-5 days"
    },
    "migraine": {
        "symptoms": ["Headache", "Dizziness", "Nausea", "Blurred Vision", "Fatigue"],
        "treatment": "Migraine Management",
        "description": "You may be experiencing migraines. Treatment includes pain relief and preventive medications.",
        "base_cost": 300.00,
        "medications": ["Migraine Medication", "Pain Reliever", "Anti-nausea"],
        "follow_up": "14 days"
    },
    "cardiovascular": {
        "symptoms": ["Chest Pain", "Shortness of Breath", "Dizziness", "Fatigue", "Swelling"],
        "treatment": "Cardiovascular Evaluation",
        "description": "Your symptoms require cardiovascular evaluation. Immediate medical attention recommended.",
        "base_cost": 800.00,
        "medications": ["Heart Medication", "Blood Pressure Medication"],
        "follow_up": "Immediate - Visit ER",
        "urgent": True
    },
    "diabetes": {
        "symptoms": ["Excessive Thirst", "Frequent Urination", "Fatigue", "Blurred Vision", "Weight Loss"],
        "treatment": "Diabetes Management",
        "description": "You may have diabetes. Treatment includes blood sugar monitoring and medication.",
        "base_cost": 450.00,
        "medications": ["Insulin/Metformin", "Blood Sugar Monitor", "Diet Plan"],
        "follow_up": "30 days"
    },
    "neurological": {
        "symptoms": ["Numbness", "Tingling", "Weakness", "Tremors", "Memory Loss"],
        "treatment": "Neurological Evaluation",
        "description": "Neurological symptoms detected. Specialist consultation recommended.",
        "base_cost": 600.00,
        "medications": ["Neurological Medication", "Physical Therapy"],
        "follow_up": "14 days"
    },
    "musculoskeletal": {
        "symptoms": ["Back Pain", "Neck Pain", "Joint Pain", "Muscle Pain", "Swelling"],
        "treatment": "Musculoskeletal Treatment",
        "description": "You have musculoskeletal issues. Treatment includes pain management and physical therapy.",
        "base_cost": 350.00,
        "medications": ["Pain Reliever", "Anti-inflammatory", "Muscle Relaxant"],
        "follow_up": "10-14 days"
    },
    "mental_health": {
        "symptoms": ["Anxiety", "Depression", "Insomnia", "Fatigue", "Loss of Appetite"],
        "treatment": "Mental Health Support",
        "description": "Mental health support recommended. Treatment includes counseling and medication if needed.",
        "base_cost": 400.00,
        "medications": ["Antidepressant/Anti-anxiety", "Sleep Aid", "Counseling Sessions"],
        "follow_up": "30 days"
    },
    "general": {
        "symptoms": ["Fatigue", "Headache", "Body Aches"],
        "treatment": "General Health Check-up",
        "description": "General symptoms detected. A comprehensive health check-up is recommended.",
        "base_cost": 150.00,
        "medications": ["Multivitamins", "Pain Reliever", "Rest"],
        "follow_up": "7 days"
    }
}

# Insurance coverage percentages
INSURANCE_COVERAGE = {
    "Premium": 0.90,  # 90% coverage
    "Gold": 0.80,     # 80% coverage
    "Silver": 0.70,   # 70% coverage
    "Bronze": 0.50,   # 50% coverage
    "Basic": 0.30,    # 30% coverage
    "None": 0.00      # No coverage
}


def analyze_symptoms(symptoms_list):
    """
    Analyze patient symptoms and return diagnosis recommendation
    """
    if not symptoms_list:
        return None
    
    # Convert symptoms to set for faster matching
    symptoms_set = set(symptoms_list)
    
    # Find best matching diagnosis
    best_match = None
    max_matches = 0
    
    for diagnosis_type, diagnosis_data in DIAGNOSIS_DATABASE.items():
        diagnosis_symptoms = set(diagnosis_data["symptoms"])
        matches = len(symptoms_set & diagnosis_symptoms)
        
        if matches > max_matches:
            max_matches = matches
            best_match = diagnosis_type
    
    # If no matches found, use general
    if best_match is None or max_matches == 0:
        best_match = "general"
    
    return DIAGNOSIS_DATABASE[best_match]


def calculate_cost(base_cost, insurance_type, age):
    """
    Calculate treatment cost based on insurance and patient factors
    """
    # Base cost
    total_cost = Decimal(str(base_cost))
    
    # Age factor (higher cost for elderly)
    if age > 65:
        total_cost *= Decimal("1.20")  # 20% increase
    elif age < 18:
        total_cost *= Decimal("0.90")  # 10% discount for children
    
    # Add consultation fee
    consultation_fee = Decimal("100.00")
    total_cost += consultation_fee
    
    # Add lab tests (random between 2-5 tests)
    num_tests = random.randint(2, 5)
    lab_cost = Decimal(str(num_tests * 50))
    total_cost += lab_cost
    
    # Calculate insurance coverage
    coverage_rate = INSURANCE_COVERAGE.get(insurance_type, 0.0)
    insurance_covered = total_cost * Decimal(str(coverage_rate))
    patient_pays = total_cost - insurance_covered
    
    return {
        "total_cost": float(total_cost),
        "insurance_covered": float(insurance_covered),
        "patient_pays": float(patient_pays),
        "consultation_fee": float(consultation_fee),
        "lab_cost": float(lab_cost),
        "treatment_cost": float(base_cost),
        "coverage_percentage": int(coverage_rate * 100),
        "num_tests": num_tests
    }


def get_diagnosis(full_name, age, gender, contact, insurance, symptoms):
    """
    Main function to get AI diagnosis
    """
    # Analyze symptoms
    diagnosis = analyze_symptoms(symptoms)
    
    if not diagnosis:
        return None
    
    # Calculate costs
    cost_breakdown = calculate_cost(
        diagnosis["base_cost"],
        insurance if insurance else "None",
        age
    )
    
    # Prepare result
    result = {
        "patient_info": {
            "full_name": full_name,
            "age": age,
            "gender": gender,
            "contact": contact,
            "insurance": insurance if insurance else "None"
        },
        "symptoms": symptoms,
        "diagnosis": {
            "treatment": diagnosis["treatment"],
            "description": diagnosis["description"],
            "medications": diagnosis["medications"],
            "follow_up": diagnosis["follow_up"],
            "urgent": diagnosis.get("urgent", False)
        },
        "cost_breakdown": cost_breakdown,
        "recommendations": generate_recommendations(diagnosis, age, insurance)
    }
    
    return result


def generate_recommendations(diagnosis, age, insurance):
    """
    Generate personalized recommendations
    """
    recommendations = []
    
    # General recommendations
    recommendations.append("Schedule an appointment with a healthcare provider")
    recommendations.append("Keep a symptom diary to track changes")
    
    # Age-specific
    if age > 65:
        recommendations.append("Consider bringing a family member to appointments")
    elif age < 18:
        recommendations.append("Parental supervision required for treatment")
    
    # Insurance-specific
    if not insurance or insurance == "None":
        recommendations.append("Consider enrolling in a health insurance plan")
        recommendations.append("Ask about payment plans and financial assistance")
    
    # Diagnosis-specific
    if diagnosis.get("urgent"):
        recommendations.append("⚠️ URGENT: Seek immediate medical attention")
        recommendations.append("Visit nearest emergency room if symptoms worsen")
    else:
        recommendations.append("Follow prescribed medications as directed")
        recommendations.append("Maintain adequate rest and hydration")
    
    return recommendations
