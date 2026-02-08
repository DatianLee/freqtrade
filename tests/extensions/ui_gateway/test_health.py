from fastapi.testclient import TestClient

from extensions.ui_gateway import app as ui_app


class FakeClient:
    def ping(self):
        return {"status": "pong"}


def test_health_returns_upstream_status():
    app = ui_app.create_app()
    app.dependency_overrides[ui_app.get_client] = lambda: FakeClient()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "freqtrade": {"status": "pong"}}
