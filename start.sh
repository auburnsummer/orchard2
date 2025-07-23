#!/usr/bin/env bash

# this is the entrypoint script for the Docker container
set -e

# run migrations
cd /app/server/cafe-backend
uv run ./manage.py migrate
uv run ./manage.py setuptypesense

cd /app

hivemind Procfile.prod