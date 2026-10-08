from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

app = FastAPI(title="HVF Security Gateway")

# Immutable Audit Log Simulation
AUDIT_LOG = []

def log_audit(action: str, user: str, status: str):
    entry = f"[{datetime.now(timezone.utc).isoformat()}] USER: {user} | ACTION: {action} | STATUS: {status}"
    AUDIT_LOG.append(entry)
    print(f"AUDIT COMMIT: {entry}")

# RBAC Matrix defined by Executive Governance
ROLES = {
    "Admin": ["read", "write", "delete", "deploy"],
    "Agronomist": ["read", "write"],
    "Field-Tech": ["read", "update_status"],
    "Viewer": ["read"]
}

@app.middleware("http")
async def rbac_middleware(request: Request, call_next):
    # In production, this extracts and validates the JWT from headers
    user_role = request.headers.get("X-User-Role", "Viewer")
    user_id = request.headers.get("X-User-ID", "unknown")
    
    method = request.method
    path = request.url.path

    # Enforce Governance: Block unauthorized destructive actions (e.g., Viewer deleting an alert)
    if method == "DELETE" and "delete" not in ROLES.get(user_role, []):
        log_audit(f"Attempted DELETE on {path}", user_id, "403_FORBIDDEN")
        return JSONResponse(status_code=403, content={"detail": "HVF Governance: Unauthorized action. Incident logged."})

    response = await call_next(request)
    
    # Log successful state changes to immutable ledger
    if method in ["POST", "PUT", "DELETE"]:
        log_audit(f"{method} on {path}", user_id, "SUCCESS")
        
    return response

if __name__ == "__main__":
    print("HVF RBAC & Audit Middleware Initialized and Enforcing Governance.")
