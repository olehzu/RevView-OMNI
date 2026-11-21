from fastapi import FastAPI

from app.errors import register_error_handlers
from app.observability import configure_logging, register_observability
from app.rev.router import router as review_package_router

configure_logging()

app = FastAPI(title="RevView/OMNI")
register_error_handlers(app)
register_observability(app)
app.include_router(review_package_router)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Report that the application is running."""
    return {"status": "ok"}
