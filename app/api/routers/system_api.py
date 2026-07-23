"""
System Health & Execution Status REST API Router
"""

import sys
import psutil
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.database.connection import get_db
from app.database.models import DownloadLog, ExecutionLog

router = APIRouter(prefix="/api/system", tags=["System API"])

START_TIME = datetime.utcnow()


@router.get("/health", summary="System Health Check")
async def health_check(db: Session = Depends(get_db)):
    # Calculate CPU and Memory Usage
    cpu_percent = psutil.cpu_percent(interval=None) if hasattr(psutil, "cpu_percent") else 0.0
    memory_info = psutil.virtual_memory() if hasattr(psutil, "virtual_memory") else None
    mem_percent = memory_info.percent if memory_info else 0.0

    total_downloads = db.query(func.count(DownloadLog.id)).scalar() or 0

    return {
        "status": "OPERATIONAL",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "python_version": sys.version.split()[0],
        "uptime_seconds": round((datetime.utcnow() - START_TIME).total_seconds(), 2),
        "cpu_usage_percent": cpu_percent,
        "memory_usage_percent": mem_percent,
        "total_file_downloads": total_downloads,
        "database_connected": True
    }


@router.get("/downloads", summary="Get Download Statistics")
async def download_stats(db: Session = Depends(get_db)):
    logs = db.query(DownloadLog).order_by(DownloadLog.timestamp.desc()).limit(50).all()
    return {
        "total_count": db.query(func.count(DownloadLog.id)).scalar() or 0,
        "recent_downloads": [
            {
                "id": l.id,
                "timestamp": l.timestamp.isoformat(),
                "file_name": l.file_name,
                "file_type": l.file_type,
                "size_bytes": l.file_size_bytes
            } for l in logs
        ]
    }
