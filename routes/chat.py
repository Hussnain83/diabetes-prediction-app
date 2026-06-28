from fastapi import APIRouter
from schemas.chat import ChatInput
from services.chat_service import chat_with_bot
from services.ml_service import predict_diabetes
from services.db_service import is_duplicate, save_check
from schemas.input import DiabetesInput
import json
import re

router = APIRouter()

@router.post("/chat")
def chat(data: ChatInput):
    response_text = chat_with_bot(data.messages)

    try:
         # JSON extract karo response se
        json_match = re.search(r'\{.*"ready":\s*true.*\}', response_text, re.DOTALL)

        if json_match:
            parsed = json.loads(json_match.group())
            
            if parsed.get("ready") == True:
                patient_data = parsed["data"]
                
                # DiabetesInput object banao
                diabetes_input = DiabetesInput(**patient_data)
                data_dict = diabetes_input.model_dump()
                result = predict_diabetes(diabetes_input)
                return {
                    "type": "prediction",
                    "name": patient_data["name"],
                    "result": result["result"],
                    "confidence": result["confidence"],
                    "message": f"Based on the information provided, {patient_data['name']} is predicted to be {result['result']} with {result['confidence']['diabetes']}% confidence."
                }
    except Exception as e:
        pass

    # Normal chat response
    return {
        "type": "message",
        "message": response_text
    }
      

