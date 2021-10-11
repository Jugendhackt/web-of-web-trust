#!/usr/bin/env bash
# -*- coding: utf-8 -*-

/env/bin/alembic upgrade head
/env/bin/gunicorn "api:api" -b "$API_HOST:$API_PORT" -k "uvicorn.workers.UvicornWorker"
