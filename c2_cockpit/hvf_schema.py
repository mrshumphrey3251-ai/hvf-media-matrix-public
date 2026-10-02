"""
HVF Media Matrix - Database Schema Definitions (Private)
Strict ORM models for the persistent memory layer.
Engineered for high-throughput media telemetry and secure asset tracking.
"""
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

# Base class for all matrix database models
Base = declarative_base()

class HVFMediaAsset(Base):
    __tablename__ = 'hvf_media_assets'

    # Immutable cryptographic primary key
    asset_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core asset metadata
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Military-grade lifecycle and clearance tracking
    is_encrypted = Column(Boolean, default=True, nullable=False)
    clearance_level = Column(String, default="standard", nullable=False)
    
    def __repr__(self):
        return f"<HVFMediaAsset(id={self.asset_id}, file={self.filename}, encrypted={self.is_encrypted})>"

if __name__ == "__main__":
    print("HVF Schema defined and ready for database migration.")
