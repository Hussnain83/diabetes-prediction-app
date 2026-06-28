from fastapi import FastAPI
from routes.predict import router
from routes.chat import router as chat_router

app = FastAPI(title="Diabetes Prediction API")

# Load model and encoder at startup

app.include_router(router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running!"}

