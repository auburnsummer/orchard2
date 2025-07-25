# build the frontend 
FROM node:lts-alpine3.21 AS client

WORKDIR /app

COPY . .

WORKDIR client

RUN ls
RUN npm install
RUN npm run build

# download hivemind binary
FROM alpine:3.22 AS hivemind  
RUN apk --no-cache add ca-certificates wget gzip
WORKDIR /tmp
RUN wget https://github.com/DarthSim/hivemind/releases/download/v1.1.0/hivemind-v1.1.0-linux-amd64.gz
RUN gzip -d hivemind-v1.1.0-linux-amd64.gz
RUN chmod +x hivemind-v1.1.0-linux-amd64
RUN mv hivemind-v1.1.0-linux-amd64 /tmp/hivemind

# this is the final image
FROM ghcr.io/astral-sh/uv:0.7.21-python3.13-bookworm-slim

# install caddy
RUN apt-get update && apt-get install -y \
    caddy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV DJANGO_SETTINGS_MODULE=orchard.settings

# static files
ENV VITE_BUNDLE_DIR=/tmp/client-dist
RUN mkdir -p /tmp/client-dist

COPY --from=client /app/client/dist /tmp/client-dist

# hivemind
COPY --from=hivemind /tmp/hivemind /usr/local/bin/hivemind

# install python dependencies
WORKDIR server
RUN uv sync

# collect static files for caddy to serve later
ENV STATIC_ROOT=/var/www/rhythm.cafe/static
WORKDIR cafe-backend

RUN uv run ./manage.py collectstatic --noinput

WORKDIR /app

CMD ["./start.sh"]