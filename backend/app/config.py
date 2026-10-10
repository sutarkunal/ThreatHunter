from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application
    APP_NAME: str = "ThreatHunter"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./data/database/threathunter.db"

    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    UPLOAD_DIR: str = "./data/uploads"
    ALLOWED_EXTENSIONS: List[str] = [".pcap", ".pcapng", ".cap"]

    # Processing
    MAX_PACKETS_PER_SESSION: int = 1000000
    PACKET_PROCESSING_BATCH_SIZE: int = 1000

    # Threat Detection Thresholds
    PORT_SCAN_THRESHOLD_MEDIUM: int = 20
    PORT_SCAN_THRESHOLD_HIGH: int = 50
    PORT_SCAN_TIME_WINDOW: int = 60  # seconds

    TRAFFIC_SPIKE_MULTIPLIER: float = 3.0

    EXCESSIVE_REQUESTS_MEDIUM: int = 100
    EXCESSIVE_REQUESTS_HIGH: int = 500
    EXCESSIVE_REQUESTS_TIME_WINDOW: int = 60  # seconds

    # Suspicious Ports
    SUSPICIOUS_PORTS: dict = {
        21: {"name": "FTP", "severity": "medium"},
        23: {"name": "Telnet", "severity": "high"},
        445: {"name": "SMB", "severity": "high"},
        3389: {"name": "RDP", "severity": "medium"},
        1433: {"name": "MSSQL", "severity": "medium"},
        3306: {"name": "MySQL", "severity": "medium"},
    }

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
