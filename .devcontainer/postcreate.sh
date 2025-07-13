#!/usr/bin/env bash

set -e

mkdir data.typesense

cat >Procfile <<EOL
server: cd ./server/cafe-backend && uv run python manage.py runserver
client: cd ./client && npm run dev -- --clearScreen false
huey: cd ./server/cafe-backend && uv run python manage.py run_huey
typesense: typesense-server --api-key=key --data-dir=./data.typesense
minio: minio server ./data.minio
EOL

# uhhhh

cp server/cafe-backend/.env.example server/cafe-backend/.env