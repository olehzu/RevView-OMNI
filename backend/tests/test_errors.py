"""The section 8.2.3 error envelope, translated once at the trust boundary (section 8.2.1)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.errors import AppError, register_error_handlers
from app.integration.svn import IntegrationUnavailable


def _app() -> FastAPI:
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/app-error")
    def app_error() -> None:
        raise AppError(409, "SOME_CONFLICT", "A safe message.")

    @app.get("/svn-down")
    def svn_down() -> None:
        raise IntegrationUnavailable("SVN")

    @app.get("/jenkins-down")
    def jenkins_down() -> None:
        raise IntegrationUnavailable("Jenkins")

    @app.get("/items/{number}")
    def item(number: int) -> dict[str, int]:
        return {"number": number}

    @app.get("/crash")
    def crash() -> None:
        raise RuntimeError("secret detail: password=hunter2")

    return app


client = TestClient(_app(), raise_server_exceptions=False)


def test_app_error_keeps_its_status_and_code_with_no_source():
    response = client.get("/app-error")

    assert response.status_code == 409
    assert response.json() == {
        "error": {"code": "SOME_CONFLICT", "message": "A safe message.", "source": None}
    }


def test_svn_unavailable_is_503_naming_svn():
    response = client.get("/svn-down")

    assert response.status_code == 503
    error = response.json()["error"]
    assert error["code"] == "SVN_UNAVAILABLE"
    assert error["source"] == "SVN"


def test_jenkins_unavailable_is_503_naming_jenkins():
    response = client.get("/jenkins-down")

    assert response.status_code == 503
    error = response.json()["error"]
    assert error["code"] == "JENKINS_UNAVAILABLE"
    assert error["source"] == "Jenkins"


def test_invalid_request_is_validation_failed():
    response = client.get("/items/not-a-number")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_FAILED"
    assert response.json()["error"]["source"] is None


def test_unknown_route_is_not_found_in_the_envelope():
    response = client.get("/no-such-route")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_unexpected_error_is_internal_error_and_leaks_no_detail():
    response = client.get("/crash")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert "hunter2" not in response.text
    assert "RuntimeError" not in response.text
