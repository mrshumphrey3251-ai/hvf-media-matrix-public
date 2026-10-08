"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: GLI CALC
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
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


if __name__ == "__main__":
    render()
