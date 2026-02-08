# UI Gateway (FastAPI)

最小可运行的 UI 网关，提供人性化的统一入口，**仅通过 Freqtrade 现有 REST API/RPC 通信**，不直连交易所。

## 功能

- `GET /health`
- `GET /bot/status`
- `GET /positions`
- `POST /trade/pause`
- `POST /trade/resume`
- `POST /strategy/switch`

## 配置

复制 `.env.example` 到 `.env`，按需填写：

```bash
cp extensions/ui_gateway/.env.example extensions/ui_gateway/.env
```

- Binance、Telegram 仍按现有 `config.json` 结构配置（此网关只调用 Freqtrade API，不解析交易所配置）。
- Hyperliquid 预留配置字段：`HYPERLIQUID_*`，当前版本未启用时保持空值即可。

## 本地运行

确保 freqtrade 的 `api_server.enabled=true`，并允许 UI 网关访问。

```bash
export $(cat extensions/ui_gateway/.env | xargs)
python -m uvicorn extensions.ui_gateway.app:app --host 0.0.0.0 --port 9000
```

## Docker 运行

使用仓库根目录的 `docker-compose.override.yml`：

```bash
docker compose up --build
```

默认暴露 `http://127.0.0.1:9000`。若需要远程访问，请自行配置反向代理/内网访问策略。

## 风险提示

- 请勿将 Freqtrade API 直接暴露到公网，务必设置强密码。
- UI 网关只是转发/封装 Freqtrade API，不提供额外安全保护。
- 交易风险自担，建议在模拟环境验证后再上生产。
