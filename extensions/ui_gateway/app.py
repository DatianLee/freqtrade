from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from extensions.ui_gateway.client import ApiError, FreqtradeApiClient
from extensions.ui_gateway.config import Settings


class StrategySwitchRequest(BaseModel):
    strategy: str | None = None


class StrategySwitchResponse(BaseModel):
    status: str
    strategy: str | None = None
    note: str
    freqtrade: dict


def get_settings() -> Settings:
    return Settings.from_env()


def get_client(settings: Settings = Depends(get_settings)) -> FreqtradeApiClient:
    return FreqtradeApiClient.from_settings(settings)


def create_app() -> FastAPI:
    app = FastAPI(title="Freqtrade UI Gateway", version="0.1.0")

    @app.get("/health")
    def health(client: FreqtradeApiClient = Depends(get_client)) -> dict:
        try:
            upstream = client.ping()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        return {"status": "ok", "freqtrade": upstream}

    @app.get("/bot/status")
    def bot_status(client: FreqtradeApiClient = Depends(get_client)) -> dict:
        try:
            config = client.show_config()
            status = client.status()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        return {"config": config, "status": status}

    @app.get("/positions")
    def positions(client: FreqtradeApiClient = Depends(get_client)) -> dict:
        try:
            status = client.status()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        return {"positions": status}

    @app.post("/trade/pause")
    def trade_pause(client: FreqtradeApiClient = Depends(get_client)) -> dict:
        try:
            result = client.pause()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        return {"status": "paused", "freqtrade": result}

    @app.post("/trade/resume")
    def trade_resume(client: FreqtradeApiClient = Depends(get_client)) -> dict:
        try:
            result = client.resume()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        return {"status": "resumed", "freqtrade": result}

    @app.post("/strategy/switch", response_model=StrategySwitchResponse)
    def strategy_switch(
        payload: StrategySwitchRequest,
        client: FreqtradeApiClient = Depends(get_client),
    ) -> StrategySwitchResponse:
        try:
            result = client.reload_config()
        except ApiError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")
        note = (
            "策略切换需更新 freqtrade 配置文件后 reload_config。"
            "该接口仅触发 reload_config，不直接修改撮合或交易所连接。"
        )
        return StrategySwitchResponse(
            status="reloaded",
            strategy=payload.strategy,
            note=note,
            freqtrade=result,
        )

    return app


app = create_app()
