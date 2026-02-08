from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    freqtrade_api_url: str
    freqtrade_username: str
    freqtrade_password: str
    freqtrade_timeout: float
    binance_config_path: str | None
    telegram_config_path: str | None
    hyperliquid_api_key: str | None
    hyperliquid_api_secret: str | None
    hyperliquid_ws_url: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            freqtrade_api_url=os.getenv("FREQTRADE_API_URL", "http://127.0.0.1:8080"),
            freqtrade_username=os.getenv("FREQTRADE_API_USERNAME", ""),
            freqtrade_password=os.getenv("FREQTRADE_API_PASSWORD", ""),
            freqtrade_timeout=float(os.getenv("FREQTRADE_API_TIMEOUT", "10")),
            binance_config_path=os.getenv("BINANCE_CONFIG_PATH"),
            telegram_config_path=os.getenv("TELEGRAM_CONFIG_PATH"),
            hyperliquid_api_key=os.getenv("HYPERLIQUID_API_KEY"),
            hyperliquid_api_secret=os.getenv("HYPERLIQUID_API_SECRET"),
            hyperliquid_ws_url=os.getenv("HYPERLIQUID_WS_URL"),
        )
