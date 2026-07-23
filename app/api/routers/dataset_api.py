"""
Dataset REST API Router
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.data_service import data_service

router = APIRouter(prefix="/api/dataset", tags=["Dataset API"])


@router.get("", summary="Get Paginated Dataset Records")
async def get_dataset_records(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by Customer ID"),
    cluster: Optional[int] = Query(None, description="Filter by Cluster ID (0..3)")
):
    return data_service.get_paginated_records(
        page=page, limit=limit, search_cust_id=search, cluster_filter=cluster
    )


@router.get("/summary", summary="Get Statistical Summary")
async def get_dataset_summary():
    return data_service.get_summary_statistics()


@router.get("/correlations", summary="Get Feature Correlation Matrix")
async def get_dataset_correlations():
    return data_service.get_correlation_matrix()
