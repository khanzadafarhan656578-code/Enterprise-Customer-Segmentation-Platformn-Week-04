"""
Database Models Module
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String(255), index=True)
    method = Column(String(10))
    status_code = Column(Integer)
    ip_address = Column(String(50), nullable=True)
    response_time_ms = Column(Float, nullable=True)


class DownloadLog(Base):
    __tablename__ = "download_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    file_name = Column(String(255), index=True)
    file_type = Column(String(50))
    file_size_bytes = Column(Integer)
    ip_address = Column(String(50), nullable=True)


class SystemStatus(Base):
    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), default="Customer Segmentation Platform")
    status = Column(String(50), default="OPERATIONAL")
    last_run_timestamp = Column(DateTime, default=datetime.utcnow)
    dataset_records = Column(Integer, default=8950)
    clusters_count = Column(Integer, default=4)
    silhouette_score = Column(Float, default=0.2086)
