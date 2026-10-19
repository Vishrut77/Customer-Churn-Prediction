from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

DATA_PATHS = [
    PROJECT_DIR / "data" / "Telco_Customer_Churn.csv",
    PROJECT_DIR / "data" / "Telco_Customer_churn.csv",
    PROJECT_DIR / "data" / "Telco-Customer-Churn.csv",
    PROJECT_DIR / "ml" / "Cleaned_Customer_churn.csv",
    PROJECT_DIR / "Cleaned_Customer_churn.csv",
]


def load_dataset():
    # Find the first dataset file that exists
    data_path = next(
        (path for path in DATA_PATHS if path.exists()),
        None,
    )

    if data_path is None:
        raise FileNotFoundError(
            "Customer churn CSV was not found."
        )

    data = pd.read_csv(data_path)

    # Ensure charges and tenure are numeric
    if "TotalCharges" in data.columns:
        data["TotalCharges"] = pd.to_numeric(
            data["TotalCharges"],
            errors="coerce",
        )

    if "MonthlyCharges" in data.columns:
        data["MonthlyCharges"] = pd.to_numeric(
            data["MonthlyCharges"],
            errors="coerce",
        )

    if "tenure" in data.columns:
        data["tenure"] = pd.to_numeric(
            data["tenure"],
            errors="coerce",
        )

    # Standardize Churn values for dashboard calculations
    if "Churn" not in data.columns:
        raise ValueError("The dataset must contain Churn.")

    churn_mapping = {
        "yes": "Yes",
        "no": "No",
        "1": "Yes",
        "0": "No",
        "1.0": "Yes",
        "0.0": "No",
    }

    data["Churn"] = (
        data["Churn"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(churn_mapping)
    )

    # Remove rows with invalid target labels
    data = data[data["Churn"].isin(["Yes", "No"])].copy()

    return data


def get_dashboard_stats():
    data = load_dataset()

    total = len(data)
    churned = int((data["Churn"] == "Yes").sum())
    retained = int((data["Churn"] == "No").sum())

    churn_rate = (
        round(float(churned) / float(total) * 100, 2)
        if total > 0
        else 0.0
    )

    return {
        "total_customers": total,
        "churned_customers": churned,
        "retained_customers": retained,
        "churn_rate": churn_rate,
    }


def get_churn_by_contract():
    data = load_dataset()

    if "Contract" not in data.columns:
        return []

    data["is_churned"] = (
        data["Churn"] == "Yes"
    )

    grouped = data.groupby("Contract")["is_churned"].agg(
        customers="count",
        churned="sum",
    )

    results = []

    for contract, row in grouped.iterrows():
        cust_cnt = int(row["customers"])
        churn_cnt = int(row["churned"])
        churn_rate = (
            round(float(churn_cnt) / float(cust_cnt) * 100, 2)
            if cust_cnt > 0
            else 0.0
        )
        results.append({
            "contract": str(contract),
            "customers": cust_cnt,
            "churned": churn_cnt,
            "churn_rate": churn_rate,
        })

    return results


def get_churn_by_tenure():
    data = load_dataset()

    if "tenure" not in data.columns:
        return []

    data = data.dropna(subset=["tenure"]).copy()

    # Group customers by tenure in months (handling any tenure >= 49)
    data["tenure_group"] = pd.cut(
        data["tenure"],
        bins=[-1, 12, 24, 48, float("inf")],
        labels=["0-12", "13-24", "25-48", "49-72"],
    )

    data["is_churned"] = (
        data["Churn"] == "Yes"
    )

    grouped = data.groupby(
        "tenure_group",
        observed=False,
    )["is_churned"].agg(
        customers="count",
        churned="sum",
    )

    results = []

    for group, row in grouped.iterrows():
        customers = int(row["customers"])
        churned = int(row["churned"])
        churn_rate = (
            round(float(churned) / float(customers) * 100, 2)
            if customers > 0
            else 0.0
        )

        results.append({
            "tenure_group": str(group),
            "customers": customers,
            "churned": churned,
            "churn_rate": churn_rate,
        })

    return results


def get_average_charges_by_churn():
    data = load_dataset()

    if "MonthlyCharges" not in data.columns:
        return []

    grouped = data.groupby("Churn")[
        "MonthlyCharges"
    ].mean()

    return [
        {
            "churn": str(churn),
            "average_monthly_charges": round(float(amount), 2),
        }
        for churn, amount in grouped.items()
        if pd.notna(amount)
    ]


def get_dashboard_data():
    return {
        "stats": get_dashboard_stats(),
        "churn_by_contract": get_churn_by_contract(),
        "churn_by_tenure": get_churn_by_tenure(),
        "average_charges_by_churn": (
            get_average_charges_by_churn()
        ),
    }


def get_customer_preview(
    search: str = "",
    churn: str | None = None,
    contract: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    data = load_dataset()

    # Filter by churn status if requested
    if churn:
        c = churn.strip().lower()
        if c in ["yes", "1", "true", "churned"]:
            data = data[data["Churn"] == "Yes"]
        elif c in ["no", "0", "false", "retained"]:
            data = data[data["Churn"] == "No"]
        # 'all' or other values result in no churn filtering

    # Filter by contract if requested
    if contract and contract.strip().lower() not in ["", "all"]:
        data = data[
            data["Contract"].astype(str).str.lower()
            == contract.strip().lower()
        ]

    # Search across the available dataset columns
    if search and search.strip():
        search_term = search.strip()
        matching_rows = data.astype(str).apply(
            lambda column: column.str.contains(
                search_term,
                case=False,
                regex=False,
                na=False,
            )
        ).any(axis=1)

        data = data[matching_rows]

    total = len(data)

    # Include all dataset columns
    columns = list(data.columns)

    # If the file has no customerID, show a row number
    if "customerID" not in columns and "row" not in columns:
        data = data.copy()
        data.insert(0, "row", data.index + 1)
        columns.insert(0, "row")

    page = data[columns].iloc[offset:offset + limit].copy()

    # Replace NaN values with JSON-compatible nulls
    page = page.astype(object).where(
        pd.notna(page),
        None,
    )

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "columns": columns,
        "rows": page.to_dict(orient="records"),
    }