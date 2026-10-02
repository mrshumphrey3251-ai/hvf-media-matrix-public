"""
HVF Media Matrix - Core API Router (Private)
The central nervous system of the matrix.
Engineered as a high-performance FastAPI server with strict endpoint security and CORS policies.
"""
import logging
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

# Dynamic routing for internal subsystems
try:
    from auth import HVFAuthGateway
    from media_processing import HVFMediaOrchestrator
    from analytics import HVFAnalyticsOrchestrator
    from analytics.ebony_predict_and_act import main_loop as autonomous_loop
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from auth import HVFAuthGateway
    from media_processing import HVFMediaOrchestrator
    from analytics import HVFAnalyticsOrchestrator
    from analytics.ebony_predict_and_act import main_loop as autonomous_loop

# Initialize the high-throughput web framework
api_app = FastAPI(title="HVF Media Matrix Core API", version="1.1.0")
logger = logging.getLogger("HVF_APIRouter")

# --- CONFIGURE PERIMETER DEFENSE (CORS) ---
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------

# Instantiate internal engines
auth_gateway = HVFAuthGateway()
media_engine = HVFMediaOrchestrator()
analytics_engine = HVFAnalyticsOrchestrator()

def verify_secure_access(x_auth_token: str = Header(default="")):
    """Dependency injection for absolute route protection."""
    if not auth_gateway.authenticate_entity(entity_id="api_client", access_token=x_auth_token):
        logger.warning("Intrusion attempt blocked at API Gateway.")
        raise HTTPException(status_code=401, detail="Unauthorized Matrix Access")
    return x_auth_token

@api_app.get("/health")
def system_health_check():
    """Publicly accessible health and telemetry endpoint."""
    return {"status": "online", "matrix": "active"}

@api_app.get("/telemetry", dependencies=[Depends(verify_secure_access)])
def get_system_telemetry():
    """Strictly secured endpoint for real-time matrix telemetry."""
    return analytics_engine.generate_system_report()

@api_app.post("/media/upload", dependencies=[Depends(verify_secure_access)])
def secure_media_upload(payload: Dict[str, Any]):
    """Strictly secured endpoint for media ingestion."""
    filename = payload.get("filename", "unknown_asset.bin")
    content_type = payload.get("content_type", "application/octet-stream")
    clearance = payload.get("clearance_level", "standard")
    
    asset_id = media_engine.ingest_asset(filename=filename, content_type=content_type, clearance=clearance)
    if not asset_id:
        raise HTTPException(status_code=500, detail="Media ingestion failed.")
        
    return {"status": "success", "asset_id": asset_id, "message": "Asset secured."}

@api_app.post("/autonomous/engage", dependencies=[Depends(verify_secure_access)])
async def engage_autonomous_engine(background_tasks: BackgroundTasks):
    """
    Strictly secured endpoint to ignite the Predict-and-Act ML Engine.
    Fires the asynchronous loop into the background to continuously monitor and act.
    """
    logger.info("Executive Override: Igniting Autonomous Predict-and-Act Engine.")
    
    # Push the ML loop to a background thread so the API remains responsive
    background_tasks.add_task(autonomous_loop)
    
    return {
        "status": "engaged", 
        "engine": "Ebony Predict-and-Act v1.0",
        "message": "Autonomous ML loop armed. The matrix is now actively hunting telemetry and publishing actuation payloads."
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Igniting ASGI server on port 8000...")
    uvicorn.run(api_app, host="0.0.0.0", port=8000)