from fastapi import FastAPI, HTTPException
from sspm_engine.engine import SSPMEngine
from sspm_engine.models import ScanResult

app = FastAPI(
    title="SSPM Engine API",
    version="1.0.0",
    description="API for SaaS Security Posture Management",
)
engine = SSPMEngine()


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "SSPM Engine is running"}


@app.get("/scan/{provider}", response_model=ScanResult, tags=["Scan"])
def scan_provider(provider: str):
    if provider not in ["all", "slack", "github", "google"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid provider. Choose 'all', 'slack', 'github', or 'google'.",
        )

    results = engine.run_scan(provider)
    return results


@app.get("/risk", tags=["Analytics"])
def get_risk_score():
    results = engine.run_scan("all")
    return {"risk_score": results.score, "counts": results.counts}
