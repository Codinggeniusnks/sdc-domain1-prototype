# Serverless worker for skill-trend forecasting. Build context = repo root.
# The model is read from the network volume (/runpod-volume/models/forecast).
FROM python:3.11-slim
WORKDIR /app
COPY runpod/forecast/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY runpod/forecast/features.py runpod/forecast/handler.py ./
CMD ["python", "-u", "handler.py"]
