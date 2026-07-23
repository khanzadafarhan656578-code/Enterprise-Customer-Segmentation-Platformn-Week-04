"""
Analytics & Machine Learning REST API Router
"""

from fastapi import APIRouter
from app.services.ml_service import ml_service

router = APIRouter(prefix="/api", tags=["Analytics API"])


@router.get("/metrics", summary="Get K-Means Evaluation Metrics (K=2..10)")
async def get_kmeans_metrics():
    return {
        "status": "success",
        "optimal_k": 4,
        "metrics": ml_service.get_kmeans_metrics()
    }


@router.get("/comparison", summary="Get Model Comparison Benchmark (K-Means vs Hierarchical)")
async def get_model_comparison():
    return {
        "status": "success",
        "comparison": ml_service.get_model_comparison()
    }


@router.get("/clusters", summary="Get Cluster Centroids & Distribution")
async def get_cluster_data():
    return {
        "status": "success",
        "cluster_info": ml_service.get_cluster_centroids()
    }


@router.get("/personas", summary="Get Customer Personas")
async def get_personas():
    return {
        "status": "success",
        "personas": ml_service.get_customer_personas()
    }


@router.get("/charts", summary="Get Chart Gallery Metadata")
async def get_charts_metadata():
    return {
        "status": "success",
        "charts": ml_service.get_chart_gallery_metadata()
    }
