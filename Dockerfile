FROM python:3.12-slim

# This project is a Python FastAPI service only.
# Node.js/npm are not required unless a frontend build step is added later.

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "agora_rivas.main"]
