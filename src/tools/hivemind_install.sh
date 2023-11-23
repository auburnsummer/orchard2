#!/usr/bin/env bash

# todo work on multiple platforms?

mkdir -p ~/.local/bin
cd ~/.local/bin

wget https://github.com/DarthSim/hivemind/releases/download/v1.1.0/hivemind-v1.1.0-linux-amd64.gz

gzip -c -d hivemind-v1.1.0-linux-amd64.gz > hivemind

chmod +x ./hivemind