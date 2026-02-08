FROM python:3.11-slim

WORKDIR /app

COPY extensions/ui_gateway /app/extensions/ui_gateway
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 9000

ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "extensions.ui_gateway.app:app", "--host", "0.0.0.0", "--port", "9000"]
