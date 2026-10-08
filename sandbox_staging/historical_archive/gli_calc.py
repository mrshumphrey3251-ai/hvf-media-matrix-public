from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="HVF Green Leaf Index (GLI) Microservice")

class RGBPayload(BaseModel):
    R: float
    G: float
    B: float

@app.post("/compute")
def compute_gli(payload: RGBPayload):
    r, g, b = np.float32(payload.R), np.float32(payload.G), np.float32(payload.B)
    denominator = (2 * g) + r + b
    if denominator == 0:
        raise HTTPException(status_code=400, detail="Invalid RGB values: Denominator cannot be zero.")
    
    gli = ((2 * g) - r - b) / denominator
    return {"GLI": float(np.clip(gli, -1.0, 1.0)), "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
