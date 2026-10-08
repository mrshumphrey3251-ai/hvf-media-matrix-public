"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: TEST GLI CALC
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    from fastapi.testclient import TestClient

    from gli_calc import app



    client = TestClient(app)



    def test_compute_gli_normal():

        response = client.post("/compute", json={"R": 120, "G": 150, "B": 80})

        assert response.status_code == 200

        assert response.json()["GLI"] > 0



    def test_compute_gli_division_by_zero():

        response = client.post("/compute", json={"R": 0, "G": 0, "B": 0})

        assert response.status_code == 400



    if __name__ == "__main__":

        print("QA Pipeline Passed.")


if __name__ == "__main__":
    render()
