"""
FastAPI Main Application Entrypoint
Enterprise Customer Segmentation Platform
"""

import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import logger
from app.core.security import setup_security
from app.database.connection import init_db, SessionLocal
from app.database.models import ExecutionLog, SystemStatus

from app.api.routers import views, dataset_api, analytics_api, reports_api, system_api

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Customer Segmentation System powered by Unsupervised Machine Learning (K-Means, Hierarchical, PCA)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS & Security Headers
setup_security(app)

# Initialize Database
init_db()

# Mount Static File Directories
app.mount("/static", StaticFiles(directory=str(settings.BASE_DIR / "app" / "static")), name="static")
app.mount("/charts_img", StaticFiles(directory=str(settings.CHARTS_DIR)), name="charts_img")


# Request Timing Middleware & Execution Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    # Log to DB asynchronously/synchronously if API path
    if request.url.path.startswith("/api"):
        try:
            db = SessionLocal()
            log_entry = ExecutionLog(
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                ip_address=request.client.host if request.client else "127.0.0.1",
                response_time_ms=duration_ms
            )
            db.add(log_entry)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Failed to record request log: {e}")

    return response


# Include Router Controllers
app.include_router(views.router)
app.include_router(dataset_api.router)
app.include_router(analytics_api.router)
app.include_router(reports_api.router)
app.include_router(system_api.router)


@app.on_event("startup")
async def startup_event():
    logger.info("==========================================================")
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Docs available at http://127.0.0.1:8000/docs")
    logger.info("==========================================================")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
