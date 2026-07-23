"""
Reports & File Downloads REST API Router
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.database.models import DownloadLog

router = APIRouter(prefix="/api/reports", tags=["Reports API"])

FILE_MAP = {
    "pdf": (settings.BASE_DIR / "Documentation.pdf", "Documentation.pdf", "application/pdf"),
    "docx": (settings.BASE_DIR / "Documentation.docx", "Documentation.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    "csv": (settings.SEGMENTED_DATA_PATH, "segmented_customer_data.csv", "text/csv"),
    "summary_csv": (settings.REPORTS_DIR / "cluster_summary_statistics.csv", "cluster_summary_statistics.csv", "text/csv"),
    "metrics_csv": (settings.REPORTS_DIR / "kmeans_metrics.csv", "kmeans_metrics.csv", "text/csv"),
    "personas_json": (settings.REPORTS_DIR / "cluster_personas.json", "cluster_personas.json", "application/json"),
    "notebook": (settings.NOTEBOOKS_DIR / "week4_clustering.ipynb", "week4_clustering.ipynb", "application/x-ipynb+json"),
    "readme": (settings.BASE_DIR / "README.md", "README.md", "text/markdown")
}


@router.get("/download/{file_id}", summary="Download Deliverable File")
async def download_file(file_id: str, request: Request, db: Session = Depends(get_db)):
    if file_id not in FILE_MAP:
        raise HTTPException(status_code=404, detail=f"File identifier '{file_id}' not found.")

    file_path, filename, media_type = FILE_MAP[file_id]

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Target file {filename} does not exist on disk.")

    # Record download log in SQLite DB
    try:
        log_entry = DownloadLog(
            file_name=filename,
            file_type=file_id,
            file_size_bytes=file_path.stat().st_size,
            ip_address=request.client.host if request.client else "127.0.0.1"
        )
        db.add(log_entry)
        db.commit()
    except Exception:
        db.rollback()

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type
    )
