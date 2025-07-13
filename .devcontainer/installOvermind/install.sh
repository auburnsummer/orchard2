#!/usr/bin/env bash

set -e

cd /usr/local/bin

curl -O -L https://github.com/DarthSim/overmind/releases/download/v2.5.1/overmind-v2.5.1-linux-amd64.gz
gzip -d overmind-v2.5.1-linux-amd64.gz
mv overmind-v2.5.1-linux-amd64 overmind
chmod +x overmind