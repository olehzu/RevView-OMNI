"""Observability (architecture section 8.2.7): request logs, request ids, and metrics."""

import logging
import re

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.observability import REQUEST_ID_HEADER

client = TestClient(app)


def _request_lines(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == "app.requests"]


def test_every_response_carries_a_request_id():
    response = client.get("/api/v1/health")

    assert re.fullmatch(r"[0-9a-f]{32}", response.headers[REQUEST_ID_HEADER])


def test_a_failed_request_is_logged_with_its_request_id_and_status(
    caplog: pytest.LogCaptureFixture,
):
    caplog.set_level(logging.INFO, logger="app")

    response = client.get("/api/v1/review-packages/rev-9999")

    assert response.status_code == 404
    request_id = response.headers[REQUEST_ID_HEADER]
    lines = [line for line in _request_lines(caplog) if request_id in line]
    assert len(lines) == 1
    assert "method=GET" in lines[0]
    assert "path=/api/v1/review-packages/rev-9999" in lines[0]
    assert "status=404" in lines[0]


def test_the_log_line_leaves_out_the_query_string(caplog: pytest.LogCaptureFixture):
    caplog.set_level(logging.INFO, logger="app")

    client.get("/api/v1/health?token=not-for-the-log")

    assert _request_lines(caplog)
    assert not any("not-for-the-log" in line for line in _request_lines(caplog))


def test_metrics_count_responses_by_status():
    before = client.get("/api/v1/metrics").json()["data"]

    client.get("/api/v1/health")
    client.get("/api/v1/review-packages/rev-9999")

    after = client.get("/api/v1/metrics").json()["data"]
    by_status_before = before["responses_by_status"]
    by_status_after = after["responses_by_status"]
    # The two calls, plus the first metrics call itself.
    assert after["requests_total"] == before["requests_total"] + 3
    assert by_status_after["200"] == by_status_before.get("200", 0) + 2
    assert by_status_after["404"] == by_status_before.get("404", 0) + 1
