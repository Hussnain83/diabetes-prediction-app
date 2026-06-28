from pydantic import BaseModel

class DiabetesInput(BaseModel):
    name: str
    gender: int            # 0 = Female, 1 = Male
    age: float
    race_african: int      # 0 or 1
    race_asian: int        # 0 or 1
    race_caucasian: int    # 0 or 1
    race_hispanic: int     # 0 or 1
    race_other: int        # 0 or 1
    hypertension: int      # 0 or 1
    heart_disease: int     # 0 or 1
    smoking_history: str   # "never", "current", "former", "ever", "not current", "No Info"
    bmi: float
    hbA1c_level: float
    blood_glucose_level: int