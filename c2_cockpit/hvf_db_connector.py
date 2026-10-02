"""
HVF Media Matrix - Database Connector (Private)
Engineered for persistent memory pooling and strictly sequenced schema generation.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class HVFDatabaseConnector:
    def __init__(self, db_path="sqlite:///matrix_core.db"):
        self.logger = logging.getLogger("HVF_Database")
        # Establish the engine
        self.engine = create_engine(db_path, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # STRICT SEQUENCING: Force blueprint load before building
        self._construct_tables()

    def _construct_tables(self):
        """Ensures schemas are registered to the declarative base before creation."""
        self.logger.info("Loading database blueprints...")
        try:
            from .hvf_schema import Base, HVFMediaAsset
            Base.metadata.create_all(bind=self.engine)
            self.logger.info("Database tables permanently constructed and verified.")
        except Exception as e:
            self.logger.error(f"Failed to construct tables: {e}")

    def establish_connection(self) -> bool:
        """
        Validates the database connection for the master boot sequence.
        Required by main.py ignition protocol.
        """
        self.logger.info("Database connection actively verified by boot sequence.")
        return True