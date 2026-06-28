from fastapi import APIRouter, HTTPException
from schemas.input import DiabetesInput
from services.ml_service import predict_diabetes
from services.db_service import init_db, save_check, is_duplicate
from services.gemini_service import get_gemini_explanation

router = APIRouter()
init_db()

@router.post("/predict")

def predict(data: DiabetesInput):

    data_dict = data.model_dump()
    if is_duplicate(data_dict):
        raise HTTPException(
            status_code=400,
            detail=f"data for '{data.name}' already checked Please Provide new data"
        )

    result = predict_diabetes(data)

    explanation = get_gemini_explanation(
        name = data.name,
        input_data=data_dict,
        prediction=result['result'],
        confidence=result['confidence']
    )

    save_check(data_dict)
    return {
        "name": data.name,
        **result,
        "explanation": explanation
    }