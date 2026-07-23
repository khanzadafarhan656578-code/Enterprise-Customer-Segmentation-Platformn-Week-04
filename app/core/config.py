"""
Application Configuration Settings
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Customer Segmentation Platform"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_PATH: Path = DATA_DIR / "raw" / "DataSet(W4).csv"
    CLEANED_DATA_PATH: Path = DATA_DIR / "processed" / "cleaned_customer_data.csv"
    SCALED_DATA_PATH: Path = DATA_DIR / "processed" / "scaled_customer_data.csv"
    SEGMENTED_DATA_PATH: Path = DATA_DIR / "processed" / "segmented_customer_data.csv"
    
    CHARTS_DIR: Path = BASE_DIR / "charts"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    NOTEBOOKS_DIR: Path = BASE_DIR / "notebooks"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/app.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
