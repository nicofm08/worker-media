FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1 \
    C_FORCE_ROOT=true

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--concurrency=1", "--pool=solo"]
