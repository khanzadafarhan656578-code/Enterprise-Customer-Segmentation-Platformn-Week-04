"""
Data Service Module
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from app.core.config import settings


class DataService:
    """
    High-performance data management and query service.
    """

    def __init__(self):
        self._df_raw: Optional[pd.DataFrame] = None
        self._df_cleaned: Optional[pd.DataFrame] = None
        self._df_segmented: Optional[pd.DataFrame] = None

    def get_cleaned_data(self) -> pd.DataFrame:
        if self._df_cleaned is None:
            if settings.CLEANED_DATA_PATH.exists():
                self._df_cleaned = pd.read_csv(settings.CLEANED_DATA_PATH)
            else:
                self._df_cleaned = pd.read_csv(settings.RAW_DATA_PATH)
        return self._df_cleaned

    def get_segmented_data(self) -> pd.DataFrame:
        if self._df_segmented is None:
            if settings.SEGMENTED_DATA_PATH.exists():
                self._df_segmented = pd.read_csv(settings.SEGMENTED_DATA_PATH)
            elif settings.CLEANED_DATA_PATH.exists():
                self._df_segmented = pd.read_csv(settings.CLEANED_DATA_PATH)
            else:
                self._df_segmented = pd.read_csv(settings.RAW_DATA_PATH)
        return self._df_segmented

    def get_paginated_records(
        self, page: int = 1, limit: int = 20, search_cust_id: Optional[str] = None, cluster_filter: Optional[int] = None
    ) -> Dict[str, Any]:
        df = self.get_segmented_data().copy()

        if search_cust_id:
            df = df[df["CUST_ID"].astype(str).str.contains(search_cust_id, case=False, na=False)]

        if cluster_filter is not None and "Cluster" in df.columns:
            df = df[df["Cluster"] == cluster_filter]

        total_records = len(df)
        total_pages = int(np.ceil(total_records / limit)) if total_records > 0 else 1
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        records = df.iloc[start_idx:end_idx].to_dict(orient="records")

        # Round numeric values for clean UI rendering
        for r in records:
            for k, v in r.items():
                if isinstance(v, float):
                    r[k] = round(v, 2)

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages,
            "columns": list(df.columns),
            "records": records
        }

    def get_summary_statistics(self) -> Dict[str, Any]:
        df = self.get_segmented_data()
        feature_cols = [c for c in df.columns if c not in ["CUST_ID", "Cluster"]]

        stats_dict = {}
        desc = df[feature_cols].describe().round(2).to_dict()

        for col in feature_cols:
            stats_dict[col] = {
                "mean": desc[col]["mean"],
                "std": desc[col]["std"],
                "min": desc[col]["min"],
                "25%": desc[col]["25%"],
                "50%": desc[col]["50%"],
                "75%": desc[col]["75%"],
                "max": desc[col]["max"],
                "missing": int(df[col].isnull().sum())
            }

        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "feature_stats": stats_dict
        }

    def get_correlation_matrix(self) -> Dict[str, Any]:
        df = self.get_segmented_data()
        feature_cols = [c for c in df.columns if c not in ["CUST_ID", "Cluster"]]
        corr = df[feature_cols].corr().round(3)
        return {
            "features": feature_cols,
            "values": corr.values.tolist()
        }


data_service = DataService()
