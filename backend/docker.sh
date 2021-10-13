#!/usr/bin/env bash
# -*- coding: utf-8 -*-

/env/bin/alembic upgrade head
if [ "$API_RELOAD" = "True" ]; then
    echo "Starting Gunicorn with Auto-Reload. Not recommended for production usage"
    /env/bin/gunicorn "api:api" --threads "$(nproc)" -t 30 --reload -b "$API_HOST:$API_PORT" -k "uvicorn.workers.UvicornWorker"
else
    /env/bin/gunicorn "api:api" -b "$API_HOST:$API_PORT" --threads "$(nproc)" -t 30 -k "uvicorn.workers.UvicornWorker"
fi
