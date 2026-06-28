import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DiabetesCare — Prediction Tool",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Sidebar background and text */
    [data-testid="stSidebar"] {
        background-color: #0f6e56 !important;
    }
    [data-testid="stSidebarNav"] a span {
        color: white !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: #1d9e75 !important;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: 8px !important;
    }

    /* Chat input field */
    [data-testid="stChatInputTextArea"] {
        color: white !important;
        background-color: #0f6e56 !important;
    }
    [data-testid="stChatInputTextArea"]::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }
    [data-testid="stChatInputContainer"] {
        background-color: #0f6e56 !important;
        border-radius: 12px !important;
        border: 1px solid #1d9e75 !important;
    }
    /* Main background */
    .stApp {
        background-color: #f0f7f4;
    }
    
    /* Hide default streamlit header */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #0f6e56 0%, #1d9e75 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: white;
    }
    .hero p {
        font-size: 1rem;
        margin: 0;
        opacity: 0.85;
        color: white;
    }

    /* Section card */
    .form-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e1f5ee;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #0f6e56;
        margin-bottom: 1rem;
    }

    /* Result cards */
    .result-diabetic {
        background: #fff0f0;
        border: 1.5px solid #ffb3b3;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .result-safe {
        background: #f0fff8;
        border: 1.5px solid #9fe1cb;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .result-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.5rem 0 0.25rem 0;
    }
    .result-sub {
        font-size: 0.9rem;
        opacity: 0.7;
        margin: 0;
    }

    /* Confidence bar */
    .conf-label {
        font-size: 0.8rem;
        color: #555;
        margin-bottom: 0.25rem;
    }
    .conf-bar-bg {
        background: #e1f5ee;
        border-radius: 99px;
        height: 10px;
        width: 100%;
    }
    .conf-bar-fill {
        background: #1d9e75;
        border-radius: 99px;
        height: 10px;
    }
    .conf-bar-fill-red {
        background: #e24b4a;
        border-radius: 99px;
        height: 10px;
    }

    /* Explanation box */
    .explanation-box {
        background: #f8fcfa;
        border-left: 4px solid #1d9e75;
        border-radius: 0 8px 8px 0;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #2d2d2d;
    }

    /* Streamlit button override */
    .stButton > button {
        background: #0f6e56 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: #085041 !important;
    }

    /* Input labels */
    label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }

    /* Warning box */
    .warning-box {
        background: #fffbeb;
        border: 1px solid #fbbf24;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #92400e;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>🩺 DiabetesCare Prediction Tool</h1>
    <p>Fill in your health details below. Our AI model will analyze your data and provide a personalized risk assessment.</p>
</div>
""", unsafe_allow_html=True)

# Personal Info Section
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Personal Information</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Full Name", placeholder="e.g. Ali Hassan")
with col2:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
with col3:
    gender = st.selectbox("Gender", ["Female", "Male"])
st.markdown('</div>', unsafe_allow_html=True)

# Health Metrics Section
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Health Metrics</div>', unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    bmi = st.number_input("BMI", min_value=10.0, max_value=100.0, value=25.0, help="Body Mass Index")
with col5:
    hba1c = st.number_input("HbA1c Level", min_value=3.0, max_value=15.0, value=5.0, help="Glycated hemoglobin level")
with col6:
    blood_glucose = st.number_input("Blood Glucose Level", min_value=50, max_value=500, value=100, help="mg/dL")
st.markdown('</div>', unsafe_allow_html=True)

# Medical History Section
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Medical History</div>', unsafe_allow_html=True)
col7, col8, col9, col10 = st.columns(4)
with col7:
    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
with col8:
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
with col9:
    smoking = st.selectbox("Smoking History", ["never", "current", "former", "ever", "not current", "No Info"])
with col10:
    race = st.selectbox("Race", ["AfricanAmerican", "Asian", "Caucasian", "Hispanic", "Other"])
st.markdown('</div>', unsafe_allow_html=True)

# Predict Button
predict_clicked = st.button("Run Prediction →", use_container_width=True)

if predict_clicked:
    if not name.strip():
        st.markdown('<div class="warning-box">⚠️ Please enter your full name to continue.</div>', unsafe_allow_html=True)
    else:
        payload = {
            "name": name.strip(),
            "gender": 1 if gender == "Male" else 0,
            "age": float(age),
            "race_african": 1 if race == "AfricanAmerican" else 0,
            "race_asian": 1 if race == "Asian" else 0,
            "race_caucasian": 1 if race == "Caucasian" else 0,
            "race_hispanic": 1 if race == "Hispanic" else 0,
            "race_other": 1 if race == "Other" else 0,
            "hypertension": 1 if hypertension == "Yes" else 0,
            "heart_disease": 1 if heart_disease == "Yes" else 0,
            "smoking_history": smoking,
            "bmi": float(bmi),
            "hbA1c_level": float(hba1c),
            "blood_glucose_level": int(blood_glucose)
        }

        with st.spinner("Analyzing your health data..."):
            response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.markdown("---")

            is_diabetic = data['prediction'] == 1
            diabetes_conf = data['confidence']['diabetes']
            no_diabetes_conf = data['confidence']['no_diabetes']

            if is_diabetic:
                st.markdown(f"""
                <div class="result-diabetic">
                    <div style="font-size:2.5rem">⚠️</div>
                    <div class="result-title" style="color:#c0392b">Diabetes Risk Detected</div>
                    <p class="result-sub">Based on the provided data, <strong>{data['name']}</strong> shows signs of diabetes.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-safe">
                    <div style="font-size:2.5rem">✅</div>
                    <div class="result-title" style="color:#0f6e56">No Diabetes Detected</div>
                    <p class="result-sub">Based on the provided data, <strong>{data['name']}</strong> does not show signs of diabetes.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Confidence bars
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="conf-label">Diabetes Probability</div>
                <div class="conf-bar-bg"><div class="conf-bar-fill-red" style="width:{diabetes_conf}%"></div></div>
                <div style="font-size:1.2rem;font-weight:700;color:#e24b4a;margin-top:4px">{diabetes_conf}%</div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <div class="conf-label">No Diabetes Probability</div>
                <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:{no_diabetes_conf}%"></div></div>
                <div style="font-size:1.2rem;font-weight:700;color:#0f6e56;margin-top:4px">{no_diabetes_conf}%</div>
                """, unsafe_allow_html=True)

            # Gemini Explanation
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="explanation-box">
                <strong style="color:#0f6e56">💡 AI Health Analysis</strong><br><br>
                {data['explanation']}
            </div>
            """, unsafe_allow_html=True)

        elif response.status_code == 400:
            st.markdown(f'<div class="warning-box">⚠️ {response.json()["detail"]}</div>', unsafe_allow_html=True)
        else:
            st.error("Something went wrong. Please try again.")