#!/usr/bin/env bash

curl --location https://github.com/DarthSim/hivemind/releases/download/v1.1.0/hivemind-v1.1.0-linux-amd64.gz | gzip -d > /usr/local/bin/hivemind
chmod +x /usr/local/bin/hivemind