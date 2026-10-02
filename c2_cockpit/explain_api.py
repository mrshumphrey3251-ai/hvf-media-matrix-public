from fastapi import FastAPI, HTTPException

app = FastAPI(title="HVF AI Explainability Layer")

# Mock database mapping alert IDs to feature contributions
# In production, this pulls from the immutable audit table
EXPLANATION_DB = {
    "alert_8492": {
        "metric": "GLI",
        "previous": 0.42,
        "current": 0.18,
        "cause": "green reflectance dropped 28%"
    }
}

@app.get("/alert-explain/{alert_id}")
def explain_alert(alert_id: str):
    record = EXPLANATION_DB.get(alert_id)
    if not record:
        raise HTTPException(status_code=404, detail="Alert record not found")
    
    explanation = f"{record['metric']} fell from {record['previous']} to {record['current']} because {record['cause']}."
    return {"alert_id": alert_id, "human_readable_explanation": explanation}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
