from typing import Literal

from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    # Numerical and binary features
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: int = Field(ge=0, le=1)
    Dependents: int = Field(ge=0, le=1)
    tenure: int = Field(ge=0)

    PhoneService: int = Field(ge=0, le=1)
    MultipleLines: int = Field(ge=0, le=1)

    OnlineSecurity: int = Field(ge=0, le=1)
    OnlineBackup: int = Field(ge=0, le=1)
    DeviceProtection: int = Field(ge=0, le=1)
    TechSupport: int = Field(ge=0, le=1)
    StreamingTV: int = Field(ge=0, le=1)
    StreamingMovies: int = Field(ge=0, le=1)

    PaperlessBilling: int = Field(ge=0, le=1)

    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)

    # Categorical features that the encoder will transform
    InternetService: Literal["DSL", "Fiber optic", "No"]

    Contract: Literal[
        "Month-to-month",
        "One year",
        "Two year"
    ]

    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]


class PredictionResponse(BaseModel):
    churn_probability: float
    predicted_churn: Literal["Yes", "No"]