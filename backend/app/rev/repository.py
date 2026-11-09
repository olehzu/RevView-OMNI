"""The in-memory Review Package store for v0.1.0; PostgreSQL replaces it behind this interface."""

from threading import Lock

from app.rev.models import ReviewPackage


class ReviewPackageRepository:
    """Holds copies, so a caller's changes reach the store only through ``save``."""

    def __init__(self) -> None:
        self._packages: dict[str, ReviewPackage] = {}
        self._lock = Lock()

    def get(self, review_id: str) -> ReviewPackage | None:
        with self._lock:
            package = self._packages.get(review_id)
            return package.model_copy(deep=True) if package else None

    def save(self, package: ReviewPackage) -> None:
        with self._lock:
            self._packages[package.review_id] = package.model_copy(deep=True)
