"""
HTML View Controller Router
"""

import os
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.services.data_service import data_service
from app.services.ml_service import ml_service

router = APIRouter(tags=["HTML Views"])

templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "page_title": "Enterprise Customer Segmentation",
        "active_page": "landing"
    })


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    personas = ml_service.get_customer_personas()
    metrics = ml_service.get_kmeans_metrics()
    centroids_data = ml_service.get_cluster_centroids()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "page_title": "Executive Dashboard",
        "active_page": "dashboard",
        "total_customers": 8950,
        "total_clusters": 4,
        "silhouette_score": 0.2086,
        "wcss_score": 92131.16,
        "calinski_score": 1942.65,
        "davies_bouldin": 1.7047,
        "personas": personas,
        "metrics": metrics,
        "centroids": centroids_data
    })


@router.get("/dataset", response_class=HTMLResponse)
async def dataset_page(request: Request):
    summary = data_service.get_summary_statistics()
    return templates.TemplateResponse("dataset.html", {
        "request": request,
        "page_title": "Dataset Explorer",
        "active_page": "dataset",
        "summary": summary
    })


@router.get("/clusters", response_class=HTMLResponse)
async def clusters_page(request: Request):
    metrics = ml_service.get_kmeans_metrics()
    comparison = ml_service.get_model_comparison()
    return templates.TemplateResponse("clusters.html", {
        "request": request,
        "page_title": "Clustering Analytics Lab",
        "active_page": "clusters",
        "metrics": metrics,
        "comparison": comparison
    })


@router.get("/personas", response_class=HTMLResponse)
async def personas_page(request: Request):
    personas = ml_service.get_customer_personas()
    return templates.TemplateResponse("personas.html", {
        "request": request,
        "page_title": "Customer Persona Profiles",
        "active_page": "personas",
        "personas": personas
    })


@router.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request):
    charts = ml_service.get_chart_gallery_metadata()
    return templates.TemplateResponse("gallery.html", {
        "request": request,
        "page_title": "Visualization Gallery",
        "active_page": "gallery",
        "charts": charts
    })


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "page_title": "Reports & Download Hub",
        "active_page": "reports"
    })


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "page_title": "Architecture & About",
        "active_page": "about"
    })
