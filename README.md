# Customer Churn Prediction System

An end-to-end Machine Learning web application and intelligence dashboard for predicting customer churn risk, visualizing retention trends, and exploring customer records. Built with **FastAPI**, **Scikit-learn**, and a modern **Vanilla HTML/CSS/JS** interface powered by **Chart.js**.

---

## Features

- **Real-Time KPI Overview**:
  - Live portfolio metrics: Total Customers, Churned, Retained, and Overall Churn Rate.
  - Dynamic status indicators reflecting backend connectivity.
- **Visual Retention Analytics**:
  - **Churn by Contract Type**: Direct comparison of month-to-month vs. 1-year and 2-year agreements.
  - **Churn by Tenure Lifespan**: Risk distribution across customer lifespan tiers (0–12m, 13–24m, 25–48m, 49–72m).
  - **Average Monthly Spend**: Side-by-side financial comparison between churned and retained accounts.
- **Customer Records Explorer**:
  - Full 21-feature tabular browser for inspecting customer profiles.
  - Instant text search across customer IDs, contract types, and service tiers.
  - Dropdown filters for Churn Status (`All`, `Churned`, `Retained`) and Contract Type.
  - Pagination controls (10, 25, 50, 100 rows per page) and smooth horizontal column scrolling.
  - **Export to CSV**: Download filtered views directly to CSV.
  - **Customer Profile Modal**: Deep-dive inspection dialog showing all 21 dataset attributes.
  - **One-Click Prediction Loading**: Instantly transfer any record from the table directly into the prediction form.
- **Machine Learning Churn Predictor**:
  - Interactive evaluation form with quick presets (**High-Risk Profile** and **Loyal Customer**).
  - **Scikit-learn Random Forest Classifier** pipeline with fitted `ColumnTransformer` (One-Hot Encoding).
  - Probability meter with color-coded risk scale (Low, Moderate, High Risk) and actionable retention recommendations.
- **FastAPI REST API**:
  - High-performance, asynchronous backend with automatic OpenAPI documentation.
  - Robust Pydantic v2 schemas validating inputs and data types.
  - Comprehensive automated test suite using `pytest`.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/), [Pydantic v2](https://docs.pydantic.dev/) |
| **Machine Learning** | [Scikit-learn](https://scikit-learn.org/) (RandomForestClassifier, ColumnTransformer, OneHotEncoder), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [Joblib](https://joblib.readthedocs.io/) |
| **Frontend UI** | Modern HTML5, Responsive Vanilla CSS (CSS Variables, Flexbox/Grid), Vanilla JavaScript (ES6+), [Chart.js](https://www.chartjs.org/) |
| **Testing** | [Pytest](https://docs.pytest.org/), [HTTPX](https://www.python-httpx.org/), Starlette TestClient |

---

## Directory Structure

```text
Customer Churn/
├── app/
│   ├── main.py                  # FastAPI application entrypoint & static mounting
│   ├── routes/
│   │   ├── dashboard.py         # /api/dashboard and /api/customers endpoints
│   │   └── prediction.py        # /api/predict inference endpoint
│   ├── schemas/
│   │   └── prediction.py        # Pydantic request/response models
│   └── services/
│       ├── analytics_service.py # Dataset parsing, metrics, and pagination
│       └── prediction_service.py# Model loading and churn probability prediction
├── data/
│   └── Telco_Customer_Churn.csv # Telco dataset (7,043 customer records)
├── frontend/
│   ├── index.html               # Main dashboard & predictor interface
│   ├── css/
│   │   └── style.css            # Responsive design tokens, cards, tables, modal
│   └── js/
│       └── app.js               # Dashboard controller, API fetchers, and Chart.js logic
├── ml/
│   ├── Cleaned_Customer_churn.csv # Cleaned training data
│   ├── Cleaning.ipynb           # EDA and preprocessing notebook
│   └── train.py                 # Random Forest training & joblib export script
├── models/
│   └── churn_pipeline.joblib    # Serialized model & encoder pipeline bundle
├── tests/
│   └── test_api.py              # Automated Pytest suite (13 test cases)
├── .gitignore                   # Git ignore configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (tested on Python 3.11, 3.12, 3.13)
- Git (optional, for cloning)

### 1. Clone or Open the Repository

```bash
git clone <repository-url>
cd "Customer Churn"
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Alternatively, if using `uv`: `uv pip install -r requirements.txt`)*

### 4. (Optional) Retrain the Machine Learning Model

The repository already comes with a pre-trained [models/churn_pipeline.joblib](file:///d:/College/Sem-7/ML/Project/Customer%20Churn/models/churn_pipeline.joblib). If you wish to retrain:

```bash
python ml/train.py
```

*Expected output: `Overall Accuracy: 78.63%`*

---

## Running the Application

Start the FastAPI backend with Uvicorn:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Once running:
- **Interactive Dashboard**: Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.
- **Interactive Swagger API Docs**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- **ReDoc API Documentation**: Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

---

## API Endpoints

### 1. Health Check
- **`GET /health`**
- Returns `{"status": "ok"}`.

### 2. Dashboard Analytics
- **`GET /api/dashboard`**
- Returns overall portfolio stats (`total_customers`, `churned_customers`, `retained_customers`, `churn_rate`), breakdowns by contract type, tenure group distributions, and average monthly charges comparison.

### 3. Customer Records Explorer
- **`GET /api/customers`**
- **Query Parameters**:
  - `search` *(str, optional)*: Filter by customer ID, contract, internet service, etc.
  - `churn` *(str, optional)*: Filter by churn status (`Yes`, `No`, or `all`).
  - `contract` *(str, optional)*: Filter by contract agreement (`Month-to-month`, `One year`, `Two year`, or `all`).
  - `offset` *(int, default 0)*: Zero-based record offset.
  - `limit` *(int, default 10, max 100)*: Records per page.
- Returns `{"total": int, "offset": int, "limit": int, "columns": [...], "rows": [...]}`.

### 4. Predict Churn Risk
- **`POST /api/predict`**
- **Request Body** (JSON):
  ```json
  {
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
    "PaymentMethod": "Electronic check"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "churn_probability": 0.5891,
    "predicted_churn": "Yes"
  }
  ```

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

All 13 test cases validate:
- Server availability and static asset delivery
- Dashboard calculations and metric consistency
- Customer Explorer pagination and search/status query filtering
- Input schema validation rules and edge cases (`tenure=0`, `TotalCharges=0`)
- ML model prediction and probability resolution

---

## Machine Learning Pipeline Details

1. **Features**:
   - **Numerical**: `tenure`, `MonthlyCharges`, `TotalCharges`.
   - **Binary Categorical (encoded as 0/1)**: `SeniorCitizen`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `PaperlessBilling`.
   - **Multi-Class Categorical**: `InternetService` (`DSL`, `Fiber optic`, `0`), `Contract` (`Month-to-month`, `One year`, `Two year`), `PaymentMethod` (`Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)`).
2. **Preprocessing**:
   - `ColumnTransformer` with `OneHotEncoder(handle_unknown="ignore")` applied specifically to multi-class columns.
   - `remainder="passthrough"` retains all binary and numeric features.
3. **Model**:
   - `RandomForestClassifier(n_estimators=100, random_state=42)` trained on 80% split with stratification on `Churn`.
   - Feature leakage prevention: CSV index `Unnamed: 0` is strictly excluded from training.
