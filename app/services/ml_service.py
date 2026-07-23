"""
Machine Learning & Analytics Intelligence Service
"""

import os
import json
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from app.core.config import settings
from app.services.data_service import data_service


class MLService:
    """
    ML Analytics Service serving pre-calculated model results, personas, metrics, and chart metadata.
    """

    def __init__(self):
        self._metrics_df: pd.DataFrame = None
        self._personas: Dict[str, Any] = None
        self._comparison_df: pd.DataFrame = None

    def get_kmeans_metrics(self) -> List[Dict[str, Any]]:
        metrics_csv = settings.REPORTS_DIR / "kmeans_metrics.csv"
        if metrics_csv.exists():
            df = pd.read_csv(metrics_csv)
            return df.to_dict(orient="records")
        return []

    def get_model_comparison(self) -> List[Dict[str, Any]]:
        comp_csv = settings.REPORTS_DIR / "clustering_comparison.csv"
        if comp_csv.exists():
            df = pd.read_csv(comp_csv)
            return df.to_dict(orient="records")
        return []

    def get_customer_personas(self) -> Dict[str, Any]:
        personas_json = settings.REPORTS_DIR / "cluster_personas.json"
        if personas_json.exists():
            with open(personas_json, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_cluster_centroids(self) -> Dict[str, Any]:
        df = data_service.get_segmented_data()
        feature_cols = [c for c in df.columns if c not in ["CUST_ID", "Cluster"]]
        
        centroids = df.groupby("Cluster")[feature_cols].mean().round(2)
        counts = df["Cluster"].value_counts().sort_index().to_dict()
        percentages = ((df["Cluster"].value_counts().sort_index() / len(df)) * 100).round(2).to_dict()

        return {
            "features": feature_cols,
            "cluster_counts": counts,
            "cluster_percentages": percentages,
            "centroids": centroids.to_dict(orient="index")
        }

    def get_chart_gallery_metadata(self) -> List[Dict[str, Any]]:
        charts = [
            {"id": "correlation_heatmap", "title": "Attribute Correlation Heatmap", "category": "EDA", "filename": "correlation_heatmap.png", "desc": "Annotated Pearson correlation matrix highlighting feature collinearity."},
            {"id": "feature_distributions", "title": "Feature Value Distributions", "category": "EDA", "filename": "feature_distributions.png", "desc": "Histograms and Kernel Density Estimation (KDE) plots across 17 attributes."},
            {"id": "boxplots_outliers", "title": "Outlier Boxplots Analysis", "category": "EDA", "filename": "boxplots_outliers.png", "desc": "IQR Boxplots illustrating extreme value spread in monetary variables."},
            {"id": "violin_plots", "title": "Violin Distribution Density", "category": "EDA", "filename": "violin_plots.png", "desc": "Multi-modal distribution density and quartiles for primary financial metrics."},
            {"id": "elbow_curve", "title": "K-Means Elbow Curve", "category": "Clustering", "filename": "elbow_curve.png", "desc": "Within-Cluster Sum of Squares (WCSS Inertia) across K=2 to K=10."},
            {"id": "cluster_metrics_comparison", "title": "Metric Evaluation Grid", "category": "Clustering", "filename": "cluster_metrics_comparison.png", "desc": "WCSS, Silhouette, Calinski-Harabasz, and Davies-Bouldin comparative curves."},
            {"id": "dendrogram", "title": "Hierarchical Ward Dendrogram", "category": "Clustering", "filename": "dendrogram.png", "desc": "Truncated taxonomy tree with horizontal d=120 distance cut threshold."},
            {"id": "pca_2d_clusters", "title": "2D PCA Cluster Scatter Plot", "category": "PCA", "filename": "pca_2d_clusters.png", "desc": "2D principal component spatial projection with segment centroids."},
            {"id": "pca_3d_clusters", "title": "3D PCA Static Cluster Space", "category": "PCA", "filename": "pca_3d_clusters.png", "desc": "3D scatter projection capturing 61.11% cumulative dataset variance."},
            {"id": "cluster_heatmap", "title": "Cluster Profiling Heatmap", "category": "Profiling", "filename": "cluster_heatmap.png", "desc": "Z-score standardized heatmap displaying cluster feature fingerprints."},
            {"id": "cluster_radar_chart", "title": "Multi-Dimensional Radar Chart", "category": "Profiling", "filename": "cluster_radar_chart.png", "desc": "Polar radar fingerprint comparison across normalized financial dimensions."},
            {"id": "cluster_feature_bars", "title": "Cluster Financial Averages", "category": "Profiling", "filename": "cluster_feature_bars.png", "desc": "Average Balance, Purchases, Cash Advance, Credit Limit, and Payments by Cluster."}
        ]
        return charts


ml_service = MLService()
