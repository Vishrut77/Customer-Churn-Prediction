from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.routes import dashboard, prediction


PROJECT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Customer churn analysis and prediction",
    version="1.0.0",
)

# Serve CSS, JavaScript, and other frontend assets
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)
app.mount(
    "/css",
    StaticFiles(directory=str(FRONTEND_DIR / "css")),
    name="css",
)
app.mount(
    "/js",
    StaticFiles(directory=str(FRONTEND_DIR / "js")),
    name="js",
)

# Register dashboard and prediction routes
app.include_router(dashboard.router)
app.include_router(prediction.router)


# Load the dashboard homepage
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# Simple health-check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Handle browser favicon requests
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)