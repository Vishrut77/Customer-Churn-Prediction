from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.services.analytics_service import get_dashboard_data,get_customer_preview


router = APIRouter(
    prefix="/api",
    tags=["Dashboard"],
)


@router.get("/dashboard")
def dashboard():
    try:
        return get_dashboard_data()

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get("/customers")
def customers(
    search: str = "",
    churn: str | None = None,
    contract: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    try:
        return get_customer_preview(
            search=search,
            churn=churn,
            contract=contract,
            offset=offset,
            limit=limit,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )