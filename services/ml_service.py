import joblib
import numpy as np

model = joblib.load("model/diabetes_model.pkl")
encoder = joblib.load("model/smoking_encoder.pkl")

print("Model loaded successfull!")

def predict_diabetes(data):
     # Encode smoking history
     smoking_encoded = encoder.transform([data.smoking_history])[0]

     # Prepare input array — same order as training
     input_data = np.array([[
          data.gender,
          data.age,
          data.race_african,
          data.race_asian,
          data.race_caucasian,
          data.race_hispanic,
          data.race_other,
          data.hypertension,
          data.heart_disease,
          smoking_encoded,
          data.bmi,
          data.hbA1c_level,
          data.blood_glucose_level
     ]])

     prediction = model.predict(input_data)[0]
     confidence = model.predict_proba(input_data)[0]

     return {
        "prediction": int(prediction),
        "result": "Diabetic" if prediction == 1 else "Not Diabetic",
        "confidence": {
            "no_diabetes": round(float(confidence[0]) * 100, 2),
            "diabetes": round(float(confidence[1]) * 100, 2)
        }
    }