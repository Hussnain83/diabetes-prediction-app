# 🩺 DiabetesCare — Diabetes Prediction App

A full-stack diabetes prediction web application built with FastAPI, Streamlit, and a Random Forest ML model. The app provides two ways to check diabetes risk: a form-based predictor with Gemini AI explanations, and a step-by-step conversational chatbot assistant.

---

## ✨ Features

- **Form-based Prediction** — Fill in health details and get instant diabetes risk assessment
- **Gemini AI Explanation** — Get a personalized explanation and health suggestions powered by Google Gemini
- **Chatbot Assistant** — A guided conversational interface that collects your data step by step
- **Duplicate Detection** — Prevents the same data from being submitted twice
- **Confidence Score** — Shows probability percentage for diabetes and no-diabetes

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| ML Model | Random Forest (Scikit-learn) |
| AI Explanations | Google Gemini API |
| Database | SQLite |
| Language | Python |

---

## 📁 Project Structure
diabetes_app/

├── model/

│   ├── diabetes_model.pkl       # trained model (generate locally)

│   └── smoking_encoder.pkl      # label encoder (generate locally)

├── routes/

│   ├── predict.py               # /predict endpoint

│   └── chat.py                  # /chat endpoint

├── schemas/

│   ├── input.py                 # Pydantic input model

│   └── chat.py                  # Pydantic chat model

├── services/

│   ├── ml_service.py            # ML prediction logic

│   ├── gemini_service.py        # Gemini API integration

│   └── db_service.py            # SQLite duplicate check

├── pages/

│   └── chatbot.py               # Streamlit chatbot page

├── app.py                       # Streamlit main form page

├── Diabetes-Prediction-RF.ipynb # Where model is trained

├── main.py                      # FastAPI entry point

├── .env                         # API keys (not pushed to GitHub)

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Hussnain83/diabetes-prediction-app.git
cd diabetes-prediction-app
```

### 2. Install dependencies
```bash
pip install "fastapi[standard]" uvicorn streamlit requests joblib scikit-learn pandas openpyxl google-generativeai python-dotenv
```

### 3. Train the ML Model
Open the Jupyter notebook `Diabetes-Prediction-RF.ipynb` and run all cells. This will generate:
- `model/diabetes_model.pkl`
- `model/smoking_encoder.pkl`

### 4. Set up environment variables
Create a `.env` file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Get your free API key from: https://aistudio.google.com/app/apikey

### 5. Run the FastAPI backend
```bash
uvicorn main:app --reload
```
Backend runs at: `http://127.0.0.1:8000`

### 6. Run the Streamlit frontend
Open a new terminal:
```bash
streamlit run app.py
```
App opens at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/predict` | Form-based diabetes prediction |
| POST | `/chat` | Chatbot message handler |

### POST `/predict` — Sample Request
```json
{
    "name": "Ali Hassan",
    "gender": 1,
    "age": 45.0,
    "race_african": 0,
    "race_asian": 1,
    "race_caucasian": 0,
    "race_hispanic": 0,
    "race_other": 0,
    "hypertension": 1,
    "heart_disease": 0,
    "smoking_history": "never",
    "bmi": 32.5,
    "hbA1c_level": 7.2,
    "blood_glucose_level": 180
}
```

### POST `/chat` — Sample Request
```json
{
    "messages": [
        { "role": "user", "content": "Hi, I want to check if I have diabetes" }
    ]
}
```

---

## 📊 Model Performance

| Metric | Score |
|---|---|
| Accuracy | 90.76% |
| Precision | 91% |
| Recall | 91% |
| F1-Score | 91% |
| Dataset Size | 17,000 records |

---

## 👥 Dataset Features

| Feature | Description |
|---|---|
| Age | Patient age |
| Gender | Male / Female |
| BMI | Body Mass Index |
| HbA1c Level | Glycated hemoglobin |
| Blood Glucose Level | Blood sugar in mg/dL |
| Hypertension | High blood pressure |
| Heart Disease | Existing heart condition |
| Smoking History | Smoking behavior |
| Race | Ethnic background |

---

## 👨‍💻 Developer

**Muhammad Hussnain Dogar**  
BS Computer Science — Air University, Islamabad  
GitHub: [@Hussnain83](https://github.com/Hussnain83)

---

## ⚠️ Disclaimer

This application is built for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
