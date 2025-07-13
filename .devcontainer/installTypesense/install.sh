#!/usr/bin/env bash

set -e

cd /usr/local/bin

curl -O https://dl.typesense.org/releases/29.0/typesense-server-29.0-linux-amd64.tar.gz
tar -xzf typesense-server-29.0-linux-amd64.tar.gz
rm typesense-server-29.0-linux-amd64.tar.gz