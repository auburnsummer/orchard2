#!/bin/bash

cd "$(dirname "$0")"
cd ../
rm django-bridge-react-0.4.0.tgz
cd client
npm uninstall @django-bridge/react
cd ../
cd django-bridge/packages/react
npm install
npm run build
npm pack --pack-destination=../../../
cd ../../../client
npm install ../django-bridge-react-0.4.0.tgz
cd ../
overmind restart