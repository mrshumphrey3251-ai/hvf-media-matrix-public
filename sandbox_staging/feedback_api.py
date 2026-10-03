from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI(title="HVF Customer Feedback Loop")

# Simulated Database for Alert Feedback
FEEDBACK_DB = []

class AlertFeedback(BaseModel):
    alert_id: str
    user_id: str
    rating: int  # 1 to 5 scale based on alert accuracy
    comments: str

@app.post("/feedback/submit")
def submit_feedback(payload: AlertFeedback):
    if payload.rating < 1 or payload.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert_id": payload.alert_id,
        "user_id": payload.user_id,
        "rating": payload.rating,
        "comments": payload.comments,
        "status": "Logged for Executive Triage"
    }
    FEEDBACK_DB.append(entry)
    print(f"FEEDBACK SECURED: {entry}")
    
    return {"status": "success", "message": "Feedback secured for monthly triage."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
