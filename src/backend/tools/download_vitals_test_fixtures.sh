#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

cd ../libs/vitals/test/fixtures

wget -nc https://cdn.discordapp.com/attachments/1059208320864501841/1094958907149008957/fixtures.tar

tar xf fixtures.tar

rm fixtures.tar