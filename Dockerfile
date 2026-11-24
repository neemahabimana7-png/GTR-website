FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system django \
    && useradd --system --gid django --home-dir /app django \
    && mkdir -p /data \
    && chown django:django /data

COPY requirements/production.txt requirements/base.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY --chown=django:django . .
RUN chmod +x /app/scripts/docker-entrypoint.sh

USER django
EXPOSE 8000

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
