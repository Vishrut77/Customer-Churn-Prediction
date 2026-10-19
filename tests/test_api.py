import pytest
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Customer Churn Prediction" in response.text
    assert "text/html" in response.headers.get("content-type", "")


def test_static_assets():
    css_res = client.get("/css/style.css")
    assert css_res.status_code == 200
    assert len(css_res.text) > 0

    js_res = client.get("/js/app.js")
    assert js_res.status_code == 200
    assert len(js_res.text) > 0


def test_dashboard_endpoint():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()

    # Check top-level keys
    assert "stats" in data
    assert "churn_by_contract" in data
    assert "churn_by_tenure" in data
    assert "average_charges_by_churn" in data

    stats = data["stats"]
    assert stats["total_customers"] > 0
    assert stats["total_customers"] == stats["churned_customers"] + stats["retained_customers"]
    assert 0 <= stats["churn_rate"] <= 100

    # Churn by contract
    contracts = data["churn_by_contract"]
    assert len(contracts) > 0
    for item in contracts:
        assert "contract" in item
        assert "customers" in item
        assert "churned" in item
        assert "churn_rate" in item
        assert item["customers"] >= item["churned"]

    # Churn by tenure
    tenures = data["churn_by_tenure"]
    assert len(tenures) > 0
    for item in tenures:
        assert "tenure_group" in item
        assert "customers" in item
        assert "churned" in item
        assert "churn_rate" in item

    # Average charges
    charges = data["average_charges_by_churn"]
    assert len(charges) >= 2
    for item in charges:
        assert item["churn"] in ["Yes", "No"]
        assert item["average_monthly_charges"] > 0


def test_customers_endpoint_pagination():
    response = client.get("/api/customers?offset=0&limit=10")
    assert response.status_code == 200
    data = response.json()

    assert data["offset"] == 0
    assert data["limit"] == 10
    assert data["total"] > 0
    assert len(data["rows"]) == 10
    assert "columns" in data
    assert len(data["columns"]) >= 20


def test_customers_endpoint_filters():
    # Filter by churn = Yes
    res_churn = client.get("/api/customers?churn=Yes&limit=5")
    assert res_churn.status_code == 200
    for row in res_churn.json()["rows"]:
        assert str(row["Churn"]).strip().lower() in ["yes", "1"]

    # Filter by churn = No
    res_retained = client.get("/api/customers?churn=No&limit=5")
    assert res_retained.status_code == 200
    for row in res_retained.json()["rows"]:
        assert str(row["Churn"]).strip().lower() in ["no", "0"]

    # Filter by contract
    res_contract = client.get("/api/customers?contract=Two%20year&limit=5")
    assert res_contract.status_code == 200
    for row in res_contract.json()["rows"]:
        assert row["Contract"].strip().lower() == "two year"

    # Search keyword
    res_search = client.get("/api/customers?search=DSL&limit=5")
    assert res_search.status_code == 200
    assert len(res_search.json()["rows"]) > 0


def test_customers_validation_errors():
    # Negative offset
    res = client.get("/api/customers?offset=-1")
    assert res.status_code == 422

    # Limit > 100
    res = client.get("/api/customers?limit=101")
    assert res.status_code == 422

    # Limit < 1
    res = client.get("/api/customers?limit=0")
    assert res.status_code == 422


def test_predict_endpoint_valid():
    payload = {
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 0,
        "tenure": 12,
        "PhoneService": 1,
        "MultipleLines": 0,
        "OnlineSecurity": 0,
        "OnlineBackup": 1,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "PaperlessBilling": 1,
        "MonthlyCharges": 70.35,
        "TotalCharges": 844.20,
        "InternetService": "Fiber optic",
        "Contract": "Month-to-month",
        "PaymentMethod": "Electronic check",
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "churn_probability" in result
    assert "predicted_churn" in result
    assert 0.0 <= result["churn_probability"] <= 1.0
    assert result["predicted_churn"] in ["Yes", "No"]


def test_predict_endpoint_internet_service_no():
    payload = {
        "SeniorCitizen": 0,
        "Partner": 0,
        "Dependents": 0,
        "tenure": 36,
        "PhoneService": 1,
        "MultipleLines": 1,
        "OnlineSecurity": 0,
        "OnlineBackup": 0,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "PaperlessBilling": 0,
        "MonthlyCharges": 20.0,
        "TotalCharges": 720.0,
        "InternetService": "No",
        "Contract": "Two year",
        "PaymentMethod": "Mailed check",
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["predicted_churn"] == "No"
    assert result["churn_probability"] < 0.5


def test_predict_endpoint_validation_errors():
    # Missing required field tenure
    payload = {
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 0,
        "PhoneService": 1,
        "MultipleLines": 0,
        "OnlineSecurity": 0,
        "OnlineBackup": 1,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "PaperlessBilling": 1,
        "MonthlyCharges": 70.35,
        "TotalCharges": 844.20,
        "InternetService": "Fiber optic",
        "Contract": "Month-to-month",
        "PaymentMethod": "Electronic check",
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422

    # Invalid category for Contract
    payload_bad_contract = dict(payload)
    payload_bad_contract["tenure"] = 10
    payload_bad_contract["Contract"] = "Infinite year"
    response = client.post("/api/predict", json=payload_bad_contract)
    assert response.status_code == 422

    # Negative charges
    payload_bad_charges = dict(payload)
    payload_bad_charges["tenure"] = 10
    payload_bad_charges["Contract"] = "Month-to-month"
    payload_bad_charges["MonthlyCharges"] = -50.0
    response = client.post("/api/predict", json=payload_bad_charges)
    assert response.status_code == 422


def test_favicon_endpoint():
    response = client.get("/favicon.ico")
    assert response.status_code == 204


def test_predict_endpoint_zero_values():
    # Test new customer with tenure 0 and zero total charges
    payload = {
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 1,
        "tenure": 0,
        "PhoneService": 1,
        "MultipleLines": 0,
        "OnlineSecurity": 1,
        "OnlineBackup": 1,
        "DeviceProtection": 1,
        "TechSupport": 1,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "PaperlessBilling": 0,
        "MonthlyCharges": 25.0,
        "TotalCharges": 0.0,
        "InternetService": "DSL",
        "Contract": "Two year",
        "PaymentMethod": "Bank transfer (automatic)",
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["predicted_churn"] in ["Yes", "No"]
    assert 0.0 <= res["churn_probability"] <= 1.0


def test_analytics_service_direct():
    from app.services.analytics_service import (
        get_average_charges_by_churn,
        get_churn_by_contract,
        get_churn_by_tenure,
        get_customer_preview,
        get_dashboard_data,
        get_dashboard_stats,
    )

    stats = get_dashboard_stats()
    assert isinstance(stats["total_customers"], int)
    assert isinstance(stats["churn_rate"], float)

    contracts = get_churn_by_contract()
    assert len(contracts) > 0
    for c in contracts:
        assert isinstance(c["churn_rate"], float)

    tenure = get_churn_by_tenure()
    assert len(tenure) > 0
    for t in tenure:
        assert isinstance(t["churn_rate"], float)

    charges = get_average_charges_by_churn()
    assert len(charges) > 0

    preview = get_customer_preview(offset=10, limit=5)
    assert len(preview["rows"]) == 5

