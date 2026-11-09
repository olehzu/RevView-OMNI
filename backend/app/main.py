from fastapi import FastAPI

from app.errors import register_error_handlers

app = FastAPI(title="RevView/OMNI")
register_error_handlers(app)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Report that the application is running."""
    return {"status": "ok"}
