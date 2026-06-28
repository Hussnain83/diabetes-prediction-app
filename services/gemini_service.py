import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_explanation(name: str, input_data: dict, prediction: str, confidence: dict) -> str:
    
    prompt = f"""
    You are a helpful medical assistant specialized in diabetes.
    
    Patient Name: {name}
    Patient Data:
    - Age: {input_data['age']}
    - Gender: {"Male" if input_data['gender'] == 1 else "Female"}
    - BMI: {input_data['bmi']}
    - HbA1c Level: {input_data['hbA1c_level']}
    - Blood Glucose Level: {input_data['blood_glucose_level']}
    - Hypertension: {"Yes" if input_data['hypertension'] == 1 else "No"}
    - Heart Disease: {"Yes" if input_data['heart_disease'] == 1 else "No"}
    - Smoking History: {input_data['smoking_history']}
    
    ML Model Prediction: {prediction}
    Confidence: {confidence['diabetes']}% chance of diabetes
    
    Please provide:
    1. A short friendly explanation of this prediction
    2. Which factors contributed most to this result
    3. 3 practical health suggestions for this patient
    
    Keep it simple, friendly and easy to understand. Address the patient by name.
    """
    
    response = model.generate_content(prompt)
    return response.text