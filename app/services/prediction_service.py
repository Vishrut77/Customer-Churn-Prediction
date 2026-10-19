from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_DIR
    / "models"
    / "churn_pipeline.joblib"
)


@lru_cache(maxsize=1)
def load_model_bundle():
    # Load the saved encoder and model only once
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run ml/train.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_customer(customer_data: dict):
    # Load the trained model and fitted encoder
    bundle = load_model_bundle()

    encoder = bundle["encoder"]
    model = bundle["model"]
    input_columns = bundle["input_columns"]

    # Convert customer information into a copy dictionary
    customer_dict = dict(customer_data)

    # Map "No" in InternetService to "0" to match training data encoder category
    if str(customer_dict.get("InternetService")).strip().lower() == "no":
        customer_dict["InternetService"] = "0"

    # Default Unnamed: 0 if present in model training features
    if "Unnamed: 0" in input_columns and "Unnamed: 0" not in customer_dict:
        customer_dict["Unnamed: 0"] = 0

    # Convert customer information into a single-row DataFrame
    customer_df = pd.DataFrame([customer_dict])

    # Ensure the column names and order match training
    customer_df = customer_df.reindex(columns=input_columns)

    if customer_df.isnull().any().any():
        missing = customer_df.columns[customer_df.isnull().any()].tolist()
        raise ValueError(
            f"Customer data is missing required feature values: {missing}"
        )

    # Encode new customer data using the fitted encoder
    encoded_customer = encoder.transform(customer_df)

    # Predict the customer's churn class
    prediction = int(model.predict(encoded_customer)[0])

    # Get the probability associated with class 1 (Churn)
    classes = list(model.classes_)
    if 1 in classes:
        churn_index = classes.index(1)
    elif "1" in classes:
        churn_index = classes.index("1")
    elif "Yes" in classes:
        churn_index = classes.index("Yes")
    else:
        churn_index = len(classes) - 1

    probability = float(
        model.predict_proba(encoded_customer)[0][churn_index]
    )

    return {
        "churn_probability": round(probability, 4),
        "predicted_churn": (
            "Yes" if prediction == 1 else "No"
        ),
    }