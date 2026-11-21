"""Operational logging and metrics (architecture section 8.2.7).

Every request gets one log line with a request id, its method, path, status, and
duration. The same id is returned in the ``X-Request-ID`` header, so a failure an
Author reports can be found in the log. Never logged: query strings, request or
response bodies, headers, credentials, tokens, source, or diff content.

Logs go to the console of the process running the Application (there is no hosted
log platform yet, ``TD-logs-console-only``). Metrics are counters held in memory
and reset when the Application restarts (``TD-metrics-in-memory``).
"""

import logging
import sys
import time
import uuid
from collections import Counter
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response

REQUEST_ID_HEADER = "X-Request-ID"

logger = logging.getLogger("app.requests")

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def configure_logging(level: int = logging.INFO) -> None:
    """Send the Application's ``app.*`` log messages to the console, timestamped in UTC.

    Safe to call more than once; it adds its handler only the first time.
    """
    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)
    if any(getattr(h, "_revview", False) for h in app_logger.handlers):
        return
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(_LOG_FORMAT, _DATE_FORMAT)
    formatter.converter = time.gmtime  # UTC, as section 8.2.2 stores times
    handler.setFormatter(formatter)
    handler._revview = True  # type: ignore[attr-defined]
    app_logger.addHandler(handler)


class Metrics:
    """Request counts since the Application started, by HTTP status code."""

    def __init__(self) -> None:
        self.requests_total = 0
        self.responses_by_status: Counter[int] = Counter()

    def record(self, status_code: int) -> None:
        self.requests_total += 1
        self.responses_by_status[status_code] += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "requests_total": self.requests_total,
            "responses_by_status": {
                str(code): count
                for code, count in sorted(self.responses_by_status.items())
            },
        }


metrics = Metrics()


def register_observability(app: FastAPI) -> None:
    """Log and count every request, and expose the counts at ``/api/v1/metrics``."""

    @app.middleware("http")
    async def log_request(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Generated here, never taken from the client, so a log line cannot be forged.
        request_id = uuid.uuid4().hex
        started = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            # Also runs when an unexpected error escapes to the 500 handler.
            metrics.record(status_code)
            logger.info(
                "request id=%s method=%s path=%s status=%d duration_ms=%.1f",
                request_id,
                request.method,
                request.url.path,
                status_code,
                (time.perf_counter() - started) * 1000,
            )

    @app.get("/api/v1/metrics")
    def get_metrics() -> dict[str, Any]:
        """Request counts since the Application started (section 8.2.3 envelope)."""
        return {"data": metrics.snapshot()}
