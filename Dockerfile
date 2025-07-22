FROM node:lts-alpine3.21 AS client

WORKDIR /app

COPY . .

WORKDIR client

RUN ls
RUN npm install
RUN npm run build

FROM ghcr.io/astral-sh/uv:0.7.21-python3.13-bookworm-slim

WORKDIR /app

COPY . .

RUN mkdir -p /tmp/client-dist

COPY --from=client /app/client/dist /tmp/client-dist

WORKDIR server

RUN uv sync

ENV STATIC_ROOT=/app/server/cafe-backend/staticfiles
ENV VITE_BUNDLE_DIR=/tmp/client-dist

WORKDIR cafe-backend

RUN uv run ./manage.py collectstatic --noinput

CMD ["bash"]