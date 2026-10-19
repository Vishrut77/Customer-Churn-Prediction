from fastapi import APIRouter, HTTPException

from app.schemas.prediction import CustomerInput,PredictionResponse
from app.services.prediction_service import predict_customer



router = APIRouter(
    prefix="/api",
    tags=["Prediction"],
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(data: CustomerInput):

    try:
        # Convert validated input into a dictionary
        customer_data = data.model_dump()

        # Call the prediction service
        result = predict_customer(customer_data)

        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model not found. Train the model first.",
        )