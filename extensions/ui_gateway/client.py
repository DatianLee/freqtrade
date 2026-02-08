from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from extensions.ui_gateway.config import Settings


class ApiError(RuntimeError):
    """Raised when upstream freqtrade API is unavailable or returns errors."""


@dataclass
class FreqtradeApiClient:
    base_url: str
    username: str
    password: str
    timeout: float = 10.0

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self.session = requests.Session()
        if self.username and self.password:
            self.session.auth = (self.username, self.password)

    @classmethod
    def from_settings(cls, settings: Settings) -> "FreqtradeApiClient":
        return cls(
            base_url=settings.freqtrade_api_url,
            username=settings.freqtrade_username,
            password=settings.freqtrade_password,
            timeout=settings.freqtrade_timeout,
        )

    def _request(self, method: str, path: str, *, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/api/v1/{path.lstrip('/')}"
        try:
            response = self.session.request(method, url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ApiError(str(exc)) from exc
        if not response.content:
            return {}
        return response.json()

    def ping(self) -> Any:
        return self._request("GET", "ping")

    def status(self) -> Any:
        return self._request("GET", "status")

    def show_config(self) -> Any:
        return self._request("GET", "show_config")

    def pause(self) -> Any:
        return self._request("POST", "pause")

    def resume(self) -> Any:
        return self._request("POST", "start")

    def reload_config(self) -> Any:
        return self._request("POST", "reload_config")
