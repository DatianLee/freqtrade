from fastapi.testclient import TestClient

from extensions.ui_gateway import app as ui_app


class FakeClient:
    def __init__(self) -> None:
        self.calls = []

    def show_config(self):
        self.calls.append("show_config")
        return {"bot_name": "freqtrade"}

    def status(self):
        self.calls.append("status")
        return [{"pair": "BTC/USDT", "is_open": True}]

    def pause(self):
        self.calls.append("pause")
        return {"status": "paused"}

    def resume(self):
        self.calls.append("resume")
        return {"status": "running"}

    def reload_config(self):
        self.calls.append("reload_config")
        return {"status": "reloaded"}


def test_bot_status_smoke():
    app = ui_app.create_app()
    fake_client = FakeClient()
    app.dependency_overrides[ui_app.get_client] = lambda: fake_client
    client = TestClient(app)

    response = client.get("/bot/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["config"] == {"bot_name": "freqtrade"}
    assert payload["status"] == [{"pair": "BTC/USDT", "is_open": True}]
    assert fake_client.calls == ["show_config", "status"]
