import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DiabetesCare — Chat Assistant",
    page_icon="💬",
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
/* Fix chat message text color */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        color: #1a1a1a !important;
    }

    /* Fix sidebar toggle button */
    [data-testid="collapsedControl"] {
        color: #0f6e56 !important;
        background: white !important;
        border-radius: 50% !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #0f6e56 !important;
    }

    /* Fix sidebar text */
    [data-testid="stSidebarNav"] a span {
        color: #1a1a1a !important;
    }

    /* Fix chat input text */
    [data-testid="stChatInputTextArea"] {
        color: #1a1a1a !important;
    }
    .stApp { background-color: #f0f7f4; }
    #MainMenu, footer, header {visibility: hidden;}

    .chat-hero {
        background: linear-gradient(135deg, #0f6e56 0%, #1d9e75 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    .chat-hero h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        color: white;
    }
    .chat-hero p {
        margin: 0;
        opacity: 0.85;
        font-size: 0.95rem;
        color: white;
    }

    .prediction-card-diabetic {
        background: #fff0f0;
        border: 1.5px solid #ffb3b3;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.5rem 0;
    }
    .prediction-card-safe {
        background: #f0fff8;
        border: 1.5px solid #9fe1cb;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.5rem 0;
    }
    .pred-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    .conf-row {
        display: flex;
        gap: 1.5rem;
        margin-top: 0.75rem;
    }
    .conf-item {
        flex: 1;
    }
    .conf-label {
        font-size: 0.75rem;
        color: #555;
        margin-bottom: 4px;
    }
    .conf-bar-bg {
        background: #e1f5ee;
        border-radius: 99px;
        height: 8px;
    }
    .conf-bar-green {
        background: #1d9e75;
        border-radius: 99px;
        height: 8px;
    }
    .conf-bar-red {
        background: #e24b4a;
        border-radius: 99px;
        height: 8px;
    }

    .stButton > button {
        background: #0f6e56 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: #085041 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="chat-hero">
    <h1>💬 Diabetes Chat Assistant</h1>
    <p>I'll guide you step by step to assess your diabetes risk. Only diabetes-related questions will be answered.</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

# Welcome message
if len(st.session_state.messages) == 0:
    welcome = "Hello! I'm your diabetes risk assistant. I'll ask you a few health questions to assess your risk. Ready to begin? Tell me your name to get started."
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })

# Display chat history
for msg in st.session_state.messages:
    display_role = "assistant" if msg["role"] == "assistant" else "user"
    with st.chat_message(display_role):
        st.write(msg["content"])

# Input — disable if prediction done
if not st.session_state.prediction_done:
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # API ko MODEL role bhejte hain — Gemini ke liye
                api_messages = []
                for msg in st.session_state.messages:
                    api_messages.append({
                        "role": "MODEL" if msg["role"] == "assistant" else "user",
                        "content": msg["content"]
                    })

                response = requests.post(f"{API_URL}/chat", json={"messages": api_messages})

            if response.status_code == 200:
                data = response.json()

                if data["type"] == "prediction":
                    st.session_state.prediction_done = True
                    is_diabetic = "Not" not in data["result"]

                    if is_diabetic:
                        st.markdown(f"""
                        <div class="prediction-card-diabetic">
                            <div class="pred-title" style="color:#c0392b">⚠️ Diabetes Risk Detected</div>
                            <p style="margin:0;font-size:0.9rem">{data['message']}</p>
                            <div class="conf-row">
                                <div class="conf-item">
                                    <div class="conf-label">Diabetes probability</div>
                                    <div class="conf-bar-bg"><div class="conf-bar-red" style="width:{data['confidence']['diabetes']}%"></div></div>
                                    <strong style="color:#e24b4a">{data['confidence']['diabetes']}%</strong>
                                </div>
                                <div class="conf-item">
                                    <div class="conf-label">No diabetes probability</div>
                                    <div class="conf-bar-bg"><div class="conf-bar-green" style="width:{data['confidence']['no_diabetes']}%"></div></div>
                                    <strong style="color:#0f6e56">{data['confidence']['no_diabetes']}%</strong>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="prediction-card-safe">
                            <div class="pred-title" style="color:#0f6e56">✅ No Diabetes Detected</div>
                            <p style="margin:0;font-size:0.9rem">{data['message']}</p>
                            <div class="conf-row">
                                <div class="conf-item">
                                    <div class="conf-label">No diabetes probability</div>
                                    <div class="conf-bar-bg"><div class="conf-bar-green" style="width:{data['confidence']['no_diabetes']}%"></div></div>
                                    <strong style="color:#0f6e56">{data['confidence']['no_diabetes']}%</strong>
                                </div>
                                <div class="conf-item">
                                    <div class="conf-label">Diabetes probability</div>
                                    <div class="conf-bar-bg"><div class="conf-bar-red" style="width:{data['confidence']['diabetes']}%"></div></div>
                                    <strong style="color:#e24b4a">{data['confidence']['diabetes']}%</strong>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["message"]
                    })

                else:
                    st.write(data["message"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["message"]
                    })
            else:
                st.error("Something went wrong. Please try again.")

# Reset button after prediction
if st.session_state.prediction_done:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.prediction_done = False
        st.rerun()