from fastapi import FastAPI

app = FastAPI(title="RevView/OMNI")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Report that the application is running."""
    return {"status": gate_demo_status}
