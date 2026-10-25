# Serverless worker for skill extraction. Build context = repo root.
# Model weights are not baked in: they are read from the network volume (/runpod-volume/models/skills).
FROM python:3.11-slim
WORKDIR /app
COPY runpod/skills/requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.5.1 \
 && pip install --no-cache-dir -r requirements.txt
COPY runpod/label_map.json runpod/skills/handler.py runpod/skills/textsplit.py ./
CMD ["python", "-u", "handler.py"]
